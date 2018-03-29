---
layout:     post
title:      我用Docker玩Jenkins
subtitle:   使用Docker构建Jenkins分布式测试架构
date:       2018-03-22
author:     Sylvia
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - Docker
    - Jenkins
    - Testing
---

> "CI使生活更美好"，为了充分地使用Jenkins实现多项目的持续集成，我们可以使用如下图的`Server-Agent`架构，即配置一个Jenkins服务器，再配置若干个Jenkins agent，随后在Jenkins服务器上将这些agent添加为节点。随后当有CI项目便都在agent服务器上执行。   
![Jenkins Agent-Server架构](https://upload-images.jianshu.io/upload_images/7208479-2805101129c601f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
今天就和大家讲述一下我使用Docker配置Jenkins以及其节点的经历吧。

##### step 1. 创建Jenkins容器
这里我使用[`jenkins/jenkins`](https://hub.docker.com/r/jenkins/jenkins/)这个镜像，  

```shell
docker pull jenkins/jenkins
```
用这个镜像创建Docker容器(这里我选择了50000端口)：

```shell
docker run -d -p 50000:8080 jenkins/jenkins:latest
```
![Jenkins容器创建](https://upload-images.jianshu.io/upload_images/7208479-915919bc7eda17a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

容器创建好之后，就可以在`http://localhost:50000`上看到Jenkins的引导配置页面啦。

![jenkins引导页面.png](https://upload-images.jianshu.io/upload_images/7208479-740f2cae7a15f5b7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

随后去Jenkins容器查看所需密码：  

```shell
docker exec -it ${CONTAINER_ID} bash
# 进入 Jenkins 容器
cat /var/jenkins_home/secrets/initialAdminPassword
# 查看密码
```

将查到的密码填入，随后就可以正式配置Jenkins啦，建议选择推荐的插件安装哦。
![Jenkins安装完成](https://upload-images.jianshu.io/upload_images/7208479-05c72543931c660f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##### step 2. 创建Agent容器
根据所要执行的CI项目选择一个Docker镜像创建容器后安装相关的依赖，或是直接用DockerFile构建一个镜像，这里我使用Dockerfile。

```shell
docker build -t agent:lts ${DockerFilePath}
```


##### step 3. 连通Jenkins和Agent
* 进入Jenkins容器，生成ssh-key:

  ```shell
  ssh-keygen
  ```
  在.ssh目录下查看公钥id_rsa.pub

  ```shell
  cat .ssh/rsa_id.pub
  ```

* 进入Agent容器，生成ssh-key并在.ssh目录下创建authorized_keys文件

  ```shell
  cd ~/.ssh
  >authorized_keys
  ```
  将Jenkins的公钥复制在authorized_keys下,修改权限：
  
  ```shell
  chmod 600 ~/.ssh/authorized_keys
  chmod 700 ~/.ssh
  ```
  随后重启ssh服务，
  
  ```shell
  /etc/init.d/ssh restart
  ```
  
* 查看agent的ip地址，之后会用哦：
  
  ```shell
  docker inspect ${AGENT_ID}
  ```
  ![agent ip](https://upload-images.jianshu.io/upload_images/7208479-2695b631cffa015b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 此时登录Jenkins容器，输入上面查到的agent的ip地址:

  ```shell
  ssh root@${AGENT_IP}
  ```
  如果能够顺利登陆agent那台机器，就说明姿势正确哦，如果不能的话。
  
  
##### step 4. Jenkins项目配置节点
进入 `Jenkins -> Nodes`，填写节点的工作目录，上面查看到的agent的IP地址等。如下图，这里有个小坑，当我使用`SSH with private key`方式创建的`Credentials`时，总是显示鉴权失败，折腾了好久。这时候我又添加了以`Username with password`方式创建的`Credentials`(需要知道agent容器的登录名密码，如果不知道，可以通过`echo 'root:root' |chpasswd`的方式去添加）时，agent便顺利连接上了。

![Jenkins添加节点](https://upload-images.jianshu.io/upload_images/7208479-845c84fa89aec928.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

新建一个项目，在"限制项目的运行节点"中填写相应的节点。

![项目节点配置](https://upload-images.jianshu.io/upload_images/7208479-b334728c67d52106.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后项目就可以在指定agent容器里运行啦～
同样地，可以配置多个agent容器，如果有多个CI项目的话，就可以并行执行了。

