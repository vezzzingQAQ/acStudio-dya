from django.db import models
from django.db.models.deletion import CASCADE
from zusers.models import User
# Create your models here.
class Project(models.Model):
    title=models.CharField(default="新建项目",max_length=50)
    introduction=models.TextField("介绍")
    code=models.TextField("code")
    type=models.CharField(default="processing.py",max_length=50)
    cover_portrait=models.CharField(max_length=50,default="defaultCover.jpg")

    repository=models.CharField(max_length=50,default="empty.zip")#项目源文件
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    state=models.IntegerField(default=1)#状态:1正常,0删除

    author_head_portrait=models.CharField(max_length=50,default="default.jpg")#作者头像
    author_name=models.CharField("用户名",max_length=30,default="无名氏")

    good_number=models.IntegerField(default=0)#点赞数

    created_time=models.DateTimeField("创建时间",auto_now_add=True)
    update_time=models.DateTimeField("更新时间",auto_now=True)

    def __str__(self):
        #return("项目"+self.title+",创建者"+str(self.user_id)+",type"+self.type+",内容"+self.code)
        return("项目"+self.title+",创建者"+str(self.user_id)+",type"+self.type)

class Comment(models.Model):
    #备份
    author_head_portrait=models.CharField(max_length=50,default="default.jpg")#作者头像
    author_name=models.CharField("用户名",max_length=30,default="无名氏")

    good_number=models.IntegerField(default=0)#点赞数

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    project=models.ForeignKey(Project,on_delete=CASCADE)

    content=models.TextField("content")

    created_time=models.DateTimeField("创建时间",auto_now_add=True)
    update_time=models.DateTimeField("更新时间",auto_now=True)
