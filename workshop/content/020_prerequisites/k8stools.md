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

#### Resize the operating system disk

```bash
cd ~/environment/tfekscode
./resize-osdisk.sh
```

This is some sample output from this script **this may include some warnings/errors - these can be ignored**

{{< output >}}
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. pip 21.0 will drop support for Python 2.7 in January 2021. More details about Python 2 support in pip can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support
Resizing OS disk
/home/ec2-user/.local/lib/python2.7/site-packages/boto3/compat.py:86: PythonDeprecationWarning: Boto3 will no longer support Python 2.7 starting July 15, 2021. To continue receiving service updates, bug fixes, and security updates please upgrade to Python 3.6 or later. More information can be found here: https://aws.amazon.com/blogs/developer/announcing-end-of-support-for-python-2-7-in-aws-sdk-for-python-and-aws-cli-v1/
  warnings.warn(warning, PythonDeprecationWarning)
{u'VolumeModification': {u'TargetSize': 30, u'OriginalMultiAttachEnabled': False, u'TargetVolumeType': 'gp2', u'ModificationState': 'modifying', u'TargetMultiAttachEnabled': False, u'VolumeId': 'vol-0b6189f48fa95b405', u'TargetIops': 100, u'StartTime': datetime.datetime(2021, 6, 6, 18, 38, 10, tzinfo=tzlocal()), u'Progress': 0, u'OriginalVolumeType': 'gp2', u'OriginalIops': 100, u'OriginalSize': 10}, 'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': 'e6376b56-f0ba-4f58-a434-f2985d7bf8c3', 'HTTPHeaders': {'x-amzn-requestid': 'e6376b56-f0ba-4f58-a434-f2985d7bf8c3', 'transfer-encoding': 'chunked', 'strict-transport-security': 'max-age=31536000; includeSubDomains', 'vary': 'accept-encoding', 'server': 'AmazonEC2', 'cache-control': 'no-cache, no-store', 'date': 'Sun, 06 Jun 2021 18:38:10 GMT', 'content-type': 'text/xml;charset=UTF-8'}}}
Rebooting ....
{{< /output >}}

**At this point the Cloud9 IDE will disconnect - wait 2 minutes - then the terminal should reconnect**

{{%expand "If your IDE does not automatically restart a terminal session expand here ......." %}}

Close your terminal session that is unresponsive:

![grey](/images/andyt/reboot-greyed.jpg)


![Close terminal](/images/andyt/close-term.jpg)

And open a new Terminal session:

![New terminal](/images/andyt/New-Term.jpg) 


----

{{% notice info %}}
If the above fails to work re-open the IDE:
Use the console to select the Cloud9 service
![serv](/images/andyt/Services-cloud9.jpg)
- In the Console select the eks-terraform Cloud9 IDE environment
![c9attachrole](/images/andyt/OpenIDE.jpg)
- Click **Open IDE**
      
**Occasionally during the workshop it may be necessary to re-open the IDE using the above technique.**

{{% /notice %}}

{{%/expand %}}

Once reconnected to a terminal you can confirm the resizing of the OS disk worked with:

```bash
df -m /
```
{{< output >}}
Filesystem     1M-blocks  Used Available Use% Mounted on
/dev/xvda1         30108  9063     20948  31% /
{{< /output >}}

As above it should show about 21,000 MB of Available storage on the / file system

---

:white_check_mark: Proceed to the next step

