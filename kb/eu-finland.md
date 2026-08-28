# EU / Finland defaults

Sources:
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/geo-data-residency
- https://learn.microsoft.com/en-us/power-platform/admin/regions-overview
- https://learn.microsoft.com/en-us/privacy/eudb/eu-data-boundary-learn

## EU Data Boundary (Copilot Studio)
If the customer provisions a tenant with a **billing address in the EU or EFTA**, that tenant is in-scope for the EU Data Boundary **if the customer also creates all of its environments within a geographic region inside the EU Data Boundary**.

## Environment placement
- Create Power Platform environments in **Europe** for FI/EU orgs.
- Document any connector that sends data to non-Microsoft external systems (maker responsibility for external connectors).

## Generative AI geography
Admins can control moving data across regions for Copilot/generative AI features when capacity is constrained — review org policy before enabling cross-geo.

## GDPR posture (not legal advice)
- Product Terms + Data Protection Addendum govern the service.
- Trust Center for certifications: https://www.microsoft.com/trustcenter
- Design for minimization, Entra access control, Purview audit, DSR process via customer admins.

## Finland delivery defaults
- Languages: Finnish primary; Swedish where required; English for global IT
- Channels: Teams first for employees
- Auth: Entra; never no-auth for employee agents
- ALM: Dev/Test/Prod all in Europe; managed solutions to Prod
- Public sector: accessibility, logging, procurement, stronger change control
- Naming: org prefix + env suffix on agents/solutions

## Checklist
- [ ] All environments inside EUDB geography
- [ ] Auth required
- [ ] DLP baseline applied
- [ ] External connectors inventory + DPIA if personal data
- [ ] Credit capacity planned
