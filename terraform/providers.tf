# Data sources for current AWS context
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_partition" "current" {}

# Random suffix for unique resource naming
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

locals {
  # Common tags applied to all resources
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    CreatedBy   = data.aws_caller_identity.current.user_id
    Region      = data.aws_region.current.name
  }
  
  # Naming convention with random suffix to avoid conflicts
  name_prefix = "${var.project_name}-${var.environment}-${random_string.suffix.result}"
}

provider "aws" {
  region  = var.aws_region
  profile = "raj-private"
  
  default_tags {
    tags = local.common_tags
  }
}
