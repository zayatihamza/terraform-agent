---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/domain"
title: "cloudstack_domain | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# CloudStack: cloudstack_domain

A `cloudstack_domain` resource manages a domain within CloudStack.

## Example Usage

```hcl hcl
resource "cloudstack_domain" "example" {
    name = "example-domain"
    network_domain = "example.local"
    parent_domain_id = "ROOT"
}
```

## Argument Reference

The following arguments are supported:

- `name` \- (Required) The name of the domain.
- `domain_id` \- (Optional) The ID of the domain.
- `network_domain` \- (Optional) The network domain for the domain.
- `parent_domain_id` \- (Optional) The ID of the parent domain.

## Attributes Reference

The following attributes are exported:

- `id` \- The ID of the domain.
- `name` \- The name of the domain.
- `network_domain` \- The network domain for the domain.
- `parent_domain_id` \- The ID of the parent domain.

## Import

Domains can be imported; use `<DOMAINID>` as the import ID. For example:

```shell shell
$ terraform import cloudstack_domain.example <DOMAINID>
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue