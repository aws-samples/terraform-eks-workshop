---
title: "Creating the EKS Cluster"
date: 2018-09-18T16:01:14-05:00
weight: 556
---

### 

```
cd ~/environment/tfekscode/cluster
```

Initialze Terraform

```
terraform init
```
{{< output >}}
Initializing the backend...

Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Checking for available provider plugins...
- Downloading plugin for provider "null" (hashicorp/null) 3.0.0...
- Downloading plugin for provider "tls" (hashicorp/tls) 3.0.0...
- Downloading plugin for provider "aws" (hashicorp/aws) 3.20.0...

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, it is recommended to add version = "..." constraints to the
corresponding provider blocks in configuration, with the constraint strings
suggested below.

* provider.null: version = "~> 3.0"
* provider.tls: version = "~> 3.0"

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

data.terraform_remote_state.net: Refreshing state...
data.terraform_remote_state.iam: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create
 <= read (data resources)

Terraform will perform the following actions:

  # data.aws_iam_policy_document.cluster_assume_role_policy will be read during apply
  # (config refers to values not yet known)
 <= data "aws_iam_policy_document" "cluster_assume_role_policy"  {
      + id   = (known after apply)
      + json = (known after apply)

      + statement {
          + actions = [
              + "sts:AssumeRoleWithWebIdentity",
            ]
          + effect  = "Allow"

          + condition {
              + test     = "StringEquals"
              + values   = [
                  + "system:serviceaccount:kube-system:aws-node",
                ]
              + variable = (known after apply)
            }

          + principals {
              + identifiers = [
                  + (known after apply),
                ]
              + type        = "Federated"
            }
        }
    }

  # data.tls_certificate.cluster will be read during apply
  # (config refers to values not yet known)
 <= data "tls_certificate" "cluster"  {
      + certificates = (known after apply)
      + id           = (known after apply)
      + url          = (known after apply)
    }

  # aws_eks_cluster.mycluster1 will be created
  + resource "aws_eks_cluster" "mycluster1" {
      + arn                       = (known after apply)
      + certificate_authority     = (known after apply)
      + created_at                = (known after apply)
      + enabled_cluster_log_types = [
          + "api",
          + "audit",
          + "authenticator",
          + "controllerManager",
          + "scheduler",
        ]
      + endpoint                  = (known after apply)
      + id                        = (known after apply)
      + identity                  = (known after apply)
      + name                      = "mycluster1"
      + platform_version          = (known after apply)
      + role_arn                  = "arn:aws:iam::566972129213:role/eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ"
      + status                    = (known after apply)
      + version                   = "1.17"

      + kubernetes_network_config {
          + service_ipv4_cidr = (known after apply)
        }

      + timeouts {}

      + vpc_config {
          + cluster_security_group_id = (known after apply)
          + endpoint_private_access   = true
          + endpoint_public_access    = false
          + public_access_cidrs       = [
              + "0.0.0.0/0",
            ]
          + security_group_ids        = [
              + "sg-03bc7680e8a66eb97",
            ]
          + subnet_ids                = [
              + "subnet-061e6c09382ccf5db",
              + "subnet-065aae4bae0e75ef3",
              + "subnet-084d1e9172caa05e5",
            ]
          + vpc_id                    = (known after apply)
        }
    }

  # aws_iam_openid_connect_provider.cluster will be created
  + resource "aws_iam_openid_connect_provider" "cluster" {
      + arn             = (known after apply)
      + client_id_list  = [
          + "sts.amazonaws.com",
        ]
      + id              = (known after apply)
      + thumbprint_list = (known after apply)
      + url             = (known after apply)
    }

  # aws_iam_role.cluster will be created
  + resource "aws_iam_role" "cluster" {
      + arn                   = (known after apply)
      + assume_role_policy    = (known after apply)
      + create_date           = (known after apply)
      + force_detach_policies = false
      + id                    = (known after apply)
      + max_session_duration  = 3600
      + name                  = "cluster"
      + path                  = "/"
      + unique_id             = (known after apply)
    }

  # null_resource.gen_cluster_auth will be created
  + resource "null_resource" "gen_cluster_auth" {
      + id       = (known after apply)
      + triggers = (known after apply)
    }

Plan: 4 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"
{{< /output >}}

You can see from the plan the following resources will be created

* An EKS Cluster
* Configure the cluster with an OIDC provider and add support for ISRA (IAM Roles for Service Accounts)
* A null resource which runs a small script to test conectivity to EKS with nmap and write the local .kubeconfig file
  

Build the environment:
```
terraform apply tfplan
```
{{< output >}}
aws_eks_cluster.mycluster1: Creating...
aws_eks_cluster.mycluster1: Still creating... [10s elapsed]

** OUTPUT TRUNCATED FOR BREVITY **

aws_eks_cluster.mycluster1: Still creating... [17m20s elapsed]
aws_eks_cluster.mycluster1: Creation complete after 17m24s [id=mycluster1]
data.tls_certificate.cluster: Refreshing state...
null_resource.gen_cluster_auth: Creating...
null_resource.gen_cluster_auth: Provisioning with 'local-exec'...
null_resource.gen_cluster_auth (local-exec): Executing: ["/bin/bash" "-c" "        echo -e \"\\x1B[32m Testing Network Connectivity mycluster1...should see port 443/tcp open  https\\x1B[0m\"\n        ./test.sh mycluster1\n        echo -e \"\\x1B[32m Checking Authorization mycluster1...should see Server Version: v1.17.xxx \\x1B[0m\"\n        ./auth.sh mycluster1\n        echo \"************************************************************************************\"\n"]
null_resource.gen_cluster_auth (local-exec):  Testing Network Connectivity mycluster1...should see port 443/tcp open  https
aws_iam_openid_connect_provider.cluster: Creating...
aws_iam_openid_connect_provider.cluster: Creation complete after 1s [id=arn:aws:iam::566972129213:oidc-provider/oidc.eks.eu-west-1.amazonaws.com/id/8D2A28E623D53AC09BC633A9CADCD434]
data.aws_iam_policy_document.cluster_assume_role_policy: Refreshing state...
aws_iam_role.cluster: Creating...
aws_iam_role.cluster: Creation complete after 0s [id=cluster]

null_resource.gen_cluster_auth (local-exec): Starting Nmap 6.40 ( http://nmap.org ) at 2020-12-10 16:14 UTC
null_resource.gen_cluster_auth (local-exec): Nmap scan report for 8D2A28E623D53AC09BC633A9CADCD434.gr7.eu-west-1.eks.amazonaws.com (10.0.3.148)
null_resource.gen_cluster_auth (local-exec): Host is up (0.00041s latency).
null_resource.gen_cluster_auth (local-exec): rDNS record for 10.0.3.148: ip-10-0-3-148.eu-west-1.compute.internal
null_resource.gen_cluster_auth (local-exec): PORT    STATE SERVICE
null_resource.gen_cluster_auth (local-exec): 443/tcp open  https

null_resource.gen_cluster_auth (local-exec): Nmap done: 1 IP address (1 host up) scanned in 0.06 seconds
null_resource.gen_cluster_auth (local-exec):  Checking Authorization mycluster1...should see Server Version: v1.17.xxx 
null_resource.gen_cluster_auth (local-exec): Added new context arn:aws:eks:eu-west-1:566972129213:cluster/mycluster1 to /home/ec2-user/.kube/config
null_resource.gen_cluster_auth (local-exec): arn:aws:eks:eu-west-1:566972129213:cluster/mycluster1
null_resource.gen_cluster_auth (local-exec): kubectl
null_resource.gen_cluster_auth (local-exec): Client Version: v1.19.4
null_resource.gen_cluster_auth (local-exec): Server Version: v1.17.12-eks-7684af
null_resource.gen_cluster_auth (local-exec): ************************************************************************************
null_resource.gen_cluster_auth: Creation complete after 5s [id=4944719165965434178]

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:

ca = LS0trUkhpbFJ0dDNRbEEzajRzdGNYWT0KLS0tLS1FTkQgQ0VSV

** OUTPUT TRUNCATED FOR BREVITY **

ElGSUNBVEUtLS0tLQo=
cluster-name = mycluster1
cluster-sg = sg-0c31d8655d63a6a83
endpoint = https://8D2A28E623D53AC09BC633A9CADCD434.gr7.eu-west-1.eks.amazonaws.com

{{< /output >}}


-----






