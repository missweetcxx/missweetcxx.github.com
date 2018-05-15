---
layout:     post
title:      Flask-Restful初探
subtitle:   使用Flask-Restful写接口
date:       2018-05-15
author:     Sylvia
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - Flask
    - Api
---

>使用Flask-Restful写API真的是件简单友好的工作！
>在这篇文章里我会从造库造表、写API代码到相应的扩展来展示我是如何使用Flask-Restful来实现API的。

源码在这里： [源码](https://github.com/missweetcxx/fragments/tree/master/projects/flask_api)

##### 1. 造库造表
step 1. 这里我用了docker创建了mysql数据库:

```shell
sudo docker run --name ${name} -p ${PORT}:3306 -e MYSQL_ROOT_PASSWORD=${PW} -d mysql:latest
```

step 2. 进入mysql终端并对用户进行授权：

```shell
mysql -u root -p
GRANT ALL PRIVILEGES ON ${TABLE_NAME}.* TO 'root'@'%';
```

step 3. 建表

```shell
此处省略建表语句若干
```

step 4. 建立ORM映射

```python
engine = create_engine('mysql+pymysql://${USERNAME}:${PW}@${HOST}:${PORT}/${DATABASE}?charset=utf8')
Session = sessionmaker()
Session.configure(bind=engine)
db_session = Session(autocommit=True)
```

##### 2. 使用flask-restful写API
首先通过`pip install flask-restful`引入flask-restful框架，然后导入这些：  

```python
from flask_restful import Resource, reqparse, Api
```
接下来就可以用以下要素写接口啦

###### 2.1 一个继承自 `Resource`的类

```python
class TaskApi(Resource):
   def __init__(self):
       super(Api, self).__init__()
       self.db_session = db_session
```

###### 2.2 一个接收参数的函数
这个函数可以用来获取接口的参数并对其进行解析，在这里，我使用了RequestParser。默认情况下，它会从flask.Request.values以及flask.Request.json解析值。 

**step 1**. 首先实例化`RequestParser`

```python
parser = reqparser.Requestparser()
```

**step 2**. 随后就可以指定要接受的参数了～  

可以指定从POST body里解析参数：
  
```python
parser.add_argument('name', type=int, location='form')
```
也可以从queryString里解析：

```python  
parser.add_argument('PageSize', type=int, location='args')
```
或是指定从headers，cookies里解析，甚至指定多个参数位置：  

```python
parser.add_argument('text', location=['headers', 'values'])
```

解析参数的函数可以这样写（这里我没有对参数位置坐限制）：

```python
def req_parse():
    parser = reqparse.RequestParser()
    parser.add_argument('task', type=str)
    parser.add_argument('priority', type=int)
    args = parser.parse_args()
    
    return args
```
在调用函数时，就可以将请求参数解析并返回一个字典，获取参数如下：

```python
args = req_parse()
task = args.get('task')
priority = args.get('priority')
```

**step 3**. 校验参数
仅仅解析函数是肯定不够的，所以我又加了一个参数校验的方法：

```python
def _validator(self):
    if not (self.args.get('task') and self.args.get('priority')):
       return Error.LACK_OF_PARAM
    ......
    else:
       return Error.SUCCESS
       
```

###### 2.3 一个HTTP方法
当完成了参数解析和校验后，就可以在创建的类下定义HTTP方法了，在flask-restful中，HTTP方法就对应着API类下的响应方法：  

GET方法像酱紫：  

```python
def get(self):
    try:
      ......
      return res
    except Exception:
      return error_res
    finally:
      self.db_session.close()
```

POST方法像酱紫：

```python
def post(self):
    try:
      ......
      return res
    except Exception:
      return error_res
    finally:
      self.db_session.close()   
```

DELETE, PUT方法同理哦～

###### 2.4 一个数据格式化的类
在上述的方法中，其实可以通过`return dict()`来返回结果，但是这样其实很不优雅，而且如果返回的结构层次比较复杂，这样写就很不妥当。所以在这里特意用了flask-restful中的`marshal`和`fields`来格式化我们想要返回的数据。

举个栗子，如果希望返回的结构是酱紫的：  

```json
{
  'success': true,
  'desc': '成功',
  'value': {
     'task': 'drink milk',
     'priority': 1,
     'owners': [{
                 'name': 'tom',
                 'age' : 10,
                },
                {
                 'name': 'amy',
                 'age' :  9,
                }
                ]
           }
}
```

那么，我们首先要用fields从小到大来定义返回结构： 

```python
from flask_restful import fields, marshal

class Fields:
   # 1. owners中的结构
   owners = {
     'name': fields.String(attribute='name'), 
     # attribute指定参数传入的名称，默认为fields dict对应的key，此处为'name'
     'age': fields.Integer(attribute='age')
   }
   
   # 2. value中的结构
   value = {
      'task': fields.String(attribute='task'),
      'priority': fields.String(attribute='priority'),
      'owners': fields.List(fields.Nested(owners)) # Nested用来映射到上述定义的owners fields
   }
   
   # 3. 整体返回结构
   resource = {
      'success': fields.Boolean(attribute='success'),
      'desc': fields.String(attribute='desc'),
      'value':fields.Nested(value)
   }
   
```

那么如何根据fields中的结构格式化呢，这里我定义了一个方法：  

```python
class Wrapper:
   @staticmethod
   def _res_stuct(error, desc, value):
       return dict(success=error, desc=desc, value=value)
   
   @staticmethod
   def wrapper(error, desc, task=None, priority=None, owners=[]):
       wrapped_owners = []
       # 格式化owner
       for owner in owners:
          wrapped_owners.append(marshal(owner, Fields.owners))
       # 格式化value
       value = dict(task=task, priority= priority, owners= wrapped_owners)
       wrapped_value = marshal(value, Fields.value)
       # 格式化整体结构
       data = Wrapper._data(error, desc, value)
       return marshal(data, Fields.resource)
```

然后上面的get方法就可以酱紫写：  

```python
def get(self):
    try:
      ......
      return Wrapper.wrapper(True, 'success', task, priority, owners)
    except Exception as ex:
      return Wrapper.wrapper(False, ex)
    finally:
      self.db_session.close()
```

###### 2.5 一个注册指令
当我们解析了参数、定义了HTTP方法、格式化了返回，可接口还是没有实现，因为最重要的注册指令还没有完成，就是把API类注册到相应的路径上：  

```python
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

# 首先实例化Api
api = Api(app)
# 将接口类注册相应路径
api.add_resource(TaskApi, '/api/getTask')
```

###### 2.6 运行

```python
from ** import app

if __name__ == '__main__':
   app.run()
```
这时候调用http://localhost:5000/api/getTask?task=..就可以返回相应的结果哦～


##### 3. 扩展
###### 3.1 Blueprint
当有多个项目共用一个host时，要为某个项目中的API设置统一路径前缀，就可以用到Blueprint。  
具体实现如下(其实应该写在不同文件下但不好展示只能放到一起了 T-T)：  

```python
from flask import Blueprint, Flask
from flask_restful import Api

project_task = Blueprint('task', __name__, url_prefix='/task')
api_task = Api(project_task)

app = Flask(__name__)
app.register_blueprint(api_task)

api_task.add_resource(TaskApi, '/api/getTask')
```
这时候接口就在 `http://localhost:5000/task/api/getTask` 下面啦～