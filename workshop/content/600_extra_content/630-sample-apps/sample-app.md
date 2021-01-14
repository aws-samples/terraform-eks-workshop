---
title: "Deploy the sample app to two node groups"
date: 2018-09-18T16:01:14-05:00
weight: 583
---


In this chapter you will deploy two sample applications to separeate node groups 

```bash
cd ~/environment/tfekscode/extra/sampleapp2
```

Initialise Terraform - note in the output that the **kubernetes** provider is also installed
```bash
terraform init
```

{{< output >}}
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/kubernetes...
- Finding hashicorp/aws versions matching "~> 3.22"...
- Finding hashicorp/null versions matching "~> 3.0"...
- Finding hashicorp/external versions matching "~> 2.0"...
- Installing hashicorp/kubernetes v1.13.3...
- Installed hashicorp/kubernetes v1.13.3 (signed by HashiCorp)
- Installing hashicorp/aws v3.23.0...
- Installed hashicorp/aws v3.23.0 (signed by HashiCorp)
- Installing hashicorp/null v3.0.0...
- Installed hashicorp/null v3.0.0 (signed by HashiCorp)
- Installing hashicorp/external v2.0.0...
- Installed hashicorp/external v2.0.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
{{< /output >}}

---

```bash
terraform plan -out tfplan
```
{{< output >}}
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # kubernetes_deployment.game1-2048__deployment1-2048 will be created
  + resource "kubernetes_deployment" "game1-2048__deployment1-2048" {
      + id               = (known after apply)
      + wait_for_rollout = true

      + metadata {
          + generation       = (known after apply)
          + name             = "deployment1-2048"
          + namespace        = "game1-2048"
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
                  + "app.kubernetes.io/name" = "app1-2048"
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
                      + "app.kubernetes.io/name" = "app1-2048"
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
                      + name                       = "app1-2048"
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

  # kubernetes_deployment.game2-2048__deployment2-2048 will be created
  + resource "kubernetes_deployment" "game2-2048__deployment2-2048" {
      + id               = (known after apply)
      + wait_for_rollout = true

      + metadata {
          + generation       = (known after apply)
          + name             = "deployment2-2048"
          + namespace        = "game2-2048"
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
                  + "app.kubernetes.io/name" = "app2-2048"
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
                      + "app.kubernetes.io/name" = "app2-2048"
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
                      + "alpha.eksctl.io/nodegroup-name" = "ng2-mycluster1"
                    }
                  + restart_policy                   = "Always"
                  + service_account_name             = (known after apply)
                  + share_process_namespace          = false
                  + termination_grace_period_seconds = 30

                  + container {
                      + image                      = "984587260948.dkr.ecr.eu-west-1.amazonaws.com/sample-app"
                      + image_pull_policy          = "Always"
                      + name                       = "app2-2048"
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

  # kubernetes_namespace.game1-2048 will be created
  + resource "kubernetes_namespace" "game1-2048" {
      + id = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "game1-2048"
          + resource_version = (known after apply)
          + self_link        = (known after apply)
          + uid              = (known after apply)
        }

      + timeouts {
          + delete = "20m"
        }
    }

  # kubernetes_namespace.game2-2048 will be created
  + resource "kubernetes_namespace" "game2-2048" {
      + id = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "game2-2048"
          + resource_version = (known after apply)
          + self_link        = (known after apply)
          + uid              = (known after apply)
        }

      + timeouts {
          + delete = "20m"
        }
    }

  # kubernetes_service.game1-2048__service1-2048 will be created
  + resource "kubernetes_service" "game1-2048__service1-2048" {
      + id                    = (known after apply)
      + load_balancer_ingress = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "service1-2048"
          + namespace        = "game1-2048"
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
              + "app.kubernetes.io/name" = "app1-2048"
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

  # kubernetes_service.game2-2048__service2-2048 will be created
  + resource "kubernetes_service" "game2-2048__service2-2048" {
      + id                    = (known after apply)
      + load_balancer_ingress = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "service2-2048"
          + namespace        = "game2-2048"
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
              + "app.kubernetes.io/name" = "app2-2048"
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

Plan: 6 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: tfplan

To perform exactly these actions, run the following command to apply:
    terraform apply "tfplan"
{{< /output >}}

---

Deploy the Kubernetes application:
```bash
terraform apply tfplan
```
{{< output >}}
kubernetes_service.game2-2048__service2-2048: Creating...
kubernetes_service.game1-2048__service1-2048: Creating...
kubernetes_namespace.game2-2048: Creating...
kubernetes_namespace.game1-2048: Creating...
kubernetes_namespace.game1-2048: Creation complete after 1s [id=game1-2048]
kubernetes_namespace.game2-2048: Creation complete after 1s [id=game2-2048]
kubernetes_service.game1-2048__service1-2048: Creation complete after 1s [id=game1-2048/service1-2048]
kubernetes_service.game2-2048__service2-2048: Creation complete after 1s [id=game2-2048/service2-2048]
kubernetes_deployment.game2-2048__deployment2-2048: Creating...
kubernetes_deployment.game1-2048__deployment1-2048: Creating...
kubernetes_deployment.game1-2048__deployment1-2048: Creation complete after 3s [id=game1-2048/deployment1-2048]
kubernetes_deployment.game2-2048__deployment2-2048: Creation complete after 8s [id=game2-2048/deployment2-2048]

Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

The state of your infrastructure has been saved to the path
below. This state is required to modify and destroy your
infrastructure, so keep it safe. To inspect the complete state
use the `terraform show` command.

State path: terraform.tfstate
{{< /output >}}






Check everything is running ?
```bash
kubectl get pods,svc,deployment -A -o wide | grep game
```

{{< output >}}
game1-2048    pod/deployment-2048-ng1-788c7f7874-mccgw            1/1     Running   0          2m8s    100.64.100.188   ip-10-0-2-179.eu-west-1.compute.internal   <none>           <none>
game1-2048    pod/deployment-2048-ng1-788c7f7874-nvlqq            1/1     Running   0          2m8s    100.64.42.14     ip-10-0-1-25.eu-west-1.compute.internal    <none>           <none>
game2-2048    pod/deployment-2048-ng2-74bbf67dc5-w9sbh            1/1     Running   0          2m7s    10.0.2.166       ip-10-0-2-71.eu-west-1.compute.internal    <none>           <none>
game2-2048    pod/deployment-2048-ng2-74bbf67dc5-zq7p6            1/1     Running   0          2m7s    10.0.1.180       ip-10-0-1-231.eu-west-1.compute.internal   <none>           <none>
game1-2048    service/service1-2048                       NodePort    172.20.87.238    <none>        80:32481/TCP    2m6s    app.kubernetes.io/name=app1-2048
game1-2048    service/service2-2048                       NodePort    172.20.206.182   <none>        80:30243/TCP    2m5s    app.kubernetes.io/name=app2-2048
game1-2048    deployment.apps/deployment-2048-ng1            2/2     2            2           2m8s    app1-2048                      136434655158.dkr.ecr.eu-west-1.amazonaws.com/sample-app                                   app.kubernetes.io/name=app1-2048
game2-2048    deployment.apps/deployment-2048-ng2            2/2     2            2           2m7s    app2-2048                      136434655158.dkr.ecr.eu-west-1.amazonaws.com/sample-app                                   app.kubernetes.io/name=app2-2048
{{< /output >}}

Note from the output that:

* The pods are depoyed to  110.64.x.x (node group 1) and 10.0.x.x addresses (node group 2).
* The services are exposing port 80.
* The deployment is referencing a private ECR repository belonging to your account.

---


Enable port forwarding so we can see the application in out Cloud9 IDE:

```bash
kubectl port-forward service/service2-2048 8080:80 -n game2-2048
```
{{< output >}}
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
{{< /output >}}

Preview the running (port-forwarded service) application from the cloud 9 IDE"

Preview -> Preview Running Application
![tf-state](/images/andyt/game-2048-0.jpg)

You should then see the app running in the browser 

![tf-state](/images/andyt/game-2048-1.jpg)


As the Terraform files are similar to the previous section they are not explained here.

----

## Cleanup


Interrupt the port forwarding with **ctrl-C**

Then use Terraform to delete the Kubernetes resources:
```
terraform destroy -auto-approve
```


---
