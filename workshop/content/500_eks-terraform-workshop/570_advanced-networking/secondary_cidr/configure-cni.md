---
title: "Configure the AWS CNI"
date: 2019-02-13T01:12:49-05:00
weight: 573
---

We will use Terraform to start two scripts via a null_resource definition to configure our nodegroup to use the secondary CIDR for POD networking:

```bash
cd ~/environment/tfekscode/eks-cidr
```

```bash
terraform init
```

Validate the Terraform code
```
terraform validate
```

----

Plan the deployment:
```
terraform plan -out tfplan
```
{{< output >}}
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

data.terraform_remote_state.cluster: Refreshing state...
data.terraform_remote_state.net: Refreshing state...
data.aws_subnet.i1: Refreshing state...
data.aws_subnet.i2: Refreshing state...
data.aws_subnet.i3: Refreshing state...
data.aws_eks_cluster.eks_cluster: Refreshing state...
data.aws_vpc.vpc-cicd: Refreshing state...

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # null_resource.cidr will be created
  + resource "null_resource" "cidr" {
      + id       = (known after apply)
      + triggers = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"

{{< /output >}}

----


## Build the envornment


This step will take several minutes -  the null_resource starts two scripts:


### 1. cni-cycle-nodes.sh

This configures the aws-node daemon set (AWS's Container Network Interface) to allow custom network configurations:

```bash
kubectl set env ds aws-node -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
```

and then has a loop to terminate (& restart via the Auto-scaling group) each node in the nodegroup ng1-mycluster1 one at a time. By doing this:

* New ENI interfaces are attached to the restarted instances - each with the customised CNI option enabled. 



### 2. annotate-nodes.sh

This script generates and applys a per zone configuration for the ENIConfig Custom Resource Definition and then annotates the appropriate node in the nodegroup ng1-mycluster1.



```
terraform apply tfplan
```

{{< output >}}
null_resource.cidr: Creating...
null_resource.cidr: Provisioning with 'local-exec'...
null_resource.cidr (local-exec): Executing: ["/bin/bash" "-c" "        az1=$(echo eu-west-1a)\n        az2=$(echo eu-west-1b)\n        az3=$(echo eu-west-1c)\n        sub1=$(echo subnet-05862b700dff60406)\n        sub2=$(echo subnet-055c0cf19b9081857)\n        sub3=$(echo subnet-0d7889e500b5d8468)\n        cn=$(echo mycluster1)\n        echo $az1 $az2 $az3 $sub1 $sub2 $sub3 $cn\n        echo -e \"\\x1B[35mCycle nodes for custom CNI setting (takes a few minutes) ......\\x1B[0m\"\n        ./cni-cycle-nodes.sh $cn\n        echo -e \"\\x1B[33mAnnotate nodes ......\\x1B[0m\"\n        ./annotate-nodes.sh $az1 $az2 $az3 $sub1 $sub2 $sub3 $cn\n        echo -e \"\\x1B[32mShould see coredns on 100.64.x.y addresses ......\\x1B[0m\"\n        echo -e \"\\x1B[32mkubectl get pods -A -o wide | grep coredns\\x1B[0m\"   \n"]
null_resource.cidr (local-exec): eu-west-1a eu-west-1b eu-west-1c subnet-05862b700dff60406 subnet-055c0cf19b9081857 subnet-0d7889e500b5d8468 mycluster1
null_resource.cidr (local-exec): Cycle nodes for custom CNI setting (takes a few minutes) ......
null_resource.cidr (local-exec): CLUSTER is mycluster1
null_resource.cidr (local-exec): daemonset.apps/aws-node env updated
null_resource.cidr (local-exec):       AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG:  true
null_resource.cidr (local-exec): Terminating EC2 instance i-0b622859aba7974f5 ...
null_resource.cidr (local-exec): shutting-down
null_resource.cidr: Still creating... [10s elapsed]
null_resource.cidr (local-exec): i-0b622859aba7974f5 shutting-down
null_resource.cidr: Still creating... [20s elapsed]
null_resource.cidr (local-exec): i-0b622859aba7974f5 shutting-down
null_resource.cidr: Still creating... [30s elapsed]
null_resource.cidr (local-exec): i-0b622859aba7974f5 shutting-down
null_resource.cidr: Still creating... [40s elapsed]
null_resource.cidr: Still creating... [50s elapsed]
null_resource.cidr (local-exec): NAME                                       STATUS   ROLES    AGE   VERSION
null_resource.cidr (local-exec): ip-10-0-1-110.eu-west-1.compute.internal   Ready    <none>   16m   v1.17.12-eks-7684af
null_resource.cidr (local-exec): Current Ready nodes = 1 of 2
null_resource.cidr: Still creating... [1m0s elapsed]
null_resource.cidr: Still creating... [1m10s elapsed]
null_resource.cidr (local-exec): NAME                                       STATUS   ROLES    AGE   VERSION
null_resource.cidr (local-exec): ip-10-0-1-110.eu-west-1.compute.internal   Ready    <none>   16m   v1.17.12-eks-7684af
null_resource.cidr (local-exec): Current Ready nodes = 1 of 2
null_resource.cidr: Still creating... [1m20s elapsed]

** OUTPUT TRUNCATED FOR BREVITY **

null_resource.cidr (local-exec): NAME                                       STATUS   ROLES    AGE   VERSION
null_resource.cidr (local-exec): ip-10-0-1-110.eu-west-1.compute.internal   Ready    <none>   18m   v1.17.12-eks-7684af
null_resource.cidr (local-exec): Current Ready nodes = 1 of 2
null_resource.cidr: Still creating... [2m40s elapsed]
null_resource.cidr: Still creating... [2m50s elapsed]
null_resource.cidr (local-exec): NAME                                       STATUS   ROLES    AGE   VERSION
null_resource.cidr (local-exec): ip-10-0-1-110.eu-west-1.compute.internal   Ready    <none>   18m   v1.17.12-eks-7684af
null_resource.cidr (local-exec): Current Ready nodes = 1 of 2
null_resource.cidr: Still creating... [3m0s elapsed]
null_resource.cidr: Still creating... [3m10s elapsed]

** OUTPUT TRUNCATED FOR BREVITY **

null_resource.cidr (local-exec): NAME                                       STATUS     ROLES    AGE   VERSION
null_resource.cidr (local-exec): ip-10-0-1-110.eu-west-1.compute.internal   Ready      <none>   18m   v1.17.12-eks-7684af
null_resource.cidr (local-exec): ip-10-0-3-166.eu-west-1.compute.internal   NotReady   <none>   21s   v1.17.12-eks-7684af
null_resource.cidr (local-exec): Current Ready nodes = 1 of 2
null_resource.cidr: Still creating... [3m40s elapsed]
null_resource.cidr (local-exec): NAME                                       STATUS   ROLES    AGE   VERSION
null_resource.cidr (local-exec): ip-10-0-1-110.eu-west-1.compute.internal   Ready    <none>   19m   v1.17.12-eks-7684af
null_resource.cidr (local-exec): ip-10-0-3-166.eu-west-1.compute.internal   Ready    <none>   39s   v1.17.12-eks-7684af
null_resource.cidr (local-exec): Current Ready nodes = 2 of 2
null_resource.cidr (local-exec): Terminating EC2 instance i-00b3b08b7090ee943 ...
null_resource.cidr (local-exec): shutting-down
null_resource.cidr: Still creating... [3m50s elapsed]
null_resource.cidr (local-exec): i-00b3b08b7090ee943 shutting-down
null_resource.cidr: Still creating... [4m0s elapsed]

** OUTPUT TRUNCATED FOR BREVITY **

null_resource.cidr (local-exec): i-00b3b08b7090ee943 shutting-down
null_resource.cidr: Still creating... [5m0s elapsed]
null_resource.cidr: Still creating... [5m10s elapsed]
null_resource.cidr (local-exec): NAME                                       STATUS     ROLES    AGE    VERSION
null_resource.cidr (local-exec): ip-10-0-1-228.eu-west-1.compute.internal   NotReady   <none>   5s     v1.17.12-eks-7684af
null_resource.cidr (local-exec): ip-10-0-3-166.eu-west-1.compute.internal   Ready      <none>   2m3s   v1.17.12-eks-7684af
null_resource.cidr (local-exec): Current Ready nodes = 1 of 2
null_resource.cidr: Still creating... [5m20s elapsed]

** OUTPUT TRUNCATED FOR BREVITY **

null_resource.cidr (local-exec): NAME                                       STATUS   ROLES    AGE     VERSION
null_resource.cidr (local-exec): ip-10-0-1-228.eu-west-1.compute.internal   Ready    <none>   39s     v1.17.12-eks-7684af
null_resource.cidr (local-exec): ip-10-0-3-166.eu-west-1.compute.internal   Ready    <none>   2m37s   v1.17.12-eks-7684af
null_resource.cidr (local-exec): Current Ready nodes = 2 of 2
null_resource.cidr (local-exec): done
null_resource.cidr (local-exec): Annotate nodes ......
null_resource.cidr (local-exec): CLUSTER is mycluster1
null_resource.cidr (local-exec): NAME                                         CREATED AT
null_resource.cidr (local-exec): eniconfigs.crd.k8s.amazonaws.com             2020-12-10T16:08:14Z
null_resource.cidr (local-exec): securitygrouppolicies.vpcresources.k8s.aws   2020-12-10T16:08:18Z
null_resource.cidr (local-exec): Descr EC2 instance i-0a2c0985030bb2c5d ...
null_resource.cidr (local-exec): subnet subnet-05862b700dff60406 zone eu-west-1a
null_resource.cidr (local-exec): subnet subnet-055c0cf19b9081857 zone eu-west-1b
null_resource.cidr (local-exec): subnet subnet-0d7889e500b5d8468 zone eu-west-1c
null_resource.cidr (local-exec): eu-west-1a
null_resource.cidr (local-exec): cat eu-west-1a-pod-netconfig.yaml
null_resource.cidr (local-exec): apiVersion: crd.k8s.amazonaws.com/v1alpha1
null_resource.cidr (local-exec): kind: ENIConfig
null_resource.cidr (local-exec): metadata:
null_resource.cidr (local-exec):  name: eu-west-1a-pod-netconfig
null_resource.cidr (local-exec): spec:
null_resource.cidr (local-exec):  subnet: subnet-05862b700dff60406
null_resource.cidr (local-exec):  securityGroups:
null_resource.cidr (local-exec):  - sg-09ab0e693218b3c7f
null_resource.cidr (local-exec): eu-west-1b
null_resource.cidr (local-exec): cat eu-west-1b-pod-netconfig.yaml
null_resource.cidr (local-exec): apiVersion: crd.k8s.amazonaws.com/v1alpha1
null_resource.cidr (local-exec): kind: ENIConfig
null_resource.cidr (local-exec): metadata:
null_resource.cidr (local-exec):  name: eu-west-1b-pod-netconfig
null_resource.cidr (local-exec): spec:
null_resource.cidr (local-exec):  subnet: subnet-055c0cf19b9081857
null_resource.cidr (local-exec):  securityGroups:
null_resource.cidr (local-exec):  - sg-09ab0e693218b3c7f
null_resource.cidr (local-exec): eu-west-1c
null_resource.cidr (local-exec): cat eu-west-1c-pod-netconfig.yaml
null_resource.cidr (local-exec): apiVersion: crd.k8s.amazonaws.com/v1alpha1
null_resource.cidr (local-exec): kind: ENIConfig
null_resource.cidr (local-exec): metadata:
null_resource.cidr (local-exec):  name: eu-west-1c-pod-netconfig
null_resource.cidr (local-exec): spec:
null_resource.cidr (local-exec):  subnet: subnet-0d7889e500b5d8468
null_resource.cidr (local-exec):  securityGroups:
null_resource.cidr (local-exec):  - sg-09ab0e693218b3c7f
null_resource.cidr (local-exec): apply the CRD eu-west-1a
null_resource.cidr: Still creating... [5m50s elapsed]
null_resource.cidr (local-exec): eniconfig.crd.k8s.amazonaws.com/eu-west-1a-pod-netconfig created
null_resource.cidr (local-exec): apply the CRD eu-west-1b
null_resource.cidr (local-exec): eniconfig.crd.k8s.amazonaws.com/eu-west-1b-pod-netconfig created
null_resource.cidr (local-exec): apply the CRD eu-west-1c
null_resource.cidr (local-exec): eniconfig.crd.k8s.amazonaws.com/eu-west-1c-pod-netconfig created
null_resource.cidr (local-exec): ip-10-0-1-228.eu-west-1.compute.internal eu-west-1a
null_resource.cidr (local-exec): kubectl annotate node ip-10-0-1-228.eu-west-1.compute.internal k8s.amazonaws.com/eniConfig=eu-west-1a-pod-netconfig
null_resource.cidr (local-exec): node/ip-10-0-1-228.eu-west-1.compute.internal annotated
null_resource.cidr (local-exec): ip-10-0-3-166.eu-west-1.compute.internal eu-west-1c
null_resource.cidr (local-exec): kubectl annotate node ip-10-0-3-166.eu-west-1.compute.internal k8s.amazonaws.com/eniConfig=eu-west-1c-pod-netconfig
null_resource.cidr (local-exec): node/ip-10-0-3-166.eu-west-1.compute.internal annotated
null_resource.cidr (local-exec): Should see coredns on 100.64.x.y addresses ......
null_resource.cidr (local-exec): kubectl get pods -A -o wide | grep coredns
null_resource.cidr: Creation complete after 5m56s [id=5700399192786917411]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

{{< /output >}}


----

After waiting for a minute you should see the coredns PODS running on 100.64.x.x addresses in the "IP" column output of this command:

```
kubectl get pods -A -o wide
```

{{< output >}}
NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE     IP              NODE                                       NOMINATED NODE   READINESS GATES
kube-system   aws-node-flx5q             1/1     Running   0          7m52s   10.0.3.166      ip-10-0-3-166.eu-west-1.compute.internal   <none>           <none>
kube-system   aws-node-pvqqg             1/1     Running   0          5m54s   10.0.1.228      ip-10-0-1-228.eu-west-1.compute.internal   <none>           <none>
kube-system   coredns-6987776bbd-g6hwz   1/1     Running   0          6m42s   100.64.130.99   ip-10-0-3-166.eu-west-1.compute.internal   <none>           <none>
kube-system   coredns-6987776bbd-lkd54   1/1     Running   0          6m42s   100.64.141.65   ip-10-0-3-166.eu-west-1.compute.internal   <none>           <none>
kube-system   kube-proxy-k72dq           1/1     Running   0          5m54s   10.0.1.228      ip-10-0-1-228.eu-west-1.compute.internal   <none>           <none>
kube-system   kube-proxy-q4sqw           1/1     Running   0          7m52s   10.0.3.166      ip-10-0-3-166.eu-west-1.compute.internal   <none>           <none>
{{< /output >}}