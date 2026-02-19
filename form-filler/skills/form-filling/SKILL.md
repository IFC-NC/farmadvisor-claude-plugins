| name | description |
|------|-------------|
| form-filling | Fill out agriculture-related forms using FarmAdvisor data. Guides the user through organization selection, property selection, and form source selection before filling. Trigger with "fill out this form", "help me complete this form", "fill this in with my farm data", or the /form-filler command. |

# Form Filling

A guided, step-by-step process to fill agriculture-related PDF forms using data from FarmAdvisor.

> **CRITICAL RULES — read before doing anything:**
> 1. **Do NOT write your own code to read or fill PDFs.** A bundled script is provided at `${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py` — use it exclusively.
> 2. **Use the FarmAdvisor MCP server tools directly** to execute GraphQL queries. The MCP server is already connected — use its `execute` tool.
> 3. **This is an interactive flow.** Complete each step, present the results to the user, and **wait for their response** before moving to the next step. Do not skip ahead.
> 4. **Return the filled PDF file to the user.** Do not just present text.

---

## Step 1: Select Organization

Use the FarmAdvisor MCP server's `execute` tool to run this query:

```graphql
{
  profile: myUserContext {
    user {
      id
      firstName
      lastName
      fullName
      emailAddress
      uto: userToOrganizations(orderBy: ORGANIZATION_BY_ORGANIZATION_ID__NAME_ASC) {
        nodes {
          organization {
            id
            name
            rootOrganization {
              id
            }
          }
          isDefault
          isAdmin
          isGuest
        }
      }
    }
  }
}
```

**Present the results to the user:**
- **1 organization**: Tell the user which organization was selected and proceed to Step 2.
- **Multiple organizations**: List them all by name. Auto-select the one where `isDefault` is `true`, but ask the user to confirm or switch. **Wait for their response.**
- **0 organizations**: Tell the user no organizations are available and stop.

---

## Step 2: Select Property

Use the FarmAdvisor MCP server's `execute` tool to run this query, substituting the selected organization's `id`:

```graphql
query GetProperties($orgId: String, $excludeDisabled: Boolean) {
  properties(
    filter: {
      organization: {
        hierarchy: {
          includes: $orgId
        }
      }
      disabledAt: { isNull: $excludeDisabled }
    }
    orderBy: [NAME_ASC]
  ) {
    nodes {
      id
      name
      boundingBox
      organization {
        id
        name
      }
      ncreifRegion {
        region
      }
      usdaRegion {
        region
      }
      centroid {
        geojson
      }
      surveyBoundary {
        geojson
      }
      grossAcres
      location
      disabledAt
    }
  }
}
```

**Variables:** `$orgId` = selected organization ID, `$excludeDisabled` = `true`

**Present the results to the user:**
- **1 property**: Tell the user which property was selected and proceed to Step 3.
- **Multiple properties**: List them all (name, location, acres). Ask the user to pick one. **Wait for their response.**
- **0 properties**: Tell the user no properties were found for this organization and stop.

---

## Step 3: Select Form Source

Ask the user how they want to provide the form:

> **How would you like to provide the form to fill?**
> 1. **Upload a file** — Upload your own PDF form
> 2. **Use a file from FarmAdvisor** — Choose from files stored in your organization or property

**Wait for the user's response.**

### Option A: User uploads a file

If the user chooses to upload, ask them to upload their PDF. Once uploaded, proceed to Step 4.

### Option B: Use a file from FarmAdvisor

Query available files from both the organization and the selected property.

**Organization PDF templates:**

```graphql
query GetOrgTemplates($orgId: String!) {
  organization(id: $orgId) {
    pdfTemplate {
      templateFiles {
        key
        name
        url
      }
    }
  }
}
```

**Organization files** (PDFs only — filter by name containing `.pdf`):

```graphql
query GetOrgFiles($orgId: String!) {
  organization(id: $orgId) {
    organizationFiles(
      filter: {
        isFolder: { equalTo: false }
        name: { includesInsensitive: ".pdf" }
      }
      orderBy: [NAME_ASC]
    ) {
      nodes {
        key
        name
        presignedUrl
        createdAt
      }
    }
  }
}
```

**Property files** (PDFs only):

```graphql
query GetPropertyFiles($propertyId: BigInt!) {
  property(id: $propertyId) {
    propertyFiles(
      filter: {
        isFolder: { equalTo: false }
        name: { includesInsensitive: ".pdf" }
      }
      orderBy: [NAME_ASC]
    ) {
      nodes {
        key
        name
        presignedUrl
        createdAt
      }
    }
  }
}
```

**Present all available files to the user**, grouped by source:
- **Templates** (from `pdfTemplate.templateFiles`)
- **Organization Files** (from `organizationFiles`)
- **Property Files** (from `propertyFiles`)

Ask the user to pick one. **Wait for their response.**

Once selected, download the file using its `presignedUrl` (or `url` for templates):

```bash
curl -sL -o /tmp/form.pdf "<presigned_url>"
```

Proceed to Step 4 with the downloaded file.

---

## Step 4: Fill the Form

### 4a. List the PDF's form fields

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --list-fields /path/to/form.pdf
```

This outputs a JSON list of all fillable AcroForm fields with their names, types, and current values.

### 4b. Map FarmAdvisor data to field names

Look at the PDF visually to understand what each field represents, then match AcroForm field names to FarmAdvisor data.

**Common field mappings:**

| Form Field | FarmAdvisor Source |
|---|---|
| Farm/Property Name | `property.name` |
| Organization Name | `property.organization.name` |
| Location / Address | `property.location` |
| Total Acres / Gross Acres | `property.grossAcres` |
| USDA Region | `property.usdaRegion.region` |
| NCREIF Region | `property.ncreifRegion.region` |
| GPS Coordinates | `property.centroid.geojson` |
| Farm Boundary | `property.surveyBoundary.geojson` |

### 4c. Fill the PDF

Build a JSON mapping of `{ "fieldName": "value" }` and run:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --fill /path/to/form.pdf /path/to/filled_form.pdf --data '{"FieldName1": "value1", "FieldName2": "value2"}'
```

For large mappings, write the JSON to a file first:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --fill /path/to/form.pdf /path/to/filled_form.pdf --data-file /tmp/mappings.json
```

### 4d. Return the filled PDF

Give the user the filled PDF file. Tell them:
- Which fields were filled and with what values
- Which fields had no matching data available

Ask the user to review the filled form for accuracy.

---

## Rules

- Only fill fields where the data clearly matches. Do not guess or fabricate values.
- If the form needs data from multiple properties, ask the user to clarify which property applies to each section.
- If the PDF has no fillable AcroForm fields (flat/scanned PDF), tell the user the form is not fillable electronically and present the data as formatted text so they can fill it in manually.
- If additional data is needed beyond what the property query returns, use the MCP server's `search` and `introspect` tools to discover available fields, then `execute` to query them.
