---
layout:     post
title:      我用Jenkins玩Docker
subtitle:   使用Docker插件动态创建节点容器
date:       2018-03-23
author:     Sylvia
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - Docker
    - Jenkins
    - Testing
---

>上一篇说到使用Docker搭建Jenkins容器以及配套的Agent节点容器。此时问题来了，平时有很长一段时间都是没有CI项目需要执行的，而固定的容器这是就可以说是一种资源浪费了，所以可不可以动态地去创建容器，当有任务执行时，容器被创建，任务执行完后容器被销毁呢？ 
>
>Jenkins的Docker插件就可以实现这个需求哦。

首先把原先的agent容器断开，在Jenkins插件管理中下载安装`Docker`。

![Docker插件](https://upload-images.jianshu.io/upload_images/7208479-6af01dbefc6ae446.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在`系统管理`-`配置`中的`云`里，添加一个`Docker云`，`Docker Host URI`指向Docker服务器端口（谁能告诉我MacOS的Docker Host URI应该怎么配 =。=，尝试很多种方法都不对），随后点击`Test Connection`，检查是否能连通。

![系统配置](https://upload-images.jianshu.io/upload_images/7208479-28e07ccb6555912d.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

进入具体CI项目的配置，选择`Define a Docker template`，选择所连Docker服务器上已存在的合适镜像，`Connect method`我选了SSH key，为了在每次任务执行后都能删除容器，这里需要勾选`Remove volumes`。

![项目配置](https://upload-images.jianshu.io/upload_images/7208479-11425e8970eb8308.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行一下任务，这是会发现当任务属于执行状态时，会增加一个docker节点，而当任务执行完毕后，这个节点会消失。  

![运行时动态创建节点](https://upload-images.jianshu.io/upload_images/7208479-50a0ce4f8963352d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Done!


