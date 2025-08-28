---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/vpn_gateway"
title: "cloudstack_vpn_gateway | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_vpn_gateway

Creates a site to site VPN local gateway.

## Example Usage

Basic usage:

```hcl hcl
resource "cloudstack_vpn_gateway" "default" {
  vpc_id = "f8141e2f-4e7e-4c63-9362-986c908b7ea7"
}
```

## Argument Reference

The following arguments are supported:

- `vpc_id` \- (Required) The ID of the VPC for which to create the VPN Gateway.
Changing this forces a new resource to be created.

## Attributes Reference

The following attributes are exported:

- `id` \- The ID of the VPN Gateway.
- `public_ip` \- The public IP address associated with the VPN Gateway.

## Import

VPC gateways can be imported; use `<VPN GATEWAY ID>` as the import ID. For
example:

```shell shell
terraform import cloudstack_vpn_gateway.default 49cf1821-3b9f-4627-be19-8a15ffec508d
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue