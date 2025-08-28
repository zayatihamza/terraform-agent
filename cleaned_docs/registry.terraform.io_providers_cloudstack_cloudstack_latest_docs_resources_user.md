---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/user"
title: "cloudstack_user | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# CloudStack: cloudstack_user

A `cloudstack_user` resource manages a user within CloudStack.

## Example Usage

```hcl hcl
resource "cloudstack_user" "example" {
    account = "example-account"
    email = "user@example.com"
    first_name = "John"
    last_name = "Doe"
    password = "securepassword"
    username = "jdoe"
}
```

## Argument Reference

The following arguments are supported:

- `account` \- (Optional) The account the user belongs to.
- `email` \- (Required) The email address of the user.
- `first_name` \- (Required) The first name of the user.
- `last_name` \- (Required) The last name of the user.
- `password` \- (Required) The password for the user.
- `username` \- (Required) The username of the user.

## Attributes Reference

No attributes are exported.

## Import

Users can be imported; use `<USERID>` as the import ID. For example:

```shell shell
$ terraform import cloudstack_user.example <USERID>
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue