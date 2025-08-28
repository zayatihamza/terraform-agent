```hcl
resource "cloudstack_instance" "example" {
  name             = "server-1"
  service_offering = "small"
  template         = "123"
  zone             = "sone-1"
}
```