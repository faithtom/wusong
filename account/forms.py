
from django import forms
from django.contrib.auth.models import User     #引用内部用户类，后台admin那些用户就是这里的
from .models import UserProfile, UserInfo   #导入新数据模型

#登录表单
class LoginForm(forms.Form):         # 括号里为继承，使用父类方法，不用我们写了，直接用
    username = forms.CharField()         #用户输入框
    password = forms.CharField(widget=forms.PasswordInput)     #密码输入框


#注册表单
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)           #密码输入框
    password2 = forms.CharField(label="Confirm Pssword", widget=forms.PasswordInput)   #密码二次输入框

    #配置内部类，写入到那个库里，model指定对应的库类
    class Meta:
        model = User  #本注册类与User库(auth_user数据库)一一对应，即一对一，注册一个用户就写一条到到用户库里,即本注册类和用户类建立关联
        fields = ("username", "email")    #声明注册类和用户类共用属性，即给HTML展示的就是这个两个字段，即输入用户名和邮箱就可以注册

    def clean_password2(self):
        cd = self.cleaned_data                          #获取验证后的密码字典数据，会执行is_valid验证
        if cd['password'] != cd['password2']:           #判断两次输入密码是否一致
            raise forms.ValidationError('密码不一致')    #raise异常处理，抛异常，直接抛不向下执行
        return cd['password2']


#新墙注册信息表单
class UserProfileForm(forms.ModelForm):
    class Meta:                #共用属性
        model = UserProfile    #本表单和UserProfile库类一对一
        fields = ("phone", "birth")   #过滤展示，显示给views的内容


#用户信息表
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo       #本类和UserInfo一对一
        fields = ("school", "company", "profession", "address", "aboutme")   #显示给前端的内容


# auth_user数据库表信息，只对前端显示邮箱
class UserForm(forms.ModelForm):
    class Meta:
        model = User            #本类与User类（auth_user表）一对一
        fields = ("email",)    #只对前端显示邮箱



