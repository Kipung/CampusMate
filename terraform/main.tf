terraform {
  required_providers {
    fly = {
      source = "fly-apps/fly"
      version = "~> 0.0.29"
    }
  }
}

provider "fly" {
  # Configuration options
}

resource "fly_app" "campusmate" {
  name = "campusmate"
  org  = "personal"
}

resource "fly_volume" "campusmate_data" {
  app    = fly_app.campusmate.name
  name   = "data"
  size   = 1
  region = "sjc"
}
