---
title: "Deploy the sample app to EKS using the CLI"
date: 2018-09-18T16:01:14-05:00
weight: 581
---


In this chapter you will deploy a sample application using Terraform.

The biggest benefit when using Terraform to maintain Kubernetes resources is integration into the Terraform plan/apply life-cycle. So you can review planned changes before applying them. 

Also, using kubectl, purging of resources from the cluster is not trivial without manual intervention. Terraform does this reliably.

For a discussion of other benefits see [here:](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/guides/getting-started)

---

```bash
cd ~/environment/tfekscode/sampleapp
```

Initialize Terraform:

```bash
terraform init
```

Plan the deployment:

```bash
terraform plan -out tfplan
```

{{< output >}}

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # kubernetes_deployment.game-2048__deployment-2048 will be created
  + resource "kubernetes_deployment" "game-2048__deployment-2048" {
      + id               = (known after apply)
      + wait_for_rollout = true

      + metadata {
          + generation       = (known after apply)
          + name             = "deployment-2048"
          + namespace        = "game-2048"
          + resource_version = (known after apply)
          + self_link        = (known after apply)
          + uid              = (known after apply)
        }

      + spec {
          + min_ready_seconds         = 0
          + paused                    = false
          + progress_deadline_seconds = 600
          + replicas                  = 4
          + revision_history_limit    = 10

          + selector {
              + match_labels = {
                  + "app.kubernetes.io/name" = "app-2048"
                }
            }

          + strategy {
              + type = "RollingUpdate"

              + rolling_update {
                  + max_surge       = "25%"
                  + max_unavailable = "25%"
                }
            }

          + template {
              + metadata {
                  + generation       = (known after apply)
                  + labels           = {
                      + "app.kubernetes.io/name" = "app-2048"
                    }
                  + name             = (known after apply)
                  + resource_version = (known after apply)
                  + self_link        = (known after apply)
                  + uid              = (known after apply)
                }

              + spec {
                  + dns_policy                       = "ClusterFirst"
                  + enable_service_links             = true
                  + host_ipc                         = false
                  + host_network                     = false
                  + host_pid                         = false
                  + hostname                         = (known after apply)
                  + node_name                        = (known after apply)
                  + node_selector                    = {
                      + "alpha.eksctl.io/nodegroup-name" = "ng1-mycluster1"
                    }
                  + restart_policy                   = "Always"
                  + service_account_name             = (known after apply)
                  + share_process_namespace          = false
                  + termination_grace_period_seconds = 30

                  + container {
                      + image                      = "984587260948.dkr.ecr.eu-west-1.amazonaws.com/sample-app"
                      + image_pull_policy          = "Always"
                      + name                       = "app-2048"
                      + stdin                      = false
                      + stdin_once                 = false
                      + termination_message_path   = "/dev/termination-log"
                      + termination_message_policy = (known after apply)
                      + tty                        = false

                      + port {
                          + container_port = 80
                          + host_port      = 0
                          + protocol       = "TCP"
                        }

                      + resources {
                          + limits {
                              + cpu    = (known after apply)
                              + memory = (known after apply)
                            }

                          + requests {
                              + cpu    = (known after apply)
                              + memory = (known after apply)
                            }
                        }

                      + volume_mount {
                          + mount_path        = (known after apply)
                          + mount_propagation = (known after apply)
                          + name              = (known after apply)
                          + read_only         = (known after apply)
                          + sub_path          = (known after apply)
                        }
                    }

                  + image_pull_secrets {
                      + name = (known after apply)
                    }

                  + volume {
                      + name = (known after apply)

                      + aws_elastic_block_store {
                          + fs_type   = (known after apply)
                          + partition = (known after apply)
                          + read_only = (known after apply)
                          + volume_id = (known after apply)
                        }

                      + azure_disk {
                          + caching_mode  = (known after apply)
                          + data_disk_uri = (known after apply)
                          + disk_name     = (known after apply)
                          + fs_type       = (known after apply)
                          + kind          = (known after apply)
                          + read_only     = (known after apply)
                        }

                      + azure_file {
                          + read_only   = (known after apply)
                          + secret_name = (known after apply)
                          + share_name  = (known after apply)
                        }

                      + ceph_fs {
                          + monitors    = (known after apply)
                          + path        = (known after apply)
                          + read_only   = (known after apply)
                          + secret_file = (known after apply)
                          + user        = (known after apply)

                          + secret_ref {
                              + name      = (known after apply)
                              + namespace = (known after apply)
                            }
                        }

                      + cinder {
                          + fs_type   = (known after apply)
                          + read_only = (known after apply)
                          + volume_id = (known after apply)
                        }

                      + config_map {
                          + default_mode = (known after apply)
                          + name         = (known after apply)
                          + optional     = (known after apply)

                          + items {
                              + key  = (known after apply)
                              + mode = (known after apply)
                              + path = (known after apply)
                            }
                        }

                      + csi {
                          + driver            = (known after apply)
                          + fs_type           = (known after apply)
                          + read_only         = (known after apply)
                          + volume_attributes = (known after apply)
                          + volume_handle     = (known after apply)

                          + controller_expand_secret_ref {
                              + name      = (known after apply)
                              + namespace = (known after apply)
                            }

                          + controller_publish_secret_ref {
                              + name      = (known after apply)
                              + namespace = (known after apply)
                            }

                          + node_publish_secret_ref {
                              + name      = (known after apply)
                              + namespace = (known after apply)
                            }

                          + node_stage_secret_ref {
                              + name      = (known after apply)
                              + namespace = (known after apply)
                            }
                        }

                      + downward_api {
                          + default_mode = (known after apply)

                          + items {
                              + mode = (known after apply)
                              + path = (known after apply)

                              + field_ref {
                                  + api_version = (known after apply)
                                  + field_path  = (known after apply)
                                }

                              + resource_field_ref {
                                  + container_name = (known after apply)
                                  + quantity       = (known after apply)
                                  + resource       = (known after apply)
                                }
                            }
                        }

                      + empty_dir {
                          + medium     = (known after apply)
                          + size_limit = (known after apply)
                        }

                      + fc {
                          + fs_type      = (known after apply)
                          + lun          = (known after apply)
                          + read_only    = (known after apply)
                          + target_ww_ns = (known after apply)
                        }

                      + flex_volume {
                          + driver    = (known after apply)
                          + fs_type   = (known after apply)
                          + options   = (known after apply)
                          + read_only = (known after apply)

                          + secret_ref {
                              + name      = (known after apply)
                              + namespace = (known after apply)
                            }
                        }

                      + flocker {
                          + dataset_name = (known after apply)
                          + dataset_uuid = (known after apply)
                        }

                      + gce_persistent_disk {
                          + fs_type   = (known after apply)
                          + partition = (known after apply)
                          + pd_name   = (known after apply)
                          + read_only = (known after apply)
                        }

                      + git_repo {
                          + directory  = (known after apply)
                          + repository = (known after apply)
                          + revision   = (known after apply)
                        }

                      + glusterfs {
                          + endpoints_name = (known after apply)
                          + path           = (known after apply)
                          + read_only      = (known after apply)
                        }

                      + host_path {
                          + path = (known after apply)
                          + type = (known after apply)
                        }

                      + iscsi {
                          + fs_type         = (known after apply)
                          + iqn             = (known after apply)
                          + iscsi_interface = (known after apply)
                          + lun             = (known after apply)
                          + read_only       = (known after apply)
                          + target_portal   = (known after apply)
                        }

                      + local {
                          + path = (known after apply)
                        }

                      + nfs {
                          + path      = (known after apply)
                          + read_only = (known after apply)
                          + server    = (known after apply)
                        }

                      + persistent_volume_claim {
                          + claim_name = (known after apply)
                          + read_only  = (known after apply)
                        }

                      + photon_persistent_disk {
                          + fs_type = (known after apply)
                          + pd_id   = (known after apply)
                        }

                      + projected {
                          + default_mode = (known after apply)

                          + sources {
                              + config_map {
                                  + name     = (known after apply)
                                  + optional = (known after apply)

                                  + items {
                                      + key  = (known after apply)
                                      + mode = (known after apply)
                                      + path = (known after apply)
                                    }
                                }

                              + downward_api {
                                  + items {
                                      + mode = (known after apply)
                                      + path = (known after apply)

                                      + field_ref {
                                          + api_version = (known after apply)
                                          + field_path  = (known after apply)
                                        }

                                      + resource_field_ref {
                                          + container_name = (known after apply)
                                          + quantity       = (known after apply)
                                          + resource       = (known after apply)
                                        }
                                    }
                                }

                              + secret {
                                  + name     = (known after apply)
                                  + optional = (known after apply)

                                  + items {
                                      + key  = (known after apply)
                                      + mode = (known after apply)
                                      + path = (known after apply)
                                    }
                                }

                              + service_account_token {
                                  + audience           = (known after apply)
                                  + expiration_seconds = (known after apply)
                                  + path               = (known after apply)
                                }
                            }
                        }

                      + quobyte {
                          + group     = (known after apply)
                          + read_only = (known after apply)
                          + registry  = (known after apply)
                          + user      = (known after apply)
                          + volume    = (known after apply)
                        }

                      + rbd {
                          + ceph_monitors = (known after apply)
                          + fs_type       = (known after apply)
                          + keyring       = (known after apply)
                          + rados_user    = (known after apply)
                          + rbd_image     = (known after apply)
                          + rbd_pool      = (known after apply)
                          + read_only     = (known after apply)

                          + secret_ref {
                              + name      = (known after apply)
                              + namespace = (known after apply)
                            }
                        }

                      + secret {
                          + default_mode = (known after apply)
                          + optional     = (known after apply)
                          + secret_name  = (known after apply)

                          + items {
                              + key  = (known after apply)
                              + mode = (known after apply)
                              + path = (known after apply)
                            }
                        }

                      + vsphere_volume {
                          + fs_type     = (known after apply)
                          + volume_path = (known after apply)
                        }
                    }
                }
            }
        }
    }

  # kubernetes_ingress.game-2048__ingress-2048 will be created
  + resource "kubernetes_ingress" "game-2048__ingress-2048" {
      + id                     = (known after apply)
      + load_balancer_ingress  = (known after apply)
      + wait_for_load_balancer = false

      + metadata {
          + annotations      = {
              + "alb.ingress.kubernetes.io/listen-ports" = jsonencode(
                    [
                      + {
                          + HTTP = 8080
                        },
                    ]
                )
              + "alb.ingress.kubernetes.io/scheme"       = "internal"
              + "alb.ingress.kubernetes.io/target-type"  = "ip"
              + "kubernetes.io/ingress.class"            = "alb"
            }
          + generation       = (known after apply)
          + name             = "ingress-2048"
          + namespace        = "game-2048"
          + resource_version = (known after apply)
          + self_link        = (known after apply)
          + uid              = (known after apply)
        }

      + spec {

          + rule {
              + http {
                  + path {
                      + path = "/*"

                      + backend {
                          + service_name = "service-2048"
                          + service_port = "80"
                        }
                    }
                }
            }
        }
    }

  # kubernetes_namespace.game-2048 will be created
  + resource "kubernetes_namespace" "game-2048" {
      + id = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "game-2048"
          + resource_version = (known after apply)
          + self_link        = (known after apply)
          + uid              = (known after apply)
        }
    }

  # kubernetes_service.game-2048__service-2048 will be created
  + resource "kubernetes_service" "game-2048__service-2048" {
      + id                    = (known after apply)
      + load_balancer_ingress = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "service-2048"
          + namespace        = "game-2048"
          + resource_version = (known after apply)
          + self_link        = (known after apply)
          + uid              = (known after apply)
        }

      + spec {
          + cluster_ip                  = (known after apply)
          + external_traffic_policy     = (known after apply)
          + health_check_node_port      = (known after apply)
          + publish_not_ready_addresses = false
          + selector                    = {
              + "app.kubernetes.io/name" = "app-2048"
            }
          + session_affinity            = "None"
          + type                        = "NodePort"

          + port {
              + node_port   = (known after apply)
              + port        = 80
              + protocol    = "TCP"
              + target_port = "80"
            }
        }
    }

  # null_resource.cleanup will be created
  + resource "null_resource" "cleanup" {
      + id       = (known after apply)
      + triggers = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"
{{< /output >}}

Deploy the sample app:

```bash
terraform apply tfplan
```

{{< output >}}
null_resource.cleanup: Creating...
null_resource.cleanup: Creation complete after 0s [id=2365623716858908811]
kubernetes_ingress.game-2048__ingress-2048: Creating...
kubernetes_service.game-2048__service-2048: Creating...
kubernetes_namespace.game-2048: Creating...
kubernetes_namespace.game-2048: Creation complete after 1s [id=game-2048]
kubernetes_ingress.game-2048__ingress-2048: Creation complete after 1s [id=game-2048/ingress-2048]
kubernetes_service.game-2048__service-2048: Creation complete after 1s [id=game-2048/service-2048]
kubernetes_deployment.game-2048__deployment-2048: Creating...
kubernetes_deployment.game-2048__deployment-2048: Creation complete after 4s [id=game-2048/deployment-2048]

Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

The state of your infrastructure has been saved to the path
below. This state is required to modify and destroy your
infrastructure, so keep it safe. To inspect the complete state
use the `terraform show` command.

State path: terraform.tfstate
{{< /output >}}



Check everything is running ?

```bash
kubectl get pods,svc,deployment -n game-2048
```

{{< output >}}
NAMESPACE     NAME                                                READY   STATUS    RESTARTS   AGE
game-2048     pod/deployment-2048-d6457c6fb-6sx2x                 1/1     Running   0          52s
game-2048     pod/deployment-2048-d6457c6fb-gfgsd                 1/1     Running   0          52s
game-2048     pod/deployment-2048-d6457c6fb-q5n6c                 1/1     Running   0          52s
game-2048     pod/deployment-2048-d6457c6fb-vk6nv                 1/1     Running   0          52s

NAMESPACE     NAME                                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)         AGE
game-2048     service/service-2048                        NodePort    172.20.190.226   <none>        80:32360/TCP    52s

NAMESPACE     NAME                                           READY   UP-TO-DATE   AVAILABLE   AGE
game-2048     deployment.apps/deployment-2048                4/4     4            4           52s
{{< /output >}}

Note that:

* The pods are deployed to  100.64.x.x addresses
* The service is exposing port 80
* The deployment is referencing a private ECR repository belonging to your account


----

Enable port forwarding so we can see the application in out Cloud9 IDE:

```bash
kubectl port-forward service/service-2048 8080:80 -n game-2048
```

{{< output >}}
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
{{< /output >}}

Preview the running (port-forwarded service) application from the cloud 9 IDE"

`Preview` -> `Preview Running Application`
![tf-state](/images/andyt/game-2048-0.jpg)

You should then see the app running in the browser 

![tf-state](/images/andyt/game-2048-1.jpg)


Interrupt the port forwarding with **ctrl-C**

---


## Finding the Internal Load Balancer  <a id="load-balancer-find"></a>

As part of the build above we also deployed a Load Balancer.

The load balancer will take about 8 minutes to provision and come online

Check how long it has bene provisioning by using the command:

```bash
kubectl get ingress -n game-2048
```

{{< output >}}
NAME           CLASS    HOSTS   ADDRESS   PORTS   AGE
ingress-2048   <none>   *                 80      5m27s
{{< /output >}}

Watching the aws-load-balancer-controller - open another terminal and use this command to watch the logs:

```
kubectl logs `kubectl get pods -n kube-system | grep aws-load-balancer-controller | awk '{print $1}'` -n kube-system --follow
```


**After 8 minutes have elapsed**


Check the `targetbindings` have populated.
This is the new CRD type that was created as part of the load balancer controller installation.

```bash
kubectl get targetgroupbindings -A
```

{{< output >}}
NAMESPACE   NAME                               SERVICE-NAME   SERVICE-PORT   TARGET-TYPE   AGE
game-2048   k8s-game2048-service2-11af83fe8f   service-2048   80             ip            82s
{{< /output >}}

Then obtain the internal DNS name of the load balancer using and check valid HTML is returned with curl

```bash
ALB=$(aws elbv2 describe-load-balancers --query 'LoadBalancers[*].DNSName' | jq -r .[])
curl $ALB:8080
```


{{< output >}}
<!DOCTYPE html>`
<html>
<head>
  <meta charset="utf-8">
  <title>2048</title>

** Output truncated for brevity **

  <script src="js/application.js"></script>
</body>
</html>
{{< /output >}}

---


## Cleanup


Use terraform to delete our sample application:

```bash
terraform destroy -auto-approve
```

Note the namespace takes several minutes to delete as it waits for the ingress resource to be deleted.

{{< output >}}
null_resource.cleanup: Destroying... [id=9012327125218962041]
null_resource.cleanup: Provisioning with 'local-exec'...
null_resource.cleanup (local-exec): Executing: ["/bin/bash" "-c" "        echo \"remote git credentials &\" sample app\n        ./cleanup.sh\n        echo \"************************************************************************************\"\n"]
null_resource.cleanup (local-exec): remote git credentials & sample app
kubernetes_namespace.game-2048: Destroying... [id=game-2048]
kubernetes_service.game-2048__service-2048: Destroying... [id=game-2048/service-2048]
kubernetes_ingress.game-2048__ingress-2048: Destroying... [id=game-2048/ingress-2048]
kubernetes_deployment.game-2048__deployment-2048: Destroying... [id=game-2048/deployment-2048]
kubernetes_ingress.game-2048__ingress-2048: Destruction complete after 2s
kubernetes_service.game-2048__service-2048: Destruction complete after 2s
kubernetes_deployment.game-2048__deployment-2048: Destruction complete after 2s
null_resource.cleanup (local-exec): ************************************************************************************
null_resource.cleanup: Destruction complete after 3s
kubernetes_namespace.game-2048: Still destroying... [id=game-2048, 10s elapsed]
kubernetes_namespace.game-2048: Still destroying... [id=game-2048, 20s elapsed]

...

kubernetes_namespace.game-2048: Still destroying... [id=game-2048, 7m10s elapsed]
kubernetes_namespace.game-2048: Destruction complete after 7m15s

Destroy complete! Resources: 5 destroyed.
{{< /output >}}

---
