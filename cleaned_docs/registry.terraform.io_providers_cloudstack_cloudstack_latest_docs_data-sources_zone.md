---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/data-sources/zone"
title: "cloudstack_zone | Data Sources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_zone

Use this datasource to get information about a zone for use in other resources.

### Example Usage

```hcl hcl
  data "cloudstack_zone" "zone-data-source"{
    filter{
    name = "name"
    value="TestZone"
    }
  }
```

### Argument Reference

- `filter` \- (Required) One or more name/value pairs to filter off of. You can apply filters on any exported attributes.

## Attributes Reference

The following attributes are exported:

- `name` \- The name of the zone.
- `dns1` \- The first DNS for the Zone.
- `internal_dns1` \- The first internal DNS for the Zone.
- `network_type` \- The network type of the zone; can be Basic or Advanced.

#### On this page

- Attributes Reference

Report an issue