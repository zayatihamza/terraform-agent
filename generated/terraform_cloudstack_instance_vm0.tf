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
  api_url    = "https://api.cloudstack.example.com"
  api_key    = "YOUR_API_KEY"
  api_secret = "YOUR_API_SECRET"
}

resource "cloudstack_instance" "instance" {
  name             = "vm0"
  service_offering = "small"
  template         = "asfa"
  zone             = "sfasf"
  network_id       = "REQUIRED_network_id"
  ip_address       = "REQUIRED_ip_address"
}
```