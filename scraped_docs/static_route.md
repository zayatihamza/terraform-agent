cloudstack_static_route

Creates a static route for the given private gateway or VPC.

Example Usage
resource "cloudstack_static_route" "default" {
  cidr       = "10.0.0.0/16"
  gateway_id = "76f607e3-e8dc-4971-8831-b2a2b0cc4cb4"
}
Copy
Argument Reference

The following arguments are supported:

cidr - (Required) The CIDR for the static route. Changing this forces a new resource to be created.

gateway_id - (Required) The ID of the Private gateway. Changing this forces a new resource to be created.

Attributes Reference

The following attributes are exported:

id - The ID of the static route.

***
Example Usage
Argument Reference
Attributes Reference
