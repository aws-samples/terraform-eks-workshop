---
title: "Attach the IAM role to your Workspace"
chapter: false
draft: true
weight: 17
---

1. Follow [this deep link to find your Cloud9 EC2 instance](https://console.aws.amazon.com/ec2/v2/home?#Instances:tag:Name=aws-cloud9-eks-terraform;sort=desc:launchTime;instanceState=running)
1. Select the instance, then choose **Actions / Security / Modify IAM Role**
![c9instancerole](/images/andyt/ModifyIAMRole.jpg)

1. Choose **eksworkshop-admin** from the **IAM Role** drop down, and select **Save**
![c9attachrole](/images/andyt/SaveIAMRole.jpg)
