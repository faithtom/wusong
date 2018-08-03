from django.contrib import admin
from .models import UserProfile  #导入新增数据库模型


#创建DJANGO后台显示类，必须按"数据库模型类+Admin方式写，即UserProfileAdmin"
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone')     #中间栏显示内容
    list_filter = ('phone',)                     #右侧边栏显示内容


admin.site.register(UserProfile, UserProfileAdmin)   #将数据模型类和显示类注册到后台



