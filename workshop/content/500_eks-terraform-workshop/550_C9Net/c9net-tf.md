---
title: "Connect the Cloud9 IDE & CICD VPC to the EKS VPC"
date: 2018-09-18T16:01:14-05:00
weight: 553
---

### 

```
cd ~/environment/tfekscode/c9net
```

Run the script to Initialize the Terraform

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
Initializing the backend...

Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Checking for available provider plugins...
- Downloading plugin for provider "aws" (hashicorp/aws) 3.20.0...

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
andyt530:~/environment/tfekscode/c9net (master) $ terraform plan -out tfplan                                                                                                                                                      
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.terraform_remote_state.net: Refreshing state...
data.aws_vpc.vpc-cicd: Refreshing state...
data.aws_instance.c9inst: Refreshing state...
data.aws_vpc.vpc-default: Refreshing state...
data.aws_route_table.cicd-rtb: Refreshing state...
data.aws_security_group.cicd-sg: Refreshing state...
data.aws_security_group.c9sg: Refreshing state...
data.aws_iam_instance_profile.c9ip: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_route.rt-cicd will be created
  + resource "aws_route" "rt-cicd" {
      + destination_cidr_block     = "10.0.0.0/22"
      + destination_prefix_list_id = (known after apply)
      + egress_only_gateway_id     = (known after apply)
      + gateway_id                 = (known after apply)
      + id                         = (known after apply)
      + instance_id                = (known after apply)
      + instance_owner_id          = (known after apply)
      + local_gateway_id           = (known after apply)
      + nat_gateway_id             = (known after apply)
      + network_interface_id       = (known after apply)
      + origin                     = (known after apply)
      + route_table_id             = "rtb-0a37e9be0159b7fbd"
      + state                      = (known after apply)
      + vpc_peering_connection_id  = (known after apply)
    }



** OUTPUT TRUNCATED FOR BREVITY **

# aws_vpc_peering_connection.def-peer will be created
  + resource "aws_vpc_peering_connection" "def-peer" {
      + accept_status = (known after apply)
      + auto_accept   = true
      + id            = (known after apply)
      + peer_owner_id = (known after apply)
      + peer_region   = (known after apply)
      + peer_vpc_id   = "vpc-0c4ad7784e8210517"
      + vpc_id        = "vpc-d16a7cb7"

      + accepter {
          + allow_classic_link_to_remote_vpc = (known after apply)
          + allow_remote_vpc_dns_resolution  = (known after apply)
          + allow_vpc_to_remote_classic_link = (known after apply)
        }

      + requester {
          + allow_classic_link_to_remote_vpc = (known after apply)
          + allow_remote_vpc_dns_resolution  = (known after apply)
          + allow_vpc_to_remote_classic_link = (known after apply)
        }
    }

Plan: 26 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"

{{< /output >}}




You can see from the plan the following resources will be created to link the Cloud9 IDE to the EKS VPC

* VPC peering.
* VPC route table entries for the default and EKS subnets:
  * A route to 172.31 via the VPC peering for the EKS VPC.
  * A route to 10.0 via the VPC peering for the Default VPC.
* VPC route table entries for the CICD subnets and EKS subnets:
  * A route to 172.30 via the VPC peering for the EKS VPC.
  * A route to 10.0 via the VPC peering for the VPC.
* A security group rule for the Cloud9 Security group allowing traffic from 10.0.x.x.
* A security group rule for the EKS Worker Nodes Security Group allowing traffic in port 22 from the Cloud9 IDE Security Group.
* A security group rule for the EKS Cluster Security Group allowing traffic in port 443 from the Cloud9 IDE Security Group

---

Build the environment:
```
terraform apply tfplan
```
{{< output >}}
aws_security_group_rule.eks-all-cicd: Creating...
aws_security_group_rule.eks-node-self: Creating...
aws_security_group_rule.sg-cicd-self: Creating...
aws_security_group_rule.eks-all-self: Creating...
aws_security_group_rule.eks-node-all: Creating...
aws_security_group_rule.eks-all-node: Creating...
aws_vpc_peering_connection.cicd-peer: Creating...
aws_security_group_rule.eks-all-egress: Creating...
aws_security_group_rule.eks-node-egress: Creating...
aws_security_group_rule.sg-def-22: Creating...
aws_security_group_rule.sg-def-22: Creation complete after 0s [id=sgrule-2739735021]
aws_security_group_rule.sg-def-eks-all: Creating...
aws_security_group_rule.eks-all-cicd: Creation complete after 0s [id=sgrule-3945960121]
aws_security_group_rule.sg-cicd-self: Creation complete after 0s [id=sgrule-1063219289]
aws_security_group_rule.eks-node-self: Creation complete after 0s [id=sgrule-1692793766]
aws_security_group_rule.sg-cicd-22: Creating...
aws_security_group_rule.eks-node: Creating...
aws_security_group_rule.sg-cicd-egress: Creating...
aws_security_group_rule.sg-cicd-22: Creation complete after 0s [id=sgrule-2858381007]
aws_security_group_rule.sg-def-eks-all: Creation complete after 0s [id=sgrule-262922946]
aws_security_group_rule.eks-all: Creating...
aws_vpc_peering_connection.def-peer: Creating...
aws_vpc_peering_connection.cicd-peer: Creation complete after 0s [id=pcx-01fd09d47ef1cb3cb]
aws_security_group_rule.sg-cicd-eks-all: Creating...
aws_security_group_rule.eks-all-node: Creation complete after 1s [id=sgrule-2729105699]
aws_route.rt-eks4: Creating...
aws_security_group_rule.eks-node-all: Creation complete after 1s [id=sgrule-1909181409]
aws_route.rt-eks6: Creating...
aws_route.rt-eks4: Creation complete after 0s [id=r-rtb-03c076a49984c561c3963506374]
aws_route.rt-eks5: Creating...
aws_route.rt-eks6: Creation complete after 0s [id=r-rtb-0ae877adf09bc9e3a3963506374]
aws_route.rt-cicd: Creating...
aws_security_group_rule.sg-cicd-egress: Creation complete after 1s [id=sgrule-2525226280]
aws_route.rt-def-cicd: Creating...
aws_vpc_peering_connection.def-peer: Creation complete after 1s [id=pcx-07b14f811dccb8ef3]
aws_route.rt-eks2: Creating...
aws_route.rt-eks5: Creation complete after 0s [id=r-rtb-0f71fb0dd8c06365f3963506374]
aws_route.rt-eks1: Creating...
aws_security_group_rule.eks-all-self: Creation complete after 1s [id=sgrule-3078941028]
aws_security_group_rule.eks-node-egress: Creation complete after 1s [id=sgrule-610072226]
aws_route.rt-eks3: Creating...
aws_route.rt-def: Creating...
aws_route.rt-cicd: Creation complete after 0s [id=r-rtb-0a37e9be0159b7fbd653952448]
aws_route.rt-def-cicd: Creation complete after 0s [id=r-rtb-09fc9ecca3d61af8e653952448]
aws_route.rt-eks2: Creation complete after 0s [id=r-rtb-0f71fb0dd8c06365f3854007479]
aws_route.rt-def: Creation complete after 0s [id=r-rtb-abe7ded2653952448]
aws_route.rt-eks1: Creation complete after 0s [id=r-rtb-03c076a49984c561c3854007479]
aws_route.rt-eks3: Creation complete after 0s [id=r-rtb-0ae877adf09bc9e3a3854007479]
aws_security_group_rule.sg-cicd-eks-all: Creation complete after 1s [id=sgrule-4117136292]
aws_security_group_rule.eks-all-egress: Creation complete after 1s [id=sgrule-2742443021]
aws_security_group_rule.eks-node: Creation complete after 2s [id=sgrule-230005274]
aws_security_group_rule.eks-all: Creation complete after 2s [id=sgrule-3426310689]

Apply complete! Resources: 26 added, 0 changed, 0 destroyed.

Outputs:

c9lab =  true 
c9role = arn:aws:iam::566972129213:role/eksworkshop-admin
cicdpeerid = pcx-01fd09d47ef1cb3cb
peerid = pcx-07b14f811dccb8ef3

{{< /output >}}

The above links the Cloud9 IDE and the CICD VPC to the EKS private VPC and allows the required traffic to flow so you can communicate with the cluster from the Cloud9 IDE in the default VPC and the CodeBuild ENI that will be provisioned in the private subnet of the CICD VPC.


-----






