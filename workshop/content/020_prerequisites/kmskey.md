---
title: "Create an AWS KMS Custom Managed Key (CMK)"
chapter: false
draft: true
weight: 900
---



Create a CMK for the EKS cluster to use when encrypting your Kubernetes secrets:
```bash
aws kms create-alias --alias-name alias/eksworkshop --target-key-id $(aws kms create-key --query KeyMetadata.Arn --output text)
```

Let's retrieve the ARN of the CMK to input into the create cluster command.

```bash
export MASTER_ARN=$(aws kms describe-key --key-id alias/eksworkshop --query KeyMetadata.Arn --output text)
```

We set the MASTER_ARN environment variable to make it easier to refer to the KMS key later.

Now, let's save the MASTER_ARN environment variable into the bash_profile

```bash
echo "export MASTER_ARN=${MASTER_ARN}" | tee -a ~/.bash_profile
```

And finally source your bash_profile:

```
. ~/.bash_profile
```
