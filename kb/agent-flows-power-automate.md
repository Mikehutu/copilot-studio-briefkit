# Agent flows and Power Automate (official)

Research pass: 2026-08-27. Learn wins. Exa MCP unavailable this session (no EXA_API_KEY in MCP process); Context7 + Learn extracts used.

## What they are

- Overview: https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- FAQ: https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-faqs
- Use with agent: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow

Agent flows are native Copilot Studio automations (standard harness): trigger + at least one action. Deterministic. Each executed action consumes **Copilot Studio capacity**, not a per-user Power Automate license.

Power Automate **cloud flows** are general automation (share, co-owners, run-only). Agent flows cannot be copied, shared, have co-owners, or run-only permissions in Copilot Studio.

PA cloud flows do not show on the Copilot Studio Flows page unless converted.

## How they connect to an agent

To add a flow as a tool it must be a **solution** flow with trigger **When an agent calls the flow** and action **Respond to the agent**.

The same agent flow can be added to multiple agents.

Convert an existing PA cloud flow (must already be in a solution, same environment with CS capacity): Power Automate portal → Edit → change plan to **Copilot Studio** → Save. **One-way**; billing switches to CS capacity.

## Actions inside agent flows

Types: AI capabilities (prompts, call an agent), human-in-the-loop, built-in control (loops, branching, child flows), **connectors** including Microsoft 365, third-party, and **custom connectors**.

Premium connectors are allowed in agent flows.

**Desktop flows cannot be called from agent flows** (FAQ).

## Capacity

When prepaid CS capacity is exhausted, **new** agent flow runs are blocked; in-flight runs finish. Microsoft 365 Copilot licensed users and designer/test-chat tests are not affected.

Topic invocation: one Classic answer + flow actions. Generative orchestration: one Autonomous action + flow actions. Embedded test chat does not consume flow capacity.

## PA limits if you stay on Power Automate billing

https://learn.microsoft.com/en-us/power-automate/limits-and-config

Re-read before quoting in a SOW. Documented examples: 500 actions per workflow; nesting depth 8; 30-day run duration; custom connectors 50 per user and 500 requests/minute/connection; premium/trial required to run custom-connector flows; consistently throttled flows turned off after 14 days.
