terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "2.48.2"
    }
  }
}

provider "digitalocean" {
 token = var.digitalocean_api_token
}
variable "digitalocean_api_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}
resource "digitalocean_droplet" "example" {
  name   = "fastapi-droplet"
  region = "ams3"               # Choose the region (example: "nyc3" for New York)
  size   = "s-1vcpu-1gb"        # Choose the droplet size (example: "s-1vcpu-1gb")
  image  = "ubuntu-20-04-x64"   # Choose the image (example: "ubuntu-20-04-x64")
  tags   = ["web", "production"] # (Optional) Add tags for easier management
}