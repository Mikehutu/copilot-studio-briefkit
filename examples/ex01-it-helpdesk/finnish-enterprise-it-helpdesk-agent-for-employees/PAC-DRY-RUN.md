# PAC dry-run — Finnish enterprise IT helpdesk agent for employees in Teams 

- Dry-run only: copy-paste after you authenticate to YOUR tenant.
- EU: prefer *.crm4.dynamics.com (Europe) environments.
- Do not run import without printed pre-flight + human YES.
- Never put secrets in CLI args; use PAC profiles / env vars.

```bash
  pac auth create --environment "https://<dev>.crm4.dynamics.com"
  pac solution export --name "<Solution>" --path ./exports/sol.zip --managed false
  pac solution unpack --zipfile ./exports/sol.zip --folder ./src/solution
  pac solution export --name "<Solution>" --path ./exports/sol_managed.zip --managed true
  pac auth create --environment "https://<test>.crm4.dynamics.com"
  pac solution import --path ./exports/sol_managed.zip --force-overwrite
```

Docs: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction
