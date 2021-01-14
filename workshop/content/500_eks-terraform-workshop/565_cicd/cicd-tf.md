---
title: "Create the CI/CD Components"
date: 2018-09-18T16:01:14-05:00
weight: 566
---

## Create the CI/CD components: ECR, CodeCoomit, CodeBuild and CodePipeline



```bash
cd ~/environment/tfekscode/cicd
```

Initialze Terraform

```bash
terraform init
```

Validate the Terraform code
```bash
terraform validate
```
{{< output >}}
Success! The configuration is valid.
{{< /output >}}

----

Plan the deployment:
```bash
terraform plan -out tfplan
```

{{< output >}}

Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.aws_vpc.cicd: Refreshing state...
data.aws_kms_alias.s3: Refreshing state...
data.aws_subnet.cicd: Refreshing state...
data.aws_security_group.cicd: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_codebuild_project.eks-cicd-build-app will be created
  + resource "aws_codebuild_project" "eks-cicd-build-app" {
      + arn            = (known after apply)
      + badge_enabled  = false
      + badge_url      = (known after apply)
      + build_timeout  = 60
      + description    = (known after apply)
      + encryption_key = "arn:aws:kms:eu-west-1:566972129213:alias/aws/s3"
      + id             = (known after apply)
      + name           = "eks-cicd-build-app"
      + queued_timeout = 480
      + service_role   = (known after apply)
      + source_version = "refs/heads/master"

      + artifacts {
          + encryption_disabled    = false
          + override_artifact_name = false
          + type                   = "NO_ARTIFACTS"
        }

      + cache {
          + modes = []
          + type  = "NO_CACHE"
        }

      + environment {
          + compute_type                = "BUILD_GENERAL1_SMALL"
          + image                       = "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
          + image_pull_credentials_type = "CODEBUILD"
          + privileged_mode             = false
          + type                        = "LINUX_CONTAINER"
        }

      + logs_config {
          + cloudwatch_logs {
              + status = "ENABLED"
            }

          + s3_logs {
              + encryption_disabled = false
              + status              = "DISABLED"
            }
        }

      + source {
          + git_clone_depth     = 1
          + insecure_ssl        = false
          + location            = (known after apply)
          + report_build_status = false
          + type                = "CODECOMMIT"

          + git_submodules_config {
              + fetch_submodules = false
            }
        }

      + vpc_config {
          + security_group_ids = [
              + "sg-0cbdfdb07537cc343",
            ]
          + subnets            = [
              + "subnet-0965178eadd9e98a5",
            ]
          + vpc_id             = "vpc-072c250898c248409"
        }
    }

  # aws_codecommit_repository.eksworkshop-app will be created
  + resource "aws_codecommit_repository" "eksworkshop-app" {
      + arn             = (known after apply)
      + clone_url_http  = (known after apply)
      + clone_url_ssh   = (known after apply)
      + description     = "This is the Sample App Repository"
      + id              = (known after apply)
      + repository_id   = (known after apply)
      + repository_name = "eksworkshop-app"
    }

  # aws_codepipeline.pipe-eksworkshop-app will be created
  + resource "aws_codepipeline" "pipe-eksworkshop-app" {
      + arn      = (known after apply)
      + id       = (known after apply)
      + name     = "pipe-eksworkshop-app"
      + role_arn = (known after apply)

      + artifact_store {
          + location = "codepipeline-eu-west-1-421985771879"
          + region   = (known after apply)
          + type     = "S3"
        }

      + stage {
          + name = "Source"

          + action {
              + category         = "Source"
              + configuration    = {
                  + "BranchName"           = "master"
                  + "OutputArtifactFormat" = "CODE_ZIP"
                  + "PollForSourceChanges" = "false"
                  + "RepositoryName"       = "eksworkshop-app"
                }
              + input_artifacts  = []
              + name             = "Source"
              + namespace        = "SourceVariables"
              + output_artifacts = [
                  + "SourceArtifact",
                ]
              + owner            = "AWS"
              + provider         = "CodeCommit"
              + region           = "eu-west-1"
              + run_order        = 1
              + version          = "1"
            }
        }
      + stage {
          + name = "Build"

          + action {
              + category         = "Build"
              + configuration    = {
                  + "ProjectName" = "eks-cicd-build-app"
                }
              + input_artifacts  = [
                  + "SourceArtifact",
                ]
              + name             = "Build"
              + namespace        = "BuildVariables"
              + output_artifacts = [
                  + "BuildArtifact",
                ]
              + owner            = "AWS"
              + provider         = "CodeBuild"
              + region           = "eu-west-1"
              + run_order        = 1
              + version          = "1"
            }
        }
    }

  # aws_ecr_repository.busybox will be created
  + resource "aws_ecr_repository" "busybox" {
      + arn                  = (known after apply)
      + id                   = (known after apply)
      + image_tag_mutability = "MUTABLE"
      + name                 = "busybox"
      + registry_id          = (known after apply)
      + repository_url       = (known after apply)

      + image_scanning_configuration {
          + scan_on_push = true
        }
    }

  # aws_ecr_repository.nginx will be created
  + resource "aws_ecr_repository" "nginx" {
      + arn                  = (known after apply)
      + id                   = (known after apply)
      + image_tag_mutability = "MUTABLE"
      + name                 = "nginx"
      + registry_id          = (known after apply)
      + repository_url       = (known after apply)

      + image_scanning_configuration {
          + scan_on_push = true
        }
    }

  # aws_ecr_repository.sample-app will be created
  + resource "aws_ecr_repository" "sample-app" {
      + arn                  = (known after apply)
      + id                   = (known after apply)
      + image_tag_mutability = "MUTABLE"
      + name                 = "sample-app"
      + registry_id          = (known after apply)
      + repository_url       = (known after apply)

      + image_scanning_configuration {
          + scan_on_push = true
        }
    }

  # aws_iam_policy.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app will be created
  + resource "aws_iam_policy" "AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app" {
      + arn         = (known after apply)
      + description = "Policy used in trust relationship with CodePipeline"
      + id          = (known after apply)
      + name        = "AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app"
      + path        = "/service-role/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action    = [
                          + "iam:PassRole",
                        ]
                      + Condition = {
                          + StringEqualsIfExists = {
                              + iam:PassedToService = [
                                  + "cloudformation.amazonaws.com",
                                  + "elasticbeanstalk.amazonaws.com",
                                  + "ec2.amazonaws.com",
                                  + "ecs-tasks.amazonaws.com",
                                ]
                            }
                        }
                      + Effect    = "Allow"
                      + Resource  = "*"
                    },
                  + {
                      + Action   = [
                          + "codecommit:CancelUploadArchive",
                          + "codecommit:GetBranch",
                          + "codecommit:GetCommit",
                          + "codecommit:GetRepository",
                          + "codecommit:GetUploadArchiveStatus",
                          + "codecommit:UploadArchive",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "codedeploy:CreateDeployment",
                          + "codedeploy:GetApplication",
                          + "codedeploy:GetApplicationRevision",
                          + "codedeploy:GetDeployment",
                          + "codedeploy:GetDeploymentConfig",
                          + "codedeploy:RegisterApplicationRevision",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "codestar-connections:UseConnection",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "elasticbeanstalk:*",
                          + "ec2:*",
                          + "elasticloadbalancing:*",
                          + "autoscaling:*",
                          + "cloudwatch:*",
                          + "s3:*",
                          + "sns:*",
                          + "cloudformation:*",
                          + "rds:*",
                          + "sqs:*",
                          + "ecs:*",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "lambda:InvokeFunction",
                          + "lambda:ListFunctions",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "opsworks:CreateDeployment",
                          + "opsworks:DescribeApps",
                          + "opsworks:DescribeCommands",
                          + "opsworks:DescribeDeployments",
                          + "opsworks:DescribeInstances",
                          + "opsworks:DescribeStacks",
                          + "opsworks:UpdateApp",
                          + "opsworks:UpdateStack",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "cloudformation:CreateStack",
                          + "cloudformation:DeleteStack",
                          + "cloudformation:DescribeStacks",
                          + "cloudformation:UpdateStack",
                          + "cloudformation:CreateChangeSet",
                          + "cloudformation:DeleteChangeSet",
                          + "cloudformation:DescribeChangeSet",
                          + "cloudformation:ExecuteChangeSet",
                          + "cloudformation:SetStackPolicy",
                          + "cloudformation:ValidateTemplate",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "codebuild:BatchGetBuilds",
                          + "codebuild:StartBuild",
                          + "codebuild:BatchGetBuildBatches",
                          + "codebuild:StartBuildBatch",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "devicefarm:ListProjects",
                          + "devicefarm:ListDevicePools",
                          + "devicefarm:GetRun",
                          + "devicefarm:GetUpload",
                          + "devicefarm:CreateUpload",
                          + "devicefarm:ScheduleRun",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "servicecatalog:ListProvisioningArtifacts",
                          + "servicecatalog:CreateProvisioningArtifact",
                          + "servicecatalog:DescribeProvisioningArtifact",
                          + "servicecatalog:DeleteProvisioningArtifact",
                          + "servicecatalog:UpdateProduct",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "cloudformation:ValidateTemplate",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "ecr:DescribeImages",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "states:DescribeExecution",
                          + "states:DescribeStateMachine",
                          + "states:StartExecution",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action   = [
                          + "appconfig:StartDeployment",
                          + "appconfig:StopDeployment",
                          + "appconfig:GetDeployment",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
    }

  # aws_iam_policy.CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1 will be created
  + resource "aws_iam_policy" "CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1" {
      + arn         = (known after apply)
      + description = "Policy used in trust relationship with CodeBuild"
      + id          = (known after apply)
      + name        = "CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1"
      + path        = "/service-role/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "logs:CreateLogGroup",
                          + "logs:CreateLogStream",
                          + "logs:PutLogEvents",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:logs:eu-west-1:566972129213:log-group:/aws/codebuild/eks-cicd-build-app",
                          + "arn:aws:logs:eu-west-1:566972129213:log-group:/aws/codebuild/eks-cicd-build-app:*",
                        ]
                    },
                  + {
                      + Action   = [
                          + "s3:PutObject",
                          + "s3:GetObject",
                          + "s3:GetObjectVersion",
                          + "s3:GetBucketAcl",
                          + "s3:GetBucketLocation",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:s3:::codepipeline-eu-west-1-*",
                        ]
                    },
                  + {
                      + Action   = [
                          + "codecommit:GitPull",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:codecommit:eu-west-1:566972129213:Terraform-EKS",
                        ]
                    },
                  + {
                      + Action   = [
                          + "codebuild:CreateReportGroup",
                          + "codebuild:CreateReport",
                          + "codebuild:UpdateReport",
                          + "codebuild:BatchPutTestCases",
                          + "codebuild:BatchPutCodeCoverages",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:codebuild:eu-west-1:566972129213:report-group/eks-cicd-build-app-*",
                        ]
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
    }

  # aws_iam_policy.CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1 will be created
  + resource "aws_iam_policy" "CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1" {
      + arn         = (known after apply)
      + description = "Policy used in trust relationship with CodeBuild"
      + id          = (known after apply)
      + name        = "CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1"
      + path        = "/service-role/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "ec2:CreateNetworkInterface",
                          + "ec2:DescribeDhcpOptions",
                          + "ec2:DescribeNetworkInterfaces",
                          + "ec2:DeleteNetworkInterface",
                          + "ec2:DescribeSubnets",
                          + "ec2:DescribeSecurityGroups",
                          + "ec2:DescribeVpcs",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                    },
                  + {
                      + Action    = [
                          + "ec2:CreateNetworkInterfacePermission",
                        ]
                      + Condition = {
                          + StringEquals = {
                              + ec2:AuthorizedService = "codebuild.amazonaws.com"
                              + ec2:Subnet            = [
                                  + "arn:aws:ec2:eu-west-1:566972129213:subnet/subnet-00cc72ac5b0b79dd4",
                                ]
                            }
                        }
                      + Effect    = "Allow"
                      + Resource  = "arn:aws:ec2:eu-west-1:566972129213:network-interface/*"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
    }

  # aws_iam_role.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app will be created
  + resource "aws_iam_role" "AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app" {
      + arn                   = (known after apply)
      + assume_role_policy    = jsonencode(
            {
              + Statement = [
                  + {
                      + Action    = "sts:AssumeRole"
                      + Effect    = "Allow"
                      + Principal = {
                          + Service = "codepipeline.amazonaws.com"
                        }
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + create_date           = (known after apply)
      + force_detach_policies = false
      + id                    = (known after apply)
      + max_session_duration  = 3600
      + name                  = "AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app"
      + path                  = "/service-role/"
      + unique_id             = (known after apply)
    }

  # aws_iam_role.codebuild-eks-cicd-build-app-service-role will be created
  + resource "aws_iam_role" "codebuild-eks-cicd-build-app-service-role" {
      + arn                   = (known after apply)
      + assume_role_policy    = jsonencode(
            {
              + Statement = [
                  + {
                      + Action    = "sts:AssumeRole"
                      + Effect    = "Allow"
                      + Principal = {
                          + Service = "codebuild.amazonaws.com"
                        }
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + create_date           = (known after apply)
      + force_detach_policies = false
      + id                    = (known after apply)
      + max_session_duration  = 3600
      + name                  = "codebuild-eks-cicd-build-app-service-role"
      + path                  = "/service-role/"
      + unique_id             = (known after apply)
    }

  # aws_iam_role_policy_attachment.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app__AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app will be created
  + resource "aws_iam_role_policy_attachment" "AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app__AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app" {
      + id         = (known after apply)
      + policy_arn = (known after apply)
      + role       = (known after apply)
    }

  # aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__AdministratorAccess will be created
  + resource "aws_iam_role_policy_attachment" "codebuild-eks-cicd-build-app-service-role__AdministratorAccess" {
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
      + role       = (known after apply)
    }

  # aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1 will be created
  + resource "aws_iam_role_policy_attachment" "codebuild-eks-cicd-build-app-service-role__CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1" {
      + id         = (known after apply)
      + policy_arn = (known after apply)
      + role       = (known after apply)
    }

  # aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1 will be created
  + resource "aws_iam_role_policy_attachment" "codebuild-eks-cicd-build-app-service-role__CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1" {
      + id         = (known after apply)
      + policy_arn = (known after apply)
      + role       = (known after apply)
    }

  # aws_iam_user.git-user will be created
  + resource "aws_iam_user" "git-user" {
      + arn           = (known after apply)
      + force_destroy = false
      + id            = (known after apply)
      + name          = "git-user"
      + path          = "/"
      + tags          = {
          + "workshop" = "eks-cicd"
        }
      + unique_id     = (known after apply)
    }

  # aws_iam_user_policy_attachment.git-attach will be created
  + resource "aws_iam_user_policy_attachment" "git-attach" {
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/AWSCodeCommitPowerUser"
      + user       = "git-user"
    }

  # aws_s3_bucket.codepipeline-eu-west-1-421985771879 will be created
  + resource "aws_s3_bucket" "codepipeline-eu-west-1-421985771879" {
      + acceleration_status         = (known after apply)
      + acl                         = "private"
      + arn                         = (known after apply)
      + bucket                      = "codepipeline-eu-west-1-421985771879"
      + bucket_domain_name          = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = "Z1BKCTXD74EZPE"
      + id                          = (known after apply)
      + region                      = (known after apply)
      + request_payer               = "BucketOwner"
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + versioning {
          + enabled    = false
          + mfa_delete = false
        }
    }

  # null_resource.load_ecr will be created
  + resource "null_resource" "load_ecr" {
      + id       = (known after apply)
      + triggers = (known after apply)
    }

Plan: 19 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"

{{< /output >}}  


You can see from the plan the following resources will be created:

* A CodeCommit repository
* A CodeBuild service for running build and deploy operations
* A CodePipeline implementationto orchastrate the triggering of the CodeBuild
* 3x private ECR repositories
* Policies and Roles for CodePipeline and CodeBuild
* A git user for the CodeCommit repo 
* A null resource - this triggers the **load-ecr.sh** script which populates the private ECR 

----

Build the environment:
```bash
terraform apply tfplan
```

{{< output >}}
aws_iam_policy.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app: Creating...
aws_iam_policy.CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1: Creating...
aws_codecommit_repository.eksworkshop-app: Creating...
aws_ecr_repository.sample-app: Creating...
aws_iam_policy.CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1: Creating...
aws_ecr_repository.nginx: Creating...
aws_ecr_repository.busybox: Creating...
aws_iam_role.codebuild-eks-cicd-build-app-service-role: Creating...
aws_s3_bucket.codepipeline-eu-west-1-421985771879: Creating...
aws_iam_role.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app: Creating...
aws_ecr_repository.busybox: Creation complete after 0s [id=busybox]
aws_iam_user.git-user: Creating...
aws_ecr_repository.sample-app: Creation complete after 0s [id=sample-app]
null_resource.load_ecr: Creating...
null_resource.load_ecr: Provisioning with 'local-exec'...
aws_ecr_repository.nginx: Creation complete after 0s [id=nginx]
null_resource.load_ecr (local-exec): Executing: ["/bin/bash" "-c" "        ./load_ecr.sh\n        echo \"************************************************************************************\"\n"]
null_resource.load_ecr (local-exec): AWS_REGION is eu-west-1
null_resource.load_ecr (local-exec): ACCOUNT_ID is 566972129213
aws_codecommit_repository.eksworkshop-app: Creation complete after 0s [id=eksworkshop-app]
aws_iam_role.codebuild-eks-cicd-build-app-service-role: Creation complete after 1s [id=codebuild-eks-cicd-build-app-service-role]
aws_codebuild_project.eks-cicd-build-app: Creating...
aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__AdministratorAccess: Creating...
aws_iam_user.git-user: Creation complete after 1s [id=git-user]
aws_iam_user_policy_attachment.git-attach: Creating...
aws_iam_role.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app: Creation complete after 1s [id=AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app]
aws_codepipeline.pipe-eksworkshop-app: Creating...
aws_iam_policy.CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1: Creation complete after 1s [id=arn:aws:iam::566972129213:policy/service-role/CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1]
aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1: Creating...
aws_iam_policy.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app: Creation complete after 1s [id=arn:aws:iam::566972129213:policy/service-role/AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app]
aws_iam_role_policy_attachment.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app__AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app: Creating...
aws_iam_policy.CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1: Creation complete after 1s [id=arn:aws:iam::566972129213:policy/service-role/CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1]
aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1: Creating...
null_resource.load_ecr (local-exec): WARNING! Your password will be stored unencrypted in /home/ec2-user/.docker/config.json.
null_resource.load_ecr (local-exec): Configure a credential helper to remove this warning. See
null_resource.load_ecr (local-exec): https://docs.docker.com/engine/reference/commandline/login/#credentials-store

null_resource.load_ecr (local-exec): Login Succeeded
null_resource.load_ecr (local-exec): Using default tag: latest
aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__AdministratorAccess: Creation complete after 1s [id=codebuild-eks-cicd-build-app-service-role-20201210180231390200000001]
aws_s3_bucket.codepipeline-eu-west-1-421985771879: Creation complete after 2s [id=codepipeline-eu-west-1-421985771879]
aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__CodeBuildVpcPolicy-eks-cicd-build-app-eu-west-1: Creation complete after 1s [id=codebuild-eks-cicd-build-app-service-role-20201210180231592800000003]
aws_iam_role_policy_attachment.AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app__AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app: Creation complete after 1s [id=AWSCodePipelineServiceRole-eu-west-1-pipe-eksworkshop-app-20201210180231661300000004]
aws_iam_role_policy_attachment.codebuild-eks-cicd-build-app-service-role__CodeBuildBasePolicy-eks-cicd-build-app-eu-west-1: Creation complete after 1s [id=codebuild-eks-cicd-build-app-service-role-20201210180231674100000005]
aws_iam_user_policy_attachment.git-attach: Creation complete after 1s [id=git-user-20201210180231394700000002]
null_resource.load_ecr (local-exec): latest: Pulling from library/nginx
null_resource.load_ecr (local-exec): Digest: sha256:6b1daa9462046581ac15be20277a7c75476283f969cb3a61c8725ec38d3b01c3
null_resource.load_ecr (local-exec): Status: Image is up to date for nginx:latest
null_resource.load_ecr (local-exec): docker.io/library/nginx:latest
null_resource.load_ecr (local-exec): The push refers to repository [566972129213.dkr.ecr.eu-west-1.amazonaws.com/nginx]
null_resource.load_ecr (local-exec): 7e914612e366: Preparing
null_resource.load_ecr (local-exec): f790aed835ee: Preparing
null_resource.load_ecr (local-exec): 850c2400ea4d: Preparing
null_resource.load_ecr (local-exec): 7ccabd267c9f: Preparing
null_resource.load_ecr (local-exec): f5600c6330da: Preparing
null_resource.load_ecr (local-exec): f790aed835ee: Pushed
null_resource.load_ecr (local-exec): 7e914612e366: Pushed
null_resource.load_ecr (local-exec): 850c2400ea4d: Pushed
null_resource.load_ecr: Still creating... [10s elapsed]
aws_codebuild_project.eks-cicd-build-app: Still creating... [10s elapsed]
aws_codepipeline.pipe-eksworkshop-app: Still creating... [10s elapsed]
null_resource.load_ecr (local-exec): 7ccabd267c9f: Pushed
null_resource.load_ecr (local-exec): f5600c6330da: Pushed
null_resource.load_ecr (local-exec): latest: digest: sha256:99d0a53e3718cef59443558607d1e100b325d6a2b678cd2a48b05e5e22ffeb49 size: 1362
null_resource.load_ecr (local-exec): Using default tag: latest
null_resource.load_ecr (local-exec): latest: Pulling from library/busybox
null_resource.load_ecr (local-exec): ea97eb0eb3ec: Pulling fs layer
aws_codebuild_project.eks-cicd-build-app: Creation complete after 16s [id=arn:aws:codebuild:eu-west-1:566972129213:project/eks-cicd-build-app]
null_resource.load_ecr (local-exec): ea97eb0eb3ec: Verifying Checksum
null_resource.load_ecr (local-exec): ea97eb0eb3ec: Download complete
aws_codepipeline.pipe-eksworkshop-app: Creation complete after 16s [id=pipe-eksworkshop-app]
null_resource.load_ecr (local-exec): ea97eb0eb3ec: Pull complete
null_resource.load_ecr (local-exec): Digest: sha256:bde48e1751173b709090c2539fdf12d6ba64e88ec7a4301591227ce925f3c678
null_resource.load_ecr (local-exec): Status: Downloaded newer image for busybox:latest
null_resource.load_ecr (local-exec): docker.io/library/busybox:latest
null_resource.load_ecr (local-exec): The push refers to repository [566972129213.dkr.ecr.eu-west-1.amazonaws.com/busybox]
null_resource.load_ecr (local-exec): de168d3b8ec4: Preparing
null_resource.load_ecr (local-exec): de168d3b8ec4: Pushed
null_resource.load_ecr (local-exec): latest: digest: sha256:31a54a0cf86d7354788a8265f60ae6acb4b348a67efbcf7c1007dd3cf7af05ab size: 527
null_resource.load_ecr (local-exec): Using default tag: latest
null_resource.load_ecr (local-exec): latest: Pulling from alexwhen/docker-2048
null_resource.load_ecr (local-exec): Image docker.io/alexwhen/docker-2048:latest uses outdated schema1 manifest format. Please upgrade to a schema2 image for better future compatibility. More information at https://docs.docker.com/registry/spec/deprecated-schema-v1/
null_resource.load_ecr (local-exec): c862d82a67a2: Already exists
null_resource.load_ecr (local-exec): a3ed95caeb02: Already exists
null_resource.load_ecr (local-exec): 69dbbd8c451d: Already exists
null_resource.load_ecr (local-exec): e9b345a0f742: Already exists
null_resource.load_ecr (local-exec): a3ed95caeb02: Already exists
null_resource.load_ecr (local-exec): a3ed95caeb02: Already exists
null_resource.load_ecr (local-exec): Digest: sha256:4913452e5bd092db9c8b005523127b8f62821867021e23a9acb1ae0f7d2432e1
null_resource.load_ecr (local-exec): Status: Image is up to date for alexwhen/docker-2048:latest
null_resource.load_ecr (local-exec): docker.io/alexwhen/docker-2048:latest
null_resource.load_ecr (local-exec): The push refers to repository [566972129213.dkr.ecr.eu-west-1.amazonaws.com/sample-app]
null_resource.load_ecr (local-exec): 5f70bf18a086: Preparing
null_resource.load_ecr (local-exec): 5f70bf18a086: Preparing
null_resource.load_ecr (local-exec): 7c624c88ed95: Preparing
null_resource.load_ecr (local-exec): 41b3adcd63c6: Preparing
null_resource.load_ecr (local-exec): 5f70bf18a086: Preparing
null_resource.load_ecr (local-exec): 745737c319fa: Preparing
null_resource.load_ecr: Still creating... [20s elapsed]
null_resource.load_ecr (local-exec): 5f70bf18a086: Pushed
null_resource.load_ecr (local-exec): 41b3adcd63c6: Pushed
null_resource.load_ecr (local-exec): 7c624c88ed95: Pushed
null_resource.load_ecr (local-exec): 745737c319fa: Pushed
null_resource.load_ecr (local-exec): latest: digest: sha256:ecfb0206e8b62c29bd737bf553420f2f460107595f2c5b4671af0a5bfd8367df size: 1567
null_resource.load_ecr (local-exec): ************************************************************************************
null_resource.load_ecr: Creation complete after 22s [id=7521613959159685341]

Apply complete! Resources: 19 added, 0 changed, 0 destroyed.

{{< /output >}}

-----

Check codebuild is authorised to access the EKS cluster ok

```bash
kubectl get -n kube-system configmap/aws-auth -o yaml | grep -i codebuild
```
{{< output >}}
     - rolearn: arn:aws:iam:011898610386:role/codebuild-eks-cicd-build-app-service-role
{{< /output >}}

If you don't see a line of output similar to the line above - run this command:


```bash
./auth-cicd.sh
```

---




