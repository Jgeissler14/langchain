
# outputs.tf

output "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer."
  value       = aws_lb.main.dns_name
}

output "researcher_ecr_repo_url" {
  description = "URL of the ECR repository for the researcher agent."
  value       = aws_ecr_repository.researcher.repository_url
}

output "writer_ecr_repo_url" {
  description = "URL of the ECR repository for the writer agent."
  value       = aws_ecr_repository.writer.repository_url
}
