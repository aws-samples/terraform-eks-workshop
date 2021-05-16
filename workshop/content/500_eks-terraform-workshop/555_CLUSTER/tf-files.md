---
title: "Terraform files explanation"
date: 2018-09-18T16:01:14-05:00
weight: 558
---

## Create the EKS Cluster

Diagram of the components, with the EKS cluster parts we are creating highlighted.

![tf-state](/images/andyt/cluster-build.jpg)

### Terraform files and explanation

### backend-cluster.tf, vars-dynamodb.tf, vars-main.tf, remote-net.tf & remote-iam.tf

These first five files have been pre-created from the gen-backend.sh script in the tf-setup stage. The contents have been explained in previous sections.

----

### aws_eks_cluster__mycluster1.tf

Create the EKS cluster, note the use of various remote output variables **data.terraform_remote_state** values.

{{%expand "Expand here to see the code" %}}

```bash
resource "aws_eks_cluster" "mycluster1" {
  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler",
  ]
  name       = "mycluster1"
  #depends_on = [data.terraform_remote_state.iam.aws_iam_role.eksctl-mycluster1-cluster-ServiceRole-HUIGIC7K7HNJ]
  role_arn   = data.terraform_remote_state.iam.outputs.cluster_service_role_arn
  tags       = {}
  version    = "1.17"

  timeouts {}

  vpc_config {
    endpoint_private_access = true
    endpoint_public_access  = false
    public_access_cidrs = [
      "0.0.0.0/0",
    ]
    security_group_ids = [
      data.terraform_remote_state.net.outputs.cluster-sg,
    ]
    subnet_ids = [
      data.terraform_remote_state.net.outputs.sub-priv1,
      data.terraform_remote_state.net.outputs.sub-priv2,
      data.terraform_remote_state.net.outputs.sub-priv3,
    ]
  }
}

output cluster-name {
  value=aws_eks_cluster.cluster.name
}

output cluster-sg {
  value=aws_eks_cluster.cluster.vpc_config[0].cluster_security_group_id
}

output ca {
  value=aws_eks_cluster.cluster.certificate_authority[0].data
}

output endpoint {
  value=aws_eks_cluster.cluster.endpoint
}

```
{{% /expand %}}

---

Cluster Additions

### aws_iam_openid_connect_provider.tf

Add the open connect provider to the EKS cluster

{{%expand "Expand here to see the code" %}}

```bash 
## OIDC Provider
data "tls_certificate" "cluster" {
  url = aws_eks_cluster.cluster.identity.0.oidc.0.issuer
}
resource "aws_iam_openid_connect_provider" "cluster" {
  client_id_list = ["sts.amazonaws.com"]
#  thumbprint_list = concat([data.tls_certificate.cluster.certificates.0.sha1_fingerprint], var.oidc_thumbprint_list)
  thumbprint_list = [data.tls_certificate.cluster.certificates.0.sha1_fingerprint]
  url = aws_eks_cluster.cluster.identity.0.oidc.0.issuer
}

### 
data "aws_iam_policy_document" "cluster_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.cluster.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:aws-node"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.cluster.arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role" "cluster" {
  assume_role_policy = data.aws_iam_policy_document.cluster_assume_role_policy.json
  name               = "cluster"
}

```
{{% /expand %}}

---

### null_resource.tf

The null resource runs the **test.sh** and **auth.sh** scripts after the creation of the cluster **depends_on = [aws_eks_cluster.cluster]**


{{%expand "Expand here to see the code" %}}
```bash
resource "null_resource" "gen_backend" {
triggers = {
    always_run = "${timestamp()}"
}
depends_on = [aws_eks_cluster.cluster]
provisioner "local-exec" {
    on_failure  = fail
    interpreter = ["/bin/bash", "-c"]
    command     = <<EOT
        echo -e "\x1B[31m Warning! Testing Network Connectivity ${aws_eks_cluster.cluster.name}...should see port 443/tcp open  https\x1B[0m"
        ./test.sh
        echo -e "\x1B[31m Warning! Checking Authorization ${aws_eks_cluster.cluster.name}...should see Server Version: v1.17.xxx \x1B[0m"
        ./auth.sh
        echo "************************************************************************************"
     EOT
}
}

```
{{% /expand %}}

---

### test.sh

From the Cloud9 IDE, lookup the DNS name of the cluster and test that port 443 is open for the clusters API endpoint. 

{{%expand "Expand here to see the code" %}}

```bash
cn=`terraform output cluster-name`
resp=$(aws eks describe-cluster --name mycluster1)
endp=$(echo $resp | jq -r .cluster.endpoint | cut -f3 -d'/')
nslookup $endp
nmap $endp -Pn -p 443

```
{{% /expand %}}

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
echo "check the context is set"
kubectx
echo "kubectl version"
kubectl version --short
```
{{% /expand %}}

---