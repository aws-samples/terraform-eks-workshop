---
title: "Terraform files explanation"
date: 2018-09-18T16:01:14-05:00
weight: 525
---

## Terraform files and explanation

![tf-state](/images/andyt/tf-state-aws.jpg)


### aws.tf

This specifices the Terraform version requirements, the AWS region and profile from variables, and the AWS credentials from a local file if present.

Look at the contents of the file aws.tf - this file is specifying to Terraform:

- Which version of Terraform should be used **required_version = "~> 0.14.3"**.
- Where the AWS, null and external "providers" come from and the version t0 use.
- And for the AWS provider itself, which region to use and where to get the AWS login credentials.


{{%expand "Expand here to see the code" %}}

```bash
terraform {
  required_version = "~> 0.14.3"
  required_providers {
    aws = {
    source = "hashicorp/aws"
    #  Allow any 3.22+  version of the AWS provider
    version = "~> 3.22"
    }
    null = {
    source = "hashicorp/null"
    version = "~> 3.0"
    }
    external = {
    source = "hashicorp/external"
    version = "~> 2.0"
    }
    
  }
}

provider "aws" {
  region                  = var.region
  shared_credentials_file = "~/.aws/credentials"
  profile                 = var.profile
}
provider "null" {}
provider "external" {}
```
{{%/expand%}}

---


### vars-dynamodb.tf

This file defines some varaibles with values for the 7x DynamoDB tables.
We use 7 tables to help lock the 7x state files that are used for the different stages/sections of our infrastructure build.

{{%expand "Expand here to see the code" %}}
```bash
variable "table_name_net" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-net"
}

variable "table_name_iam" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-iam"
}

variable "table_name_c9net" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-c9net"
}

variable "table_name_cicd" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-cicd"
}

variable "table_name_cluster" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-cluster"
}

variable "table_name_nodeg" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-nodeg"
}

variable "table_name_eks-cidr" {
  description = "The name of the DynamoDB table. Must be unique in this AWS account."
  type        = string
  default     = "at-terraform-eks-workshop1-eks-cidr"
}
```

{{%/expand%}}

---

### vars-main.tf

Some other general varables are set in this file: the region, default AWS profile name, the EKS cluster name and a string map of the 7 stages in the build. 


{{%expand "Expand here to see the code" %}}

```bash
variable "region" {
  description = "The name of the AWS Region"
  type        = string
  default     = "eu-west-1"
}

variable "profile" {
  description = "The name of the AWS profile in the credentials file"
  type        = string
  default     = "default"
}

variable "cluster-name" {
  description = "The name of the EKS Cluster"
  type        = string
  default     = "mycluster1"
}

variable "stages" {
type=list(string)
default=["net","iam","c9net","cicd","cluster","nodeg","eks-cidr"]
}

variable "stagecount" {
type=number
default=7
}
```

{{%/expand%}}

---

### dynamodb-tables.tf

This file specifies that Terraform should create the five dynamoDB tables used to hold the locks for accessing the Terraform state files we wil create later in the S3 bucket, Note the **depends_on** statement to ensure the S3 bucket gets created before the DynamoDB table.

Note how this uses the special terraform "count" capability to create 7x **var.stagecount** different DynamoDB tables.
Each table's name is constructed by assembling a string **format(** that contains a fixed value **terraform_locks_** and a string value from our string array **%s",var.stages** - idexed by the **[count.index]**     

{{%expand "Expand here to see the code" %}}
```bash
resource "aws_dynamodb_table" "terraform_locks" {
  count=var.stagecount
  depends_on=[aws_s3_bucket.terraform_state]
  name         = format("terraform_locks_%s",var.stages[count.index])
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

```

{{%/expand%}}

---

### get-bucket-name.sh

This script simply returns a json formatted unique bucket name, the bucket wil be used to store the Terraform state files. This script is started by the  data "external" "bucket_name" resource in the s3-bucket.tf file (see later).

The only output this script is allowd to produce is a valid JSON formatted string. This is done in the last line of the code by the jq utility **jq -n --arg bn "$BUCKET_NAME" '{"Name":$bn}'**.

{{%expand "Expand here to see the code" %}}
```bash
#!/bin/bash
# Exit if any of the intermediate steps fail
set -e
t1=`hostname | cut -f1 -d'.'`
BUCKET_NAME=`printf "terraform-state-%s" $t1 | awk '{print tolower($0)}'`
jq -n --arg bn "$BUCKET_NAME" '{"Name":$bn}'
```

{{%/expand%}}

---

### s3-bucket.tf

This creates an s3 bucket the bucket name **bucket = data.external.bucket_name.result.Name** is populated via the *data "external" "bucket_name"* resource which in turn starts the script **get-bucket-name.sh** (see above).

{{%expand "Expand here to see the code" %}}
```bash
data "external" "bucket_name" {
  program = ["bash", "get-bucket-name.sh"]
}

output "Name" {
  value = data.external.bucket_name.result.Name
}


resource "aws_s3_bucket" "terraform_state" {

  bucket = data.external.bucket_name.result.Name

  // This is only here so we can destroy the bucket as part of automated tests. You should not copy this for production
  // usage
  force_destroy = true

  # Enable versioning so we can see the full revision history of our
  # state files
  versioning {
    enabled = true
  }

  # Enable server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

```

{{%/expand%}}

---


###  null_resource.tf

The **null_resource** type allow us to run local (or remote) commands as part of an infrastructure build. In this file the first null_resource **depends_on** the second null_resource and the second **depends_on** the DynamoDB table terraform_locks_nodeg. This helps both sequence script invocation and prevents any race conditions (the sleep 5) so that resources are created properly before they are used.

The aim of these two is to call the **gen-backend.sh** script at the right time. 

{{%expand "Expand here to see the code" %}}
```bash
resource "null_resource" "gen_backend" {
triggers = {
    always_run = "${timestamp()}"
}
depends_on = [null_resource.sleep]
provisioner "local-exec" {
    when = create
    command = "./gen-backend.sh"
}
}


resource "null_resource" "sleep" {
triggers = {
    always_run = "${timestamp()}"
}
depends_on = [aws_dynamodb_table.terraform_locks]
provisioner "local-exec" {
    when = create
    command = "sleep 5"
}
}
```

{{%/expand%}}

---


### gen-backend.sh

This script generates these terraform files for use in the other 7 sections of the Terraform build of our EKS infrstructure:

* generated/backend-{section}.tf   *(For each section this defines where our Terraform state file and DynamoDB lock table is located)*
* generated/remote-{section}.tf *(This allows us to access output variables from other sections, helping to ensure 7x independant infrastructure build tasks can be performed)* 
* var-dynamodb.tf and var.main.tf are also copied to each of the sections.
* For the sample application and the optional extra activities - a local state file is configured see **aws.tf** this is very similar to what was used for the Terraform primer lab.

{{%expand "Expand here to see the code" %}}
```bash
#!/bin/bash
d=`pwd`
sleep 5
reg=`terraform output -json region | jq -r .[]`
if [[ -z ${reg} ]] ; then
    echo "no terraform output variables - exiting ....."
    echo "run terraform init/plan/apply in the the init directory first"
else
    echo "region=$reg"
    rm -f $of $of
fi

mkdir -p generated

#default=["net","iam","c9net","cluster","nodeg","cicd","eks-cidr"]
SECTIONS=('net' 'iam' 'c9net' 'cicd' 'cluster' 'nodeg' 'eks-cidr')
 
for section in "${SECTIONS[@]}"
do

    tabn=`terraform output dynamodb_table_name_$section | tr -d '"'`
    s3b=`terraform output -json s3_bucket | jq -r .[]`
    echo $s3b $tabn

    cd $d

    of=`echo "generated/backend-${section}.tf"`
    vf=`echo "generated/vars-${section}.tf"`

    # write out the backend config 
    printf "" > $of
    printf "terraform {\n" >> $of
    printf "required_version = \"~> 0.14.3\"\n" >> $of
    printf "required_providers {\n" >> $of
    printf "  aws = {\n" >> $of
    printf "   source = \"hashicorp/aws\"\n" >> $of
    printf "#  Allow any 3.1x version of the AWS provider\n" >> $of
    printf "   version = \"~> 3.22\"\n" >> $of
    printf "  }\n" >> $of
    printf " }\n" >> $of
    printf "backend \"s3\" {\n" >> $of
    printf "bucket = \"%s\"\n"  $s3b >> $of
    printf "key = \"terraform/%s.tfstate\"\n"  $tabn >> $of
    printf "region = \"%s\"\n"  $reg >> $of
    printf "dynamodb_table = \"%s\"\n"  $tabn >> $of
    printf "encrypt = \"true\"\n"   >> $of
    printf "}\n" >> $of
    printf "}\n" >> $of
    ##
    printf "provider \"aws\" {\n" >> $of
    printf "region = var.region\n"  >> $of
    printf "shared_credentials_file = \"~/.aws/credentials\"\n" >> $of
    printf "profile = var.profile\n" >> $of
    printf "}\n" >> $of

    # copy the files into place
    cp -v $of ../$section
    cp  vars-dynamodb.tf ../$section
    cp  vars-main.tf ../$section
   

done

# next generate the remote_state config files 


cd $d
echo "**** REMOTE ****"

RSECTIONS=('net' 'iam' 'c9net' 'cluster') 
for section in "${RSECTIONS[@]}"
do
    tabn=`terraform output dynamodb_table_name_$section | tr -d '"'`
    s3b=`terraform output -json s3_bucket | jq -r .[]`

    echo $s3b $tabn
    of=`echo "generated/remote-${section}.tf"`
    printf "" > $of

    # write out the remote_state terraform files
    printf "data terraform_remote_state \"%s\" {\n" $section>> $of
    printf "backend = \"s3\"\n" >> $of
    printf "config = {\n" >> $of
    printf "bucket = \"%s\"\n"  $s3b >> $of
    printf "region = \"%s\"\n"  $reg >> $of
    printf "key = \"terraform/%s.tfstate\"\n"  $tabn >> $of
    printf "}\n" >> $of
    printf "}\n" >> $of
done

# put in place remote state access where required
cp  generated/remote-net.tf ../c9net 
cp  generated/remote-net.tf ../cluster
cp  generated/remote-net.tf ../nodeg
cp  generated/remote-net.tf ../extra/nodeg2
cp  generated/remote-net.tf ../eks-cidr
cp  generated/remote-net.tf ../extra/eks-cidr2

cp  generated/remote-iam.tf ../cluster 
cp  generated/remote-iam.tf ../nodeg
cp  generated/remote-iam.tf ../extra/nodeg2

cp  generated/remote-cluster.tf ../nodeg
cp  generated/remote-cluster.tf ../eks-cidr
cp  generated/remote-cluster.tf ../extra/eks-cidr2
cp  generated/remote-cluster.tf ../lb2
cp  generated/remote-cluster.tf ../extra/nodeg2

# Prepare "local state" for the sample app and extra activities
cp  aws.tf ../sampleapp
cp  vars-main.tf ../sampleapp
cp  aws.tf ../lb2
cp  vars-main.tf ../lb2
cp  aws.tf ../extra/sampleapp2
cp  vars-main.tf ../extra/sampleapp2
cp  aws.tf ../extra/nodeg2
cp  vars-main.tf ../extra/nodeg2
cp  aws.tf ../extra/eks-cidr2
cp  vars-main.tf ../extra/eks-cidr2
```

{{%/expand%}}

---


