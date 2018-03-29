---
layout:     post
title:      SonarQube使用介绍
subtitle:   静态扫描工具SonarQube介绍
date:       2017-08-15
author:     Sylvia
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - SonarQube
    - Continuous Integration
---

![](http://upload-images.jianshu.io/upload_images/7208479-c1d8ddc3921ce779.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### SonarQube特性
##### 多语言的平台
支持超过20种编程语言，包括Java, Python, C#, C/C++, JavaScript等常用语言。通常采用添加插件的方式增加某种语言。
##### 持续集成
通过对某项目的持续扫描，可以对该项目的代码质量做长期的把控，并且预防新增代码中的不严谨和冗余。
##### 关注新代码
有一个词叫"fixing the water leak"，不知道用中文该如何翻译，大概就是从水源处控制漏水。而SonarQube正是一款专注于新代码漏洞的工具，可以修复及改善新代码，从源头把控整体代码质量。
##### 质量门
在扫描代码后可以通过对“质量门”的比对判定此次“构建”的结果是否通过，质量门可以由用户定义，由多维度判定是否通过。
##### 自定义规则
用户可根据不同项目自定义Quality Profile以及Quality Gates。
##### 丰富的插件
SonarQube拥有丰富的插件，从而拥有强大的可扩展性。

### SonarQube使用
##### SonarQube入口
* 将Jenkins与SonarQube“绑定”后，便可通过Jenkins进入SonarQube的相应项目页面。具体方法如下： `进入项目` -> `SonarQube` （此时下方展示的SonarQube Quality Gate显示的是最近一次SonarQube扫描结果）

![SonarQube Entrance.jpeg](http://upload-images.jianshu.io/upload_images/7208479-77ad8f2da1a16069.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 当然也可以直接通过输入SonarQube Server URL进入哦

##### 代码质量评判维度
如何评判项目代码的优劣呢？代码语法是否合规、重复率、是否安全并易于后续的维护与修改等等因素都在其考量范围内。而SonarQube则主要提供了以下评判代码优劣的维度，用户也可以根据以下维度的通过标准来定义项目的Quality Gate。

* 可靠性  
所谓可靠性，就是指代码中的语法是否合规，是否有语法逻辑错误或是一些不推荐使用的方法，主要用Bugs来衡量。  
例如，break和continue是否在循环体内，分支语句的判断条件是否不同，数组是否越界，是否使用了print函数，当然也包括单元测试是否全部通过等等。还有很多不同语言所特有的编码规范，SonarQube都会通过相应语言的Quality Profile检测出来。

![py bug.png](http://upload-images.jianshu.io/upload_images/7208479-f0488e61a60e7966.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 安全性  
安全性也是考量一个项目代码质量的重要维度，这里的安全性主要指的是项目代码是否有潜在的“可被攻击”的漏洞，SonarQube主要用Vulnerability来衡量。  
例如，代码中是否有写死的IP地址，写死的或是空的数据库密码。

![py vulnerability.png](http://upload-images.jianshu.io/upload_images/7208479-63b814dc826236cd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 可维护性  
可靠性和安全性可以说是评判代码质量最重要的两个因素，也被SonarQube列在最顶端。所以Bugs和Vulnerabilities是建议用户立即修改并且日后避免的。而任何项目都需要维护，所以可维护性也是考量代码质量的重要标准，当然，优先级稍逊于可靠性与安全性。  
这里，SonarQube使用Code Smell来衡量。例如，循环或分支太深（眼睛都要看花了），java中的main方法最好不要"throw"异常等等。

![py code smell.png](http://upload-images.jianshu.io/upload_images/7208479-f6331cd186355748.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 代码重复率
SonarQube使用Duplications来评判代码的重复率，开发人员也可以以此标准来衡量自己的代码是否精简，从而将一些通用的类或方法进行封装哦。

* 单元测试覆盖率
完善的单元测试可以使代码更加可靠，也可以减少很多后续的风险呢。SonarQube用Coverage来考量单元测试覆盖率。


##### 结果查看
当您打开SonarQube时，建议您按以下步骤查看您代码的扫描结果并做出适当的修改哦。

* Step1. Quality Gate   
一般来说，当项目紧急时，如果Quality Gate为Pass完全就可以不用进入SonarQube查看代码质量分析结果了，因为当其Pass时说明您的代码质量已经没有太大问题了，只需要改一些不影响代码结果的小地方就可以了。当然，前提是您设置了一个比较合适的Quality Gate哦。

![Quality Gate](http://upload-images.jianshu.io/upload_images/7208479-7e37055a27ee236e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* Step2. Bugs & Vulnerabilities  
  这两个的数量便对应着上文"可靠性"以及"安全性"这两个维度的质量标准哦，这两个指标可以说在很大程度上反映了代码的质量水平，所以建议开发者尽量将这两个数量降为0哦。

![Bug and Vulnerability](http://upload-images.jianshu.io/upload_images/7208479-33566a35e728d8f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
  
* Step3. Leak Period  
  都说新提交的代码容易出问题，如果之前的代码都已使用SonarQube的扫描结果做了相应的修改的话，我建议可以主要关注"Leak Period"的衡量指标，它主要反映了新提交的代码的质量水平。开发者可以及时修改新提交代码中的问题以绝后患。  
  不过第一次扫描的时候是没有"Lead Period"的哦，所以建议第一次跑代码的时候还是将所有维度的质量问题都检查一遍以免后续漏改。

![Leak Period](http://upload-images.jianshu.io/upload_images/7208479-407dffc887b906fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)