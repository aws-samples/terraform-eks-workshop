---
title: "Terraform files explanation"
date: 2018-09-18T16:01:14-05:00
weight: 576
---

### Terraform files and explanation

### backend-eks-cidr.tf, vars-dynamodb.tf, vars-main.tf, remote-cluster.tf & remote-net.tf

These first five files have been pre-created from the gen-backend.sh script in the tf-setup stage and have been described in previous sections.

----

### data-eks-cluster.tf	& data-subnet-i.tf

These populate terraform data resources with the EKS cluster name and the 3 subnets used for the 100.64.x.x secondary CIDR addresses in the EKS VPC

{{%expand "Expand here to see the code" %}}
```bash
data "aws_eks_cluster" "eks_cluster" {
  name = data.terraform_remote_state.cluster.outputs.cluster-name
}
```

```bash
data "aws_subnet" "i1" {
  vpc_id=data.terraform_remote_state.net.outputs.eks-vpc
    filter {
    name   = "tag:workshop"
    values = ["subnet-i1"]
  }
}

data "aws_subnet" "i2" {
  vpc_id=data.terraform_remote_state.net.outputs.eks-vpc
    filter {
    name   = "tag:workshop"
    values = ["subnet-i2"]
  }
}


data "aws_subnet" "i3" {
  vpc_id=data.terraform_remote_state.net.outputs.eks-vpc
  filter {
    name   = "tag:workshop"
    values = ["subnet-i3"]
  }
}
```

{{%/expand%}}

---


### null_cidr.tf

This starts the cni-cycle-nodes.sh and annotate-nodes.sh scripts
Note within how various parameters are populated from Terraform data resources **az1=$(echo ${data.aws_subnet.i1.availability_zone})**


{{%expand "Expand here to see the code" %}}

```bash
resource "null_resource" "cidr" {
triggers = {
    always_run = timestamp()
}
provisioner "local-exec" {
    on_failure  = fail
    when = create
    interpreter = ["/bin/bash", "-c"]
    command     = <<EOT
        az1=$(echo ${data.aws_subnet.i1.availability_zone})
        az2=$(echo ${data.aws_subnet.i2.availability_zone})
        az3=$(echo ${data.aws_subnet.i3.availability_zone})
        sub1=$(echo ${data.aws_subnet.i1.id})
        sub2=$(echo ${data.aws_subnet.i2.id})
        sub3=$(echo ${data.aws_subnet.i3.id})
        cn=$(echo ${data.aws_eks_cluster.eks_cluster.name})
        echo $az1 $az2 $az3 $sub1 $sub2 $sub3 $cn
        echo -e "\x1B[35mCycle nodes for custom CNI setting (takes a few minutes) ......\x1B[0m"
        ./cni-cycle-nodes.sh $cn
        echo -e "\x1B[33mAnnotate nodes ......\x1B[0m"
        ./annotate-nodes.sh $az1 $az2 $az3 $sub1 $sub2 $sub3 $cn
        echo -e "\x1B[32mShould see coredns on 100.64.x.y addresses ......\x1B[0m"
        echo -e "\x1B[32mkubectl get pods -A -o wide | grep coredns\x1B[0m"   
     EOT
}
}

```
{{% /expand %}}

---

### cni-cycle-nodes.sh

This script enables the custom networking option in the AWS CNI and then cycles each of our worker nodes in turn.

{{%expand "Expand here to see the code" %}}
```bash
test -n "$1" && echo CLUSTER is "$1" || "echo CLUSTER is not set && exit"
CLUSTER=$(echo $1)
# set custom networking for the CNI
kubectl set env ds aws-node -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
# quick look to see if it's now set
kubectl describe daemonset aws-node -n kube-system | grep -A5 Environment | grep CUSTOM
# Get a list of all the instances in the node group
INSTANCE_IDS=(`aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' --filters "Name=tag-key,Values=eks:nodegroup-name" "Name=instance-state-name,Values=running" "Name=tag-value,Values=ng1-mycluster1" --output text` )
target=$(kubectl get nodes | grep Read | wc -l)
# iterate through nodes - terminate one at a time
for i in "${INSTANCE_IDS[@]}"
do
curr=0
echo "Terminating EC2 instance $i ... "
aws ec2 terminate-instances --instance-ids $i | jq -r .TerminatingInstances[0].CurrentState.Name
while [ $curr -ne $target ]; do
    stat=$(aws ec2 describe-instance-status --instance-ids $i  --include-all-instances | jq -r .InstanceStatuses[0].InstanceState.Name)
    
    if [ "$stat" == "terminated" ]; then
        sleep 15
        curr=$(kubectl get nodes | grep -v NotReady | grep Read | wc -l)
        kubectl get nodes
        echo "Current Ready nodes = $curr of $target"
    fi
    if [ "$stat" != "terminated" ]; then
        sleep 10
        echo "$i $stat"
    fi
done
done
echo "done"
```

{{%/expand%}}

---

### annotate-nodes.sh

This script:

* Constructs Custom Resource Definition configuration files with the correct security groups and subnets for each AWS Availability Zone .
* Apply the above configuration.
* Annotates each worker node in the node group with an annotation to link to the correct configuration.

{{%expand "Expand here to see the code" %}}
```bash
test -n "$7" && echo CLUSTER is "$7" || "echo CLUSTER is not set && exit"
zone1=$(echo $1)
zone2=$(echo $2)
zone3=$(echo $3)
sub1=$(echo $4)
sub2=$(echo $5)
sub3=$(echo $6)
CLUSTER=$(echo $7)
kubectl get crd
# get the SG's
# get a list of the instances in the node group
INSTANCE_IDS=(`aws ec2 describe-instances --query 'Reservations[*].Instances[*].InstanceId' --filters "Name=tag-key,Values=eks:nodegroup-name" "Name=tag-value,Values=ng1-mycluster1" "Name=instance-state-name,Values=running" --output text`)
# extract the security groups
for i in "${INSTANCE_IDS[0]}"
do
echo "Descr EC2 instance $i ..."
sg0=`aws ec2 describe-instances --instance-ids $i | jq -r '.Reservations[].Instances[].SecurityGroups[0].GroupId'`
sg1=`aws ec2 describe-instances --instance-ids $i | jq -r '.Reservations[].Instances[].SecurityGroups[1].GroupId'`
done
echo "subnet $sub1 zone $zone1"
echo "subnet $sub2 zone $zone2"
echo "subnet $sub3 zone $zone3"

# Create the CRD config files - mapping the right security groups, subnets for the zone
echo ${zone1}
cat << EOF > ${zone1}-pod-netconfig.yaml
apiVersion: crd.k8s.amazonaws.com/v1alpha1
kind: ENIConfig
metadata:
 name: ${zone1}-pod-netconfig
spec:
 subnet: ${sub1}
 securityGroups:
 - ${sg0}
EOF
echo "cat ${zone1}-pod-netconfig.yaml"
cat ${zone1}-pod-netconfig.yaml
#

echo ${zone2}
cat << EOF > ${zone2}-pod-netconfig.yaml
apiVersion: crd.k8s.amazonaws.com/v1alpha1
kind: ENIConfig
metadata:
 name: ${zone2}-pod-netconfig
spec:
 subnet: ${sub2}
 securityGroups:
 - ${sg0}
EOF

echo "cat ${zone2}-pod-netconfig.yaml"
cat ${zone2}-pod-netconfig.yaml
#
echo ${zone3}
cat << EOF > ${zone3}-pod-netconfig.yaml
apiVersion: crd.k8s.amazonaws.com/v1alpha1
kind: ENIConfig
metadata:
 name: ${zone3}-pod-netconfig
spec:
 subnet: ${sub3}
 securityGroups:
 - ${sg0}
EOF
echo "cat ${zone3}-pod-netconfig.yaml"
cat ${zone3}-pod-netconfig.yaml

# Apply the CRD config
echo "apply the CRD ${zone1}"
kubectl apply -f ${zone1}-pod-netconfig.yaml
echo "apply the CRD ${zone2}"
kubectl apply -f ${zone2}-pod-netconfig.yaml
echo "apply the CRD ${zone3}"
kubectl apply -f ${zone3}-pod-netconfig.yaml
# get all the nodes
allnodes=`kubectl get node --selector='eks.amazonaws.com/nodegroup==ng1-mycluster1' -o json`
len=`kubectl get node --selector='eks.amazonaws.com/nodegroup==ng1-mycluster1' -o json | jq '.items | length-1'`
# iterate through the nodes and apply the annotation - so the eniConfig can match
for i in `seq 0 $len`; do
nn=`echo $allnodes | jq ".items[(${i})].metadata.name" | tr -d '"'`
nz=`echo $allnodes | jq ".items[(${i})].metadata.labels" | grep failure | grep zone | cut -f2 -d':' | tr -d ' ' | tr -d ','| tr -d '"'`
echo $nn $nz $nr
echo "kubectl annotate node ${nn} k8s.amazonaws.com/eniConfig=${nz}-pod-netconfig"
kubectl annotate node ${nn} k8s.amazonaws.com/eniConfig=${nz}-pod-netconfig
done
```

{{%/expand%}}

---

