---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/zone"
title: "cloudstack_zone | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# CloudStack: cloudstack_zone

A `cloudstack_zone` resource manages a zone within CloudStack.

## Example Usage

```hcl hcl
resource "cloudstack_zone" "example" {
    name = "example-zone"
    dns1 = "8.8.8.8"
    internal_dns1 = "8.8.4.4"
    network_type = "Basic"
}
```

## Argument Reference

The following arguments are supported:

- `name` \- (Required) The name of the zone.
- `dns1` \- (Required) The DNS server 1 for the zone.
- `internal_dns1` \- (Required) The internal DNS server 1 for the zone.
- `network_type` \- (Required) The type of network to use for the zone.

## Attributes Reference

The following attributes are exported:

- `id` \- The ID of the zone.
- `name` \- The name of the zone.
- `dns1` \- The DNS server 1 for the zone.
- `internal_dns1` \- The internal DNS server 1 for the zone.
- `network_type` \- The type of network to use for the zone.

## Import

Zones can be imported; use `<ZONEID>` as the import ID. For example:

```shell shell
$ terraform import cloudstack_zone.example <ZONEID>
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue