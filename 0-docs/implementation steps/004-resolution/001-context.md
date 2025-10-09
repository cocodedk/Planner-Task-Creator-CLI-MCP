# Resolution Module Context

**Purpose**: Resolve plan and bucket names to IDs using Microsoft Graph API.

**Scope**: Handle name-to-ID resolution with case-insensitive matching and ambiguity detection.

**Key Requirements**:
- Case-insensitive name matching
- ID detection (GUID format validation)
- Ambiguity detection with candidate suggestions
- Structured error responses for CLI
