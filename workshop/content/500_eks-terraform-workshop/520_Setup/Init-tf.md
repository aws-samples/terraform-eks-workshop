---
title: "Using Terraform to create the Terraform state bucket"
date: 2018-09-18T16:01:14-05:00
weight: 522
---

## Initializing the Terraform state bucket and DynamoDB lock tables


```
cd ~/environment/tfekscode/tf-setup 
```

Initialize the Terraform backend environment:

```
terraform init
```

The command wil create a hidden directory in your file system called ".terraform" and it will download all the resource providers that are needed, for our environment this includes the aws, external and null providers:


{{< output >}}
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/null versions matching "~> 3.0"...
- Finding hashicorp/external versions matching "~> 2.0"...
- Finding hashicorp/aws versions matching "~> 3.22"...
- Installing hashicorp/null v3.0.0...
- Installed hashicorp/null v3.0.0 (signed by HashiCorp)
- Installing hashicorp/external v2.0.0...
- Installed hashicorp/external v2.0.0 (signed by HashiCorp)
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

----

### Validate the Terraform code
```
terraform validate
```
{{< output >}}
Success! The configuration is valid.
{{< /output >}}

----

### Plan the deployment:
```
terraform plan -out tfplan
```

{{< output >}}
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_dynamodb_table.terraform_locks[0] will be created
  + resource "aws_dynamodb_table" "terraform_locks" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "terraform_locks_net"
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = (known after apply)
        }

      + server_side_encryption {
          + enabled     = (known after apply)
          + kms_key_arn = (known after apply)
        }
    }

  # aws_dynamodb_table.terraform_locks[1] will be created
  + resource "aws_dynamodb_table" "terraform_locks" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "terraform_locks_iam"
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = (known after apply)
        }

      + server_side_encryption {
          + enabled     = (known after apply)
          + kms_key_arn = (known after apply)
        }
    }

  # aws_dynamodb_table.terraform_locks[2] will be created
  + resource "aws_dynamodb_table" "terraform_locks" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "terraform_locks_c9net"
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = (known after apply)
        }

      + server_side_encryption {
          + enabled     = (known after apply)
          + kms_key_arn = (known after apply)
        }
    }

  # aws_dynamodb_table.terraform_locks[3] will be created
  + resource "aws_dynamodb_table" "terraform_locks" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "terraform_locks_cluster"
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = (known after apply)
        }

      + server_side_encryption {
          + enabled     = (known after apply)
          + kms_key_arn = (known after apply)
        }
    }

  # aws_dynamodb_table.terraform_locks[4] will be created
  + resource "aws_dynamodb_table" "terraform_locks" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "terraform_locks_nodeg"
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = (known after apply)
        }

      + server_side_encryption {
          + enabled     = (known after apply)
          + kms_key_arn = (known after apply)
        }
    }

  # aws_dynamodb_table.terraform_locks[5] will be created
  + resource "aws_dynamodb_table" "terraform_locks" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "terraform_locks_cicd"
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = (known after apply)
        }

      + server_side_encryption {
          + enabled     = (known after apply)
          + kms_key_arn = (known after apply)
        }
    }

  # aws_dynamodb_table.terraform_locks[6] will be created
  + resource "aws_dynamodb_table" "terraform_locks" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "terraform_locks_eks-cidr"
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }

      + point_in_time_recovery {
          + enabled = (known after apply)
        }

      + server_side_encryption {
          + enabled     = (known after apply)
          + kms_key_arn = (known after apply)
        }
    }

  # aws_s3_bucket.terraform_state will be created
  + resource "aws_s3_bucket" "terraform_state" {
      + acceleration_status         = (known after apply)
      + acl                         = "private"
      + arn                         = (known after apply)
      + bucket                      = "terraform-state-ip-172-31-2-146"
      + bucket_domain_name          = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = true
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)

      + server_side_encryption_configuration {
          + rule {
              + apply_server_side_encryption_by_default {
                  + sse_algorithm = "AES256"
                }
            }
        }

      + versioning {
          + enabled    = true
          + mfa_delete = false
        }
    }

  # null_resource.gen_backend will be created
  + resource "null_resource" "gen_backend" {
      + id       = (known after apply)
      + triggers = (known after apply)
    }

  # null_resource.sleep will be created
  + resource "null_resource" "sleep" {
      + id       = (known after apply)
      + triggers = (known after apply)
    }

Plan: 10 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + Name                         = "terraform-state-ip-172-31-2-146"
  + dynamodb_table_name_c9net    = "terraform_locks_c9net"
  + dynamodb_table_name_cicd     = "terraform_locks_cicd"
  + dynamodb_table_name_cluster  = "terraform_locks_cluster"
  + dynamodb_table_name_eks-cidr = "terraform_locks_eks-cidr"
  + dynamodb_table_name_iam      = "terraform_locks_iam"
  + dynamodb_table_name_net      = "terraform_locks_net"
  + dynamodb_table_name_nodeg    = "terraform_locks_nodeg"
  + region                       = [
      + (known after apply),
    ]
  + s3_bucket                    = [
      + "terraform-state-ip-172-31-2-146",
    ]

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"
{{< /output >}}

----

### Next "apply" the plan to build the infrastructure in AWS

```
terraform apply tfplan
```

{{< output >}}
aws_s3_bucket.terraform_state: Creating...
aws_s3_bucket.terraform_state: Creation complete after 2s [id=terraform-state-ip-172-31-2-146]
aws_dynamodb_table.terraform_locks[3]: Creating...
aws_dynamodb_table.terraform_locks[2]: Creating...
aws_dynamodb_table.terraform_locks[5]: Creating...
aws_dynamodb_table.terraform_locks[0]: Creating...
aws_dynamodb_table.terraform_locks[4]: Creating...
aws_dynamodb_table.terraform_locks[6]: Creating...
aws_dynamodb_table.terraform_locks[1]: Creating...
aws_dynamodb_table.terraform_locks[4]: Creation complete after 7s [id=terraform_locks_nodeg]
aws_dynamodb_table.terraform_locks[6]: Creation complete after 7s [id=terraform_locks_eks-cidr]
aws_dynamodb_table.terraform_locks[0]: Creation complete after 7s [id=terraform_locks_net]
aws_dynamodb_table.terraform_locks[5]: Creation complete after 8s [id=terraform_locks_cicd]
aws_dynamodb_table.terraform_locks[3]: Creation complete after 8s [id=terraform_locks_cluster]
aws_dynamodb_table.terraform_locks[1]: Creation complete after 8s [id=terraform_locks_iam]
aws_dynamodb_table.terraform_locks[2]: Creation complete after 9s [id=terraform_locks_c9net]
null_resource.sleep: Creating...
null_resource.sleep: Provisioning with 'local-exec'...
null_resource.sleep (local-exec): Executing: ["/bin/sh" "-c" "sleep 5"]
null_resource.sleep: Creation complete after 5s [id=3192253516749502333]
null_resource.gen_backend: Creating...
null_resource.gen_backend: Provisioning with 'local-exec'...
null_resource.gen_backend (local-exec): Executing: ["/bin/sh" "-c" "./gen-backend.sh"]
null_resource.gen_backend (local-exec): region=eu-west-1
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_net
null_resource.gen_backend (local-exec): ‘generated/backend-net.tf’ -> ‘../net/backend-net.tf’
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_iam
null_resource.gen_backend (local-exec): ‘generated/backend-iam.tf’ -> ‘../iam/backend-iam.tf’
null_resource.gen_backend: Still creating... [10s elapsed]
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_c9net
null_resource.gen_backend (local-exec): ‘generated/backend-c9net.tf’ -> ‘../c9net/backend-c9net.tf’
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_cicd
null_resource.gen_backend (local-exec): ‘generated/backend-cicd.tf’ -> ‘../cicd/backend-cicd.tf’
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_cluster
null_resource.gen_backend (local-exec): ‘generated/backend-cluster.tf’ -> ‘../cluster/backend-cluster.tf’
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_nodeg
null_resource.gen_backend (local-exec): ‘generated/backend-nodeg.tf’ -> ‘../nodeg/backend-nodeg.tf’
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_eks-cidr
null_resource.gen_backend (local-exec): ‘generated/backend-eks-cidr.tf’ -> ‘../eks-cidr/backend-eks-cidr.tf’
null_resource.gen_backend (local-exec): **** REMOTE ****
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_net
null_resource.gen_backend: Still creating... [20s elapsed]
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_iam
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_c9net
null_resource.gen_backend (local-exec): terraform-state-ip-172-31-2-146 terraform_locks_cluster
null_resource.gen_backend: Creation complete after 23s [id=6083657761230822814]

Apply complete! Resources: 10 added, 0 changed, 0 destroyed.

The state of your infrastructure has been saved to the path
below. This state is required to modify and destroy your
infrastructure, so keep it safe. To inspect the complete state
use the `terraform show` command.

State path: terraform.tfstate

Outputs:

Name = "terraform-state-ip-172-31-2-146"
dynamodb_table_name_c9net = "terraform_locks_c9net"
dynamodb_table_name_cicd = "terraform_locks_cicd"
dynamodb_table_name_cluster = "terraform_locks_cluster"
dynamodb_table_name_eks-cidr = "terraform_locks_eks-cidr"
dynamodb_table_name_iam = "terraform_locks_iam"
dynamodb_table_name_net = "terraform_locks_net"
dynamodb_table_name_nodeg = "terraform_locks_nodeg"
region = [
  "eu-west-1",
]
s3_bucket = [
  "terraform-state-ip-172-31-2-146",
]
{{< /output >}}


### The above performed the following actions:

* Creates a unique bucket name based on your hostname. (see gen-bucket-name.sh)
* Initializes Terraform in the tf-setup directory.
* Runs Terraform  (plan and apply) which:
  * Creates a s3 bucket
  * Creates the DynamoDB tables for terraform locks
  * Runs the the gen-backend.sh script from a Terraform "null resource"


![tf-state](/images/andyt/tf-state-aws.jpg)


The **gen-backend.sh script** generates these terraform files for use in other sections and copies them into place:

* generated/backend-{section}.tf   *(For each section this defines where our Terraform state file is located)*
* generated/remote-{section}.tf *(This allows us to access output variables from other sections)*
* var-dynamodb.tf is also copied to each of the sections  
* Various other files are copied into place to ensure Terraform can initialize correctly in your environment. 


  

