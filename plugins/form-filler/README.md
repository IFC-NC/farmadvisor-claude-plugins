# Form Filler Plugin

Fill out agriculture-related forms using data from FarmAdvisor organizations and properties.

## Overview

The Form Filler plugin helps users complete agriculture-related forms by pulling data from their FarmAdvisor account. When a user uploads a form, the plugin scopes into the correct organization, loads the relevant properties, and uses that data to populate form fields.

## Setup Flow

When a user wants to fill out a form, follow these steps in order:

### Step 1: Organization Selection

Query the user's profile and organization memberships:

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
- If there is **1** organization in `uto.nodes`: Auto-select that organization. Inform the user which organization was selected and proceed to Step 2.
- If there are **multiple** organizations: Select the one where `isDefault` is `true`. Inform the user which organization was auto-selected (their default). If the user wants to switch, present the full list by name and let them choose. Proceed to Step 2.
- If there are **0** organizations: Inform the user that no organizations are available and stop.

### Step 2: Load Properties

Once an organization is selected, load the properties for that organization. Use the selected organization's `id` as the `$orgId` variable:

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

### Step 3: Fill the Form

With the organization and property data loaded, analyze the uploaded form and map FarmAdvisor data to the appropriate form fields. Common field mappings include:

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

If the form requires data for a specific property, ask the user to select one from the loaded list. If only one property exists, auto-select it.

## Usage

1. Upload a form (PDF, image, or document)
2. The plugin will query your organizations and auto-select or prompt you to choose
3. Properties are loaded for the selected organization
4. The plugin maps FarmAdvisor data to form fields and fills them in

## Requirements

- Active FarmAdvisor account with at least one organization
- MCP server connection to `https://ai.farmadvisor.com/mcp`
