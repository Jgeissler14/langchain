from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, ECR
from diagrams.aws.network import ELB, VPC, PublicSubnet, InternetGateway, RouteTable
from diagrams.aws.security import IAMRole
from diagrams.generic.network import Router

with Diagram("Cloud Architecture", show=False, filename="cloud_architecture"):
    internet = Router("User")

    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            igw = InternetGateway("Internet Gateway")

            with Cluster("Public Subnets"):
                alb = ELB("Application Load Balancer")

            rt = RouteTable("Route Table")
            internet >> igw >> rt >> alb

        with Cluster("ECR"):
            researcher_repo = ECR("Researcher ECR Repository")
            writer_repo = ECR("Writer ECR Repository")

        with Cluster("ECS Cluster (Fargate)"):
            researcher_service = ECS("Researcher Service")
            writer_service = ECS("Writer Service")

        # ALB Routing
        alb >> Edge(label="/research") >> researcher_service
        alb >> Edge(label="/write") >> writer_service

        # Image Pulling
        researcher_service << researcher_repo
        writer_service << writer_repo