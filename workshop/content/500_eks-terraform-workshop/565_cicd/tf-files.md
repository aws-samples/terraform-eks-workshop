---
title: "Terraform files explanation"
date: 2018-09-18T16:01:14-05:00
weight: 568
---

## Terraform files and explanation


The first three files have been pre-created from the gen-backend.sh script in the tf-setup stage, The S3 bucket and DynamoDB tables were also pre-created in the tf-setup stage.

### backend-cicd.tf, vars-dynamodb.tf & vars-main.tf

As described in previous sections

---


### aws_ecr_repository__xxxx.tf

These files define privare ECR repositories for the docker images we will use, one example is shown here as they are all similar:

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_ecr_repository" "nginx" {
  name                 = "nginx"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
```

{{%/expand%}}

---

## Data resources - Read only references we need to build the infrastructure

### data-cicdvpc.tf

{{%expand "Expand here to see the code" %}}
```bash
data "aws_vpc" "cicd" {
  default = false
  filter {
    name   = "tag:workshop"
    values = ["eks-cicd"]
  }
}
```

{{%/expand%}}

---
### data_subnet_cicd.tf
{{%expand "Expand here to see the code" %}}
```bash
data "aws_subnet" "cicd" {

  filter {
    name   = "tag:workshop"
    values = ["cicd-private1"]
  }
}
```

{{%/expand%}}

---
### data-sg-cicd.tf
{{%expand "Expand here to see the code" %}}
```bash
data "aws_security_group" "cicd" {
  vpc_id=data.aws_vpc.cicd.id
  filter {
    name   = "tag:workshop"
    values = ["eks-cicd"]
  }

```

{{%/expand%}}

---
### data_kms_alias_s3.tf
{{%expand "Expand here to see the code" %}}
```bash
data "aws_kms_alias" "s3" {
  name = "alias/aws/s3"
}
```

{{%/expand%}}

---


## CodeBuild and CodePipeline Roles Policies and Policy Attachments 

These Terraform files define the required Policies, Roles and Policy attachments to the roles that CodeBuild and CodePipeline require:

Policies:

* aws_iam_policy__AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app.tf
* aws_iam_policy__CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1.tf
* aws_iam_policy__CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1.tf

Roles:

* aws_iam_role__AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app.tf
* aws_iam_role__codebuild-eks-cicd-build-app-service-role.tf

Role Policy attachments:

* aws_iam_role_policy_attachment__AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app.tf
* aws_iam_role_policy_attachment__codebuild-eks-cicd-build-app-service-role__AdministratorAccess.tf
* aws_iam_role_policy_attachment__codebuild-eks-cicd-build-app-service-role__CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1.tf
* aws_iam_role_policy_attachment__codebuild-eks-cicd-build-app-service-role__CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1.tf


---


### aws_s3_bucket__codepipeline-bucket.tf

This uses an external data provider to run a script: **get-bucket-name.sh** whcih returns a hopefully unique name for the bucket based on you hostname and a fine-grained timestamp.


{{%expand "Expand here to see the code" %}}
```bash
data "external" "bucket_name" {
  program = ["bash", "get-bucket-name.sh"]
}

output "Name" {
  value = data.external.bucket_name.result.Name
}

resource "aws_s3_bucket" "codepipeline-bucket" {
  bucket = data.external.bucket_name.result.Name
  request_payer  = "BucketOwner"
  tags           = {}

  versioning {
    enabled    = false
    mfa_delete = false
  }
  force_destroy = false
  acl           = "private"
}
```

{{%/expand%}}


---

## CodeCommit, CodeBuild and CodePipeline recources

### aws_codecommit_repository__eksworkshop-app.tf

Create a CodeCommit repository for our sample application 

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_codecommit_repository" "eksworkshop-app" {
  repository_name = "eksworkshop-app"
  description     = "This is the Sample App Repository"
}
```

{{%/expand%}}


### aws_codebuild_project__eks-cicd-build-app.tf

This creates a CodeBuild project , this will encrypt our repo using the key specified **encryption_key = data.aws_kms_alias.s3.arn**, and use the defined service role **aws_iam_role.codebuild-eks-cicd-build-app-service-role**

By default CodeBuild looks for a file called **buildspec.yml** in the root of the code repository. This file defines all ther steps to be taken by the build process.

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_codebuild_project" "eks-cicd-build-app" {
  badge_enabled  = false
  build_timeout  = 60
  encryption_key = data.aws_kms_alias.s3.arn
  name           = "eks-cicd-build-app"
  queued_timeout = 480
  depends_on     = [aws_iam_role.codebuild-eks-cicd-build-app-service-role]
  service_role   = aws_iam_role.codebuild-eks-cicd-build-app-service-role.arn
  source_version = "refs/heads/master"
  tags           = {}

  artifacts {
    encryption_disabled    = false
    override_artifact_name = false
    type                   = "NO_ARTIFACTS"
  }

  cache {
    modes = []
    type  = "NO_CACHE"
  }
```

{{%/expand%}}


### aws_codepipeline__pipe-eksworkshop-app.tf
A CodePipeline resource is created - this consists of two parts - a source location which is our CodeCommit repo and a build stage that references the CodeBuild project.

A previously defined s3 bucket **location = aws_s3_bucket.codepipeline-bucket.bucket** is used to store build artifacts.


{{%expand "Expand here to see the code" %}}
```bash
resource "aws_codepipeline" "pipe-eksworkshop-app" {
  name       = "pipe-eksworkshop-app"
  depends_on = [aws_iam_role.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app]
  role_arn   = aws_iam_role.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app.arn
  tags       = {}

    artifact_store {
    location = aws_s3_bucket.codepipeline-bucket.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      category = "Source"
      configuration = {
        "BranchName"           = "master"
        "OutputArtifactFormat" = "CODE_ZIP"
        "PollForSourceChanges" = "false"
        "RepositoryName"       = "eksworkshop-app"
      }
      input_artifacts = []
      name            = "Source"
      namespace       = "SourceVariables"
      output_artifacts = [
        "SourceArtifact",
      ]
      owner     = "AWS"
      provider  = "CodeCommit"
      region    = "eu-west-1"
      run_order = 1
      version   = "1"
    }
  }
  stage {
    name = "Build"

    action {
      category = "Build"
      configuration = {
        "ProjectName" = "eks-cicd-build-app"
      }
      input_artifacts = [
        "SourceArtifact",
      ]
      name      = "Build"
      namespace = "BuildVariables"
      output_artifacts = [
        "BuildArtifact",
      ]
      owner     = "AWS"
      provider  = "CodeBuild"
      region    = "eu-west-1"
      run_order = 1
      version   = "1"
    }
  }
}

```

{{%/expand%}}


---


### null-auth-cicd.tf & null-load_ecr.tf

These null provioners envoke the auth-cicd.sh and load_ecr.sh scripts below
Note the use of the **depends_on** in both to ensure they don't run until the underlying recources are in place

{{%expand "Expand here to see the code" %}}
```bash
resource "null_resource" "auth-cidr" {
triggers = {
    always_run = timestamp()
}
depends_on     = [aws_iam_role.codebuild-eks-cicd-build-app-service-role]
provisioner "local-exec" {
    on_failure  = fail
    when = create
    interpreter = ["/bin/bash", "-c"]
    command     = <<EOT
        echo "auth cicd role for K8s"
        ./auth-cicd.sh
        echo "************************************************************************************"
     EOT
}
}
```

```bash
resource "null_resource" "load_ecr" {
triggers = {
    always_run = timestamp()
}
depends_on = [aws_ecr_repository.busybox]
provisioner "local-exec" {
    on_failure  = fail
    when = create
    interpreter = ["/bin/bash", "-c"]
    command     = <<EOT
        ./load_ecr.sh
        echo "************************************************************************************"
     EOT
}
}

```

{{%/expand%}}

---



null provisioner scripts

###  auth-cicd.sh

This scipt authorizes the CodeBuild role to access the EKS cluster by patching the aws-auth configmap

The CodeBuild role **codebuild-eks-cicd-build-app-service-role** is added to the **system:masters** kubernets group which gives full admin rights to the cluster.

In production environments you would want to scope this down to perhaps a specific namespace using Kubernetes RBAC. 

{{%expand "Expand here to see the code" %}}
```bash
test -n "$ACCOUNT_ID" && echo ACCOUNT_ID is "$ACCOUNT_ID" || "echo ACCOUNT_ID is not set && exit"
ROLE="    - rolearn: arn:aws:iam::$ACCOUNT_ID:role/codebuild-eks-cicd-build-app-service-role\n      username: build\n      groups:\n        - system:masters"
#
kubectl get -n kube-system configmap/aws-auth -o yaml | awk "/mapRoles: \|/{print;print \"$ROLE\";next}1" > /tmp/aws-auth-patch.yml
#
kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"

```

{{%/expand%}}

---

###  load_ecr.sh

This script logs in to our private ECR repo and then pulls some docker images to the Cloud9 IDE, tags them appropriately for our private ECR repo's and docker push's them into place.

We have to do this as the EKS cluster can only access this private container repo, it has no access to public container repositories.


{{%expand "Expand here to see the code" %}}
```bash
test -n "$AWS_REGION" && echo AWS_REGION is "$AWS_REGION" || "echo AWS_REGION is not set && exit"
test -n "$ACCOUNT_ID" && echo ACCOUNT_ID is "$ACCOUNT_ID" || "echo ACCOUNT_ID is not set && exit"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
#docker pull alexwhen/docker-2048
#docker tag docker-2048 aws_account_id.dkr.ecr.region.amazonaws.com/docker-2048
dirs="nginx busybox"
for i in $dirs; do
docker pull $i
docker tag $i $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$i
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$i
done

#docker pull alexwhen/docker-2048 
#docker tag alexwhen/docker-2048 $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sample-app
#docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sample-app

docker pull public.ecr.aws/awsandy/docker-2048 
docker tag public.ecr.aws/awsandy/docker-2048 $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sample-app
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/sample-app

```

{{%/expand%}}


---