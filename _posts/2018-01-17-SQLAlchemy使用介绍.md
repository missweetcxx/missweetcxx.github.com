---
layout:     post
title:      SQLAlchemy使用介绍
subtitle:   简单粗暴使用SQLAlchemy
date:       2018-01-17
author:     Sylvia
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - SQLAlchemy
    - Python
---

#### 一、介绍
SQLAlchemy是Python编程语言下的一款ORM框架，使用此库可以便捷的使用python代码来操作SQL数据库，下面，我们以MySQL数据库为例，来介绍一下SQLAlchemy的使用吧。

#### 二、连接数据库
在使用`pip install SQLAlchemy`安装SQLAlchemy之后，就可以使用其进行数据库的连接了。在这里，我们使用`create_engine`，如下例： 

```
engine = create_engine ('数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名’）

例如：
 (‘mysql+pymysql://root: password@localhost:3306/test’)
```

通常在连接完数据库后，我们会创建Session并绑定上文建立的数据库连接，之后对数据库的操作都在通过Session对象来完成。

```
# 首先要导入sessionmaker
from sqlalchemy.orm import sessionmaker

# 创建Session对象来绑定上文建立的engine连接
Session = sessionmaker(bind=engine)

# 实例化Session
session = Session()

之后的增删查改操作都使用实例化后的session来进行哦
```
#### 三、声明映射
当我们使用SQLAlchemy ORM框架连接完数据库后，接下来的就要将数据库中的表转换为python对象了。一般来说这个环节可以有两种方法：
##### 1. 手动声明
> 首先，使用`declarative_base`创建对象基类
> 
> ```
> from sqlalchemy.ext.declarative import declarative_base
> 
> Base = declarative_base()
> ```
> 创建完对象基类后，我们就可以对照数据库定义表对象了
> 
> ```
> from sqlalchemy import Column, Integer, String
> 
> class User(Base):
>     # 定义表名
>     __tablename__ = 'users'
>     # 定义表内容
>     id = Column(Integer, primary_key=True)
>     name = Column(String(20))
>     score = Column(Integer)
> ```

##### 2. 指令声明
> 终端一行指令，优雅搞定
> 
> ```
> sqlacodegen mysql+pymysql://用户名:密码@机器地址:端口号/数据库名 > 数据库对象存放路径
> 
> 例如：
> sqlacodegen mysql+pymysql://root:password@localhost:3306/test >temp.py 
> 
> 随后，打开temp.py就可以看到生成的数据库对象啦
> ```


#### 四、插入记录
以上面的User表为例，下面来讲解一下如何向其添加记录：

1.  实例化新的User对象

```
assemble_user = User(id = 1, name = 'sweet', pwd = 'abc')
```

2. 添加至session

```
session.add(assemble_user)
```

3.  提交保存至数据库

```
session.commit()
```

4.  关闭session
 
```
session.close()
```
 提交完成后需要关闭session断开数据库连接， 不然数据库会一直连接，直到程序终止

那么，如何在一个session中批量向数据库添加记录呢？

```
# 创建一个存放记录的列表
user_list = []
user_a = User(id = 1, name = 'sweet', score = 87)
user_b = User(id = 2, name = 'candy', score = 91)
user_list.append(user_a, user_b)

# 注意这里要用add_all
session.add_all(user_list)
session.commit()
session.close()
```

#### 五、查询记录
SQLAlchemy既然是用python来操作数据库，那么对于基本的SQL语句，也能“翻译”为对应的代码，下面我们以上面的users表为例，来说一下SQLAlchemy查询语句的基本用法。

#### · 基本查询
 
##### a. 查询users表内的所有的记录
 
> SQL语句
> 
> ```
> SELECT * FROM users;
> ```
> SQLAlchemy python
> 
> ```
> session.query(User).all()
> ```
> Note:  
> 这里需要注意哦，虽然操作的表名为users，但其对应的对象名为User，所以我们还是以 'User' 来操作表哦；  
> 使用all()查询出来的结果是一个list，可以使用list的取值或遍历方法来对其进行操作。


##### b. 查询users表内所有name
> 
> SQL语句
> 
> ```
> SELECT users.name FROM users;
> ```
> SQLAlchemy python
> 
> ```
> session.query(User.name).all()
> ```

##### c. 查询users表内name为candy的记录
> 
> SQL语句
> ```
> SELECT * FROM users WHERE users.name = 'candy';
> ```
>
> SQLAlchemy python
> 
> ```
> session.query(User).filter(User.name == 'candy').all()
> ```
> 
> Note:  
> filter的用法类似于SQL语句里的WHERE，但要注意的是，这里面的等于需要用'=='哦。

##### d. 查询users表内id大于2并且name是'sweet'或'candy'的记录
 
> SQL语句
>
> ```
> SELECT * FROM users WHERE users.id > 2 AND users.name IN ('sweet', 'candy');
> ```
> 
> SQLAlchemy python 
> 
> ```
> session.query(User).filter(User.id > 2,
>                            User.name.in_(['sweet'.'candy'])).all()
> ```
> 
> Note:  
> 这里有两个"与"条件，SQLAlchemy的用法是在filter()中用 ',' 作为分割；  
> 而在SQLAlchemy中使用in_(list)的方式来表示字段值在list范围内。

##### e. 查询users表内name中有'ee'的记录

> SQL语句
> ```
> SELECT * FROM users WHERE users.name LIKE '%ee%';
> ```
> 
> SQLAlchemy python 
> 
> ```
> session.query(User).filter(User.name.like('%ee%')).all()
> ```

##### f. 查询users表内id为1或name以's'开头的记录

> SQL语句
> ```
> SELECT * FROM users WHERE users.name LIKE 's%' OR users.id = 1;
> ```
> 
> SQLAlchemy python 
> 
> ```
> session.query(User).filter(or_(User.name.like('s%'),
>                                User.id == 1)).all()
> ```

##### g. 根据id倒序查询users表内的记录

> SQL语句
> ```
> SELECT * FROM users ORDER BY users.id DESC;
> ```
> 
> SQLAlchemy python 
> 
> ```
> session.query(User).order_by(User.id.desc())
> ```
> 
> Note:  
> GROUP_BY使用方式与其类似，不做赘述；  
> asc使用方式与其类似，不做赘述。
>


以上的查询已经可以覆盖80%的业务需求了，但SQLAlchemy的使用还远远不止这些，下面就来介绍一下SQLAlchemy的高级运用吧。


#### · 多表联合查询

> 可以使用filter语句来进行多表关联
> ```
> session.query(User, Address).filter(User.id==Address.user_id)\
>                             .filter(Address.city=='sh')>.all()
> ```
 
> 也可以简单粗暴使用join()
> ```
> session.query(User).join(Address)\
>        .filter(Address.city=='sh').all()


#### · 函数计算

##### a. 查询users表内的总分数
 
> SQL语句
> 
> ```
> SELECT SUM(score) FROM users;
> ```
> SQLAlchemy python
> 
> ```
> session.query(sqlalchemy.func.sum(score)).scalar()
> ```

##### b. 查询users表内分数大于90的个数

> SQL语句
> 
> ```
> SELECT COUNT(score) FROM users WHERE users.score > 80;
> ```
>  SQLAlchemy python
> 
> ```
> session.query(sqlalchemy.func.avg(User.score)).filter(User.score>80).scalar()
> ```
> Note:  
> 一般来说，不太会使用fun.count()这个函数，因为可以取出数据记录列表后利用python的len()来计算长度。
> 


#### · 语义化用法
翻译成“语义化”用法不知妥不妥当，原文是"Textual SQL"。这里的意思就是将SQL语句直接写入python代码中，如下例：

> 使用param()来传参
> 
>```
>session.query(User).filter(text("id<:value")).params(value=2).one()
>```

> 简单粗暴execute()执行SQL语句
> 
> ```
> session.execute(text('SELECT * FROM users WHERE id = :value'), ({'value': 1})).one()
> ```

> 或者酱紫用from_statement
> 
> ```
> stmt = text("SELECT name, id, fullname, password FROM users where name=:name")
> session.query(User).from_statement(stmt).params(name='sweet').all()
> ```
> 

#### 六、删除记录
简单粗暴上栗子：

```
session.query(User).filter(User.name=='sweet').delete()
```
如果查询条件里有in_，需要在delete()中加如下参数：

```
session.query(User).filter(User.in_(['sweet'])).delete(synchronize_session='fetch')
