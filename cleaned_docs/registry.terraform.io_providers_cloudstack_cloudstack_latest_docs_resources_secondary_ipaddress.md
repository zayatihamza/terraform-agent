---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/secondary_ipaddress"
title: "cloudstack_secondary_ipaddress | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_secondary_ipaddress

Assigns a secondary IP to a NIC.

## Example Usage

```hcl hcl
resource "cloudstack_secondary_ipaddress" "default" {
  virtual_machine_id = "server-1"
}
```

## Argument Reference

The following arguments are supported:

- `ip_address` \- (Optional) The IP address to bind the to NIC. If not supplied
an IP address will be selected randomly. Changing this forces a new resource
to be created.

- `nic_id` \- (Optional) The NIC ID to which you want to attach the secondary IP
address. Changing this forces a new resource to be created (defaults to the
ID of the primary NIC)

- `virtual_machine_id` \- (Required) The ID of the virtual machine to which you
want to attach the secondary IP address. Changing this forces a new resource
to be created.

## Attributes Reference

The following attributes are exported:

- `id` \- The secondary IP address ID.
- `ip_address` \- The IP address that was acquired and associated.

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference

Report an issue