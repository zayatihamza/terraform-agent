---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/data-sources/network_offering"
title: "cloudstack_network_offering | Data Sources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_network_offering

Use this datasource to get information about a network offering for use in other resources.

### Example Usage

```hcl hcl
  data "cloudstack_network_offering" "net-off-data-source"{
    filter{
    name = "name"
    value="TestNetworkDisplay12"
    }
  }
```

### Argument Reference

- `filter` \- (Required) One or more name/value pairs to filter off of. You can apply filters on any exported attributes.

## Attributes Reference

The following attributes are exported:

- `name` \- The name of the network offering.
- `display_text` \- An alternate display text of the network offering.
- `guest_ip_type` \- Guest type of the network offering, can be Shared or Isolated.
- `traffic_type` \- The traffic type for the network offering, supported types are Public, Management, Control, Guest, Vlan or Storage.

#### On this page

- Attributes Reference

Report an issue