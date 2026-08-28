# Using cs-agent with OpenAI-compatible model providers

`cs-agent` (the CLI) is **deterministic and model-free** — design packs, KB Q&A, and
PAC dry-run work offline with **zero dependencies and no API key**. There is no code path
that calls an LLM.

This guide is about the **other things you may want to point at a model** — the
OpenAI-compatible consumers around this project:

- **VS Code GitHub Copilot Chat** with a custom/BYOK model
- **aimock** (`aimock/` here) when you record real answers as fixtures
- your **own coding agents** (Hermes, Antigravity CLI, Claude Code, etc.)
- any **OpenAI SDK** script (`openai` Python/Node, LangChain, etc.)

All of these speak the **OpenAI Chat Completions API**. The only two things you
change are the **base URL** and the **API key** (the `model` string too, for some
providers). Copy `.env.example` → `.env` for the variables below.

---

## 0. How "OpenAI-compatible" works

The OpenAI Chat Completions contract is: `POST {base_url}/chat/completions` with
`Authorization: Bearer <key>` (or `api-key: <key>` for Azure) and a JSON body like:

```json
{
  "model": "gpt-4o-mini",
  "messages": [{ "role": "user", "content": "Hello" }]
}
```

Every provider below satisfies this contract — the SDK just needs the right
`base_url` + `api_key` (+ a `model` name that the server knows).

---

## 1. Local OpenAI-compatible endpoints

Serve an open model on a box you own, then point any consumer at it.

### vLLM / llama.cpp / Ollama / LM Studio

| Server      | Typical base URL            | Notes |
|-------------|-----------------------------|-------|
| **vLLM** (Docker/GPU) | `http://<HOST>:<PORT>/v1` | `--served-model-name` sets the exact model id |
| **llama.cpp / llama-server** | `http://<HOST>:<PORT>/v1` | model = the GGUF you loaded |
| **Ollama** | `http://<HOST>:11434/v1` | OpenAI-compat route built in |
| **LM Studio** | `http://127.0.0.1:1234/v1` | local dev default |

**Example — start vLLM (GPU):**

```bash
python -m vllm.entrypoints.openai.api_server \
  --model deepseek-ai/DeepSeek-V3 \
  --served-model-name deepseek-v4-flash \
  --port 8888
# → /v1/models lists "deepseek-v4-flash"
```

**Example — ask the endpoint:**

```bash
curl -s http://127.0.0.1:8888/v1/models | python3 -m json.tool   # see the exact model id
curl -s http://127.0.0.1:8888/v1/chat/completions \
  -H 'Content-Type: application/json' -H 'Authorization: Bearer dummy' \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Hello"}]}'
```

> The model `id` in `/v1/models` is the ONLY id that works — it must match the
> consumer's `model` field exactly. vLLM uses `--served-model-name`; llama.cpp
> uses whatever GGUF you loaded; Ollama uses the tag name.

### Verify with one command

```bash
curl -s http://<HOST>:<PORT>/v1/models
```

---

## 2. Microsoft cloud providers

### A. GitHub Models (free, PAT auth)

- **Base URL:** `https://models.github.ai/inference`
- **Key:** a GitHub personal access token (fine-grained, `Models` read) or classic PAT
- **Model format:** `owner/name` (e.g. `openai/gpt-4.1-mini`, `deepseek-ai/deepseek-v3`)

```bash
curl -s https://models.github.ai/inference/v1/models \
  -H "Authorization: Bearer $GITHUB_TOKEN"
```

OpenAI SDK:

```python
from openai import OpenAI
client = OpenAI(base_url="https://models.github.ai/inference", api_key="<GITHUB_PAT>")
resp = client.chat.completions.create(model="openai/gpt-4.1-mini", messages=[...])
```

> Docs: https://docs.github.com/en/github-models — free daily rate limits, rate-limited,
> not for production apps. The legacy `https://models.inference.ai.azure.com` URL is
> deprecated; use `https://models.github.ai/inference`.

### B. Azure OpenAI

- **Base URL:** `https://YOUR_RESOURCE.openai.azure.com/openai/v1/`
- **Key:** Azure OpenAI API key (header `api-key:`) — or Entra `Bearer` token
- **Model:** your **deployment name** (not the base model name)

```bash
curl -s https://YOUR_RESOURCE.openai.azure.com/openai/v1/chat/completions?api-version=2024-06-01 \
  -H "Content-Type: application/json" -H "api-key: $AZURE_OPENAI_KEY" \
  -d '{"model":"YOUR_DEPLOYMENT","messages":[{"role":"user","content":"Hello"}]}'
```

OpenAI SDK:

```python
from openai import OpenAI
client = OpenAI(
    base_url="https://YOUR_RESOURCE.openai.azure.com/openai/v1/",
    api_key="<AZURE_OPENAI_KEY>",   # or Entra token as api_key
)
resp = client.chat.completions.create(model="YOUR_DEPLOYMENT", messages=[...])
```

> Docs: https://learn.microsoft.com/en-us/azure/ai-services/openai/reference —
> Chat Completions lives under `/openai/deployments/<DEPLOYMENT>/chat/completions?api-version=...`.

### C. Azure AI Foundry (managed model endpoint)

- **Base URL:** `https://<YOUR_PROJECT>.services.ai.azure.com/models`
- **Key:** AI Foundry key (header `api-key:`) or Entra (`Bearer`)
- **Model:** model name (e.g. `gpt-4o-mini`, `DeepSeek-V3`)

```bash
curl -s https://<YOUR_PROJECT>.services.ai.azure.com/models/chat/completions?api-version=... \
  -H "Content-Type: application/json" -H "api-key: $AZURE_AI_FOUNDRY_KEY" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Hello"}]}'
```

OpenAI SDK:

```python
from openai import OpenAI
client = OpenAI(
    base_url="https://<YOUR_PROJECT>.services.ai.azure.com/models",
    api_key="<FOUNDRY_KEY>",   # or DefaultAzureCredential token
)
resp = client.chat.completions.create(model="gpt-4o-mini", messages=[...])
```

> Docs: https://learn.microsoft.com/en-us/azure/foundry/model-inference/quickstart —
> the endpoint supports both `Responses` and `chat/completions`; uses `api-key`/Entra.

---

## 3. Wiring the providers into consumers

### VS Code GitHub Copilot Chat (custom endpoint / BYOK)

Edit `chatLanguageModels.json` (`%APPDATA%\Code\User\` on Windows), add each provider:

```json
[
  {
    "name": "Local vLLM",
    "vendor": "customendpoint",
    "apiKey": "${input:chat.lm.secret.local}",
    "apiType": "chat-completions",
    "models": [
      {
        "id": "deepseek-v4-flash",
        "name": "Local DeepSeek",
        "url": "http://127.0.0.1:8888/v1/chat/completions",
        "toolCalling": true,
        "vision": false,
        "thinking": true
      }
    ]
  },
  {
    "name": "GitHub Models",
    "vendor": "customendpoint",
    "apiKey": "${input:chat.lm.secret.gh}",
    "apiType": "chat-completions",
    "models": [
      {
        "id": "openai/gpt-4.1-mini",
        "name": "GitHub Models GPT-4.1 mini",
        "url": "https://models.github.ai/inference/v1/chat/completions",
        "toolCalling": true,
        "vision": false,
        "thinking": false
      }
    ]
  },
  {
    "name": "Azure OpenAI",
    "vendor": "customendpoint",
    "apiKey": "${input:chat.lm.secret.azure}",
    "apiType": "chat-completions",
    "models": [
      {
        "id": "YOUR_DEPLOYMENT",
        "name": "Azure OpenAI GPT-4o",
        "url": "https://YOUR_RESOURCE.openai.azure.com/openai/v1/chat/completions",
        "toolCalling": true,
        "vision": true,
        "thinking": false
      }
    ]
  }
]
```

Rules (verified):
- The **model `id` must exactly match** the server's `/v1/models` id (or the deployment name on Azure).
- The **URL is used as-is** if it ends in `/chat/completions` (VS Code appends nothing).
- `toolCalling: true` is required or the model won't be usable in Copilot agents.
- Reload window after editing; check server logs if "can't connect".

### aimock (record real answers into fixtures)

```bash
llmock --record --provider-openai http://<HOST>:<PORT>    # local
llmock --record --provider-openai https://models.github.ai/inference   # GitHub Models
```

An unmatched request is proxied to the provider and the real answer saved as a
fixture. Replay with no upstream → deterministic/offline. See `aimock/README.md`.

### Any OpenAI SDK

```python
from openai import OpenAI
# swap base_url + api_key per provider table above
client = OpenAI(base_url="http://127.0.0.1:8888/v1", api_key="dummy")
```

---

## 4. Provider quick reference

| Provider | Base URL | Key header | Model string |
|----------|----------|------------|--------------|
| Local vLLM/llama.cpp | `http://<HOST>:<PORT>/v1` | `Bearer` | served id |
| Ollama | `http://<HOST>:11434/v1` | `Bearer` (any) | tag name |
| LM Studio | `http://127.0.0.1:1234/v1` | `Bearer` (any) | loaded model |
| GitHub Models | `https://models.github.ai/inference` | `Bearer` (PAT) | `owner/name` |
| Azure OpenAI | `https://<RES>.openai.azure.com/openai/v1/` | `api-key` (or Bearer/Entra) | deployment name |
| Azure AI Foundry | `https://<PROJ>.services.ai.azure.com/models` | `api-key` (or Bearer/Entra) | model name |

Security notes:
- Never commit API keys. Use env vars (`$AZURE_OPENAI_KEY`, `$GITHUB_TOKEN`, …) or
  secret storage (`${input:...}` in VS Code).
- Local LAN endpoints: keep them on your private network; don't bind vLLM to `0.0.0.0`
  unless you intend LAN access, and prefer auth.
- Azure: use Entra ID managed identity / `Bearer` in production over static keys where possible.
