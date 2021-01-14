---
title: "Terraform files explanation"
date: 2018-09-18T16:01:14-05:00
weight: 547
---

### Terraform files and explanation


The first three files have been pre-created from the gen-backend.sh script in the tf-setup stage and have been explained in previous sections.



### backend-iam.tf

This specifices the location of the backend Terraform state file on S3 and the dynamoDB table used for the state file locking. Also the Terraform version requirements, the AWS region and profile from variables, and the AWS credentials from a local file if present.

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
key = "terraform/terraform_locks_iam.tfstate"
region = "eu-west-1"
dynamodb_table = "terraform_locks_iam"
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

This file defines some varaibles with default values for the 7x dynamoDB tables, the region and default profile name

{{%expand "Expand here to see the code" %}}
```bash
variable "table_name_net" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-net"
}
** OUTPUT TRUNCATED FOR BREVITY **
```

{{%/expand%}}

---

### vars-main.tf

Same as previous sections

---


EKS requires a few roles to be pre-defined to operate correctly

The cluster service role, an output is defined **cluster_service_role_arn** which is used in the EKS cluster creation in a later stage.

### aws_iam_role__cluster-ServiceRole.tf

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_iam_role" "eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ" {
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = [
              "eks-fargate-pods.amazonaws.com",
              "eks.amazonaws.com",
            ]
          }
        },
      ]
      Version = "2012-10-17"
    }
  )
  force_detach_policies = false
  max_session_duration  = 3600
  name                  = "eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ"
  path                  = "/"
  tags = {
    "Name"                                        = "eksctl-mycluster1-cluster/ServiceRole"
    "alpha.eksctl.io/cluster-name"                = "mycluster1"
    "alpha.eksctl.io/eksctl-version"              = "0.29.2"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
  }
}

output "cluster_service_role_arn" {
  value = aws_iam_role.eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ.arn
}
```

{{%/expand%}}

---


And a managed nodegroup role, an output is defined **nodegroup_role_arn** which is also used in the EKS cluster creation in a later stage.

### aws_iam_role__nodegroup-NodeInstanceRole.tf

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_iam_role" "eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO" {
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "ec2.amazonaws.com"
          }
        },
      ]
      Version = "2012-10-17"
    }
  )
  force_detach_policies = false
  max_session_duration  = 3600
  name                  = "eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO"
  path                  = "/"
  tags = {
    "Name"                                        = "eksctl-mycluster1-nodegroup-ng-maneksami2/NodeInstanceRole"
    "alpha.eksctl.io/cluster-name"                = "mycluster1"
    "alpha.eksctl.io/eksctl-version"              = "0.29.2"
    "alpha.eksctl.io/nodegroup-name"              = "ng-maneksami2"
    "alpha.eksctl.io/nodegroup-type"              = "managed"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
  }
}

output "nodegroup_role_arn" {
  value = aws_iam_role.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO.arn
}

```

{{%/expand%}}

---

To these two roles, various policies are then defined and later on attached to the Role.

One example of a policy that is defined is shown here:

### aws_iam_role_policy__cluster-ServiceRole__PolicyCloudWatchMetrics.tf

{{%expand "Expand here to see the code" %}}
```bash

resource "aws_iam_role_policy" "eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ__eksctl-mycluster1-cluster-PolicyCloudWatchMetrics" {
  name = "eksctl-mycluster1-cluster-PolicyCloudWatchMetrics"
  policy = jsonencode(
    {
      Statement = [
        {
          Action = [
            "cloudwatch:PutMetricData",
          ]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
      Version = "2012-10-17"
    }
  )
  role = aws_iam_role.eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ.id
}

```

{{%/expand%}}

---

And one example of a policy for the nodegroup role:

### aws_iam_role_policy__eksctl-manamieksp-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO

One example is shoown here:

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_iam_role_policy" "eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__eksctl-mycluster1-nodegroup-ng-maneksami2-PolicyAutoScaling" {
  name = "eksctl-mycluster1-nodegroup-ng-maneksami2-PolicyAutoScaling"
  policy = jsonencode(
    {
      Statement = [
        {
          Action = [
            "autoscaling:DescribeAutoScalingGroups",
            "autoscaling:DescribeAutoScalingInstances",
            "autoscaling:DescribeLaunchConfigurations",
            "autoscaling:DescribeTags",
            "autoscaling:SetDesiredCapacity",
            "autoscaling:TerminateInstanceInAutoScalingGroup",
            "ec2:DescribeLaunchTemplateVersions",
          ]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
      Version = "2012-10-17"
    }
  )
  role = aws_iam_role.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO.id
}

```

{{%/expand%}}

---

And finally Policy attachments are specified, one example of each are shown below:

### aws_iam_role_policy_attachment__eksctl-manamieksp-cluster-ServiceRole-HUIGIC7K7HNJ*.tf

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_iam_role_policy_attachment" "eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ__AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ.id
}
```

{{%/expand%}}

---

### aws_iam_role_policy_attachment__eksctl-manamieksp-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO*.tf

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_iam_role_policy_attachment" "eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO.id
}

```

{{%/expand%}}

---
