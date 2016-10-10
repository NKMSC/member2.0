# -*- coding: utf-8 -*-
import re
import smtplib 
import httplib, urllib
import datetime
import json
import hashlib
import threading
import time
from settings import debug
from settings import CURRENT_YEAR
from django.template.loader import get_template
from django.template import Context
from email.mime.text import MIMEText
from database.models import *
from smsTool import sendSMS
from constant_number import * # 引入常量

def sendMailFreshRegConfirm(freshMember):#发送确认信息的邮件，只发送给一个人
    sendMail=get_template('freshReg/manage/mail_regConfirm.html')
    #sendMail = get_template('freshReg/manage/apologize.html')

    if freshMember.aspiration1==u'技术部' or freshMember.aspiration2==u'技术部':
        written_test = True
    else:
        written_test = False

    sendMailHtml = sendMail.render(Context({'fm':freshMember,'test_date':u'10月九日晚上7点到8点半','test_room':'综合教学楼B104','written_test':written_test}))
    sub = u'南微软注册信息确认'
    return sendEmail(freshMember.mailbox,sub,sendMailHtml,freshMember.student_id,"注册信息验证")

def sendMailTestInformation(freshMember):#发送确认信息的邮件，只发送给一个人
    sendMail=get_template('freshReg/manage/mail_regConfirm.html')
    #sendMail = get_template('freshReg/manage/apologize.html')

    if freshMember.aspiration1==u'技术部' or freshMember.aspiration2==u'技术部':
        written_test = True
    else:
        written_test = False

    sendMailHtml = sendMail.render(Context({'fm':freshMember,'written_test':written_test}))
    sub = u'南微软笔试时间通知'
    return sendEmail(freshMember.mailbox,sub,sendMailHtml,freshMember.student_id,"笔试时间通知")

def sendMailInterviewQualification(freshMember):#发送是否进入面试的邮件，只发送给一个人
    sendMail=get_template('freshReg/manage/mail_interview.html')
    sendMailHtml=sendMail.render(Context({'freshMember':freshMember,"testTime":"","testLocation":""}))
    sub=u'南微软面试资格通知'
    return sendEmail(freshMember.mailbox,sub,sendMailHtml,freshMember.student_id,"面试资格通知")

def sendMailFinalResult(freshMember):#发送最终录取结果的邮件，只发送给一个人
    sendMail=get_template('freshReg/manage/mail_finalresult.html')
    if not debug: # 本地调试则将转至本地
        weburl = "http://nkumstcer.applinzi.com/"
    else:
        weburl = "http://127.0.0.1:8000/login/"
    sendMailHtml=sendMail.render(Context({'freshMember':freshMember,'weburl':weburl}))
    sub=u'南微软录取结果通知'
    return sendEmail(freshMember.mailbox,sub,sendMailHtml,freshMember.student_id,"录取结果通知")



def sendMailLst_testlocationtime():
    #告知笔试地点时间
    freshMemberList = FreshMembers.objects.filter(aspiration1=u'技术部',register_year=CURRENT_YEAR) | FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部',register_year=CURRENT_YEAR)
    status=True
    for freshMember in freshMemberList:
        if not sendMailTestInformation(freshMember):
            status=False
    return status


def sendMailLst_interviewqulification():
    #选取参加笔试的人，发送笔试结果
    freshMemberList = FreshMembers.objects.filter(aspiration1=u'技术部',register_year=CURRENT_YEAR) | FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部',register_year=CURRENT_YEAR)
    status=True
    for freshMember in freshMemberList:
        if not sendMailInterviewQualification(freshMember):
            status=False
    return status

def sendMailLst_finalResult():
    #选取参加面试的人，发送录取结果
    freshMemberList=FreshMembers.objects.filter(interviewqualification=1,register_year=CURRENT_YEAR)
    status=True
    for freshMember in freshMemberList:
        if freshMember.memberqualifiction == 1:# 数据库中的笔误
            freshmember2user(freshMember) # 将该人注册
        if not sendMailFinalResult(freshMember):
            status=False
    return status

def sendEmail(email,sub,content,student_id,mail_abstract):
    status = send_mail([email],sub,content)	
    mail_record = EmailHistory()
    mail_record.student_id = student_id
    mail_record.time = datetime.datetime.now()
    mail_record.abstract = mail_abstract
    mail_record.status = status
    mail_record.email = email
    mail_record.save()
    return status    

def send_mail(to_list,sub,content):  
    #mail_user="member@nkumstc.cn"    #用户名
    #mail_pass="password"   #密码
    #mail_host="smtp.qq.com"  #设置服务器
    #mail_user="member@nkumstc.cn"    #用户名
    #mail_pass="LIUCE20103301"   #密码
    mail_host = "smtp.yeah.net"
    mail_user = "nkumstc@yeah.net"
    mail_pass = "poi23333"
    me="南微软"+"<"+mail_user+">"  
    msg = MIMEText(content,_subtype='html',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string()) 
        time.sleep(4) 
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False
#mailto_list=["XXX@qq.com"] # 发送对象的列表
# send_mail(mailto_list,"hello","hello world！")

def check_input(str,strType = 'null'):
    if strType == 'null':
        if str == 'null':
            return 0
        else:
            return 1
    if strType == 'email':
        p=re.compile(r'^([\w\d]+)([\d\w\_\.]+)@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?(?:\.[\d\w]+)?$')
        m=p.match(str)
        if m==None:
            return 0
        else:
            return 1
    if strType == 'phoneNumber':
        p=re.compile(r'^(?:\+86)?(\d{3})\d{8}$|^(?:\+86)?(0\d{2,3})\d{7,8}$')
        m=p.match(str)
        if m==None:
            return 0
        else:
            return 1

    if strType == 'studentID':
        return 1
        #p=re.compile(r'^\d{7}$')
        #q=re.compile(r'^\d{10}$')
        #m=p.match(str)
        #n=q.match(str)
        #if m==None and n==None:
        #    return 0
        #else:
        #    return 1
def sendSMSList(freshMemberList,param,templateId):
    SMSStatus=True
    for freshMember in freshMemberList:
        
        name = freshMember.name
        tempid=templateId
        param=name+","+param
        phone=freshMember.phonenumber

        responseStirng=sendSMS(phone,param,templateId)
        #返回的json示例
        #{"resp":{"respCode":"000000","templateSMS":{"createDate":"20151008205027","smsId":"e5e8da5a0062c808fe399dc94049ce15"}}}
        responseCode = json.loads(responseStirng)['resp']['respCode']
        SMSRecord=SmsHistory()
        SMSRecord.fresh_member_id=freshMember.id
        SMSRecord.time=datetime.datetime.now()
        SMSRecord.sms_abstract=templateId
        SMSRecord.response_json=json
        SMSRecord.responseCode=responseCode
        if responseCode=="000000":
            SMSRecord.status=1
        else :
            SMSRecord.status=0
            SMSStatus=False
        SMSRecord.save()
    return SMSStatus

def sendSMSLst_testlocationtime(freshMemberList):
    #告知笔试地点时间
    status=sendSMSList(freshMemberList,"10月9日晚7点到8点半,综合教学楼b104",TEMPLATE_ID['testlocationtime'])
    return status

def check_migrate_status(freshmember):# 检查纳新人员是否已经迁移进了通讯录
    if User.objects.filter(studentid=int(freshmember.student_id)).exists():
        return True
    else:
        return False

def freshmember2user(freshmember):
    u=User() # 新建一个User对象，把它存入数据库
    #password =  freshmember.student_id #从表单里拿到密码
    #mail
    #name =  request.POST['name']
    #if name=='':
    #    return HttpResponse('注册失败！请填写真实姓名')
    #invitecode =  request.POST['invitecode']
    #if invitecode=='':
    #    return HttpResponse('注册失败！请填写邀请码')
    #sec = request.POST['sec']
    #if sec==u'主席团':
    #    u.sec=Section.objects.get(id=2)
    #if sec==u'技术部':
    #    u.sec=Section.objects.get(id=1)
    #if sec==u'运营部':
    #    u.sec=Section.objects.get(id=3)
    #if sec==u'宣传部':
    #    u.sec=Section.objects.get(id=4)
    #if sec==u'顾问团':
    #    u.sec=Section.objects.get(id=5)

    name = freshmember.name
    college = freshmember.major
    password = freshmember.student_id 
    grade = freshmember.grade
    campus = freshmember.campus
    phone = freshmember.phonenumber
    sec = freshmember.finalaspiration
    email = freshmember.mailbox
    if sec==u'主席团':
        u.sec=Section.objects.get(id=2)
    if sec==u'技术部':
        u.sec=Section.objects.get(id=1)
    if sec==u'运营部':
        u.sec=Section.objects.get(id=3)
    if sec==u'宣传部':
        u.sec=Section.objects.get(id=4)
    if sec==u'顾问团':
        u.sec=Section.objects.get(id=5)
    u.school='南开大学'
    u.email=email
    u.id = freshmember.student_id
    u.password=hashlib.sha1(password).hexdigest() # 这是生成hash值代替明文的密码
    u.name=name
    u.college=college
    u.grade=grade
    u.campus=campus
    u.phone=phone
    u.effective=1
    u.authority=0

    try: # 测试邮箱是否已经被使用过了
        User.objects.get(email = email)
    except User.DoesNotExist:
        pass
    else:
        return HttpResponse("该邮箱已被注册,请您换一个未被注册过的有效邮箱进行转换!")
    
    u.save()
