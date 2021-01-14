---
title: "Terraform files explanation"
date: 2018-09-18T16:01:14-05:00
weight: 535
---

### Terraform files and explanation


The first three files have been pre-created from the gen-backend.sh script in the tf-setup stage, The S3 bucket and DynamoDB tables were also pre-created in the tf-setup stage.

### backend-net.tf

This specifices the location of the backend Terraform state file on S3 and the dynamoDB table used for the state file locking. Also the Terraform version requirements.

{{%expand "Expand here to see the code" %}}
```bash
terraform {
required_version = "~> 0.14.3"
required_providers {
  aws = {
   source = "hashicorp/aws"
#  Allow any 3.1x version of the AWS provider
   version = "~> 3.22"
  }
 }
backend "s3" {
bucket = "terraform-state-ip-172-31-2-146"
key = "terraform/terraform_locks_net.tfstate"
region = "eu-west-1"
dynamodb_table = "terraform_locks_net"
encrypt = "true"
}
}
provider "aws" {
region = var.region
shared_credentials_file = "~/.aws/credentials"
profile = var.profile
}
```

{{%/expand%}}

---

### vars-dynamodb.tf

This file defines some varaibles with default values for the seven DynamoDB tables.


{{%expand "Expand here to see the code" %}}
```bash
variable "table_name_net" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-net"
}

variable "table_name_iam" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-iam"
}

variable "table_name_c9net" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-c9net"
}

variable "table_name_cicd" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-cicd"
}

variable "table_name_cluster" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-cluster"
}

variable "table_name_nodeg" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-nodeg"
}

variable "table_name_eks-cidr" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-eks-cidr"
}
```

{{%/expand%}}

---

### vars-main.tf

This file defines some varaibles with default the region and default profile name and EKS cluster name


{{%expand "Expand here to see the code" %}}
```bash
# TF_VAR_region
variable "region" {
  description = "The name of the AWS Region"
  type        = string
  default     = "eu-west-1"
}

variable "profile" {
  description = "The name of the AWS profile in the credentials file"
  type        = string
  default     = "default"
}

variable "cluster-name" {
  description = "The name of the EKS Cluster"
  type        = string
  default     = "mycluster1"
}

variable "stages" {
type=list(string)
default=["net","iam","c9net","cluster","nodeg","cicd","eks-cidr"]
}

variable "stagecount" {
type=number
default=7
}

```

{{%/expand%}}

---

### vpc-mycluster1.tf

This defines the VPC we are going to use, note the "output" variables eks-vpc and eks-cidr, These values can be accessed from other build sections using Terraform remote state which will be descibled later.

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_vpc" "vpc-mycluster1" {
  assign_generated_ipv6_cidr_block = false
  cidr_block                       = "10.0.0.0/22"
  enable_classiclink               = false
  enable_classiclink_dns_support   = false
  enable_dns_hostnames             = true
  enable_dns_support               = true
  instance_tenancy                 = "default"
  tags = {
    "Name"                                        = "mycluster1-cluster/VPC"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = var.cluster-name
  }
}

output "eks-vpc" {
  value = aws_vpc.vpc-mycluster1.id
}

output "eks-cidr" {
  value = aws_vpc.vpc-mycluster1.cidr_block
}
```

{{%/expand%}}

---


### aws_vpc_ipv4_cidr_block_association__vpc-cidr-assoc.tf

This adds a secondary CIDR block to the VPC using the RFC6598 address space 100.64.0.0/16. This is used by a set of 3 additional subnets that can be dedicated to Kubernetes pods. This capability will be explored later in the workshop.


{{%expand "Expand here to see the code" %}}
```bash
resource "aws_vpc_ipv4_cidr_block_association" "vpc-cidr-assoc" {
  cidr_block = "100.64.0.0/16"
  vpc_id     = aws_vpc.vpc-mycluster1.id

  timeouts {}
}

```

{{%/expand%}}

---

### subnets-eks.tf

This file defines the 6x private subnets into which we will provision the managed worker node network interfaces that make up our clusters node groups. Three private subnets in the 10.0.x.x address space and three more in the secondary CIDR address space 100.64.x.x.

Note once agian that an outputs for the firat 3 subnets *sub-priv1* etc. are defined.

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_subnet" "subnet-p1" {
  assign_ipv6_address_on_creation = false
  availability_zone               = "eu-west-1a"
  cidr_block                      = "10.0.1.0/24"
  map_public_ip_on_launch         = false
  tags = {
    "Name"                                        = "Private1"
 #   "alpha.eksctl.io/cluster-name"                = "mycluster1"
 #   "alpha.eksctl.io/eksctl-version"              = "0.29.2"
 #   "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
    "kubernetes.io/cluster/mycluster1"            = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
    "workshop" = "subnet-p1"
  }
  vpc_id = aws_vpc.vpc-mycluster1.id

  timeouts {}
}

output "sub-priv1" {
  value = aws_subnet.subnet-p1.id
}

** contents truncated for brevity **

resource "aws_subnet" "subnet-i1" {
  depends_on=[aws_vpc_ipv4_cidr_block_association.vpc-cidr-assoc]
  assign_ipv6_address_on_creation = false
  availability_zone               = "eu-west-1a"
  cidr_block                      = "100.64.0.0/19"
  map_public_ip_on_launch         = false
  tags = {
    "Name"                                        = "i1-mycluster1"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
    "kubernetes.io/cluster/mycluster1"            = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
  vpc_id = aws_vpc.vpc-mycluster1.id

  timeouts {}
}
```

{{%/expand%}}

---


Two security groups are now defined that are used by our EKS cluster. The cluster shared node security group is used to enable all nodes within the cluster to communicate with each other. Note the output value *allnodes-sg* which is used by other sections of the cluster build.

### aws_security_group__allnodes-sg.tf

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_security_group" "sg-073762dd312483127" {
  description = "Communication between all nodes in the cluster"
  vpc_id      = aws_vpc.vpc-mycluster1.id
  tags = {
    "alpha.eksctl.io/cluster-name"                = "mycluster1"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
    "Name"                                        = "eksctl-mycluster1-cluster/ClusterSharedNodeSecurityGroup"
    "alpha.eksctl.io/eksctl-version"              = "0.29.2"
    "Label"                            = "TF-EKS All Nodes Comms"
  }
}

output "allnodes-sg" {
  value = aws_security_group.sg-073762dd312483127.id
}

```

{{%/expand%}}

---


### aws_security_group__cluster-sg.tf

This second security group is the "cluster security group" and controls traffic between the control plane and all worker nodes, another output is defined for the security group id **cluster-sg** This is used later during the build.

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_security_group" "sg-0a1578a53b37b12c6" {
  description = "Communication between the control plane and worker nodegroups"
  vpc_id      = aws_vpc.vpc-mycluster1.id
  tags = {
    "alpha.eksctl.io/cluster-name"                = "mycluster1"
    "alpha.eksctl.io/eksctl-version"              = "0.29.2"
    "Name"                                        = "eksctl-mycluster1-cluster/ControlPlaneSecurityGroup"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
    "Label"                            = "TF-EKS Control Plane & all worker nodes comms"
  }
}

output "cluster-sg" {
  value = aws_security_group.sg-0a1578a53b37b12c6.id
}
```

{{%/expand%}}


**Note that neither of these security groups have any rules associated with them at this stage, they get populated later on by the provisioning of the cluster and node groups.**

---

Next 4 route tables are defined, only one of them is shown here. Note there arte no routes defined, these get populated later. 

###  aws_route_table__rtb-*.tf

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_route_table" "rtb-0939e7f3ae6e7b829" {
  propagating_vgws = []
  route            = []
  tags             = {}
  vpc_id           = aws_vpc.vpc-mycluster1.id
}

```

{{%/expand%}}

---


The route tables are associated with the 6 subnets, as they are all similar only one is shown here. Note the output value for the route table id. This is used in the section to adjust the route table's routes in the c9net (Cloud9 IDE Networking) section, where we connect the Cloud9 IDE & Default VPC to our private EKS VPC.

###  aws_route_table_association__rtbassoc-*.tf

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_route_table_association" "rtbassoc-029eb518ff8c1739a" {
  route_table_id = aws_route_table.rtb-041267f0474c24068.id
  subnet_id      = aws_subnet.subnet-p1.id
}


output "rtb-priv1" {
  value = aws_route_table.rtb-041267f0474c24068.id
}

```

{{%/expand%}}

---

### aws_vpc_endpoint__vpce-xxxxx.tf


These files create the necessary VPC endpoints. these are easy to read and understand the most complex one is for the S3 endpoint and it is listed below.

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_vpc_endpoint" "vpce-s3" {
  policy = jsonencode(
    {
      Statement = [
        {
          Action    = "*"
          Effect    = "Allow"
          Principal = "*"
          Resource  = "*"
        },
      ]
      Version = "2008-10-17"
    }
  )
  private_dns_enabled = false
  route_table_ids = [
    aws_route_table.rtb-0102c621469c344cd.id,
    aws_route_table.rtb-0329e787bbafcb2c4.id,
    aws_route_table.rtb-041267f0474c24068.id,
  ]
  security_group_ids = []
  service_name       = "com.amazonaws.eu-west-1.s3"
  subnet_ids         = []
  tags               = {}
  vpc_endpoint_type  = "Gateway"
  vpc_id             = aws_vpc.vpc-mycluster1.id

  timeouts {}
}


```

{{%/expand%}}

---

There are other Terraform files that define the VPC used for our CICD pipeline with a single public and private subnet and outbound internet access for CodeBuild.


- aws_vpc__eks-cicd.tf
- aws_subnet__eks-cicd-private1.tf
- aws_subnet__eks-cicd-public1.tf
- aws_internet_gateway__eks-cicd.tf
- aws_nat_gateway__eks-cicd.tf
- aws_eip__eipalloc-cicd-natgw.tf
- aws_security_group__sg-eks-cicd.tf
- aws_route_table__private1.tf
- aws_route_table__public1.tf
- aws_route_table_association__private1.tf
- aws_route_table_association__public1.tf

Having read the Terraform files above you should find these straight forward to follow and understand.

The the CICD VPC does have (outbound) internet connectivity and so needs an Internet Gateway **aws_internet_gateway__eks-cicd.tf** a NAT Gateway **aws_nat_gateway__eks-cicd.tf** and an assiciated public IP address **aws_eip__eipalloc-cicd-natgw.tf**


---