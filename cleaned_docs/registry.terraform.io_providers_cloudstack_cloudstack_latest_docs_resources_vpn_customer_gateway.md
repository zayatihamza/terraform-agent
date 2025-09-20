---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/vpn_customer_gateway"
title: "cloudstack_vpn_customer_gateway | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_vpn_customer_gateway

Creates a site to site VPN local customer gateway.

## Example Usage

Basic usage:

```hcl hcl
resource "cloudstack_vpn_customer_gateway" "default" {
  name       = "test-vpc"
  cidr       = "10.0.0.0/8"
  esp_policy = "aes256-sha1;modp1024"
  gateway    = "192.168.0.1"
  ike_policy = "aes256-sha1;modp1024"
  ipsec_psk  = "terraform"
}
```

## Argument Reference

The following arguments are supported:

- `name` \- (Required) The name of the VPN Customer Gateway.

- `cidr` \- (Required) The CIDR block that needs to be routed through this gateway.

- `esp_policy` \- (Required) The ESP policy to use for this VPN Customer Gateway.

- `gateway` \- (Required) The public IP address of the related VPN Gateway.

- `ike_policy` \- (Required) The IKE policy to use for this VPN Customer Gateway.

- `ipsec_psk` \- (Required) The IPSEC pre-shared key used for this gateway.

- `dpd` \- (Optional) If DPD is enabled for the related VPN connection (defaults false)

- `esp_lifetime` \- (Optional) The ESP lifetime of phase 2 VPN connection to this
VPN Customer Gateway in seconds (defaults 86400)

- `ike_lifetime` \- (Optional) The IKE lifetime of phase 2 VPN connection to this
VPN Customer Gateway in seconds (defaults 86400)

- `project` \- (Optional) The name or ID of the project to create this VPN Customer
Gateway in. Changing this forces a new resource to be created.

## Attributes Reference

The following attributes are exported:

- `id` \- The ID of the VPN Customer Gateway.
- `dpd` \- Enable or disable DPD is enabled for the related VPN connection.
- `esp_lifetime` \- The ESP lifetime of phase 2 VPN connection to this VPN Customer Gateway.
- `ike_lifetime` \- The IKE lifetime of phase 2 VPN connection to this VPN Customer Gateway.

## Import

VPN customer gateways can be imported; use `<VPN CUSTOMER GATEWAY ID>` as the import ID. For
example:

```shell shell
terraform import cloudstack_vpn_customer_gateway.default 741a7fca-1d05-4bb6-9290-1008300f0e5a
```

When importing into a project you need to prefix the import ID with the project name:

```shell shell
terraform import cloudstack_vpn_customer_gateway.default my-project/741a7fca-1d05-4bb6-9290-1008300f0e5a
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue