from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserInfoForm  #导入表单类
from django.contrib.auth.decorators import login_required    #导入装饰器
from .models import UserProfile, UserInfo            #导入数据库模型
from django.contrib.auth.models import User        #导入默认User数据库类


#自定义登录方法
def user_login(request):
    if request.method == "POST":                 #如果是登录框提交数据
        login_form = LoginForm(request.POST)     #获取提交的数据
        if login_form.is_valid():                #验证成功
            cd = login_form.cleaned_data         #获取数据
            user = authenticate(username=cd['username'], password=cd['password'])   #验证数据库密码都正确（和库里对比）

            if user:                     # 验证正确
                login(request, user)    #登录
                return HttpResponse("登录成功")    #返回给页面展示
            else:
                return HttpResponse("用户名密码不对")
        else:
            return HttpResponse("瞎输入，不识别")


    if request.method == "GET":             #如果是GET请求
        login_form = LoginForm()            #即请求页面，类似刷新
        return render(request, "account/login.html", {"form":login_form})   #将登录框显示给用户，将输出框login_form类传给html页面



# #配置注册方法1
# def register(request):
#     if request.method == "POST":                    #如果是post提交则继续
#         user_form = RegistrationForm(request.POST)  #接收数据，放到表单中，将前端提交的请求作为参数传给注册Form表单
#         if user_form.is_valid():                    #如果验证符合规范，则继续
#             new_user = user_form.save(commit=False)    #只作标记，并不真保存
#             new_user.set_password(user_form.cleaned_data['password'])   #获取输入的密码
#             new_user.save()                         #保存到库
#             return HttpResponse("注册成功")          #直接返加给页面，占整个浏览器，返回注册成功
#         else:                                       #注册不符合规范
#             return HttpResponse("抱歉，注册失败")     #返回注册失败
#     else:                                           #如果是GET请求（不是POST就是GET）
#         user_form = RegistrationForm()              #赋值空表单
#         return render(request, "account/register.html", {"form": user_form})    #将空表单传给HTML显示给用户，也叫渲染





#配置注册方法2,新增注册信息
def register(request):
    if request.method == "POST":                    #如果是post提交则继续
        user_form = RegistrationForm(request.POST)  #接收数据，放到表单中，将前端提交的请求作为参数传给注册Form表单
        userprofile_form = UserProfileForm(request.POST)    #接收前端提交的手机号和生日请求信息
        if user_form.is_valid():                    #如果验证符合规范，则继续
            new_user = user_form.save(commit=False)    #只作标记，并不真保存
            new_user.set_password(user_form.cleaned_data['password'])   #获取输入的密码
            new_user.save()                         #保存到库
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)  #效里是用户注册后在account_userinfo数据表中写入该用户的ID信息
            return HttpResponse("注册成功")          #直接返加给页面，占整个浏览器，返回注册成功
        else:                                       #注册不符合规范
            return HttpResponse("抱歉，注册失败")     #返回注册失败
    else:                                           #如果是GET请求（不是POST就是GET）
        user_form = RegistrationForm()              #赋值空表单
        userprofile_form = UserProfileForm()        #赋值空表单
        return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form}) #将空表单传给HTML显示给用户，也叫渲染,profile为HTML调用名


#根据用户获取数据，传给HTML
@login_required(login_url='/account/login/')    #装饰器，作用是必须登录才能查看信息，不登录就跳到登录的URL：/account/login/
def myself(request):
    user = User.objects.get(username=request.user.username)    #获取页面登录后的用户名
    userprofile = UserProfile.objects.get(user=user)           #根据登录的用户获取库里用户的个人信息
    userinfo = UserInfo.objects.get(user=user)                 #根据用户获取默认用户数据库表个人信息
    return render(request, "account/myself.html", {"user":user, "userinfo":userinfo, "userprofile":userprofile})  #获取的数据传给HTML



#从前端获得表单数据，更改字典值，再保存数据，返回给前端
@login_required(login_url='/account/login')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)          #根据前端请求用户获取数据
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)                  #获取user表单前端提交的信息
        userprofile_form = UserProfileForm(request.POST)    #获取Userprofile表单前端提交的信息
        userinfo_form = UserInfoForm(request.POST)          #获取Userinfo表单前端提交的信息
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():   #如果三个表单信息均验证成功
            user_cd = user_form.cleaned_data                      #获取前端输入的信息，以下同理
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd["email"])
            user.email = user_cd['email']                        #获取对应字符的前端信息并赋值给表字段的值，是更改了值
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()                                          #保存修改后的信息到数据库，以下同理
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')      #更改完数据后，页面重定向跳转到信息页
    else:
        user_form = UserForm(instance=request.user)                  # 如果是GET请求，则获取前端用户，作为表单的参数，从而获取库数据
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth, "phone":userprofile.phone})     #获取库数据
        userinfo_form = UserInfoForm(initial={"school":userinfo.school, "company":userinfo.company, "profession":userinfo.profession,
                                              "address":userinfo.address, "aboutme":userinfo.aboutme})      #获取库数居
        return render(request, "account/myself_edit.html", {"user_form":user_form,
                                                            "userprofile_form":userprofile_form, "userinfo_form":userinfo_form})   #将获取的数据定义别名，传给前端










