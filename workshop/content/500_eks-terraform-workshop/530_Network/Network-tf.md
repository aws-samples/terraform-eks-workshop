---
title: "Using Terraform to create VPC and other Network related resources"
date: 2018-09-18T16:01:14-05:00
weight: 533
---


From the Cloud9 IDE we will next build the main networking components for our EKS cluster

This diagram shows the EKS VPC and CI/CD VPC we will build in this section: 
![tf-state](/images/andyt/net-1.jpg)


{{% notice info %}}
*Disclaimer: For production workloads you should expand the default and CI/CD VPC's to use multiple subnets in two or three availability zones.*
{{% /notice %}}

### Deploying the Network

```
cd ~/environment/tfekscode/net 
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
- Finding hashicorp/aws versions matching "~> 3.22"...
- Installing hashicorp/aws v3.22.0...
- Installed hashicorp/aws v3.22.0 (signed by HashiCorp)

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


**OUTPUT TRUNCATED FOR BREVITY**


  # aws_vpc_ipv4_cidr_block_association.vpc-cidr-assoc will be created
  + resource "aws_vpc_ipv4_cidr_block_association" "vpc-cidr-assoc" {
      + cidr_block = "100.64.0.0/16"
      + id         = (known after apply)
      + vpc_id     = (known after apply)

      + timeouts {}
    }

Plan: 42 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"

{{< /output >}}

You can see from the plan the following resources will be created - open the corresponding files to see the Terraform HCL code that details the configuration:

* A VPC (**vpc-cluster.tf**).
* A secondary VPC CIDR block (**aws_vpc_ipv4_cidr_block_association__vpc-cidr-assoc.tf**).
* Various VPE Endpoints (__vpce.tf__).
* Subnets (**subnets-eks.tf**).
* Route Tables (**aws_route_table__rtb-*.tf**).
* Route Table Assciations (**aws_route_table_association__rtbassoc*.tf**).
* Security Groups (**aws_security_group__allnodes-sg.tf** & **aws_security_group__cluster-sg.tf**).
* NAT Gateway (**aws_nat_gateway__eks-cicd.tf**).

There are also Terraform file to setup the VPC and subnets used by CodeBuild part of the CICD pipeline

* The VPC (**aws_vpc__eks-cicd.tf**) and it's associated:
* Subnets (**aws_subnet__eks-cicd*.tf**).
* Security groups (**aws_security_group__sg-eks-cicd.tf**).
* Route tables (**aws_route_table__private1.tf** & **aws_route_table__public1.tf**).
* Route Table Associations (**aws_route_table_association__private1.tf** & **aws_route_table_association__public1.tf** ).
* Internet Gateway (**aws_internet_gateway__eks-cicd.tf**).
* A NAT Gateway (**aws_eip__eipalloc-cicd-natgw.tf**).

----

Build the Network environment (**note this will take a few minutes**):

```
terraform apply tfplan
```
{{< output >}}
aws_vpc.vpc-cicd: Creating...
aws_eip.eipalloc-052dd24eaa93ed064: Creating...
aws_vpc.cluster: Creating...
aws_eip.eipalloc-052dd24eaa93ed064: Creation complete after 0s [id=eipalloc-04d80992ad3626c3d]
aws_vpc.vpc-cicd: Creation complete after 1s [id=vpc-0973e883cf3e8623b]

**OUTPUT TRUNCATED FOR BREVITY**

aws_vpc_endpoint.vpce-ssmmessages: Still creating... [1m30s elapsed]
aws_vpc_endpoint.vpce-ssmmessages: Still creating... [1m40s elapsed]
aws_vpc_endpoint.vpce-ssmmessages: Still creating... [1m50s elapsed]
aws_vpc_endpoint.vpce-ssmmessages: Still creating... [2m0s elapsed]
aws_vpc_endpoint.vpce-ssmmessages: Creation complete after 2m2s [id=vpce-0886cfb2249002aa1]

Apply complete! Resources: 42 added, 0 changed, 0 destroyed.

Outputs:

allnodes-sg = sg-067adf4dcc68f61f5
cluster-sg = sg-098604be92f19d230
eks-cidr = 10.0.0.0/22
eks-vpc = vpc-02314cece21fd4a5e
rtb-priv1 = rtb-07726ca4a9de959c5
rtb-priv2 = rtb-085c8974ed72c2aec
rtb-priv3 = rtb-05b0283d052293e66
sub-priv1 = subnet-0450b36fa76835001
sub-priv2 = subnet-07293b1ce1809c47b
sub-priv3 = subnet-0b7a75c9280d189bc
{{< /output >}}


The above Creates the VPC we will use for EKS and CICD.
Note several of the parameters are captured at Outputs, these will be used in later stages of the build.

Examine the results in AWS console. Look for new VPC's, Subnets etc.


-----






