---
title: "Testing - Part 1"
date: 2018-10-03T10:14:46-07:00
draft: false
weight: 55
---

## Testing using ping and other command line tools

Connect to the first instance `instance-10-1-4-first` you created in vpc-10-1 using Systems Manager.


* Go to `AWS Systems Manager` in the AWS console
  
* On the left hand menu click `Fleet Manager`

* Select the `instance-10-1-4-first` instance, click `Instance Actions`, `Start Session`


![sm1](/images/andyt/syst-man1.png)

  
While connected to the instance...

* Can you reach the internet? - `ping aws.amazon.com`

* What is your private ip address? -  `ip address`

* What is your public ip address? - `curl ipinfo.io/json` or `curl ifconfig.io`

* What route are in this instance? -  `ip route`

* What services or IPs are connected to this instance? `sudo netstat -pant`


---

:white_check_mark: Proceed to the next step

