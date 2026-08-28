# ALM — Internal procurement assistant in Teams using SAP for purcha

## Solution strategy
1. Create unmanaged solution in **Dev** (EU).
2. Add agent + connection references + env variables.
3. Export unmanaged for source control (`pac solution unpack`).
4. Export **managed** for Test/Prod import.

## PAC CLI sketch
```bash
pac auth create --environment "https://<dev>.crm4.dynamics.com"
pac solution export --name "<Solution>" --path ./exports/sol.zip --managed false
pac solution unpack --zipfile ./exports/sol.zip --folder ./src/solution
# after review
pac solution export --name "<Solution>" --path ./exports/sol_managed.zip --managed true
pac auth create --environment "https://<test>.crm4.dynamics.com"
pac solution import --path ./exports/sol_managed.zip --force-overwrite
```

Docs: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction  
ALM: https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm

## Testing
- Power CAT Copilot Studio Kit: https://github.com/microsoft/Power-CAT-Copilot-Studio-Kit
- Direct Line automated tests for core utterances
- Evaluation test sets before prod

## Dry-run CLI
```bash
cs-agent pac plan
# never: cs-agent pac plan --execute  (blocked without --i-confirm-yes; writes still refused)
```

## Tier note
Delivery tier for this design: **Tier 3 Action agents** — ALM mandatory for production at Tier 2+.
