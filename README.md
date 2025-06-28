# Langchain Agents & Infrastructure

This repository houses a collection of AI agents built with Langchain, along with the necessary infrastructure defined using Terraform.

## Features

-   **Researcher Agent**: An AI agent designed for research tasks.
-   **Writer Agent**: An AI agent focused on generating written content.
-   **Terraform Infrastructure**: Infrastructure as Code (IaC) for deploying the necessary cloud resources.
-   **GitHub Actions CI/CD**: Automated workflows for building, testing, and deploying the agents and infrastructure.

## Prerequisites

Before you begin, ensure you have the following installed:

-   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
-   [Python 3.9+](https://www.python.org/downloads/)
-   [Docker](https://docs.docker.com/get-docker/)
-   [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## Setup

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Set up Python Virtual Environment** (for local development/dependency management):

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

## Running the Agents

Each agent (researcher, writer) is containerized using Docker. You can build and run them as follows:

### Researcher Agent

```bash
cd agents/researcher
docker build -t researcher-agent .
docker run researcher-agent
```

### Writer Agent

```bash
cd agents/writer
docker build -t writer-agent .
docker run writer-agent
```

*Note: You may need to configure environment variables or API keys for the agents to function correctly. Refer to each agent's `main.py` for details.*

## Infrastructure Deployment (Terraform)

The `terraform/` directory contains the infrastructure definitions. To deploy:

1.  **Initialize Terraform**:

    ```bash
    cd terraform
    terraform init
    ```

2.  **Review the plan** (optional but recommended):

    ```bash
    terraform plan
    ```

3.  **Apply the changes**:

    ```bash
    terraform apply
    ```

    Type `yes` when prompted to confirm the deployment.

4.  **Destroy the infrastructure** (when no longer needed):

    ```bash
    terraform destroy
    ```

    Type `yes` when prompted to confirm.

*Note: Ensure your AWS (or other cloud provider) credentials are configured for Terraform to access your account.*

## CI/CD with GitHub Actions

This repository uses GitHub Actions for automated deployments. The workflow defined in `.github/workflows/deploy.yml` handles:

-   Building Docker images for the agents.
-   Deploying the infrastructure via Terraform.

Refer to the `deploy.yml` file for specific triggers and steps.