
variable "aws_region" {
  description = "The AWS region to deploy the resources to."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "multi-agent-ecs"
}

variable "openai_api_key" {
  description = "The OpenAI API key."
  type        = string
  sensitive   = true
}
