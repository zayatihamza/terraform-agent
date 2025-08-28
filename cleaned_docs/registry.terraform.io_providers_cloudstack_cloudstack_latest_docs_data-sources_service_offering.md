---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/data-sources/service_offering"
title: "cloudstack_service_offering | Data Sources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_service_offering

Use this datasource to get information about a service offering for use in other resources.

### Example Usage

```hcl hcl
    data "cloudstack_service_offering" "service-offering-data-source"{
    filter{
    name = "name"
    value = "TestServiceUpdate"
    }
  }
```

### Argument Reference

- `filter` \- (Required) One or more name/value pairs to filter off of. You can apply filters on any exported attributes.

## Attributes Reference

The following attributes are exported:

- `name` \- The name of the service offering.
- `display_text` \- An alternate display text of the service offering.

#### On this page

- Attributes Reference

Report an issue