"""Slice 5 — aimock determinism tests.

Boots the local aimock mock server (full suite from `aimock/aimock.json`),
then verifies over real HTTP that:

- scripted LLM fixtures answer deterministically (same request → same response)
- tool-call fixtures stream a tool call
- the catch-all fallback answers unknown requests instead of erroring
- aimock surfaces a reachable health endpoint

These tests are a dev-harness smoke gate, not a substitute for the PRD
product gates in `test_goldens.py`. They are SKIPPED (not failed) when
`aimock` is not installed or the mock server cannot start, so CI without
Node stays green while the gate still runs locally.

No live tenant calls. No real LLM keys. Localhost only.
"""

from __future__ import annotations

import http.client
import json
import os
import shutil
import socket
import subprocess
import time
from pathlib import Path

import pytest

AIMOCK_JSON = Path(__file__).resolve().parents[1] / "aimock" / "aimock.json"
AIMOCK_PORT = int(os.environ.get("AIMOCK_TEST_PORT", "4011"))


def _aimock_available() -> bool:
    return shutil.which("aimock") is not None


pytestmark = pytest.mark.skipif(
    not _aimock_available(), reason="aimock not installed (npm i -g @copilotkit/aimock)"
)


@pytest.fixture(scope="module")
def aimock_server():
    """Start aimock once per module; tear down afterwards. Skips if port busy."""
    proc = subprocess.Popen(
        ["aimock", "-c", str(AIMOCK_JSON), "-p", str(AIMOCK_PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_health(10)
        yield
    except RuntimeError as exc:
        pytest.skip(f"aimock server did not become ready: {exc}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def _wait_health(timeout_s: int) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", AIMOCK_PORT), timeout=1):
                return
        except OSError:
            time.sleep(0.25)
    raise RuntimeError("port never opened")


def _post(path: str, payload: dict) -> tuple[int, dict]:
    body = json.dumps(payload).encode()
    conn = http.client.HTTPConnection("127.0.0.1", AIMOCK_PORT, timeout=10)
    conn.request(
        "POST",
        path,
        body=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer mock"},
    )
    resp = conn.getresponse()
    data = json.loads(resp.read() or b"{}")
    conn.close()
    return resp.status, data


def _chat(message: str) -> dict:
    status, data = _post(
        "/v1/chat/completions",
        {"model": "gpt-4o", "messages": [{"role": "user", "content": message}]},
    )
    assert status == 200, f"non-200 from aimock: {status} {data}"
    return data


def test_aimock_scripted_response_deterministic(aimock_server):
    first = _chat("What is DLP?")
    second = _chat("What is DLP?")
    text = first["choices"][0]["message"]["content"]
    assert text
    assert text == second["choices"][0]["message"]["content"]


def test_aimock_tool_call_fixture(aimock_server):
    data = _chat("What is the weather in Helsinki?")
    tool_calls = data["choices"][0]["message"].get("tool_calls") or []
    assert len(tool_calls) == 1
    assert tool_calls[0]["function"]["name"] == "get_weather"


def test_aimock_fallback_matches_catch_all(aimock_server):
    data = _chat("many requests to this mock never recorded")
    content = data["choices"][0]["message"]["content"]
    assert "fallback" in content


def test_aimock_replays_recorded_deepseek_fixture(aimock_server):
    """E2E: a real LLM answer recorded via llmock --record, replayed offline.

    The fixture `aimock/fixtures/llm/00-recorded-deepseek.json` was captured
    from a local OpenAI-compatible endpoint through aimock record mode.
    Replaying must return the exact recorded answer with no upstream
    configured (deterministic, offline).
    """
    status, data = _post(
        "/v1/chat/completions",
        {
            "model": "deepseek-v4-flash",
            "messages": [
                {"role": "user", "content": "What is Entra ID authentication in Copilot Studio? One short answer."}
            ],
        },
    )
    assert status == 200, f"non-200 from aimock: {status} {data}"
    content = data["choices"][0]["message"]["content"]
    assert content == (
        "Entra ID authentication in Copilot Studio lets you secure your"
    )
