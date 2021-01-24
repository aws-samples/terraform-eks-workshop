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

Clone the workshop repo - and use a helper script to setup the workshop tools: 

```bash
cd ~/environment
```

```
git clone https://github.com/aws-samples/terraform-eks-code.git tfekscode
```

Setup the workshop tools:

```
cd ~/environment/tfekscode
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

---

#### Resize the operating system disk

```
cd ~/environment/tfekscode
./resize-osdisk.sh
```

{{< output >}}
Collecting boto3
  Downloading https://files.pythonhosted.org/packages/6d/7e/3668fb3049a568dead633f8727810e04db95fda9269effdaf8abab56b8fd/boto3-1.16.18-py2.py3-none-any.whl (129kB)
    100% |████████████████████████████████| 133kB 4.9MB/s 
Requirement already up-to-date: jmespath<1.0.0,>=0.7.1 in /usr/local/lib/python3.6/site-packages (from boto3)
Requirement already up-to-date: s3transfer<0.4.0,>=0.3.0 in /usr/local/lib/python3.6/site-packages (from boto3)
Collecting botocore<1.20.0,>=1.19.18 (from boto3)
  Downloading https://files.pythonhosted.org/packages/d1/e4/3f243b98244f13ac3f7bbe3ec6c4f8473194a200e9785d68696dc5e0d72f/botocore-1.19.18-py2.py3-none-any.whl (6.8MB)
    100% |████████████████████████████████| 6.8MB 197kB/s 
Requirement already up-to-date: python-dateutil<3.0.0,>=2.1 in /usr/local/lib/python3.6/site-packages (from botocore<1.20.0,>=1.19.18->boto3)
Collecting urllib3<1.27,>=1.25.4; python_version != "3.4" (from botocore<1.20.0,>=1.19.18->boto3)
  Downloading https://files.pythonhosted.org/packages/f5/71/45d36a8df68f3ebb098d6861b2c017f3d094538c0fb98fa61d4dc43e69b9/urllib3-1.26.2-py2.py3-none-any.whl (136kB)
    100% |████████████████████████████████| 143kB 7.9MB/s 
Requirement already up-to-date: six>=1.5 in /usr/local/lib/python3.6/site-packages (from python-dateutil<3.0.0,>=2.1->botocore<1.20.0,>=1.19.18->boto3)
Installing collected packages: urllib3, botocore, boto3
Successfully installed boto3-1.16.18 botocore-1.19.18 urllib3-1.26.2
You are using pip version 9.0.3, however version 20.2.4 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
{'VolumeModification': {'VolumeId': 'vol-00d49631551b76ee2', 'ModificationState': 'modifying', 'TargetSize': 30, 'TargetIops': 100, 'TargetVolumeType': 'gp2', 'OriginalSize': 10, 'OriginalIops': 100, 'OriginalVolumeType': 'gp2', 'Progress': 0, 'StartTime': datetime.datetime(2020, 11, 15, 13, 45, 28, tzinfo=tzlocal())}, 'ResponseMetadata': {'RequestId': '8a45385a-238e-4276-97d1-dbf4aacee230', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '8a45385a-238e-4276-97d1-dbf4aacee230', 'content-type': 'text/xml;charset=UTF-8', 'transfer-encoding': 'chunked', 'vary': 'accept-encoding', 'date': 'Sun, 15 Nov 2020 13:45:28 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}
{{< /output >}}


**At this point the Cloud9 IDE will disconnect - wait 2 minutes then:**

If your IDE does not automatically restart a terminal session then:

Close your terminal session that is unresponsive:

![grey](/images/andyt/reboot-greyed.jpg)


![Close terminal](/images/andyt/close-term.jpg)

And open a new Terminal session

![New terminal](/images/andyt/New-Term.jpg) 


----

{{% notice info %}}
If the above fails to work re-open the IDE:
Use the console to select the Cloud9 service
![serv](/images/andyt/Services-cloud9.jpg)
- In the Console select the eks-terraform Cloud9 IDE environment
![c9attachrole](/images/andyt/OpenIDE.jpg)
- Click **Open IDE**
      
**Occassionally during the workshop it may be necessary to re-open the IDE using the above technique.**

{{% /notice %}}


Once reconnected to a terminal you can confirm the resize of the OS disk worked with:

```bash
df -m /
```
{{< output >}}
Filesystem     1M-blocks  Used Available Use% Mounted on
/dev/xvda1         30108  9063     20948  31% /
{{< /output >}}

As above - it should show about 21,000 MB of Available storage on the / file system

---

:white_check_mark: Proceed to the next step

