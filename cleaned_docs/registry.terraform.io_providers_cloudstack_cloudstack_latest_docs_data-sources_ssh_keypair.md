---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/data-sources/ssh_keypair"
title: "cloudstack_ssh_keypair | Data Sources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# cloudstack_ssh_keypair

Use this datasource to get information about a ssh keypair for use in other resources.

### Example Usage

```hcl hcl
  data "cloudstack_ssh_keypair" "ssh-keypair-data" {
      filter {
      name = "name"
      value = "myKey"
    }
  }
```

### Argument Reference

- `filter` \- (Required) One or more name/value pairs to filter off of. You can apply filters on any exported attributes.

## Attributes Reference

The following attributes are exported:

- `name` \- Name of the keypair.
- `fingerprint` \- Fingerprint of the public key.

#### On this page

- Attributes Reference

Report an issue