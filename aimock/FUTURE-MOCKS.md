# aimock — Future Mock Surfaces (how to add more mocks)

This project's aimock harness currently mocks the **LLM** surface (`aimock/fixtures/llm`).
aimock supports far more. This doc explains how to extend the harness when the
project needs to mock other things — with the mechanism **verified** against the
real aimock server (MCP fully exercised; record/replay proven with a local upstream).

## Verified mechanism: one config, one port, many surfaces

A single `aimock.json` can declare `llm`, `mcp`, `a2a`, `vector`, and more. aimock
mounts **all** declared surfaces on **one** port:

```json
{
  "llm":    { "fixtures": "./aimock/fixtures/llm" },
  "mcp":    { "tools": ["search_kb", "get_weather"] },
  "a2a":    { "agents": ["planner"] },
  "vector": { "provider": "pinecone" }
}
```

Verified: with `llm` + `mcp` + `a2a` + `vector` declared, `/health` reported
every service `ok`, and the MCP server answered a full handshake on `/mcp`
(see below). No extra package — just add the stanza and restart.

> Note: `mcp.tools` is the list of **tool names** the mock MCP exposes. The
> response for a tool call comes from the LLM fixture (or programmatic fixture),
> not a per-tool JSON — plan your fixtures accordingly.

---

## Surface cheat-sheet (aimock suite)

| Surface | Config key | Mount | What it mocks |
|---|---|---|---|
| LLM | `llm.fixtures` | `/v1` | OpenAI/Claude/Gemini/Azure/Ollama/Cohere/OpenRouter chat, responses, embeddings, images, speech, transcription, video |
| MCP | `mcp.tools` | `/mcp` | Tools, resources, prompts, sessions (JSON-RPC) |
| A2A | `a2a.agents` | `/a2a` | Agent cards, tasks, SSE streaming |
| AG-UI | `agui` | `/agui` | Agent-to-UI event streams (CopilotKit frontends) |
| Vector | `vector.provider` | `/vector` | Pinecone / Qdrant / ChromaDB compatible endpoints |
| Services | `services` | — | Search (Tavily), rerank (Cohere), moderation, speech |

---

## MCP — verified working end-to-end

Start with `mcp` in the config. The MCP handshake is **three JSON-RPC steps** and
requires a session id from the server:

```bash
# 1. initialize → server returns Mcp-Session-Id header + capabilities
curl -i http://127.0.0.1:4010/mcp \
  -H "Content-Type: application/json" -H "Authorization: Bearer mock" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'
# → set -H "mcp-session-id: <SID from header>"

# 2. notifications/initialized (marks session ready)
curl http://127.0.0.1:4010/mcp \
  -H "Content-Type: application/json" -H "mcp-session-id: <SID>" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 3. tools/list, tools/call, ...
curl http://127.0.0.1:4010/mcp \
  -H "Content-Type: application/json" -H "mcp-session-id: <SID>" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Verified responses: `initialize` → `serverInfo.name = "mcp-mock"`,
`tools/list` → the configured tool names. (This is exactly how a real MCP client,
e.g. a tier-3 MCP-brief agent, would talk to the mock.)

---

## Record & replay — verified working (mechanism proven)

`llmock` (not the config `aimock` bin) has `--record`. Unmatched requests proxy to
a real upstream (`--provider-*`), and the response is saved as a fixture, then
replayed on subsequent identical requests.

```bash
# Record against a real (or local) upstream
AIMOCK_ALLOW_PRIVATE_URLS=1 llmock -p 4320 -f ./aimock/fixtures/llm \
  --record --provider-openai https://api.openai.com

# Later: replay with zero network
llmock -p 4320 -f ./aimock/fixtures/llm
```

Verified against a **local** upstream (`http://127.0.0.1:4599`): an unmatched
POST was proxied, the upstream's (501) response was saved to
`fixtures/llm/recorded/<id>.json`, and the exact same request then **replayed**
from the saved fixture. The recorded `match` carries `userMessage`, `model`,
`turnIndex`, `hasToolResult`.

> Real providers (`api.openai.com`, …) need network + `AIMOCK_PROVIDER_*_KEY`
> (env var **names** only) and are blocked by the SSRF guard unless
> `AIMOCK_ALLOW_PRIVATE_URLS=1` for private hosts. Never commit recorded
> fixtures containing secrets.

---

## How to extend this repo

1. **Add a stanza** to `aimock/aimock.json` (e.g. `"mcp": { "tools": ["search_kb"] }`).
2. **Restart** the server: `aimock -c aimock/aimock.json -p 4010 &`.
3. **Extend `tests/test_aimock.py`** with a probe for the new surface (like the
   MCP handshake above) — keep it deterministic and skip-if-absent.
4. **Update `aimock/README.md`, docs/benchmark/aimock.md, CHANGELOG, TASKS** in
   lockstep (SDD discipline).

### Test ideas tied to this product
- **MCP tools**: briefs that recommend MCP (tier 3+) → agent must call `search_kb`;
  mock server returns the tool, tests assert the agent's tool-call path without a real MCP server.
- **A2A**: multi-agent briefs (tier 5) → mock the "planner" agent's SSE stream.
- **Vector**: knowledge-grounding tests → mock Pinecone/Qdrant instead of a real DB.
- **Record & replay**: capture a real connector/DI trace once, replay in CI with no keys.
- **Chaos**: 500s / malformed JSON / disconnects → retry & error-UX tests.

## Reference
Docs: https://aimock.copilotkit.dev/docs · Fixtures: https://aimock.copilotkit.dev/fixtures ·
Record & replay: https://aimock.copilotkit.dev/record-replay
