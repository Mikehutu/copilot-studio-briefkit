# Licensing and Copilot Credits (official)

Primary: https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing  
Licensing guide: https://go.microsoft.com/fwlink/?linkid=2320995  
Usage estimator: https://microsoft.github.io/copilot-studio-estimator/

## Currency
- Since 2025-09-01, common currency is **Copilot Credits** (formerly messages). Prepaid pack quantity and PAYG rate unchanged at cutover.

## How orgs buy capacity
1. **Prepaid Copilot Credit packs** (tenant subscription)
2. **Pay-as-you-go** via Azure billing policy linked to environments
3. **Prepurchase CCCU plan** (Azure) usable across eligible products
4. **M365 Copilot** license path for extending M365 Copilot (some zero-rated usage scenarios for classic/generative answers / Graph grounding when used inside M365 by licensed users — verify current licensing guide)

## Maker access
- Copilot Studio user license (requires tenant capacity subscription path) OR
- Copilot Studio authors role via PPAC security group OR
- M365 Copilot license (extensibility scenarios) OR
- Trial (test chat; **cannot publish**)

## Capacity enforcement
- Monthly enforcement; unused credits do not roll over.
- Exceeding capacity can lead to technical enforcement / service denial.
- Monitor via PPAC Copilot Hub / credit governance.

## Design implication
Every enterprise solution pack should estimate credit drivers: generative answers, tools, autonomous runs, computer-use steps (CUA bills multiple credits per step).
