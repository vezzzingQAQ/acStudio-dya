from django.http import request
from django.shortcuts import render
from django.core.paginator import Paginator
from zprojects.models import Project
from zusers.models import User
from django.http import HttpResponse,HttpResponseRedirect
import time,os
from PIL import Image

# Create your views here.
#**********************************************************************
#◉在函数被执行前会先执行装饰器
def check_login(fn):
    def warp(request,*args,**kwargs):
        #这里写判断
        if "username" not in request.session or "userid" not in request.session:
                return(HttpResponseRedirect("/users/loginPage"))
        return fn(request,*args,**kwargs)
    return warp
#**********************************************************************
@check_login
def index_page(request,currentPage=1):
    #try:
        ulist=Project.objects.filter()
        p=Paginator(ulist,4)#4条数据一页
        #判断页码值是否有效
        if currentPage<1:
            currentPage=1
        if currentPage>p.num_pages:
            currentPage=p.num_pages
        #重新返回表格
        currentlist=p.page(currentPage)
        #传输作者头像信息
        #for project in currentlist:

        uploadContext={"projectsList":currentlist,"currentPage":currentPage,"pagesList":p.page_range}
        return(render(request,"projects/index.html",uploadContext))#加载模板
    #except:
        return(HttpResponse("没有找到信息(○´･д･)ﾉ"))
#**********************************************************************
@check_login
def add_project_page(request):
    return(render(request,"projects/addProject.html"))
#**********************************************************************
def add_project_action(request):
    currentProject=Project()
    currentProject.title=request.POST["title"]
    currentProject.introduction=request.POST["introduction"]
    currentProject.code=request.POST["code"]
    currentProject.type=request.POST["type"]
    currentProject.user_id=request.session["userid"]
    currentProject.author_head_portrait=User.objects.get(id=request.session["userid"]).head_portrait
    currentProject.author_name=User.objects.get(id=request.session["userid"]).username

    myfile=request.FILES.get("pic",None)#上传的图片
    if not myfile:
        return(HttpResponse("没有上传的文件信息"))
    
    #{
    print(myfile)
    #}
    filename=str(time.time())+"."+myfile.name.split(".").pop()#随机时间戳+原来的后缀名
    destination=open("static/projects/coverPicturesTemp/"+filename,"wb+")

    for chunk in myfile.chunks():#分块读取上传文件内容并写入目标文件
        destination.write(chunk)
    destination.close()

    #用Pillow实现图片自动缩放成75*75,也可以用来加水印
    im=Image.open("static/projects/coverPicturesTemp/"+filename)
    im.thumbnail((375,375))
    im.save("static/projects/coverPictures/"+filename,None)

    os.remove("static/projects/coverPicturesTemp/"+filename)
    #图片操作*****************************************************

    currentProject.cover_portrait=filename

    currentProject.save()

    return(HttpResponse("添加成功"))
#**********************************************************************
#返回项目的详细页面,传入一个项目id
@check_login
def show_project_page(request,projectId=1):
    currentPorject=Project.objects.get(id=projectId)
    uploadContext={"project":currentPorject}
    print(currentPorject)
    return(render(request,"projects/showProject.html",uploadContext))

