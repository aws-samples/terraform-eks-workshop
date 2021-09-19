---
title: "Install Kubernetes Tools"
chapter: false
weight: 20
---

Amazon EKS clusters require kubectl, the aws-cli or aws-iam-authenticator
binary to allow IAM authentication for your Kubernetes cluster.

<!--
When you fist open the IDE you will see the auto load of the git hub repo in the terminal

{{< output >}}
/tmp/git-cloning-runner-1605447789774-026172363884.sh
~/environment $ /tmp/git-cloning-runner-1605447789774-026172363884.sh
Cloning into '/home/ec2-user/environment/tfekscode'...
remote: Enumerating objects: 1032, done.
remote: Counting objects: 100% (1032/1032), done.
remote: Compressing objects: 100% (549/549), done.
remote: Total 1032 (delta 530), reused 976 (delta 474), pack-reused 0
Receiving objects: 100% (1032/1032), 393.22 KiB | 493.00 KiB/s, done.
Resolving deltas: 100% (530/530), done.

Navigate to your cloned repository by typing "cd /home/ec2-user/environment/tfekscode" to start working with "https://github.com/aws-samples/terraform-eks-code.git"

To set your display name run "git config --global user.name YOUR_USER_NAME"
To set your display email run "git config --global user.email YOUR_EMAIL_ADDRESS"

~/environment $ 

{{< /output >}}
-->


#### Install the tools

Clone the workshop repo and use a helper script to setup the workshop tools: 

```
cd ~/environment
```

```
git clone https://github.com/aws-samples/terraform-eks-code.git tfekscode
```


#### Setup the workshop tools:

```bash
cd ~/environment/tfekscode
```


```
source ./setup-tools.sh
```

Check you see messages at the end of the output that terraform, kubectl, jq and aws in the path. Also that the AWS_REGION is set and the ACCOUNT_ID to a 12 digit number.

{{< output >}}
Install OS tools

**Output truncated for brevity**

Verify ....
jq in path
aws in path
wget in path
kubectl in path
terraform in path
eksctl in path
helm in path
kubectx in path
AWS_REGION is eu-west-1
ACCOUNT_ID is 123456789012
{{< /output >}}


You may see a pop up message during the tools installation that looks like this:

![grey](/images/andyt/git-warning.png)

You can safely ignore this and click `Don't Show Again`

---

#### Check the Cloud9 IDE is setup correctly:

```bash
./check.sh
```

Provided the Cloud9 workspace was setup as described the following script should show 3x `PASSED:` messages:

{{< output >}}
Checking workshop setup ...
PASSED: Found Instance profile eksworkshop-admin - proceed with the workshop
PASSED: IAM role valid - eksworkshop-admin
PASSED: Cloud9 IDE name is valid - contains eks-terraform
{{< /output >}}


----


:white_check_mark: Proceed to the next step

