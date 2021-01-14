---
title: "Prerequisites"
date: 2019-02-08T00:35:29-05:00
weight: 572
---

Before we configure EKS, we need to enable secondary CIDR blocks in your VPC and make sure they have proper tags and route table configurations

### Add secondary CIDRs & subnets to your VPC

This step was already performed as part of the Terraform network build

{{% notice info %}}
There are restrictions on the range of secondary CIDRs you can use to extend your VPC. For more info, see [IPv4 CIDR Block Association Restrictions](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#add-cidr-block-restrictions)
{{% /notice %}}

As our first private CIDR is in the 10.0.x.x address range we used 100.64.x.x for our secondary address range in this workshop.


