yum install -y MySQL-python libffi-devel python-devel zlib zlib-devel openssl openssl-devel libcurl-devel gcc gcc-c++

wget https://pypi.python.org/packages/26/10/0493cb0579b34e453fcd9c56fbf4504a5e4a9d9c8db80cece3fbc92e06d2/pika-0.11.0.tar.gz#md5=5127731ff530c46bc9a34eff1cfc64ef
tar -zxvf pika-0.11.0.tar.gz
cd pika-0.11.0
python setup.py install 
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# release_sdjj
1.django使用1.6.11开发,安装django
        python get-pip.py
        #pip install Django==1.6.11 #老版本使用
        pip install Django==1.10.8
	pip install paramiko==1.16.0 #如果不用apk更新功能，可以不用安装
        #tar -zxvf Django-1.6.11.tar.gz
        ##cd Django-1.6.11
        ##python setup.py install
        pip install requests
	pip install GitPython
	pip install uwsgi #测试和正式环境需要
#bootstarp 使用3.3.7版本，这个在项目中的
# 环境配置文件修改，例如release_sdjj/testenv_settings.py
# 修改manage.py中---> os.environ.setdefault("DJANGO_SETTINGS_MODULE", "release_sdjj.testenv_settings")
#执行./manage.py syncdb ，生成数据库表---    ./manage.py validate这个是测试数据表的
#导入左导航数据，mysql -h 192.168.30.132 -u webadmin -p release_sdjj < release_sdjj/release_left_nav.sql
#修改root用户中文名
        ./manage.py shell
        from django.contrib.auth.models import User
        User.objects.filter(id=1).update(last_name='超级管理员')
#修改文件属性 chown apache:apache -R /data/release_sdjj
#
#在文件release/release_view.py中，记得修改developer.conf文件的路径
#切换apache用户启动，nohup python manage.py runserver 0.0.0.0:8080 > /data/bzlogs/nginx/release_sdjj.log 2>&1 &
# 开机启动 ： su - apache -c 'cd /data/release_sdjj/ && nohup python manage.py runserver 0.0.0.0:8080 > /data/bzlogs/nginx/release_sdjj.log 2>&1 &'


#######################1.2更新###########
 更新apk------

from release.models import left_nav
a= left_nav.objects.filter(left_navid=6)
a.update(left_nav_sort=5)
a= left_nav.objects.filter(left_navid=5)
a.update(left_nav_sort=4)
 p = left_nav(left_nav_pid='1',left_nav_title='更新APK',left_nav_url='/apkupdate',left_nav_sort='3')
p.save()

#赋权
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
user = User.objects.get(username='linlei')
change_release = Permission.objects.get(codename='change_release')
user.user_permissions.add(change_release)

#########################1.4更新##########
队列式APK更新---------
#django需要添加左导航
增加左导航
a= left_nav.objects.filter(left_navid=6)
a.update(left_nav_sort=6)
a= left_nav.objects.filter(left_navid=5)
a.update(left_nav_sort=5)
p = left_nav(left_nav_pid='1',left_nav_title='APK队列',left_nav_url='/apkupdate/apkqueue',left_nav_sort='4')
p.save()

#django端
建表
./manager sqlall apkbuild
./manager syncdb

#work需要安装的软件,脚本文件在apkbuild/build_apk_for_work.tar.gz 里
yum install -y MySQL-python libffi-devel python-devel zlib zlib-devel openssl openssl-devel libcurl-devel gcc gcc-c++

1.安装RabbitMQ服务器，配置好tcp超时时间和hearbeat 时间
2.安装pika——python模块. install_pika.sh
3.安装paramiko模块. pip install paramiko==1.16.0
4.复制ssh到文件服务器的私钥. 
5.安装apktool. apktool_install.sh
6,修改configs/BuildApk.conf 配置文件
7,work目前容易内存报错，自动关闭进程，需要check_process.sh来重启进程


#刷新cdn脚本,放在计划任务里执行，脚本文件在apkbuild/build_apk_for_work.tar.gz 里
1，修改configs/BuildApk.conf 配置文件
2.修改cdn_renew_MQ.py 脚本的process数据，根据需求


#################################1.4.2更新################
./manager.py dbshell
alter table apkbuild_apk_build_queue add `project_name` varchar(255) NOT NULL;

apk新增项目请注意
	修改配置文件:apkbuild/configs/ProjectName.conf 
	
#############################1.8.0更新#################################
1,新版本 ，需要django 1.10.8 python 2.7 ，pip也需要安装2.7版本的
2.新环境需要执行./manage.py migrate 迁移数据库
3.遇到没有的表 ./manage.py makemigrations apkbuild 这样来重新来生成关系，再执行./manage.py migrate
4.需要导入mysql -h 192.168.30.132 -u webadmin -p release_sdjj < release_sdjj/release_left_nav.sql 左导航
5.启动用uwsgi，配置文件自己编写，启动脚本自己编写
6.新版发布，上传php文件的时候需要校验php语法，必须安装php
7,测试环境建用户，一定得选择活动开发。
8,线上部署需要配置邮箱服务器，配置文件是/etc/postfix/main.cf，程序是调用本地的smtp来发邮件的

##############################update config###########################
setting.py里面添加一个配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{    ------------------>添加行
            'splitt': 'cmdb.tag.splitt',   --------------------->添加行
        },
    },
}
#################################################
