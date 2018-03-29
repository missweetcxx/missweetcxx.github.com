---
layout:     post
title:      SonarQube with Jenkins
subtitle:   使用Jenkins集成静态扫描工具SonarQube
date:       2017-08-14
author:     Sylvia
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - Jenkins
    - Continuous Integration
---

> 什么工具都是配置最揪心了 = 。= 作为一名测试工程师，捉虫固然最重要，但提高程序员（也包括测试员自己）的代码质量，便可从根本上预防一些因代码不规范引起的bug。而利用持续集成（Continuous Integration）亦可从项目前期便开始控制代码质量，严格把控新增代码的不严谨或是冗余。前不久研究了一款开源的静态代码扫描工具SonarQube，可在不同维度管理源代码的质量，并开始利用Jenkins来持续为开发工程师的代码进行体检，感觉实用而有成就感，下面就和大家分享一下吧。

#### Jenkins 配置
#####第一步
在 `系统管理` -> `插件管理` -> `可选插件` 搜索 "SonarQube Scanner"，并安装待Jenkins重启；  
![Jenkins Step1](http://upload-images.jianshu.io/upload_images/7208479-9e45c746fe5c5f72.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/800)


#####第二步
进入 `系统管理` -> `系统设置` -> `SonarQube Server`:  

* *Server URL*:   
填写相应SonarQube的服务器地址 （如http://0.0.0.0:9000)
* *Login & password*:   
如果选了Server version为5.2或以下，则需要填写此信息，为gitlab的登录密码
* *Authentication token*:   
如果选了Server version为5.3或以上，则需要填写此信息，为gitlab的API token（可在profile里查看）  

![Jenkins Step2](http://upload-images.jianshu.io/upload_images/7208479-4646fdcee3ab0f70.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/800)


#####第三步  
进入 `系统管理` -> `Global Tool Configuration` -> `SonarQube Scanner`: 
选择 "SonarQube Scanner安装"，建议选择 "自动安装"

![Jenkins Step3](http://upload-images.jianshu.io/upload_images/7208479-0aca10bd5d64459a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/800)

#####第四步  
创建一个需要进行扫描的项目：

* 在`构建环境` 中勾选 "Prepare SonarQube Scanner environment"  

![Jenkins Step4-1](http://upload-images.jianshu.io/upload_images/7208479-4075f14b92125370.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/800)
* 在`构建` 中填写 "Analysis properties" 信息，具体的参数含义可参考 [SonarQube 参数配置介绍](https://docs.sonarqube.org/display/SONAR/Analysis+Parameters)  

![Jenkins Step4-2](http://upload-images.jianshu.io/upload_images/7208479-972b69afe95810c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/800)

#### SonarQube 配置
#####第一步  
进入 `Administration` -> `System` -> `Update Center`，安装 "Git"以及要进行扫描的语言插件  

![SonarQube Step1](http://upload-images.jianshu.io/upload_images/7208479-0cde92cd2ba5d01f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/800)

#####第二步   
进入 `Administration` -> `Configuration` -> `General Settings` -> `SCM`，勾选 "Disable the SCM Sensor"  

![SonarQube Step2](http://upload-images.jianshu.io/upload_images/7208479-8949a9c8b30772cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/800)

#####Done !