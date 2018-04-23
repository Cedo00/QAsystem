Python + Flask 做的一个简单的问题系统，包括以下功能：

1.注册

2.发布问答

3.评论

4.搜索问题

其模型为最最最最最基础版的知乎。

本项目参考《Flask Web开发：基于Python的Web应用开发实践》，其gitbook地址为：https://l1nwatch.gitbooks.io/flask-web-python-web/content/

Ubuntu下使用方法：

1.下载仓库到本地：git clone https://github.com/cairns0214/Question-And-Answering-System.git

2.切换到仓库所在路径：cd Question-And-Answering-System

3.创建Python虚拟环境：先先删除项目中的venv文件夹然后使用如下命令创建Python虚拟环境virtualenv venv（如果没有这个工具可以使用$sudo apt-get install python-virtualenv命令进行安装）

4.激活虚拟环境：$source venv/bin/activate，激活后显示为：(venv)$

5.安装依赖：pip install -r requirements.txt(依赖不完全的话在运行时可以提示缺少的模块继续安装即可)

6.创建数据库：打开一个新的终端，使用如下命令：mysql -uroot -p，输入你的密码，然后用如下命令创建数据库create database 数据库名 charset utf8;（注意别忘了分号）（Ununtu下安装使用mysql可以参考：https://www.cnblogs.com/EasonJim/p/7147787.html）

7.修改配置文件config.py中USERNAME PASSWORD DATABASE分别为数据库登录名，数据库登录密码，数据库名

8.数据库迁移（先删除项目中的migrations文件夹）：

  创建迁移仓库：python manage.py db init
  
  创建迁移脚本：python manage.py db migrate -m "initial migration"
  
  更新数据库：python manage.py db upgrade
  
9.运行项目：python manage.py runserver

10.打开浏览器，在地址栏输入127.0.0.1:5000即可访问

