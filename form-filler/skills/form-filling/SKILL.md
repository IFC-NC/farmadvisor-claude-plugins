| name | description |
|------|-------------|
| form-filling | Fill out agriculture-related forms using FarmAdvisor data. Automatically selects the user's organization, loads properties, and maps farm data to form fields. Trigger with "fill out this form", "help me complete this form", "fill this in with my farm data", or when a user uploads a form document. |

# Form Filling

Fill out agriculture-related forms by pulling organization and property data from FarmAdvisor. Works with PDFs, images, and documents.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│ FORM FILLER                                                     │
├─────────────────────────────────────────────────────────────────┤
│ STEP 1: Organization Selection                                  │
│  ✓ Query user's profile and organization memberships            │
│  ✓ Auto-select if only one org available                        │
│  ✓ Auto-select default org if multiple available                │
│  ✓ Allow user to switch organizations                           │
├─────────────────────────────────────────────────────────────────┤
│ STEP 2: Load Properties                                         │
│  ✓ Fetch all active properties for the selected organization    │
│  ✓ Include name, location, acreage, regions, boundaries         │
│  ✓ Auto-select if only one property, otherwise ask user         │
├─────────────────────────────────────────────────────────────────┤
│ STEP 3: Fill the Form                                           │
│  ✓ Analyze the uploaded form to identify fields                 │
│  ✓ Map FarmAdvisor data to matching form fields                 │
│  ✓ Present completed form for user review                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Execution Flow

### Step 1: Organization Selection

Query the user's profile and organization memberships using the FarmAdvisor MCP server:

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

**Selection logic:**
- If there is **1** organization in `uto.nodes`: Auto-select it. Inform the user which organization was selected and proceed to Step 2.
- If there are **multiple** organizations: Select the one where `isDefault` is `true`. Inform the user which organization was auto-selected (their default). If the user wants to switch, present the full list by name and let them choose. Proceed to Step 2.
- If there are **0** organizations: Inform the user that no organizations are available and stop.

### Step 2: Load Properties

Once an organization is selected, load the properties. Use the selected organization's `id` as the `$orgId` variable:

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

**Variables:**
- `$orgId`: The `id` of the selected organization
- `$excludeDisabled`: Set to `true` to exclude disabled properties

**Property selection:**
- If **1** property: Auto-select it.
- If **multiple** properties: Ask the user which property (or properties) the form relates to.
- If **0** properties: Inform the user no properties were found for this organization.

### Step 3: Fill the Form

With organization and property data loaded, analyze the uploaded form and map FarmAdvisor data to the appropriate fields.

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

**Guidelines:**
- Only fill fields where the data clearly matches. Do not guess.
- If a form field doesn't map to any available data, leave it blank and note it for the user.
- Present the completed form to the user for review before finalizing.
- If the form spans multiple properties, ask the user to clarify which property applies to each section.

---

## Tips

1. **Upload the form first** — Provide the form as a PDF, image, or document so it can be analyzed.
2. **Specify the property** — If you have multiple properties, mention which one the form is for.
3. **Review before submitting** — Always review the filled fields for accuracy before using the form.
