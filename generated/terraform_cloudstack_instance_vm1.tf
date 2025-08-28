```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    cloudstack = {
      source  = "cloudstack/cloudstack"
      version = "latest"
    }
  }
}

provider "cloudstack" {
  api_url    = "REQUIRED_api_url"
  api_key    = "REQUIRED_api_key"
  secret_key = "REQUIRED_secret_key"
}

resource "cloudstack_instance" "instance" {
  name             = "vm1"
  service_offering = "small"
  template         = "ubuntu"
  zone             = "zone1"
  network_id       = "REQUIRED_network_id"
}
```