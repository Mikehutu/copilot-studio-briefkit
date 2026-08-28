# Channels and publishing (official)

Primary: https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams

## Teams + Microsoft 365 Copilot channel
- Publish at least once before users can interact.
- Connect **Teams and Microsoft 365 Copilot** channels after publish.
- Option: make agent available in M365 Copilot (not only Teams).
- Share agent so users can install; org may need Power Platform apps allowed in Teams admin center.
- Availability: install for self → copy link for shared users → Built with Power Platform store section → admin approval for **Built for your org**.
- Data note: adding to Teams can share agent/user chat content with Teams; may flow outside org compliance/geo boundaries — review Teams app permissions docs.
- Internal security: turn on authentication for internal employee agents.
- Known: new publish content may not appear in ongoing chats (user can Start over); SystemError sometimes needs channel toggle / admin disable-enable.

## M365 Copilot channel limitations (selected)
- Conversation Start topic not supported the same way; suggested prompts instead.
- Some media/node types unsupported (speech ops, CSR handoff, certain cards/media).
- No user reaction feedback on agents in M365 Copilot in some cases.

## Other channels (DLP-governable)
- Direct Line (demo site, custom website, mobile, other DL)
- Facebook
- Omnichannel (Dynamics contact center)
- SharePoint channel
- WhatsApp

DLP can block each channel connector by name — see kb/dlp-governance.md.

## Threat model for public / B2B / external channels
An agent exposed beyond the internal tenant is an attack surface. Treat these as tenant-only notes, never steps to enable silently:

- **Direct Line is effectively a public bot endpoint** — anyone with a token can call it.
  - Rotate Direct Line secrets; place the site **behind an auth layer / WAF**.
  - OAuth/Entra on the agent before exposing; **no-auth only for anonymous demo** with a dedicated limited scope.
  - Rate-limit / throttle; monitor for prompt-injection via public utterances.
  - Docs: https://learn.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-directline
- **Teams / M365 Copilot distribution** — chat content can flow outside org compliance/geo boundaries; review app permission + data-residency docs before sharing beyond trusted groups.
- **WhatsApp / Facebook / Omnichannel** — each has DLP-governable connector names; blocking connector = channel effectively disabled. Review official per-channel docs before enabling.
- **Secrets hygiene** — never embed Direct Line tokens or connector credentials in the agent config / repo. Use **environment variables / connection references**; treat any committed token as compromised.

## EU/FI recommendation
- Internal: Teams + M365 first, Entra auth, share to security groups.
- External web: Direct Line only with auth + threat model; avoid no-auth.
- Public/B2B agents get an explicit **threat-model section** in the pack (see pack DESIGN.md).
