from django.http import request
from django.shortcuts import render
from django.core.paginator import Paginator
from zprojects.models import Project,Comment
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
    try:
        #增加分类查找功能
        kw=request.GET.get("keyWord",None)
        mypara=""#用于储存搜索条件
        if kw is not None:
            ulist=Project.objects.filter(type=kw)#模糊查询name字段
            mypara="?keyWord=%s"%(kw)
        else:
            ulist=Project.objects.filter()
            ulist=ulist.order_by("-created_time")
        p=Paginator(ulist,28)#4条数据一页
        #判断页码值是否有效
        if currentPage<1:
            currentPage=1
        if currentPage>p.num_pages:
            currentPage=p.num_pages
        #重新返回表格
        currentlist=p.page(currentPage)

        uploadContext={"projectsList":currentlist,"currentPage":currentPage,"pagesList":p.page_range,"mypara":mypara}
        return(render(request,"projects/index.html",uploadContext))#加载模板
    except:
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

    mypic=request.FILES.get("pic",None)#上传的图片
    if not mypic:
        return(HttpResponse("没有上传的文件信息"))
    
    #{
    print(mypic)
    #}
    picname=str(time.time())+"."+mypic.name.split(".").pop()#随机时间戳+原来的后缀名
    destination=open("static/projects/coverPicturesTemp/"+picname,"wb+")

    for chunk in mypic.chunks():#分块读取上传文件内容并写入目标文件
        destination.write(chunk)
    destination.close()

    #用Pillow实现图片自动缩放成75*75,也可以用来加水印
    im=Image.open("static/projects/coverPicturesTemp/"+picname)
    im.thumbnail((375,375))
    im.save("static/projects/coverPictures/"+picname,None)

    os.remove("static/projects/coverPicturesTemp/"+picname)
    #图片操作*****************************************************
    currentProject.cover_portrait=picname
    #写入.zip文件
    myfile=request.FILES.get("pjt",None)#上传的zip
    if not myfile:
        return(HttpResponse("没有上传的文件信息"))
    filename=str(time.time())+"."+myfile.name.split(".").pop()#随机时间戳+原来的后缀名
    destination=open("static/projects/repository/"+filename,"wb+")
    for chunk in myfile.chunks():#分块读取上传文件内容并写入目标文件
        destination.write(chunk)
    destination.close()
    #********
    currentProject.repository=filename

    currentProject.save()

    #积分加成
    currentUser=User.objects.get(id=request.session["userid"])
    currentUser.score+=5
    currentUser.save()

    return(HttpResponse("添加成功"))
#**********************************************************************
#返回项目的详细页面,传入一个项目id
@check_login
def delete_project_action(request,projectId=0):
    delProject=Project.objects.get(id=projectId)
    if delProject.user_id==request.session["userid"]:
        os.remove("static/projects/coverPictures/"+delProject.cover_portrait)
        if delProject.repository!="empty.zip":
            os.remove("static/projects/repository/"+delProject.repository)
        delProject.delete()
    else:
        return(HttpResponse(request,"不好意思你没有权限"))
    #只有用户自己可以删除,所以直接传入session
    return(HttpResponseRedirect("/users/showUserInfoPage/"+str(request.session["userid"])+"/1"))
#**********************************************************************
#返回项目的详细页面,传入一个项目id
@check_login
def show_project_page(request,projectId=1):
    currentPorject=Project.objects.get(id=projectId)
    currentComments=Comment.objects.filter(project_id=projectId)
    for comment in currentComments:
        comment.author_name=User.objects.get(id=comment.user_id).username
        comment.author_head_portrait=User.objects.get(id=comment.user_id).head_portrait
    uploadContext={"project":currentPorject,"commentsList":currentComments}
    #print(currentPorject)
    return(render(request,"projects/showProject.html",uploadContext))
#**********************************************************************
#添加评论
@check_login
def add_comment_action(request):
    currentComment=Comment()
    currentComment.user_id=request.session["userid"]
    currentComment.project_id=request.POST["projectId"]
    currentComment.content=request.POST["content"]
    currentComment.save()
    return(HttpResponseRedirect("/projects/showProjectPage/"+request.POST["projectId"]))


