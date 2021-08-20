from django.db import models

# Create your models here.
class User(models.Model):
    #登录登出
    username=models.CharField("用户名",max_length=30,unique=True)#不能重复
    password=models.CharField("密码",max_length=32)

    #积分等级
    score=models.IntegerField(default=10)
    level=models.IntegerField(default=0)

    #个人足迹
    project_number=models.IntegerField(default=0)#创建的项目数量
    comment_number=models.IntegerField(default=0)#留下的评论数

    #个人主页
    head_portrait=models.CharField(max_length=50,default="default.jpg")
    introduction=models.CharField(max_length=255,default="这人啥都没留v(○´･д･)ﾉ")#一句话
    sex=models.IntegerField(default=0)#0男1女
    grade=models.IntegerField(default=1)#1234大一-大四567研一-研三8老师
    profession=models.CharField(default="艺术与科技",max_length=30)#专业

    created_time=models.DateTimeField("创建时间",auto_now_add=True)
    update_time=models.DateTimeField("更新时间",auto_now=True)

    state=models.IntegerField(default=1)#状态:1正常,0删除

    def __str__(self):
        return("用户"+self.username+",score"+self.score+",level"+self.level)