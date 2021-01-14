---
title: "Deploy the sample app to EKS using CICD"
date: 2018-09-18T16:01:14-05:00
weight: 593
---

In this challenge you will deploy a sample application using CodeCommit, CodePipeline & CodeBuild

```bash
cd ~/environment/tfekscode/sampleapp
```

Create a service credential to use with our CodeCommit git repo:

```bash
usercred=$(aws iam create-service-specific-credential --user-name git-user --service-name codecommit.amazonaws.com)
GIT_USERNAME=$(echo $usercred | jq -r '.ServiceSpecificCredential.ServiceUserName')
GIT_PASSWORD=$(echo $usercred | jq -r '.ServiceSpecificCredential.ServicePassword')
CREDENTIAL_ID=$(echo $usercred| jq -r '.ServiceSpecificCredential.ServiceSpecificCredentialId')
test -n "$GIT_USERNAME" && echo GIT_USERNAME is "$GIT_USERNAME" || "echo GIT_USERNAME is not set"

```

Clone the (empty) repo:

```bash
test -n "$AWS_REGION" && echo AWS_REGION is "$AWS_REGION" || "echo AWS_REGION is not set"
git clone codecommit::$AWS_REGION://eksworkshop-app
```

{{< output >}}
Cloning into 'eksworkshop-app'...

'Namespace' object has no attribute 'cli_binary_format'
warning: You appear to have cloned an empty repository.
{{< /output >}}

---

Populate with our source files - including the special file **buildspec.yaml** which has the steps CodeBuild will follow.



```bash
cd eksworkshop-app
cp ../buildspec.yml .
cp ../*.tf .
```

Add files, commit and push
```bash
git add --all
git commit -m "Initial commit."
git push
```
---

This should now trigger a few activities

Check you can see your code in CodeCommit - navigate to your repository in the console and confirm you can see the files:

![tf-state](/images/andyt/codecommit-1.png)

Next check if the CodePipeline is running - navigate to it in the console

![tf-state](/images/andyt/pipeline-1.png)

You can also link through to the CodeBuild project:

![tf-state](/images/andyt/codebuild-1.png)

And tail to logs of the build job (scroll the window or use the `Tail Logs` button):

![tf-state](/images/andyt/codebuild-2.png)

----


Check everything is running ?


```
kubectl get pods,svc,deployment -n game-2048 -o wide
```
```
NAME                                   READY   STATUS    RESTARTS   AGE   IP              NODE                                       NOMINATED NODE   READINESS GATES
pod/deployment-2048-76d4bff958-5w94k   1/1     Running   0          55s   100.64.143.56   ip-10-0-3-166.eu-west-1.compute.internal   <none>           <none>
pod/deployment-2048-76d4bff958-r4jhb   1/1     Running   0          55s   100.64.24.3     ip-10-0-1-228.eu-west-1.compute.internal   <none>           <none>

NAME                   TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE   SELECTOR
service/service-2048   NodePort   172.20.162.86   <none>        80:32624/TCP   20s   app.kubernetes.io/name=app-2048

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                                                    SELECTOR
deployment.apps/deployment-2048   2/2     2            2           55s   app-2048     123456789012.dkr.ecr.eu-west-1.amazonaws.com/sample-app   app.kubernetes.io/name=app-2048

```

Note that

* The pods are depoyed to a 110.64 address
* The service is exposing port 80
* The deployment is referencing a private ECR repository beonging to your account




Enable port forwarding so we can see the application in out Cloud9 IDE

```
kubectl port-forward service/service-2048 8080:80 -n game-2048
```
```
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080

```

Preview the running (port-forwarded service) application from the cloud 9 IDE

Preview -> Preview Running Application
![tf-state](/images/andyt/game-2048-0.jpg)

You should then see the app running in the browser 

![tf-state](/images/andyt/game-2048-1.jpg)

----


Check the Load Balancer & Ingress in the same way as described in the previous section.

----


## Cleanup

Interrupt the port forwarding with ctrl-c if necessary.


```bash
terraform destroy -auto-approve
```
