# Authentication (official)

Source: https://learn.microsoft.com/en-us/microsoft-copilot-studio/configuration-end-user-authentication

## Options
1. **No authentication** — public link access. Forbidden default for EU enterprise internal agents.
2. **Authenticate with Microsoft** — Entra for Teams/M365; variables User.ID, User.DisplayName.
3. **Authenticate manually** — Entra V2 (secret/cert/federated), OAuth2; includes User.AccessToken, User.IsLoggedIn.

## EU/FI defaults
- Internal agents: Authenticate with Microsoft (Teams-only) or manual Entra (multi-channel/token).
- Prefer tools running as **user credentials**.
- Publish required for auth changes to take effect.
- DLP can block connector **Chat without Microsoft Entra ID authentication in Copilot Studio**.
