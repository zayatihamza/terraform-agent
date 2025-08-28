---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/data-sources/vpc"
title: "cloudstack_vpc | Data Sources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_vpc

Use this datasource to get information about a vpc for use in other resources.

### Example Usage

```hcl hcl
data "cloudstack_vpc" "vpc-data-source"{
    filter{
    name = "name"
    value= "test-vpc"
    }
    filter{
    name = "cidr"
    value= "10.0.0.0/16"
  }
```

### Argument Reference

- `filter` \- (Required) One or more name/value pairs to filter off of. You can apply filters on any exported attributes.

## Attributes Reference

The following attributes are exported:

- `name` \- The name of the VPC.
- `display_text` \- An alternate display text of the VPC.
- `cidr` \- The cidr the VPC.
- `vpc_offering_name` \- Vpc offering name the VPC is created from.
- `network_domain` \- The network domain of the VPC.
- `project` \- The project name of the VPC.
- `zone_name` \- The name of the zone the VPC belongs to.

#### On this page

- Attributes Reference

Report an issue