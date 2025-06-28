
# variables.tf

variable "aws_region" {
  description = "The AWS region to deploy resources to."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "A unique name for your project, used as a prefix for resources."
  type        = string
  default     = "langchain-agents"
}

variable "public_subnets_cidr" {
  description = "List of CIDR blocks for public subnets."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "openai_api_key" {
  description = "OpenAI API key for accessing OpenAI services."
  type        = string
  sensitive   = true
  default     = ""
  
}
