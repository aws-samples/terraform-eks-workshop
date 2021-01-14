---
title: "Cleanup the Terraform Resources"
date: 2018-08-07T12:37:34-07:00
weight: 10
draft: false
---
To clean up the resources in your AWS account created by this workshop.
Run the following commands:

```
cd ~/environment/tfekscode/testing
```

run this script which will delete all the resources created by terraform:

```
./destroy-everything.sh
```

-----

Check if the Load Balancer & Target Groups have been deleted, if not use the console to remove these resources.
