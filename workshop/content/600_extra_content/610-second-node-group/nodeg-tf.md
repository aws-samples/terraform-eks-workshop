---
title: "Creating the second Node Group"
date: 2018-09-18T16:01:14-05:00
weight: 611
---

## Create a second managed nodegroup.


```bash
cd ~/environment/tfekscode/extra/nodeg2
```

Initialize Terraform:

```bash
terraform init
```
{{< output >}}
Initializing the backend...

Initializing provider plugins...
- terraform.io/builtin/terraform is built in to Terraform
- Finding hashicorp/external versions matching "~> 2.0"...
- Finding hashicorp/aws versions matching "~> 3.22"...
- Finding hashicorp/null versions matching "~> 3.0"...
- Installing hashicorp/external v2.0.0...
- Installed hashicorp/external v2.0.0 (signed by HashiCorp)
- Installing hashicorp/aws v3.23.0...
- Installed hashicorp/aws v3.23.0 (signed by HashiCorp)
- Installing hashicorp/null v3.0.0...
- Installed hashicorp/null v3.0.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
{{< /output >}}


Validate the Terraform code:

```bash
terraform validate
```


----

Plan the deployment:

```bash
terraform plan -out tfplan
```

{{< output >}}
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_eks_node_group.ng2 will be created
  + resource "aws_eks_node_group" "ng2" {
      + ami_type        = (known after apply)
      + arn             = (known after apply)
      + capacity_type   = (known after apply)
      + cluster_name    = "mycluster1"
      + disk_size       = 0
      + id              = (known after apply)
      + instance_types  = []
      + labels          = {
          + "alpha.eksctl.io/cluster-name"   = "mycluster1"
          + "alpha.eksctl.io/nodegroup-name" = "ng2-mycluster1"
        }
      + node_group_name = "ng2-mycluster1"
      + node_role_arn   = "arn:aws:iam::136434655158:role/eksctl-mycluster1-nodegroup-ng-ma-NodeInstanceRole-1GFKA1037E1XO"
      + release_version = (known after apply)
      + resources       = (known after apply)
      + status          = (known after apply)
      + subnet_ids      = [
          + "subnet-02525726fccc295e9",
          + "subnet-0531461221c74e971",
          + "subnet-0647eb732e6034eba",
        ]
      + tags            = {
          + "alpha.eksctl.io/cluster-name"                = "mycluster1"
          + "alpha.eksctl.io/eksctl-version"              = "0.29.2"
          + "alpha.eksctl.io/nodegroup-name"              = "ng2-mycluster1"
          + "alpha.eksctl.io/nodegroup-type"              = "managed"
          + "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "mycluster1"
          + "eksnet"                                      = "net-main"
        }
      + version         = (known after apply)

      + launch_template {
          + id      = (known after apply)
          + name    = "at-lt-mycluster1-ng2"
          + version = "1"
        }

      + scaling_config {
          + desired_size = 2
          + max_size     = 3
          + min_size     = 1
        }

      + timeouts {}
    }

  # aws_launch_template.lt-ng2 will be created
  + resource "aws_launch_template" "lt-ng2" {
      + arn                    = (known after apply)
      + default_version        = (known after apply)
      + id                     = (known after apply)
      + image_id               = "ami-0bf2eefa92a02a84f"
      + instance_type          = "t3.small"
      + key_name               = "eksworkshop"
      + latest_version         = (known after apply)
      + name                   = "at-lt-mycluster1-ng2"
      + user_data              = "TUlNRS1WZXJ  ** TRNCATED ** EQVJPT0tLQo="
      + vpc_security_group_ids = [
          + "sg-0cdc1db1f2fd0d186",
        ]

      + metadata_options {
          + http_endpoint               = (known after apply)
          + http_put_response_hop_limit = (known after apply)
          + http_tokens                 = (known after apply)
        }

      + tag_specifications {
          + resource_type = "instance"
          + tags          = {
              + "Name" = "mycluster1-ng2"
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + ca                   = "LS0tLS1CRUdJTiBDRWUVFERXdwcmRXSm  ** TRNCATED** kQgQ0VSVElGSUNBVEUtLS0tLQo="
  + cluster-name         = "mycluster1"
  + config-map-aws-auth  = "local.config-map-aws-auth"
  + endpoint             = "https://282B6894A779D89321B8EB6E5D920ACB.gr7.eu-west-1.eks.amazonaws.com"
  + identity-oidc-issuer = "https://oidc.eks.eu-west-1.amazonaws.com/id/282B6894A779D89321B8EB6E5D920ACB"
  + kubeconfig           = "local.kubeconfig"

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"

{{< /output >}}   


You can see from the plan the following resources will be created

* A Launch template
* A NodeGroup using the launch template above 



----

Build the environment:
```
terraform apply tfplan
```

{{< output >}}
aws_launch_template.lt-ng2: Creating...
aws_launch_template.lt-ng2: Creation complete after 0s [id=lt-03fb470e8ade921a9]
aws_eks_node_group.ng2: Creating...
aws_eks_node_group.ng2: Still creating... [10s elapsed]

...

aws_eks_node_group.ng2: Still creating... [2m40s elapsed]
aws_eks_node_group.ng2: Creation complete after 2m47s [id=mycluster1:ng2-mycluster1]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

The state of your infrastructure has been saved to the path
below. This state is required to modify and destroy your
infrastructure, so keep it safe. To inspect the complete state
use the `terraform show` command.

State path: terraform.tfstate

Outputs:

ca = "LS0tLSXdwcmRXSmw ** TRUNCATED ** KY201bGRHVnpNQjRYRFRVEUtLS0tLQo="
cluster-name = "mycluster1"
config-map-aws-auth = "local.config-map-aws-auth"
endpoint = "https://282B6894A779D89321B8EB6E5D920ACB.gr7.eu-west-1.eks.amazonaws.com"
identity-oidc-issuer = "https://oidc.eks.eu-west-1.amazonaws.com/id/282B6894A779D89321B8EB6E5D920ACB"
kubeconfig = "local.kubeconfig"

{{< /output >}}


----

We should now have 4 kubernetes worker nodes

```bash
kubectl get nodes 
```

{{< output >}}
NAME                                       STATUS   ROLES    AGE     VERSION
ip-10-0-1-231.eu-west-1.compute.internal   Ready    <none>   3m      v1.18.9-eks-d1db3c
ip-10-0-1-25.eu-west-1.compute.internal    Ready    <none>   3h58m   v1.18.9-eks-d1db3c
ip-10-0-2-179.eu-west-1.compute.internal   Ready    <none>   3h56m   v1.18.9-eks-d1db3c
ip-10-0-2-71.eu-west-1.compute.internal    Ready    <none>   2m57s   v1.18.9-eks-d1db3c
{{< /output >}}

-----

The Terraform files are almost identical to the previous node group - so they are not described here.




