---
title: "Creating the EKS NodeGroup"
date: 2018-09-18T16:01:14-05:00
weight: 562
---

## Create a managed node group with a custom ami and user_data

![tf-state](/images/andyt/nodeg-build.jpg)


```bash
cd ~/environment/tfekscode/nodeg
```

Initialize Terraform:

```bash
terraform init
```

Validate the Terraform code:
```
terraform validate
```

----

Plan the deployment:
```
terraform plan -out tfplan
```

{{< output >}}
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.terraform_remote_state.iam: Refreshing state...
data.terraform_remote_state.cluster: Refreshing state...
data.terraform_remote_state.net: Refreshing state...
data.aws_eks_cluster.eks_cluster: Refreshing state...
data.aws_ssm_parameter.eksami: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_eks_node_group.ng1 will be created
  + resource "aws_eks_node_group" "ng1" {
      + ami_type        = (known after apply)
      + arn             = (known after apply)
      + capacity_type   = (known after apply)
      + cluster_name    = "mycluster1"
      + disk_size       = 0
      + id              = (known after apply)
      + instance_types  = []
      + labels          = {
          + "alpha.eksctl.io/cluster-name"   = "mycluster1"
          + "alpha.eksctl.io/nodegroup-name" = "ng1-mycluster1"
        }
      + node_group_name = "ng1-mycluster1"
      + node_role_arn   = "arn:aws:iam::566972129213:role/eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO"
      + release_version = (known after apply)
      + resources       = (known after apply)
      + status          = (known after apply)
      + subnet_ids      = [
          + "subnet-061e6c09382ccf5db",
          + "subnet-065aae4bae0e75ef3",
          + "subnet-084d1e9172caa05e5",
        ]
      + tags            = {
          + "alpha.eksctl.io/cluster-name"                = "mycluster1"
          + "alpha.eksctl.io/eksctl-version"              = "0.29.2"
          + "alpha.eksctl.io/nodegroup-name"              = "ng1-mycluster1"
          + "alpha.eksctl.io/nodegroup-type"              = "managed"
          + "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
        }
      + version         = (known after apply)

      + launch_template {
          + id      = (known after apply)
          + name    = "at-lt-mycluster1-ng1"
          + version = "1"
        }

      + scaling_config {
          + desired_size = 2
          + max_size     = 3
          + min_size     = 1
        }

      + timeouts {}
    }

  # aws_launch_template.lt-ng1 will be created
  + resource "aws_launch_template" "lt-ng1" {
      + arn                    = (known after apply)
      + default_version        = (known after apply)
      + id                     = (known after apply)
      + image_id               = "ami-09e27bb6e561e4a40"
      + instance_type          = "t3.small"
      + key_name               = "eksworkshop"
      + latest_version         = (known after apply)
      + name                   = "at-lt-mycluster1-ng1"
      + user_data              = "TUlNRS1WZ  ** TRUNCATED ** 5EQVJZPT0tLQo="
      + vpc_security_group_ids = [
          + "sg-09ab0e693218b3c7f",
        ]

      + metadata_options {
          + http_endpoint               = (known after apply)
          + http_put_response_hop_limit = (known after apply)
          + http_tokens                 = (known after apply)
        }

      + tag_specifications {
          + resource_type = "instance"
          + tags          = {
              + "Name" = "mycluster1-ng1"
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"

{{< /output >}}    


You can see from the plan the following resources will be created

* A Launch template
* A NodeGroup using the launch template above 
* A null resource (this will auth us to the cluster)


----

Build the environment:
```
terraform apply tfplan
```

{{< output >}} 
aws_launch_template.lt-ng1: Creating...
aws_launch_template.lt-ng1: Creation complete after 1s [id=lt-03e8c112a02f079f7]
aws_eks_node_group.ng1: Creating...
aws_eks_node_group.ng1: Still creating... [10s elapsed]
aws_eks_node_group.ng1: Still creating... [20s elapsed]

** OUTPUT TRUNCATED FOR BREVITY **

aws_eks_node_group.ng1: Still creating... [2m10s elapsed]
aws_eks_node_group.ng1: Creation complete after 2m17s [id=mycluster1:ng1-mycluster1]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

ca = LS0tLS1CRUdJTi

** OUTPUT TRUNCATED FOR BREVITY **

RbEEzajRzdGNYWT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
cluster-name = mycluster1
config-map-aws-auth = local.config-map-aws-auth
endpoint = https://8D2A28E623D53AC09BC633A9CADCD434.gr7.eu-west-1.eks.amazonaws.com
identity-oidc-issuer = https://oidc.eks.eu-west-1.amazonaws.com/id/8D2A28E623D53AC09BC633A9CADCD434
kubeconfig = local.kubeconfig

{{< /output >}} 

---

### Check the custom software install

Our user_data.tf resource boot strapped our node into the cluster and installed the SSM agent.

You can check the SSM agent has worked by looking in the console for 

`Systems Manager`  then `Fleet Manager`

You should see the two worker node instances listed, as well as your Cloud9 IDE instance.

![tf-state](/images/andyt/ssm-eks-node.png)


You can start a SSM session and login to the node if required. 

Select a node, `Instance actions` and then `Start session`

This provides a more secure way to access worker nodes compared with allowing ssh based access. It also enables other Systems Manager capabilities such as automation, inventory collection and patching.

-----






