# Generative orchestration (official)

Primary: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions

## Modes
| | Generative | Classic |
|---|---|---|
| Topics | Selected by **description** | Trigger phrase match |
| Tools | Chosen by name/description | Only explicit from topics |
| Knowledge | Proactive search | Fallback / explicit node |
| Multi-intent | Can combine topics/tools/knowledge | Single topic preference |
| Missing inputs | Auto-generated questions | Author Question nodes |
| Responses | Auto-summarized | Author Message nodes |

- New agents default to **generative** orchestration.
- Admins can disable generative orchestration per environment → classic only.
- Prebuilt agent templates may force a mode.

## Authoring quality
- High-quality **descriptions** for topics, tools, knowledge, child agents are mandatory for reliable selection.
- Classic→generative migration auto-generates topic descriptions from trigger phrases; revise them.

## Required for
- MCP tools
- Computer use
- Many autonomous multi-tool plans

## Limitations (selected)
- Generative mode does not use Conversational boosting system topic customizations the same way.
- Custom entities as tool/topic input parameters limited — use Question nodes.
- Disambiguation / Multiple Topics Matched behavior differs.
- Conversation history window limited on long channels (Teams).
- Knowledge hyperlinks may render as plain text.

## EU enterprise default
Turn **on** generative orchestration for Tier 2+ action agents; invest in descriptions; disable ungrounded responses for compliance bots (knowledge settings).
