---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/security_group"
title: "cloudstack_security_group | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_security_group

Creates a security group.

## Example Usage

```hcl hcl
resource "cloudstack_security_group" "default" {
  name        = "allow_web"
  description = "Allow access to HTTP and HTTPS"
}
```

## Argument Reference

The following arguments are supported:

- `name` \- (Required) The name of the security group. Changing this forces a
new resource to be created.

- `description` \- (Optional) The description of the security group. Changing
this forces a new resource to be created.

- `project` \- (Optional) The name or ID of the project to create this security
group in. Changing this forces a new resource to be created.

## Attributes Reference

The following attributes are exported:

- `id` \- The ID of the security group.

## Import

Security groups can be imported; use `<SECURITY GROUP ID>` as the import ID. For
example:

```shell shell
terraform import cloudstack_security_group.default e54970f1-f563-46dd-a365-2b2e9b78c54b
```

When importing into a project you need to prefix the import ID with the project name:

```shell shell
terraform import cloudstack_security_group.default my-project/e54970f1-f563-46dd-a365-2b2e9b78c54b
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue