provider "aws" {
  region  = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket = "yfinance-ingestion-backend"
    key    = "application.tfstate"
    region = "eu-west-2"
  }
}