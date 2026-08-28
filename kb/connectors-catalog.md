# Enterprise connector patterns (not a full 1400 dump)

Full catalog: https://learn.microsoft.com/en-us/connectors/connector-reference/

This file maps **common enterprise systems** to connector *families* for design. Always verify exact operations in the connector reference at build time.

## Microsoft 365 / Power Platform
| Need | Typical connector / surface |
|---|---|
| Email send/read | Office 365 Outlook |
| Files | SharePoint, OneDrive for Business |
| Chat/channels | Microsoft Teams |
| Tables | Dataverse, SharePoint lists |
| Approvals | Approvals + Teams adaptive cards |
| Excel online | Excel Online (Business) |
| Calendar | Office 365 Outlook |
| Users/groups | Microsoft Entra ID, Office 365 Users |
| Meetings | Microsoft Bookings, Outlook |
| BI | Power BI |

## ITSM / Dev
| System | Pattern |
|---|---|
| ServiceNow | ServiceNow connector — create/update/get incident/record |
| Jira | Jira connector — issues |
| Azure DevOps | Azure DevOps connector |
| GitHub | GitHub connector |
| PagerDuty | PagerDuty / HTTP |

## CRM / Sales
| System | Pattern |
|---|---|
| Dynamics 365 | Dynamics 365 / Dataverse |
| Salesforce | Salesforce connector |
| HubSpot | HubSpot connector |

## ERP / Finance / HR
| System | Pattern |
|---|---|
| Dynamics 365 Finance/SCM/HR | Dynamics connectors + Dataverse |
| SAP | SAP connectors / custom |
| Workday | Workday connector |
| SuccessFactors | SAP SuccessFactors |
| Oracle | Oracle connectors / custom |

## Integration styles (prefer order)
1. Prebuilt connector action
2. Agent flow wrapping connectors + conditions + approval
3. Custom connector (OpenAPI) for internal APIs
4. HTTP request node (endpoint-filtered via DLP)
5. MCP server tools (dynamic; DLP via connectors)
6. Computer use (no API)

## Auth on tools
Prefer **user credentials** so agent only acts within caller permissions (SharePoint trimming, CRM roles).

## FI/EU delivery tip
Document connection references + environment variables per Dev/Test/Prod; never hardcode endpoints/secrets in topics.
