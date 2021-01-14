---
title: "Open the Workspace"
chapter: false
weight: 14
---


{{% notice tip %}}
Ad blockers, javascript disablers, and tracking blockers should be disabled for
the cloud9 domain, or connecting to the workspace might be impacted.
Cloud9 requires third-party-cookies. You can whitelist the [specific domains]( https://docs.aws.amazon.com/cloud9/latest/user-guide/troubleshooting.html#troubleshooting-env-loading).
{{% /notice %}}


{{% notice tip %}}
Use Chrome or Firefox browsers to run this workshop.
{{% /notice %}}

<!--
### Launch Cloud9 in your closest region:
{{< tabs name="Region" >}}
{{{< tab name="Ireland" include="eu-west-1.md" />}}
{{{< tab name="West USA" include="us-west-2.md" />}}
{{< /tabs >}}


- Select **Next**
- Select **Next**
- Select **Next**
- Select **Create Stack**
-->

Use the console to select the Cloud9 service

![serv](/images/andyt/Services-cloud9.jpg)

- In the Console select the eks-terraform Cloud9 IDE environment

![c9attachrole](/images/andyt/OpenIDE.jpg)

- Click **Open IDE**

- When it comes up, customize the environment by closing the **welcome tab**
and **lower work area**, and opening a new **terminal** tab in the main work area:
![c9before](/images/c9before.png)

- Your workspace should now look like this:
![c9after](/images/c9after.png)

- If you like this theme, you can choose it yourself by selecting **View / Themes / Solarized / Solarized Dark**
in the Cloud9 workspace menu.

:white_check_mark: Proceed to the next step
