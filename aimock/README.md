# aimock dev harness

Local deterministic **mock server** for testing anything the AI stack talks to — LLM APIs, MCP, A2A, AG-UI, vector DBs, search — without keys, network, or surprise bills. One port, one process, zero dependencies.

Used here to test agents designed by `cs-agent` against scripted responses **before** any tenant work. This is a dev/test tool; it does not change the `cs-agent` runtime (still zero runtime deps, still deterministic).

> **Offense counterpart:** `aimock` mocks; **PyRIT** attacks. See `docs/pyrit-redteam.md` for red-teaming the agents you design (consent-gated, own/client-authorized targets only).

## Prereq

Node.js + npm, then:

```bash
npm install -g @copilotkit/aimock
aimock --help    # expect usage output
```

## Run

From the **project root** (fixture paths in `aimock.json` are relative to CWD):

```bash
aimock -c aimock/aimock.json -p 4010 &
```

- LLM endpoints: `http://127.0.0.1:4010/v1/chat/completions` (OpenAI-compatible)
- MCP/A2A etc.: add the stanza to `aimock.json` and restart.

Point any OpenAI/Anthropic-style client at the mock URL with a dummy key:

```bash
curl http://127.0.0.1:4010/v1/chat/completions \
  -H "Content-Type: application/json" -H "Authorization: Bearer mock" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"What is DLP?"}]}'
```

## Core concepts

| Concept | Meaning |
|---|---|
| **Fixture** | `{ match, response }` — what the mock returns and when |
| **Match** | `userMessage` (last user message, substring/regex), `model`, `systemMessage`, `toolCallId`, `hasToolResult`, `context`, `endpoint`, … |
| **Catch-all** | Empty `match: {}` — must stay **last** in the file |
| **Latency / chunkSize** | Per-fixture streaming physics (`ttft`, `tps`, `jitter`) |
| **Chaos** | 500s, malformed JSON, mid-stream disconnects at a probability — for failure-mode tests |

## This repo's fixtures

`aimock/fixtures/llm/chat.json` ships 4 scripted scenarios:

1. `"What is DLP?"` → deterministic DLP answer
2. `"Design a Finnish IT helpdesk"` → deterministic Tier 2 pack sketch
3. `"What is the weather..."` → tool call `get_weather` (finishReason `tool_calls`)
4. empty match → catch-all fallback (must stay last)

## Tests

```bash
cd <repo root>
python -m pytest tests/test_aimock.py -v
```

Brings the mock server up on `127.0.0.1:4011` and asserts deterministic text, tool calls, and catch-all behavior **over real HTTP**. The module **skips** (not fails) when `aimock` is missing, so CI without Node stays green; the gate still runs locally.

## Record & replay

```bash
aimock -c aimock/aimock.json -p 4010 --record --provider-openai https://api.openai.com
```

Unmatched requests proxy to the real provider and are saved as fixtures; replay them later with zero network. Never commit recorded fixtures containing secrets. See https://aimock.copilotkit.dev/record-replay.

## Docs

- Docs: https://aimock.copilotkit.dev/docs
- Fixtures: https://aimock.copilotkit.dev/fixtures
- Record & replay: https://aimock.copilotkit.dev/record-replay
- GitHub: https://github.com/CopilotKit/aimock (MIT)
