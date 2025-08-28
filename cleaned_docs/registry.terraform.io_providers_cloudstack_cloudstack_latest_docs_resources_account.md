---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/account"
title: "cloudstack_account | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# CloudStack: cloudstack_account

A `cloudstack_account` resource manages an account within CloudStack.

## Example Usage

```hcl hcl
resource "cloudstack_account" "example" {
    email = "user@example.com"
    first_name = "John"
    last_name = "Doe"
    password = "securepassword"
    username = "jdoe"
    account_type = 1 # 1 for admin, 2 for domain admin, 0 for regular user
    role_id = "1234abcd" # ID of the role associated with the account
}
```

## Argument Reference

The following arguments are supported:

- `email` \- (Required) The email address of the account owner.
- `first_name` \- (Required) The first name of the account owner.
- `last_name` \- (Required) The last name of the account owner.
- `password` \- (Required) The password for the account.
- `username` \- (Required) The username of the account.
- `account_type` \- (Required) The account type. Possible values are `0` for regular user, `1` for admin, and `2` for domain admin.
- `role_id` \- (Required) The ID of the role associated with the account.
- `account` \- (Optional) The account name. If not specified, the username will be used as the account name.

## Attributes Reference

The following attributes are exported:

- `id` \- The ID of the account.

## Import

Accounts can be imported; use `<ACCOUNTID>` as the import ID. For example:

```shell shell
$ terraform import cloudstack_account.example <ACCOUNTID>
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue