from django.http.response import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from zusers.models import User
from zprojects.models import Project
import hashlib
import time,os
from PIL import Image
from django.core.paginator import Paginator
#发送邮件
from django.core import mail
import random
# Create your views here.
#**********************************************************************
#验证码
ecode=""
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
#返回登录界面
def register_page(request):
    return(render(request,"users/register.html"))
#**********************************************************************
#发送验证码
def send_ecode_action(request,email):
    global ecode
    ecode=""
    for i in range(8):
        currentNumber=int(random.randrange(0,9))
        ecode+=str(currentNumber)
    #{
    print("--register:ecode:"+ecode)
    #}
    tempstr="验证码:\n"+ecode
    mail.send_mail(subject="验证码",message=tempstr,from_email="1932966162@qq.com",recipient_list=[email])
    return(JsonResponse({"state":0}))
#**********************************************************************
#进行注册
def register_action(request):
    global ecode
    username=request.POST["username"]
    password_1=request.POST["password_1"]
    password_2=request.POST["password_2"]
    currentEcode=request.POST["ecode"]
    email=request.POST["email"]
    if password_1!=password_2:
        uploadContext={"info":"两次密码不一致"}
        return(render(request,"users/registerError.html",context=uploadContext))

    #hash加密
    m=hashlib.md5()
    m.update(password_1.encode())
    password_m=m.hexdigest()

    #用户名是否已经存在
    old_users=User.objects.filter(username=username)
    if old_users:
        uploadContext={"info":"该用户名(%s)已存在"%(username)}
        return(render(request,"users/registerError.html",context=uploadContext))

    #实现注册后免登录【默认14天】
    if currentEcode!=ecode:
        uploadContext={"info":"验证码错误"}
        return(render(request,"users/registerError.html",context=uploadContext))

    #插入数据
    try:
        new_user=User.objects.create(username=username,password=password_m,email=email)
        #{
        print("--create user:username=%s;userpassword=%s"%(username,password_1))
        #}
    except Exception as e:
        #{
        print("--create user error %s"%(e))
        #}
        uploadContext={"info":"该用户名已存在"}
        return(render(request,"users/registerError.html",context=uploadContext))


    request.session["username"]=username
    request.session["userid"]=new_user.id

    return(HttpResponseRedirect("/projects/indexPage/1"))
#**********************************************************************
def login_page(request):
    if request.session.get("username") and request.session.get("userid"):
        return(HttpResponse("已登录(%s)"%(request.session.get("username"))))
    else:
        return(render(request,"users/login.html"))
#**********************************************************************
#登录
def login_action(request):
    username=request.POST["username"]
    password=request.POST["password"]

    #先遍历数据库查找有没有这个用户
    try:
        user=User.objects.get(username=username)
    except Exception as e:
        #{
        print("--login user error %s"%(e))
        #}
        uploadContext={"info":"用户名或密码错误"}
        return(render(request,"users/loginError.html",context=uploadContext))

    #判断用户状态0删除
    if user.state==0:
        uploadContext={"info":"用户名或密码错误"}
        return(render(request,"users/loginError.html",context=uploadContext))
    
    #找到用户,比对密码
    m=hashlib.md5()
    m.update(password.encode())
    if m.hexdigest()!=user.password:
        uploadContext={"info":"用户名或密码错误"}
        return(render(request,"users/loginError.html",context=uploadContext))

    #用户名密码都对
    request.session["username"]=username
    request.session["userid"]=user.id

    resp=HttpResponseRedirect("/projects/indexPage/1")

    return(resp)
#**********************************************************************
@check_login
#退出登录
def logout_action(request):
    if "username" in request.session:
        del request.session["username"]
    if "userid" in request.session:
        del request.session["userid"]
    return(HttpResponseRedirect("/users/loginPage"))
#**********************************************************************
#改变用户设置主题页
@check_login
def change_user_settings_page(request):
    return(render(request,"users/userSettings.html"))
#**********************************************************************
#改变用户设置
@check_login
def change_user_settings_action(request):
    currentUser=User.objects.get(username=request.session["username"])
    currentUser.introduction=request.POST["introduction"]
    #用户名
    currentUser.username=request.POST["username"]
    #性别
    if request.POST["sex"]=="man":
        currentUser.sex=0
    else:
        currentUser.sex=1
    #年级
    if request.POST["grade"]=="d1":
        currentUser.grade=1
    elif request.POST["grade"]=="d2":
        currentUser.grade=2
    elif request.POST["grade"]=="d3":
        currentUser.grade=3
    elif request.POST["grade"]=="d4":
        currentUser.grade=4
    elif request.POST["grade"]=="y1":
        currentUser.grade=5
    elif request.POST["grade"]=="y2":
        currentUser.grade=6
    elif request.POST["grade"]=="y3":
        currentUser.grade=7
    elif request.POST["grade"]=="tc":
        currentUser.grade=8
    #专业
    currentUser.profession=request.POST["profession"]
    #头像
    myfile=request.FILES.get("pic",None)#上传的图片
    if not myfile:
        return(HttpResponse("没有上传的文件信息"))
    
    #{
    print(myfile)
    #}
    #先删掉原来的头像
    try:
        os.remove("static/users/headPictures/"+str(currentUser.head_portrait))
        os.remove("static/users/headPicturesSmall/"+str(currentUser.head_portrait))
    except:
        #{
        print("error") 
        #}

    filename=str(time.time())+"."+myfile.name.split(".").pop()#随机时间戳+原来的后缀名
    destination=open("static/users/headPicturesTemp/"+filename,"wb+")
    for chunk in myfile.chunks():#分块读取上传文件内容并写入目标文件
        destination.write(chunk)
    destination.close()

    #大头像
    im=Image.open("static/users/headPicturesTemp/"+filename)
    im.thumbnail((375,375))
    im.save("static/users/headPictures/"+filename,None)
    #小头像
    im=Image.open("static/users/headPicturesTemp/"+filename)
    im.thumbnail((55,55))
    im.save("static/users/headPicturesSmall/"+filename,None)

    os.remove("static/users/headPicturesTemp/"+filename)
    currentUser.head_portrait=filename
    #currentProject.author_head_portrait=User.objects.get(id=request.session["userid"]).head_portrait
    currentProjects=Project.objects.filter(user_id=request.session["userid"])
    for project in currentProjects:
        project.author_head_portrait=filename
        project.author_name=currentUser.username
        project.save()
    
    currentUser.save()
    return(HttpResponse("修改成功"))
#**********************************************************************
#用户主页
@check_login
def show_user_info_page(request,userId=1,currentPage=1):
    isAdmin=False#是否是已经登录的用户自己
    currentUser=User.objects.get(id=userId)
    if currentUser.id==request.session["userid"]:
        isAdmin=True
    curentProjects=Project.objects.filter(user_id=userId)
    curentProjects=curentProjects.order_by("-created_time")
    p=Paginator(curentProjects,4)#4条数据一页
    #判断页码值是否有效
    if currentPage<1:
        currentPage=1
    if currentPage>p.num_pages:
        currentPage=p.num_pages
    #重新返回表格
    projectsList=p.page(currentPage)

    uploadContext={"currentUser":currentUser,"projectsList":projectsList,"currentPage":currentPage,"pagesList":p.page_range,"isAdmin":isAdmin}
    return(render(request,"users/showUserInfo.html",uploadContext))
