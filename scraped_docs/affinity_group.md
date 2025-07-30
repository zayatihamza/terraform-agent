
cloudstack_affinity_group

Creates an affinity group.

Example Usage
resource "cloudstack_affinity_group" "default" {
  name = "test-affinity-group"
  type = "host anti-affinity"
}
Copy
Argument Reference

The following arguments are supported:

name - (Required) The name of the affinity group. Changing this forces a new resource to be created.

description - (Optional) The description of the affinity group.

type - (Required) The affinity group type. Changing this forces a new resource to be created.

project - (Optional) The name or ID of the project to register this affinity group to. Changing this forces a new resource to be created.

Attributes Reference

The following attributes are exported:

id - The id of the affinity group.
description - The description of the affinity group.
Import

Affinity groups can be imported; use <AFFINITY GROUP ID> as the import ID. For example:

terraform import cloudstack_affinity_group.default 6226ea4d-9cbe-4cc9-b30c-b9532146da5b
Copy

When importing into a project you need to prefix the import ID with the project name:

terraform import cloudstack_affinity_group.default my-project/6226ea4d-9cbe-4cc9-b30c-b9532146da5b

***
Example Usage
Argument Reference
Attributes Reference
Import

