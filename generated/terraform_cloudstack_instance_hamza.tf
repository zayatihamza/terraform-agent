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
  name             = "hamza"
  service_offering = "azlkfna"
  template         = "akfnaf"
  zone             = "aflknasf"
  network_id       = "REQUIRED_network_id"
}
```