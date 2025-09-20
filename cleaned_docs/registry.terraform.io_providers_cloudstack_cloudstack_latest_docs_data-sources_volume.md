---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/data-sources/volume"
title: "cloudstack_volume | Data Sources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_volume

Use this datasource to get information about a volume for use in other resources.

### Example Usage

```hcl hcl
  data "cloudstack_volume" "volume-data-source"{
    filter{
    name = "name"
    value="TestVolume"
    }
  }
```

### Argument Reference

- `filter` \- (Required) One or more name/value pairs to filter off of. You can apply filters on any exported attributes.

## Attributes Reference

The following attributes are exported:

- `name` \- Name of the disk volume.
- `disk_offering_id` \- ID of the disk offering.
- `zone_id` \- ID of the availability zone.

#### On this page

- Attributes Reference

Report an issue