---
title: "Deploy the load balancer"
date: 2018-09-18T16:01:14-05:00
weight: 584
draft: true
---


## Set up the load balancer

[docs]https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/

```bash
kubectl apply -f 2048_ingresses.yml
```

## Finding the Internal Load Balancer

The load balancer will take about 8 minutes to provision and come online

Check how long it has bene provisioning by using the command:

```bash
kubectl get ingress -A
```

{{< output >}}
NAME           CLASS    HOSTS   ADDRESS   PORTS   AGE
ingress-2048   <none>   *                 80      5m27s
{{< /output >}}

**After 8 minutes have elapsed**

Obtain the internal DNS name of the load balancer using:

```bash
aws elbv2 describe-load-balancers --query 'LoadBalancers[*].DNSName' | jq -r .[]
```
{{< output >}}
internal-k8s-game2048-ingress2-37939b3b49-1011210476.eu-west-1.elb.amazonaws.com
{{< /output >}}

And check it is returning web page html content with curl:

```bash
curl internal-k8s-game2048-ingress2-37939b3b49-1011210476.eu-west-1.elb.amazonaws.com:8080/app1/index.html
```
{{< output >}}
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>2048</title>

** Output truncated for brevity **

{{< /output >}}

Repeat the above for the other path through the ingress:

```bash
curl internal-k8s-game2048-ingress2-37939b3b49-1011210476.eu-west-1.elb.amazonaws.com:8080/app2/index.html
```

---


## Cleanup

Interrupt the port forwarding with **ctrl-C**

Use the helper script to delete the app:
```
./delete-app.sh
```


---
