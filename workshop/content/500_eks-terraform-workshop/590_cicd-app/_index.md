---
title: "12. Private CI/CD for EKS"
chapter: true
weight: 590
tags:
  - tfeks
---

# Use the CI/CD Pipeline to deploy the sample app 

[Continuous integration](https://aws.amazon.com/devops/continuous-integration/) (CI) and [continuous delivery](https://aws.amazon.com/devops/continuous-delivery/) (CD)
are essential for deft organizations. Teams are more productive when they can make discrete changes frequently, release those changes programmatically and deliver updates
without disruption.

In this module, we will use the previously created CI/CD pipeline using [AWS CodeCommit](https://aws.amazon.com/codecommit/), [AWS CodeBuild](https://aws.amazon.com/codebuild/) & [AWS CodePipeline](https://aws.amazon.com/codepipeline/). 

The CI/CD pipeline will deploy a sample application,
we will copy the code to the CodeCommit repository and observe the automated deployment of the sample application to the Kubernetes (EKS) cluster.