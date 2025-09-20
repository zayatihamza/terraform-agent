---
url: "https://registry.terraform.io/providers/cloudstack/cloudstack/latest/docs/resources/disk_offering"
title: "cloudstack_disk_offering | Resources | cloudstack/cloudstack | Terraform | Terraform Registry"
---

Browse cloudstack documentation

# CloudStack: cloudstack_disk_offering

A `cloudstack_disk_offering` resource manages a disk offering within CloudStack.

## Example Usage

```hcl hcl
resource "cloudstack_disk_offering" "example" {
    name = "example-disk-offering"
    display_text = "Example Disk Offering"
    disk_size = 100
}
```

## Argument Reference

The following arguments are supported:

- `name` \- (Required) The name of the disk offering.
- `display_text` \- (Required) The display text of the disk offering.
- `disk_size` \- (Required) The size of the disk offering in GB.

## Attributes Reference

The following attributes are exported:

- `id` \- The ID of the disk offering.
- `name` \- The name of the disk offering.
- `display_text` \- The display text of the disk offering.
- `disk_size` \- The size of the disk offering in GB.

## Import

Disk offerings can be imported; use `<DISKOFFERINGID>` as the import ID. For example:

```shell shell
$ terraform import cloudstack_disk_offering.example <DISKOFFERINGID>
```

#### On this page

- Example Usage
- Argument Reference
- Attributes Reference
- Import

Report an issue