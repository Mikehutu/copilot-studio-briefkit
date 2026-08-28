# Deployment / ALM runbook — Internal customer support coach in Teams using Zendesk to ch

**Human-executed, no silent import.** Every command here is a step a human runs
after printed pre-flight and tenant consent. PAC never mutates a tenant from this
repo or CLI automatically.

## Pipeline

1. **Dev** (Europe env) — build and test the agent in the unmanaged solution.
2. **Export unmanaged** → unpack to git for review + source control.
3. **Export managed** → import to **Test**, validate, then **Prod**.
4. Connection references + environment variables keep endpoints/secrets out of the zip.

## PAC sequence (copy-paste after your OWN `pac auth`)

```bash
# 1. Dev export (unmanaged) → source control
pac solution export --name "<Solution>" --path ./exports/sol_dev.zip --managed false
pac solution unpack --zipfile ./exports/sol_dev.zip --folder ./src/solution
git add ./src/solution && git commit -m "solution unpack: <Solution>"

# 2. Managed import → Test
pac solution export --name "<Solution>" --path ./exports/sol_test.zip --managed true
pac auth create --environment "https://<test>.crm4.dynamics.com"
pac solution import --path ./exports/sol_test.zip --force-overwrite

# 3. Managed import → Prod (after Test sign-off + printed pre-flight)
pac auth create --environment "https://<prod>.crm4.dynamics.com"
pac solution import --path ./exports/sol_prod.zip --force-overwrite
```

> Replace `<Solution>`, `<test>`, `<prod>` with real names. Secrets are env vars /
> connection reference names, never literals in this file.

## Connection references / env vars

- Name each external endpoint as an **environment variable** (e.g. `SERVICENOW_URL`)
- Store connector credentials as **connection references** (not in code/packs)
- Rotation = update the reference; no redeploy

## Verification gates (no silent skip)

- [ ] Dev unmanaged exports cleanly + unpacks to git
- [ ] Test import succeeds; agent answers a smoke utterance with EU region
- [ ] Prod import succeeds only after Test green + explicit approval
- [ ] No secrets in commit; `pac org list` shows Europe envs (use `cs-agent pac status`)

## ALM docs
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm
- https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction
- Power CAT Copilot Studio Kit: https://github.com/microsoft/Power-CAT-Copilot-Studio-Kit
