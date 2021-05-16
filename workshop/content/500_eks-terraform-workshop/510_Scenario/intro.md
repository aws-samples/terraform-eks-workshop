---
title: "EKS multi-part Build with Terraform"
weight: 515
draft: false
---


In this workshop we will build a private EKS cluster using Terraform, using our Cloud9 IDE as a bastion host and also create a VPC hosted CI/CD pipeline using CodeCommit, CodeBuild and CodePipeline.

The following diagram pictures the end state for this workshop:

![tf-state](/images/andyt/master-scenario.png)



### Building a Private EKS cluster with a multi-part responsibility model.

Security is a critical component of configuring and maintaining Kubernetes clusters and applications. Amazon EKS provides secure, managed Kubernetes clusters by default. 

This can be further enhanced by provisioning an EKS cluster to operate in a private VPC with no Internet ingress or egress connectivity.

In this section, we take a look at how to build the private EKS cluster in distinct stages designed to reflect different responsibility and minimum privilege models that are sometimes seen in large organizations.


The build out of our private EKS Cluster is divided into these stages, each of which could be performed by a separate team.

You will perform each of these stages in turn as you progress through the workshop.

#### Initial setup for Terraform

In this stage we create some pre-requisite S3 buckets and dynamodDB tables that will be used to centrally hold the Terraform "state" and control locking of that state:

![tf-state](/images/andyt/tf-state-aws.jpg)

#### VPC and Network Build

In this stage we build the necessary base networking components for out EKS Cluster, and the VPC for CICD (CodeBuild).

![tf-state](/images/andyt/vpc3.png)

#### IAM Roles and Policies for EKS

In the next stage we create the required IAM roles and policies for EKS.

#### Connecting the Cloud9 IDE to the EKS network

This stage inter-connects the Cloud9 IDE & CICD VPC with the private EKS VPC. 

![tf-state](/images/andyt/c9net-build.png)


#### Deploy the CICD Infrastructure

This stage deploys a private ECR container registry and sets up CodeCommit, CodeBuild and CodePipeline.

![tf-state](/images/andyt/cicd-build.png)

#### Creating an EKS CLuster

This stage deploys the EKS control plane.

![tf-state](/images/andyt/cluster-build.jpg)

#### Adding customized managed worker nodes

In this stage we deploy a private node group using a launch template, a specific AMI and a customized user data to install the SSM agent.

![tf-state](/images/andyt/nodeg-build.jpg)

#### Configure the worker nodes to use advanced networking

This stage changes the worker nodes int he node group so this will use the secondary CIDR address range for pods running in the EKS cluster.

![tf-state](/images/andyt/adv-net-nodes.png)

#### Enable the AWS Load Balancer controller

In this part we enable the aws load balancer controller 

----

#### Deploy and test a sample app (Manually and with CICD)

Finally we do some testing of our cluster and CICD pipeline.

![tf-state](/images/andyt/cicd-app.png)
