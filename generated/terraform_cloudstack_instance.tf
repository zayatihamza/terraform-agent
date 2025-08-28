```hcl
provider "cloudstack" {
  # Configuration options
}

resource "cloudstack_instance" "instance" {
  name             = "vm1"
  service_offering = "small"
  template         = "ubuntu"
  zone             = "zone1"
  # network_id       = "<FILL network_id>" # Optional
  # ip_address       = "<FILL ip_address>" # Optional
  # keypair          = "<FILL keypair>" # Optional
  # security_group_ids = ["<FILL security_group_id>"] # Optional
  # security_group_names = ["<FILL security_group_name>"] # Optional
  # project         = "<FILL project>" # Optional
}
```