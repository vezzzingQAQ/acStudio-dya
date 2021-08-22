#中间件
#2021.8.22
from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse, HttpResponseRedirect
#异常测试
import traceback
#发送邮件
from django.core import mail
#引入自定义收件人
from django.conf import settings
#捕获异常并发送邮件
class ExceptionMW(MiddlewareMixin):
    def process_exception(self,request,exception):
        texttemp=""
        texttemp+="error:"+str(exception)+"\n"
        texttemp+="error_ip:"+str(request.META["REMOTE_ADDR"])+"\n"
        texttemp+="error_path:"+str(request.path_info)+"\n"
        texttemp+="error_detail:"+str(traceback.format_exc())+"\n"
        print(texttemp)
        mail.send_mail(subject="caacodingpalace报错>v(っ °Д °;)っ",message=texttemp,from_email="1932966162@qq.com",recipient_list=settings.MY_EMAIL)
        return HttpResponse("网站卡bug了 正在联系运维(○´･д･)ﾉ")
