---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/data-sources/user"
title: "cloudstack_user | Data Sources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_user

Use this datasource to get information about a cloudstack user for use in other resources.

### Example Usage

```hcl hcl
data "cloudstack_user" "user-data-source"{
    filter{
    name = "first_name"
    value= "jon"
    }
  }
```

### Argument Reference

- `filter` \- (Required) One or more name/value pairs to filter off of. You can apply filters on any exported attributes.

## Attributes Reference

The following attributes are exported:

- `account` \- The account name of the userg.
- `email` \- The user email address.
- `first_name` \- The user firstname.
- `last_name` \- The user lastname.
- `username` \- The user name

#### On this page

- Attributes Reference

Report an issue