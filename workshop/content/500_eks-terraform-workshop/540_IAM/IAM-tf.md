---
title: "Using Terraform to create the IAM Roles and Policies for EKS"
date: 2018-09-18T16:01:14-05:00
weight: 545
---

## Create the Required EKS Roles

```
cd ~/environment/tfekscode/iam
```

Initialize Terraform

```
terraform init
```
{{< output >}}
Initializing the backend...

Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Checking for available provider plugins...
- Downloading plugin for provider "aws" (hashicorp/aws) 3.15.0...

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

{{< /output >}}

Validate the Terraform code
```
terraform validate
```
{{< output >}}
Success! The configuration is valid.
{{< /output >}}

Plan the deployment:
```
terraform plan -out tfplan
```
{{< output >}}
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.


------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_iam_role.cluster-ServiceRole will be created
  + resource "aws_iam_role" "eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ" {
      + arn                   = (known after apply)
      + assume_role_policy    = jsonencode(
            {
              + Statement = [
                  + {
                      + Action    = "sts:AssumeRole"
                      + Effect    = "Allow"
                      + Principal = {
                          + Service = [
                              + "eks-fargate-pods.amazonaws.com",
                              + "eks.amazonaws.com",
                            ]
                        }
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + create_date           = (known after apply)
      + force_detach_policies = false
      + id                    = (known after apply)
      + max_session_duration  = 3600
      + name                  = "eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ"
      + path                  = "/"
      + tags                  = {
          + "Name"                                        = "eksctl-mycluster1-cluster/ServiceRole"
          + "alpha.eksctl.io/cluster-name"                = "mycluster1"
          + "alpha.eksctl.io/eksctl-version"              = "0.29.2"
          + "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
        }
      + unique_id             = (known after apply)
    }


** OUTPUT TRUNCATED FOR BREVITY **

  # aws_iam_role_policy_attachment.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__AmazonSSMManagedInstanceCore will be created
  + resource "aws_iam_role_policy_attachment" "eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__AmazonSSMManagedInstanceCore" {
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
      + role       = (known after apply)
    }

  # aws_iam_role_policy_attachment.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__CloudWatchAgentServerPolicy will be created
  + resource "aws_iam_role_policy_attachment" "eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__CloudWatchAgentServerPolicy" {
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
      + role       = (known after apply)
    }

Plan: 20 to add, 0 to change, 0 to destroy.

{{< /output >}}


You can see from the plan the following resources will be created - open the corresponding files to see the Terraform HCL code that details the configuration

* A Cluster Service Role (**aws_iam_role__cluster-ServiceRole.tf**)
* A Node Group Service Role (**aws_iam_role__nodegroup-NodeInstanceRole.tf**)
* Various policy definitions that EKS needs eg: (**aws_iam_role_policy__nodegroup-NodeInstanceRole-PolicyAutoScaling.tf**)
* Policy attachments to the cluster and node group roles eg:  (**aws_iam_role_policy_attachment__cluster-ServiceRole-AmazonEKSClusterPolicy.tf**)




### Build the Roles, Policies etc.:
```
terraform apply tfplan
```
{{< output >}}
aws_iam_role.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO: Creating...
aws_iam_role.eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ: Creating...
aws_iam_role.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO: Creation complete after 2s [id=eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO]
aws_iam_role_policy.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__eksctl-mycluster1-nodegroup-ng-maneksami2-PolicyCertManagerGetChange: Creating...
aws_iam_role_policy.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__eksctl-mycluster1-nodegroup-ng-maneksami2-PolicyCertManagerChangeSet: Creating...
aws_iam_role_policy_attachment.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__AmazonEKS_CNI_Policy: Creating....


** OUTPUT TRUNCATED FOR BREVITY **


aws_iam_role_policy_attachment.eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ__AmazonEKSVPCResourceController: Creation complete after 0s [id=eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ-20201207191049995300000007]
aws_iam_role_policy_attachment.eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO__AmazonEC2RoleforSSM: Creation complete after 0s [id=eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO-20201207191049960000000006]
aws_iam_role_policy_attachment.eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ__AmazonEKSClusterPolicy: Creation complete after 0s [id=eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ-20201207191050026600000008]

Apply complete! Resources: 20 added, 0 changed, 0 destroyed.

Outputs:

cluster_service_role_arn = arn:aws:iam::566972129213:role/eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ
nodegroup_role_arn = arn:aws:iam::566972129213:role/eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO

{{< /output >}}


The above creates the necessary Roles with attached Policies needed by EKS 
Examine the results in AWS console (IAM section)

-----






