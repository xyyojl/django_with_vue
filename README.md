# 整合 Django 2.x + Vue.js 框架快速搭建web项目

## 一、 背景

在工作中我们经常须要构建一些基于web的项目，例如内部测试平台、运维系统等。本篇主要介绍如何使用后端Django + 前端Vue.js的技术栈快速地搭建起一套web项目的框架。

**为什么使用Django和Vue.js?**

Django是Python体系下最成熟的web框架之一，由于Python语言的易用性和受众面广，Django框架也因其能够快速开发网站应用的特性成为了中小型网站开发框架首选。且Django具备的数据分析( Pandas )、任务队列( Celery )、Restful API( Django REST framework )、ORM(类似java的hibernate)等一众功能都使得用户在面对任何建站需求时都能够得心应手。

Vue.js是当下很火的一个JavaScript MVVM库，它是以数据驱动和组件化的思想构建的。相比于Angular.js，Vue.js同样支持双向绑定、mustache标签语法等特性，并提供了更加简洁、更易于理解的API，使得我们能够快速地上手并使用Vue.js。

**本篇使用Vue.js作为前端框架，代替Django本身较为孱弱的模板引擎，Django则作为服务端提供api接口，使得前后端实现完全分离，更适合单页应用的开发构建。**

## 二、 项目使用的相关技术和环境

- 操作系统：Windows 10

- 数据库：MySQL 5.7 

- 后端：Django 2.x 框架，Python 3.x 
- 前端：HTML/CSS/jQuery/JavaScript/Vue.js

注：python 相关的模块，通过使用 python 自带的 pip 安装器安装。前端相关的第三方包，我们使用 node 自带的 npm 包管理器安装。

## 三、 构建Django项目

1、 进入一个安全目录，打开命令行提示符 CMD，输入命令：

```python
django-admin startproject myproject
```

目录结构：

![](https://s2.ax1x.com/2020/01/31/13gszQ.png)

2、进入 myproject 这个目录，新建一个虚拟环境并激活：

```python
cd myproject
# 需安装 Virtualenv 
pip install virtualenv
# 新建虚拟环境
virtualenv env
# 激活虚拟环境
.\env\Scripts\activate
# 安装 django
pip install django
# 提前安装好所需模块
pip install requests
```

激活虚拟环境的标记：

[![132LcQ.md.png](https://s2.ax1x.com/2020/01/31/132LcQ.md.png)](https://imgchr.com/i/132LcQ)

3、创建一个app：

```python
python manage.py startapp myapp
```

目录结构：

![Snipaste 2020 01 31 17 09 41](https://s2.ax1x.com/2020/01/31/13Wnqs.png)

4、在myproject下的settings.py配置文件中，把默认的sqlite3数据库换成我们的mysql数据库：

```python
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
    }
}
# 温馨小提示
# 将上面的 user 和 password 换成你自己的，同时保证自己有一个数据库名为 myproject 的数据库
```

并把app加入到installed_apps列表里：

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp'
]

```

5、 在app目录下的models.py里我们简单写一个model如下：

```python
from django.db import models

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_name
```

**只有两个字段，书名book_name和添加时间add_time。如果没有指定主键的话django会自动新增一个自增id作为主键**

在命令行窗口输入命令：

```python
# 安装 mysqlclient
pip install mysqlclient
# 数据库迁移
python manage.py makemigrations myapp
python manage.py migrate
```

[![13hZHs.md.png](https://s2.ax1x.com/2020/01/31/13hZHs.md.png)](https://imgchr.com/i/13hZHs)

通过命令行查询数据库，看到book表已经自动创建了/通过图形化工具 Navicat Premium 12 直接查看是否有这个数据库表：

![image](https://s2.ax1x.com/2020/01/31/13h0gO.png)

6、 在app目录下的 views.py 里我们新增两个接口，一个是show_books**返回所有的书籍列表**（通过JsonResponse返回能被前端识别的json格式数据），二是add_book 接受一个get请求，往数据库里添加一条book数据

```python
from django.shortcuts import render

# Create your views here.
# 需要导入相关的模块
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import requests
import json

from .models import Book

@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list']  = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
```

**可以看出，在ORM的帮忙下，我们的接口实际上不需要自己去组织SQL代码**

7、在app目录下，新增一个urls.py文件，把我们新增的两个接口添加到路由里：

```python
from django.urls import path,re_path
# 导入 myapp 应用的 views 文件
from . import views

urlpatterns = [
    re_path(r'add_book$', views.add_book),
    re_path(r'show_books$', views.show_books)
]
```

此外，我们还要把app下的urls添加到project下的urls中，才能完成路由：

```python
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url, include
import myapp.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/', include(myapp.urls)),
]
```

8、输入命令，启动服务器：

```python
python manage.py runserver
```

**测试接口方式一**：通过浏览器，由于这些请求都是 get 请求，所以可以直接在浏览器上直接看到服务器返回的结果
直接在浏览器地址栏输入 http://localhost:8000/api/show_books，你会看到下面这张图片的效果：

![image](https://s2.ax1x.com/2020/01/31/13TefI.png)

直接在浏览器地址栏输入http://localhost:8000/api/add_book?book_name=test，你会看到下面这张图片的效果：

![image](https://s2.ax1x.com/2020/01/31/13TYhn.png)**测试接口方式二**：postman

通过postman测试一下我们刚才写的两个接口：

add_book 接口：

![image](https://s2.ax1x.com/2020/02/04/1DQ1Qs.md.png)

show_books 接口：

![image](https://s2.ax1x.com/2020/02/04/1DQ6w6.md.png)

学习链接：

- [Postman 使用教程详解](https://www.jianshu.com/p/6c9b45994c34)
- [postman的使用方法详解！最全面的教程](https://www.cnblogs.com/Skyyj/p/6856728.html)

- [Postman安装与使用](https://www.cnblogs.com/fnng/p/9136434.html)

## 四、 构建Vue.js前端项目

前提：安装了 NODE，安装好之后会自带 npm 包管理器

1、 先用npm安装vue-cli脚手架工具（vue-cli是官方脚手架工具，能迅速帮你搭建起vue项目的框架）：

```js
npm install -g vue-cli
```

安装好后，在project项目根目录下，新建一个前端工程目录：

```js
vue-init webpack appfront  //安装中把vue-router选上，我们须要它来做前端路由
```

现在我们可以看到整个文件目录结构是这样的：

![image](https://s2.ax1x.com/2020/01/31/13O91A.png)

2、 在目录src下包含入口文件main.js，入口组件App.vue等。后缀为vue的文件是Vue.js框架定义的单文件组件，其中标签中的内容可以理解为是类html的页面结构内容，标签中的是js的方法、数据方面的内容，而则是css样式方面的内容：

![img](https://blog-10039692.file.myqcloud.com/1501640610939_1925_1501640611338.png)

3、安装并引入 element ui 和 axios

首先在命令行当中安装 element ui 和 axios

```js
npm install element-ui
npm install axios
```

然后在 src/main.js 在原有代码的基础上，添加下面代码：

```js
// 引入 element-ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

// 引入 axios
import axios from 'axios'
Vue.prototype.$axios = axios

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  axios,
  components: { App },
  template: '<App/>'
})

```

4、在src/component文件夹下新建一个名为Home.vue的组件，通过调用之前在Django上写好的api，实现添加书籍和展示书籍信息的功能。

```vue
<template>
  <div class="home">
    <el-row display="margin-top:10px">
        <el-input v-model="input" placeholder="请输入书名" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-button type="primary" @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
    </el-row>
    <el-row>
        <el-table :data="bookList" style="width: 100%" border>
          <el-table-column prop="id" label="编号" min-width="100">
            <template slot-scope="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="book_name" label="书名" min-width="100">
            <template slot-scope="scope"> {{ scope.row.fields.book_name }} </template>
          </el-table-column>
          <el-table-column prop="add_time" label="添加时间" min-width="100">
            <template slot-scope="scope"> {{ scope.row.fields.add_time }} </template>
          </el-table-column>
        </el-table>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      input: '',
      bookList: [],
    }
  },
  mounted: function() {
      this.showBooks()
  },
  methods: {
    addBook(){
      this.$axios.get('http://127.0.0.1:8000/api/add_book?book_name=' + this.input)
        .then((res) => {
            // console.log(res)
            var res = res.data;
            if (res.error_num == 0) {
              this.showBooks()
            } else {
              this.$message.error('新增书籍失败，请重试')
              console.log(res['msg'])
            }
        })
    },
    showBooks(){
      this.$axios.get('http://127.0.0.1:8000/api/show_books')
        .then((res) => {
            var res = res.data;
            // console.log(res)
            if (res.error_num == 0) {
              this.bookList = res['list']
            } else {
              this.$message.error('查询书籍失败')
              console.log(res['msg'])
            }
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>

```

5、如果发现列表抓取不到数据，可能是出现了跨域问题，打开浏览器console确认：

![img](https://blog-10039692.file.myqcloud.com/1501640848145_4871_1501640848404.jpg)

这时候我们须要在Django层注入header，用Django的第三方包`django-cors-headers`来解决跨域问题：

```python
pip install django-cors-headers
```

修改 settings.py 

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # 新增的中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
```

6、在前端工程目录下，输入`npm run dev`启动node自带的服务器，浏览器会自动打开， 我们能看到页面：

![image](https://s2.ax1x.com/2020/01/31/18Zbj0.png)

7、在前端工程目录下，输入`npm run build`，如果项目没有错误的话，就能够看到所有的组件、css、图片等都被webpack自动打包到dist目录下了：

![image](https://s2.ax1x.com/2020/01/31/18eFu6.png)

## 五、 整合Django和Vue.js

目前我们已经分别完成了 **Django 后端**和 **Vue.js 前端工程**的创建和编写，但实际上它们是运行在各自的服务器上，和我们的要求是不一致的。因此我们须要把Django的`TemplateView指向我们刚才生成的前端dist文件即可。`

我个人理解，如果要想实现**前后端分离的项目**，基本不用看下面的内容，Vue.js 实现项目的前台，Django 实现项目的后台，提供 api。

1、 找到project目录的urls.py，使用通用视图创建最简单的模板控制器，访问 『/』时直接返回 index.html：

```python
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url, include
import myapp.urls
from django.views.generic import TemplateView # 新增的

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/', include(myapp.urls)),
    re_path(r'^$', TemplateView.as_view(template_name="index.html")), # 新增的
]

```

2、 上一步使用了Django的模板系统，所以需要配置一下模板使Django知道从哪里找到index.html。在project目录的settings.py下：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['appfront/dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

3、 我们还需要配置一下静态文件的搜索路径。同样是project目录的settings.py下：

```python
# Add for vuejs
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "appfront/dist/static"),
]
```

4、 配置完成，我们在project目录下输入命令`python manage.py runserver`，就能够看到我们的前端页面在浏览器上展现：

![image](https://s2.ax1x.com/2020/01/31/18K8Qs.png)

**注：服务的端口已经是Django服务的8000而不是node服务的8080了**

## 六、 部署

由于python的跨平台特性，因此理论上只要在服务器上安装好所有的依赖，直接把项目目录拷贝到服务器上即可运行。这里只提一点：**如果为项目配置了nginx作为反向代理，那么要在nginx中配置所有的静态文件path都指向Django项目中配置的静态文件url，在settings.py中可配置url路径：**

```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
```

## 七、 其他

实例项目的源码都可以点击下面的链接进入下载：

https://github.com/xyyojl/django_with_vue

最后，特别感谢原作者 [．╂遊牧](https://cloud.tencent.com/developer/user/1002805) 写的博客 [整合 Django + Vue.js 框架快速搭建web项目](https://cloud.tencent.com/developer/article/1005607)，整篇博客文章参考原作者写的博客，采用最新的技术栈重写那个实例项目，跟原来的会有写不一样。