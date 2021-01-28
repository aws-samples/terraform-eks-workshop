---
title: "Terraform files explanation"
date: 2018-09-18T16:01:14-05:00
weight: 564
---

### Terraform files and explanation


The first five files have been pre-created from the gen-backend.sh script in the tf-setup stage, The S3 bucket and DynamoDB tables were also pre-created in the tf-setup stage.

### backend-cluster.tf, vars-dynamodb.tf, vars-main.tf 

As described in previous sections.

###  remote-net.tf

Location of the "net" stage build state file - so we can access it's output variables.

{{%expand "Expand here to see the code" %}}
```bash
data terraform_remote_state "net" {
backend = "s3"
config = {
bucket = "terraform-state-f8ffc212119c-1604689183n"
region = "eu-west-1"
key = "terraform/at-terraform-eks-workshop1-net.tfstate"
}
}
```
{{% /expand %}}

----

### remote-iam.tf

Location of the "iam" stage build state file - so we can access it's output variables.

{{%expand "Expand here to see the code" %}}
```bash
data terraform_remote_state "iam" {
backend = "s3"
config = {
bucket = "terraform-state-f8ffc212119c-1604689183n"
region = "eu-west-1"
key = "terraform/at-terraform-eks-workshop1-iam.tfstate"
}
}
```

{{% /expand %}}

----

### remote-cluster.tf

Location of the "cluster" stage build state file - so we can access it's output variables.

{{%expand "Expand here to see the code" %}}
```bash
data terraform_remote_state "cluster" {
backend = "s3"
config = {
bucket = "terraform-state-f8ffc212119c-1604689183n"
region = "eu-west-1"
key = "terraform/at-terraform-eks-workshop1-cluster.tfstate"
}
}
```
{{% /expand %}}

----

### data-eks-cluster.tf

Get a data resource ("read only") refernce for the EKS cluster control plane. Note the use of **data.terraform_remote_state.cluster.xxx** variables.

{{%expand "Expand here to see the code" %}}

```bash
data "aws_eks_cluster" "eks_cluster" {
  name = data.terraform_remote_state.cluster.outputs.cluster-name
}

output "endpoint" {
  value = data.aws_eks_cluster.eks_cluster.endpoint
}

output "ca" {
  value = data.aws_eks_cluster.eks_cluster.certificate_authority[0].data
}

# Only available on Kubernetes version 1.13 and 1.14 clusters created or upgraded on or after September 3, 2019.
output "identity-oidc-issuer" {
  value = data.aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer
}

output "cluster-name" {
  value = data.aws_eks_cluster.eks_cluster.name
}
```
{{% /expand %}}

---

### user_data.tf

This file will be base64 encoded and passed into the launch template is will:

* Join this node to the cluster **sudo /etc/eks/bootstrap.sh**
  * Note how soem paremeters for this are passed via Terraform data resources eg. **'${data.aws_eks_cluster.eks_cluster.name}'**
* Install our custom software/configuration - in this case the SSM agent.
  

{{%expand "Expand here to see the code" %}}

```bash
locals {
  eks-node-private-userdata = <<USERDATA
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="==MYBOUNDARY=="

--==MYBOUNDARY==
Content-Type: text/x-shellscript; charset="us-ascii"

#!/bin/bash -xe
sudo /etc/eks/bootstrap.sh --apiserver-endpoint '${data.aws_eks_cluster.eks_cluster.endpoint}' --b64-cluster-ca '${data.aws_eks_cluster.eks_cluster.certificate_authority[0].data}' '${data.aws_eks_cluster.eks_cluster.name}'
echo "Running custom user data script" > /tmp/me.txt
yum install -y amazon-ssm-agent
echo "yum'd agent" >> /tmp/me.txt
systemctl enable amazon-ssm-agent && systemctl start amazon-ssm-agent
date >> /tmp/me.txt

--==MYBOUNDARY==--
USERDATA
}
```
{{% /expand %}}

----

### ssm-param-ami.tf

This gets the latest Amazon Linux 2 AMI for EKS from Systems Manager parameter store.

{{%expand "Expand here to see the code" %}}
```bash
data "aws_ssm_parameter" "eksami" {
  name=format("/aws/service/eks/optimized-ami/%s/amazon-linux-2/recommended/image_id", data.aws_eks_cluster.eks_cluster.version)
}
```
{{% /expand %}}

----

### launch_template.tf

The lauch template to use with the EKS managed node, this refernces:

* Our choice of AMI: **image_id = data.aws_ssm_parameter.eksami.value**.
* Our base64 user data script **user_data = base64encode(local.eks-node-private-userdata)**.

The use of **create_before_destroy=true** is also important to allow us to create new versions of the launch tmeplate.

{{%expand "Expand here to see the code" %}}
```bash
#### User data for worker launch

resource "aws_launch_template" "lt-ng1" {
  depends_on = [null_resource.auth_cluster]
  instance_type           = "t3.small"
  key_name                = "eksworkshop"
  name                    = format("at-lt-%s-ng1", data.aws_eks_cluster.eks_cluster.name)
  tags                    = {}
  image_id                = data.aws_ssm_parameter.eksami.value
  user_data            = base64encode(local.eks-node-private-userdata)
  vpc_security_group_ids  = [data.terraform_remote_state.net.outputs.allnodes-sg] 
  tag_specifications { 
        resource_type = "instance"
    tags = {
        Name = format("%s-ng1", data.aws_eks_cluster.eks_cluster.name)
        }
    }
  lifecycle {
    create_before_destroy=true
  }
}

```
{{% /expand %}}

----

### aws_eks_node_group__manamieksp_ng1.tf

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_eks_node_group" "ng1" {
  #ami_type       = "AL2_x86_64"
  depends_on     = [aws_launch_template.lt-ng1]
  cluster_name   = data.aws_eks_cluster.eks_cluster.name
  disk_size      = 0
  instance_types = []
  labels = {
    "alpha.eksctl.io/cluster-name"   = data.aws_eks_cluster.eks_cluster.name
    "alpha.eksctl.io/nodegroup-name" = format("ng1-%s", data.aws_eks_cluster.eks_cluster.name)
  }
  node_group_name = format("ng1-%s", data.aws_eks_cluster.eks_cluster.name)
  node_role_arn   = data.terraform_remote_state.iam.outputs.nodegroup_role_arn
  #release_version = "1.17.11-20201007"
  subnet_ids = [
      data.terraform_remote_state.net.outputs.sub-priv1,
      data.terraform_remote_state.net.outputs.sub-priv2,
      data.terraform_remote_state.net.outputs.sub-priv3,
  ]
  tags = {
    "alpha.eksctl.io/cluster-name"                = data.aws_eks_cluster.eks_cluster.name
    "alpha.eksctl.io/eksctl-version"              = "0.29.2"
    "alpha.eksctl.io/nodegroup-name"              = format("ng1-%s", data.aws_eks_cluster.eks_cluster.name)
    "alpha.eksctl.io/nodegroup-type"              = "managed"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = data.aws_eks_cluster.eks_cluster.name
  }
  #version = "1.17"

  launch_template {
    name    = aws_launch_template.lt-ng1.name
    version = "1"
  }

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }

  timeouts {}
}

```
{{% /expand %}}

---

### null_resource.tf


The null resource runs the test.sh and auth.sh script after the creation of the cluster **depends_on = [aws_eks_cluster.cluster]**

{{%expand "Expand here to see the code" %}}
```bash
resource "null_resource" "auth_cluster" {
triggers = {
    always_run = "${timestamp()}"
}
depends_on = [data.aws_eks_cluster.eks_cluster]
provisioner "local-exec" {
    on_failure  = fail
    interpreter = ["/bin/bash", "-c"]
    command     = <<EOT
        echo -e "\x1B[31m Warning! Checking Authorization ${data.aws_eks_cluster.eks_cluster.name}...should see Server Version: v1.17.xxx \x1B[0m"
        ./auth.sh
        echo "************************************************************************************"
     EOT
}
}

```
{{% /expand %}}

---

### auth.sh

Authorize the local user to the cluster via ~/.kube/config

{{%expand "Expand here to see the code" %}}
```bash
echo "sleep 5 for sync"
sleep 5
rm -f ~/.kube/config
cn=`terraform output cluster-name`
arn=$(aws sts get-caller-identity | jq -r .Arn)
aws eks update-kubeconfig --name $cn
#aws eks update-kubeconfig --name $cn  --role-arn $arn
kubectx
echo "kubectl"
kubectl version --short

```
{{% /expand %}}

---

### output.tf

Some output variables are defined,but they are not used in this workshop

{{%expand "Expand here to see the code" %}}

```bash
locals {
  config-map-aws-auth = <<CONFIGMAPAWSAUTH
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: data.terraform_remote_state.iam.outputs.nodegroup_role_arn
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
CONFIGMAPAWSAUTH

  kubeconfig = <<KUBECONFIG
apiVersion: v1
clusters:
- cluster:
    server: aws_eks_cluster.eks-cluster.endpoint
    certificate-authority-data: aws_eks_cluster.eks-cluster.certificate_authority.0.data
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: aws
  name: aws
current-context: aws
kind: Config
preferences: {}
users:
- name: aws
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      command: aws-iam-authenticator
      args:
        - "token"
        - "-i"
        - "aws_eks_cluster.eks-cluster.name"
KUBECONFIG
}

output "config-map-aws-auth" {
  value = "local.config-map-aws-auth"
}

output "kubeconfig" {
  value = "local.kubeconfig"
}
```
{{% /expand %}}

---