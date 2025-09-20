---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/private_gateway"
title: "cloudstack_private_gateway | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_private_gateway

Creates a private gateway for the given VPC.

_NOTE: private gateway can only be created using a ROOT account!_

## Example Usage

```hcl hcl
resource "cloudstack_private_gateway" "default" {
  gateway    = "10.0.0.1"
  ip_address = "10.0.0.2"
  netmask    = "255.255.255.252"
  vlan       = "200"
  vpc_id     = "76f6e8dc-07e3-4971-b2a2-8831b0cc4cb4"
}
```

## Argument Reference

The following arguments are supported:

- `gateway` \- (Required) the gateway of the Private gateway. Changing this
forces a new resource to be created.

- `ip_address` \- (Required) the IP address of the Private gateway. Changing this forces
a new resource to be created.

- `netmask` \- (Required) The netmask of the Private gateway. Changing
this forces a new resource to be created.

- `vlan` \- (Required) The VLAN number (1-4095) the network will use.

- `physical_network_id` \- (Optional) The ID of the physical network this private
gateway belongs to.

- `network_offering` \- (Optional) The name or ID of the network offering to use for
the private gateways network connection.

- `acl_id` \- (Required) The ACL ID that should be attached to the network.

- `vpc_id` \- (Required) The VPC ID in which to create this Private gateway. Changing
this forces a new resource to be created.

## Attributes Reference

The following attributes are exported:

- `id` \- The ID of the private gateway.

## Import

Private gateways can be imported; use `<PRIVATE GATEWAY ID>` as the import ID. For
example:

```shell shell
terraform import cloudstack_private_gateway.default e42a24d2-46cb-4b18-9d41-382582fad309
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue