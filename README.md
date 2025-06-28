# Deploying Multiple AI Agents to AWS ECS with Terraform

This project provides a complete setup for deploying two AI agents (a "Researcher" and a "Writer") to AWS ECS using Terraform. The agents are built with FastAPI and LangChain, and they are exposed via an Application Load Balancer.

## Project Structure

```
.
├── .github
│   └── workflows
│       ├── researcher.yml
│       └── writer.yml
├── agents
│   ├── researcher
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   └── writer
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
├── main.py
├── README.md
└── terraform
    ├── main.tf
    ├── outputs.tf
    └── variables.tf
```

## Prerequisites

*   [AWS CLI](https://aws.amazon.com/cli/) configured with your credentials.
*   [Docker](https://www.docker.com/get-started) installed and running.
*   [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed.
*   An [OpenAI API key](https://beta.openai.com/signup/).

## GitHub Actions Deployment

This project includes GitHub Actions workflows to automatically build and push the Docker images for the `researcher` and `writer` agents to Amazon ECR.

### Workflow Triggers

-   The **Researcher Agent** workflow is triggered when changes are pushed to the `main` branch within the `agents/researcher/` directory.
-   The **Writer Agent** workflow is triggered when changes are pushed to the `main` branch within the `agents/writer/` directory.

### Required GitHub Secrets

To allow GitHub Actions to authenticate with your AWS account, you must add the following secrets to your GitHub repository's settings:

-   `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
-   `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.

To add these secrets, go to your GitHub repository and navigate to **Settings** > **Secrets and variables** > **Actions**, then click **New repository secret** for each secret.

Once these secrets are configured, the workflows will automatically build and push the Docker images to ECR whenever the corresponding agent's code is updated on the `main` branch.

## Deployment Steps

### 1. Build and Push Docker Images

The recommended way to build and push the Docker images is to use the provided GitHub Actions workflows. Once you have configured the required secrets, the images will be built and pushed to ECR automatically when you push changes to the `main` branch.

Alternatively, you can build and push the images manually by following these steps:

**a. Login to AWS ECR:**

```bash
aws ecr get-login-password --region <your-aws-region> | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.<your-aws-region>.amazonaws.com
```

**b. Build and Push the Researcher Agent:**

```bash
# Navigate to the researcher agent's directory
cd agents/researcher

# Build the Docker image
docker build -t multi-agent-ecs-researcher .

# Tag the image
docker tag multi-agent-ecs-researcher:latest <your-aws-account-id>.dkr.ecr.<your-aws-region>.amazonaws.com/multi-agent-ecs-researcher:latest

# Push the image to ECR
docker push <your-aws-account-id>.dkr.ecr.<your-aws-region>.amazonaws.com/multi-agent-ecs-researcher:latest

# Return to the root directory
cd ../..
```

**c. Build and Push the Writer Agent:**

```bash
# Navigate to the writer agent's directory
cd agents/writer

# Build the Docker image
docker build -t multi-agent-ecs-writer .

# Tag the image
docker tag multi-agent-ecs-writer:latest <your-aws-account-id>.dkr.ecr.<your-aws-region>.amazonaws.com/multi-agent-ecs-writer:latest

# Push the image to ECR
docker push <your-aws-account-id>.dkr.ecr.<your-aws-region>.amazonaws.com/multi-agent-ecs-writer:latest

# Return to the root directory
cd ../..
```

### 2. Deploy with Terraform

Now that the Docker images are in ECR, you can deploy the infrastructure using Terraform.

**a. Initialize Terraform:**

```bash
# Navigate to the terraform directory
cd terraform

# Initialize Terraform
terraform init
```

**b. Plan the Deployment:**

```bash
# Create a terraform.tfvars file with your OpenAI API key
echo 'openai_api_key = "your-openai-api-key"' > terraform.tfvars

# Run terraform plan
terraform plan -var-file="terraform.tfvars"
```

**c. Apply the Configuration:**

```bash
# Apply the Terraform configuration
terraform apply -var-file="terraform.tfvars" -auto-approve
```

Terraform will now provision all the necessary AWS resources. This process will take a few minutes. Once it's complete, Terraform will output the DNS name of the Application Load Balancer.

### 3. Test the Agents

You can now interact with your deployed agents using the ALB DNS name.

**a. Get the ALB DNS Name:**

You can get the ALB DNS name from the Terraform output:

```bash
terraform output alb_dns_name
```

**b. Send a Request to the Researcher Agent:**

```bash
curl -X POST http://<your-alb-dns-name>/research \
-H "Content-Type: application/json" \
-d '{"topic": "The future of AI"}'
```

**c. Send a Request to the Writer Agent:**

```bash
# First, get some research notes from the researcher
RESEARCH_NOTES=$(curl -s -X POST http://<your-alb-dns-name>/research \
-H "Content-Type: application/json" \
-d '{"topic": "The future of AI"}' | jq -r .results)

# Now, send the research notes to the writer
curl -X POST http://<your-alb-dns-name>/write \
-H "Content-Type: application/json" \
-d '{
  "topic": "The future of AI",
  "research_notes": "'""$RESEARCH_NOTES""'"
}'
```

## Cleanup

To avoid incurring ongoing costs, you should destroy the AWS resources when you're finished.

```bash
# Navigate to the terraform directory
cd terraform

# Destroy the AWS resources
terraform destroy -var-file="terraform.tfvars" -auto-approve
```

This will remove all the resources that were created by Terraform. You will also need to manually delete the ECR repositories if you no longer need them.

```