from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):     #创建数据库类，库中表名为account_userprofile
    user = models.OneToOneField(User, unique=True)    #本类和User类一对一，即本表和auth_user表一对一，本表以user为唯一性，意思就是说所有获取数据都要通过user字段
    birth = models.DateField(blank=True, null=True)   #定义生日字段，blank=True是可以为空
    phone = models.CharField(max_length=20, null=True)  #定义电话字段

    def __str__(self):      #传给views的数据类型，显示的内容
        return 'user {}'.format(self.user.username)  #.format为字符串格式化，format后返回一个新的字符串，从0开始编号



class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True)
    school = models.CharField(max_length=100, blank=True)       # blank允许为空
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)

    def __str__(self):
        return "user:{}".format(self.user.username)    #以字符串形式，对外显示


