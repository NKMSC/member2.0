# -*- coding: utf-8 -*-
import re
import random
import hashlib
import smtplib 
import httplib, urllib 
import django.core.exceptions
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context
from database.models import Activity , Code,Log,Section,User,UserTakePartInActivity, Reg,FreshMembers, EmailHistory
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage,InvalidPage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from constant_number import * # 引入常量
from util import *
from settings import CURRENT_YEAR,PERIOD, PERIOD_TIME
from django.shortcuts import render_to_response
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#def temp_sendmail(request):
#    user=request.session.get('manager')
#    if user is None:
#        login=get_template('freshReg/manage/login.html')
#        loginHtml=login.render(Context({'errors':False}))
#        return HttpResponse(loginHtml)
    


def test(request):
    test=get_template('freshReg/manage/base.html')
    testHtml=test.render(Context())
    return HttpResponse(testHtml)

def home(request):
    return HttpResponse('this is home')

#def reg(request):#注册
#    try:
#        invitecode=request.GET.get('invitecode', '')
#    except ValueError: 
#        invitecode = ''
#    reg=get_template('reg.html')
#    regHtml=reg.render(Context({'invitecode':invitecode}))
#    return HttpResponse(regHtml)

#@csrf_exempt
#def reg_result(request): # 注册的结果页面
#    u=User() # 新建一个User对象，把它存入数据库
#    password =  request.POST['password'] #从表单里拿到密码
#    if password=='': # 没填密码
#        return HttpResponse('注册失败！请填写密码')
#    email =  request.POST['email']
#    if email=='':# 没填邮箱
#        return HttpResponse('注册失败！请填写邮箱')
#    name =  request.POST['name']
#    if name=='':
#        return HttpResponse('注册失败！请填写真实姓名')
#    invitecode =  request.POST['invitecode']
#    if invitecode=='':
#        return HttpResponse('注册失败！请填写邀请码')
#    sec = request.POST['sec']
#    if sec==u'主席团':
#        u.sec=Section.objects.get(id=2)
#    if sec==u'技术部':
#        u.sec=Section.objects.get(id=1)
#    if sec==u'运营部':
#        u.sec=Section.objects.get(id=3)
#    if sec==u'宣传部':
#        u.sec=Section.objects.get(id=4)
#    if sec==u'顾问团':
#        u.sec=Section.objects.get(id=5)
    
#    college = request.POST['college']
#    major = request.POST['major']
#    entry_year = request.POST['entry_year']
#    grade = request.POST['grade']
#    campus = request.POST['campus']
#    sex = request.POST['sex']
#    phone = request.POST['phone']
#    province = request.POST['province']
#    city = request.POST['city']
#    area = request.POST['area']
#    qq = request.POST['qq']
#    love = request.POST['love']
#    #city = request.POST['city']

#    u.school='南开大学'
#    u.email=email
#    u.password=hashlib.sha1(password).hexdigest() # 这是生成hash值代替明文的密码
#    u.name=name
#    u.college=college
#    u.major=major
#    u.entry_year=entry_year
#    u.grade=grade
#    u.campus=campus
#    u.sex=sex
#    u.phone=phone
#    u.province=province
#    u.city=city
#    u.area=area
#    u.qq=qq
#    u.love=love
#    u.effective=1
#    u.authority=0

#    try: # 测试邮箱是否已经被使用过了
#        User.objects.get(email = email)
#    except User.DoesNotExist:
#        pass
#    else:
#        return HttpResponse("该邮箱已被注册,请您换一个未被注册过的有效邮箱进行注册!")

#    try:
#        c=Code.objects.get(code=invitecode)
#        if c.effective==0:
#            return HttpResponse("该邀请码已经被使用过了！请确认您拥有正确的邀请码！")
#        else:
#            u.save()
#            c.effective=0
#            c.use =User.objects.get(email = email)  # 把验证码和用户关联上
#            c.save()
#    except Code.DoesNotExist:
#        return HttpResponse("该邀请码不存在！请确认您拥有正确的邀请码！")
    
#    request.session['user']=u # 把user对象放到session里面去
#    result=get_template('result.html')
#    resultHtml=result.render(Context({'result':'You have registered successfully! <a href="/index/">click this to turnback</a>',
#                                    'meta':'http-equiv="refresh" content="2;url=/index/" '},autoescape=False))#防止将'<'、 '/'和'>'自动转义
#    return HttpResponse(resultHtml)

def login(request):
    user=request.session.get('user')
    if user is None:
        login=get_template('login.html')
        loginHtml=login.render(Context())
        return HttpResponse(loginHtml)
    else:
        return HttpResponseRedirect("/index/")# 跳转到个人主页

def index(request):# 显示自己的详细信息
    index=get_template('index.html')
    user=request.session.get('user')# 从session对象里面拿出user对象，session是运行这个网站时，每个页面
    if user is None: #都共有的一个公共对象，所以可以利用它来在各个页面之间传递参数之类
        return HttpResponse("请先登录！")# 如果session里面没有user对象，说明用户并没有登陆，所以返回错误页面
    #user = {'name': 'Sally', 'depart':'技术部','grade':'大一','college':'软件学园','major':'软件工程','phone':'15224652255','QQ':'7983452798'}
    
    indexHtml=index.render(Context({'user':user}))
    return HttpResponse(indexHtml)

def index_of_others(request,offset):# 显示别人的详细信息
    # offset是其他用户的name
    index=get_template('index_of_others.html')
    user=User.objects.get(id=int(offset))# 从数据库里查找所点击的用户
    u=request.session.get('user')# 没登陆的话报错
    if u is None:
        return HttpResponse("请先登录！")
    indexHtml=index.render(Context({'user':user}))
    return HttpResponse(indexHtml)

@csrf_exempt
def edit(request):
    edit=get_template('edit.html')
    user=request.session.get('user')
    if user is None:
        return HttpResponse("请先登录！")
    editHtml=edit.render(Context({'user':user}))
    return HttpResponse(editHtml)

@csrf_exempt
def edit_result(request):# 编辑页面返回的结果
    sex= request.POST['sex']# 从前台的表单中拿回各种数据
    sec=request.POST['sec']
    college= request.POST['college']
    major= request.POST['major']
    grade= request.POST['grade']
    phone= request.POST['phone']
    qq= request.POST['qq']
    province= request.POST['province']
    city= request.POST['city']
    area= request.POST['area']
    campus= request.POST['campus']
    wechat= request.POST['wechat']
    love= request.POST['love']
    dormitory= request.POST['dormitory']
    u=request.session.get('user')
    email=u.email
    user=User.objects.get(email=email)#数据库里拿到所编辑的对象
    if user is None:
        return HttpResponse("请先登录！")
    
    user.sex=sex
    user.college=college
    user.major=major
    user.grade=grade
    user.phone=phone
    user.qq=qq
    user.province=province
    user.city=city
    user.area=area
    user.campus=campus
    user.wechat=wechat
    user.love=love
    user.dormitory=dormitory# 保存修改
    user.sec=Section.objects.get(id=sec)
    user.save()# 修改后的对象存入数据库
    request.session['user']=user# 用新的user替换掉之前旧的session里面的user对象
    return HttpResponseRedirect("/index/")# 跳转到个人主页

def depart(request,offset):
	#depart=get_template('depart.html')
        user=request.session.get('user')
        if user is None:
            return HttpResponse("请先登录！")
	if offset=='all' :# 如果访问的网址是 depart/all的话，返回所有的用户信息
            #userlst=User.objects.all()
            userlst=User.objects.filter(effective = 1)
            paginator = Paginator(userlst, 5) # 分页系统，每页显示5个用户
            try:
                page = int(request.GET.get('page', '1'))# 访问的网址是depart/all/page=?
            except ValueError: # 这里的page对象就是“？”后面的数字，用来标记访问的第几页
                page = 1# 出错的话直接访问第一页
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            user=request.session.get('user')
            #user.name='南微软'
            #user.depart='技术部'
            isactive='active'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'user':user,'contacts':userlst,'isactive1':isactive}))
            return HttpResponse(departHtml)
        if offset=='pre' or offset=='2':# 如果访问的是depart/pre或者 depart/2，显示主席团的成员信息
            userlst=User.objects.filter(sec=2, effective=1)# 主席团的部门id是2，其他与上面相同
            user=request.session.get('user')
            paginator = Paginator(userlst, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            #user.name='南微软'
            #user.depart='技术部'
            isactive='active'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':userlst,'user':user,'isactive2':isactive}))
            return HttpResponse(departHtml)
        if offset=='tech' or offset=='1':# 技术部
            userlst=User.objects.filter(sec=1, effective=1)
            user=request.session.get('user')
            paginator = Paginator(userlst, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            #user.name='南微软'
            #user.depart='技术部'
            isactive='active'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':userlst,'user':user,'isactive3':isactive}))
            return HttpResponse(departHtml)
        if offset=='ope' or offset=='3': #运营部
            userlst=User.objects.filter(sec=3, effective=1)
            user=request.session.get('user')
            paginator = Paginator(userlst, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            #user.name='南微软'
            #user.depart='技术部'
            isactive='active'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':userlst,'user':user,'isactive4':isactive}))
            return HttpResponse(departHtml)
        if offset=='adv' or offset=='4': #宣传
            userlst=User.objects.filter(sec=4, effective=1)
            user=request.session.get('user')
            paginator = Paginator(userlst, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            #user.name='南微软'
            #user.depart='技术部'
            isactive='active'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':userlst,'user':user,'isactive5':isactive}))
            return HttpResponse(departHtml)
        if offset=='cons' or offset=='6': #顾问
            userlst=User.objects.filter(sec=6,effective=1)
            user=request.session.get('user')
            paginator = Paginator(userlst,5)
            try:
                page = int(request.GET.get('page','1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage,InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            isactive='active'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':userlst,'user':user,'isactive7':isactive}))
            return HttpResponse(departHtml)
	# 查询数百具
	# 封装对象
	#departHtml=depart.render(Context());
	#return HttpResponse(departHtml)
	if offset=='me':
            return HttpResponseRedirect("/index/")
        if offset=='logout':
            return HttpResponseRedirect("/logout/")
        if offset=='edit':
            return HttpResponseRedirect("/edit/")





def freshReg_request(request):
    regfresh=get_template('freshReg/regfresh_2buttons.html')
    regHtml=regfresh.render(Context())
    return HttpResponse(regHtml)

def freshReg_request_register(request):
    regfresh=get_template('freshReg/regfresh.html')
    regHtml=regfresh.render(Context())
    return HttpResponse(regHtml)# 跳转到freshReg_result

def freshReg_request_check(request):
    check=get_template('freshReg/regfresh_check.html')
    checkHtml=check.render(Context())
    return HttpResponse(checkHtml)

def freshReg_request_check_result(request):
    notifications = []
    #notifications.append("show sth")
    studentid = int(request.POST['studentid'])
    if FreshMembers.objects.filter(register_year = CURRENT_YEAR, student_id = studentid).exists():
        fm = FreshMembers.objects.filter(register_year = CURRENT_YEAR, student_id = studentid)[0]
        notifications.append(u"亲爱的%s同学您好！"%fm.name)
        if int(fm.student_id) in [1611476,1612849,1611385,1611473,1612831,1612888,1611532]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，我们的面试时间为%s，您可以自行选择到场时间"%("运营部/新闻媒体部","其他部门","图书馆二楼半文汇厅","9月25日周日下午6点至8点"))
        
        elif int(fm.student_id) in [1612937,1613420,1611322,1612940,1611478,1612833]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，您的面试开始时间为%s"%("运营部/新闻媒体部","其他部门","图书馆二楼半文汇厅","9月25日周日下午6点"))
        elif int(fm.student_id) in [1612847,1612851,1611317,1611527,1613545]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，您的面试开始时间为%s"%("运营部/新闻媒体部","其他部门","图书馆二楼半文汇厅","9月25日周日下午6点30分"))
        elif int(fm.student_id) in [1611343,1611358,1511395,1612840,1612895]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，您的面试开始时间为%s"%("运营部/新闻媒体部","其他部门","图书馆二楼半文汇厅","9月25日周日下午7点"))
        elif int(fm.student_id) in [1611383,1613508,1613669,1410606,1613419]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，您的面试开始时间为%s"%("运营部/新闻媒体部","其他部门","图书馆二楼半文汇厅","9月25日周日下午7点30分"))
        
        elif int(fm.student_id) in [1310650,1611321,1511509,1510193]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，您的面试开始时间为%s"%("技术部","其他部门","图书馆二楼半文汇厅","9月25日周日下午6点"))
        elif int(fm.student_id) in [1511431,1611040,1612873,1612916]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，您的面试开始时间为%s"%("技术部","其他部门","图书馆二楼半文汇厅","9月25日周日下午6点30分"))
        elif int(fm.student_id) in [1611498,1611521,1611345,1611335]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，您的面试开始时间为%s"%("技术部","其他部门","图书馆二楼半文汇厅","9月25日周日下午7点"))
        elif int(fm.student_id) in [1310652,1613594,1412623]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s（该时段也有%s面试，请注意勿走错会场），面试地点为%s，您的面试开始时间为%s"%("技术部","其他部门","图书馆二楼半文汇厅","9月25日周日下午7点30分"))

        elif int(fm.student_id) in [1611599,1611085,1611509,1612887]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s，面试地点为%s，您的面试开始时间为%s"%("技术部","图书馆二楼半文汇厅","9月24日周六下午6点"))
        elif int(fm.student_id) in [1613511,1511498,1612906,1612893]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s，面试地点为%s，您的面试开始时间为%s"%("技术部","图书馆二楼半文汇厅","9月24日周六下午6点30分"))
        elif int(fm.student_id) in [1612898,1612919,1611109,1611077]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s，面试地点为%s，您的面试开始时间为%s"%("技术部","图书馆二楼半文汇厅","9月24日周六下午7点"))
        elif int(fm.student_id) in [1612872,1611301,1612877]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s，面试地点为%s，您的面试开始时间为%s"%("技术部","图书馆二楼半文汇厅","9月24日周六下午7点30分"))
        elif int(fm.student_id) in [1613235,1611339,1612931,1510908]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s，面试地点为%s，您的面试开始时间为%s"%("技术部","图书馆二楼半文汇厅","9月24日周六下午8点"))
        elif int(fm.student_id) in [1611207,1611155,1611271]:
            notifications.append(u"您已进入面试阶段，您将面试的部门为%s，面试地点为%s，您的面试开始时间为%s"%("技术部","图书馆二楼半文汇厅","9月24日周六下午8点30分"))
            
        else:
            notifications.append(u'纳新下一阶段为%s阶段！'%(PERIOD))
            notifications.append(u'很遗憾您未获得面试资格')

        notifications.append(u'以下是您的部分个人信息：')
        notifications.append(u"电话：%s"%fm.phonenumber)
        notifications.append(u"邮箱：%s"%fm.mailbox)
        notifications.append(u"第一志愿：%s"%fm.aspiration1)
        notifications.append(u"第二志愿：%s"%fm.aspiration2)
        notifications.append(u"我们会将后续的结果通过邮件或本网页告知，请注意查看")

    else:
        notifications.append(u"该id尚未注册！")
    #check = get_template('freshReg/regfresh_check.html')
    #checkHtml = check.render(Context({"notifications":notifications}))
    return render_to_response('freshReg/regfresh_check.html',{"notifications":notifications})





@csrf_exempt
def freshReg_result(request):# 可能会调用sendMailFreshRegConfirm函数 该函数在util里面

    # 逻辑：检查手机号，学号，邮箱，任意一个
    
    email = request.POST['email']
    name = request.POST['name']
    studentid = request.POST['studentId']
    phonenumber=request.POST['phone']
    if (check_input(phonenumber,'phoneNumber') and check_input(email,'email') and check_input(name)):#and check_input(studentid,'studentID') ):因为没法检查研究生学号，所以这句话被我注释掉了==
        pass
    else:
        return HttpResponse(u'相关注册信息缺失或格式有误，请重新注册！')
        
     # 逻辑：注册年份相同时，检查学号，邮箱
     #       若任意一个相同则给出提示信息禁止注册
     # 对应情况如下
     # 学号存在：邮箱相同/不同
     # 学号不存在：邮箱存在

     # fresh2user要解决的问题
     # 会不会有其他年份的人用了邮箱a，并被录取
     # 此年份也有人使用邮箱a，被录取
     # 
    errors=[]
    if FreshMembers.objects.filter(student_id=studentid, register_year = CURRENT_YEAR):
        fm_existed = FreshMembers.objects.filter(student_id=studentid, register_year = CURRENT_YEAR)[0]
        if fm_existed.mailbox == email:
            errors.append(u"您之前已注册，请查看您的邮箱，如果没有收到邮件请检查垃圾邮件")
        else:
            errors.append(u"您之前已注册，但使用的并非此邮箱，请查看您的注册邮箱，如果没有收到邮件请与工作人员联系或使用注册首页的 STATUS 功能查看目前的纳新状态")
    elif FreshMembers.objects.filter(mailbox=email, register_year = CURRENT_YEAR).exists():
        errors.append(u"该邮箱已被您以外的人注册，请更换邮箱进行注册！")

    # 发生错误则转至原始页面
    if errors:
        return render_to_response("freshReg/regfresh.html",{"errors":errors, 'email':email, 'name':name,
                                  'studentId':studentid, 'phone':phonenumber})


    fm=FreshMembers()
    fm.register_year = CURRENT_YEAR
    fm.student_id=studentid
    fm.name=name
    fm.mailbox=email
    fm.phonenumber=phonenumber
    fm.grade=request.POST['grade']
    fm.campus=request.POST['campus']
    fm.major=request.POST['major']
    fm.aspiration1=request.POST['aspiration1']
    fm.aspiration2=request.POST['aspiration2']


    if fm.aspiration1 == u'技术部':
        fm.interviewqualification = 0
    else:
        fm.interviewqualification = 1
    fm.save()
    request.session['fresh members'] = fm
    temp = sendMailFreshRegConfirm(fm)#发送注册邮件

    notifications = []
    if temp:
        notifications.append(u'信息已注册成功！您的注册信息已发回注册邮箱，请确认！（该邮件有可能被识别为了垃圾邮件，请注意查看）')
        notifications.append(u"您也可以使用注册首页的 STATUS功能查看目前的纳新状态")
    else:
        notification.append(u'注册成功但是 发送邮件失败！请与工作人员联系或使用注册首页的 STATUS功能查看目前的纳新状态')
    return render_to_response("freshReg/regfresh.html",{"notifications":notifications, 'email':email, 'name':name,
                                  'studentId':studentid, 'phone':phonenumber})

#def resend_fresh_email(request):
#    if request.method == POST:
#        pass
#    else:
#        return HttpResponseRedirect("freshReg_request")



def sendSMSList(request):
    option = request.GET['option']
    status=False
    if option=="testlocationtime":
        #return HttpResponse("功能未开放")
        # freshMemberList = FreshMembers.objects.filter(aspiration1=u'技术部') | FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部')
        freshMemberList=FreshMembers.objects.filter(name=u'刘策')
        status=sendSMSLst_testlocationtime(freshMemberList)
    # elif option=="interviewqulification":
    #     # return HttpResponse("功能未开放")
    #     status=sendSMSLst_interviewqulification()
    # elif option=="finalresult":
    #     status=sendSMSLst_finalResult()
    else:#不应该进入这里
        return HttpResponse("error")
    
    if status:
        return HttpResponse("短信全部发送成功")
    else:
        return HttpResponse("部分短信发送失败，请查看邮件发记录")
    return HttpResponse("功能未开放")

def sendEmailList(request):
    
    option=request.GET['option']
    status=False    
    if option=="finalresult":
        
        # return HttpResponse("功能未开放")
        status=sendMailLst_finalResult()
    elif option=="interviewqualification":
        # return HttpResponse("功能未开放")
        status=sendMailLst_interviewqulification()
    elif option=="testlocationtime":
        status=sendMailLst_testlocationtime()
    else:#不应该进入这里
        return HttpResponse("error")
    
    if status:
        return HttpResponse("邮件全部发送成功")
    else:
        return HttpResponse("部分邮件发送失败，请查看邮件发记录")
    return HttpResponse("功能未开放")
def resendSMS(request):
    recordID=request.GET['id']
    SMSRecord=EmailHistory.objects.get(id=recordID)
    status=False

    if SMSRecord.sms_abstract==TEMPLATE_ID['testlocationtime']:
        freshMember=FreshMembers.objects.get(id=SMSRecord.fresh_member_id)
        status=sendSMSLst_testlocationtime([freshMember])


    if status:#success
        SMSRecord.status=1
        SMSRecord.save()
        return HttpResponse("success")

    else :#fail
        SMSRecord.status=2
        SMSRecord.save()
        return HttpResponse("fail")

def resendEmail(request):
    recordID=request.GET['id']
    emailRecord=EmailHistory.objects.get(id=recordID)
    status=False
    freshMember=FreshMembers.objects.get(mailbox=emailRecord.email)
    if emailRecord.abstract=="注册信息验证" :
        status=sendMailFreshRegConfirm(freshMember)
    elif emailRecord.abstract=="面试资格通知":
        status=sendMailInterviewQualification(freshMember)
    elif emailRecord.abstract=="录取结果通知":
        status=sendMailFinalResult(freshMember)
    elif emailRecord.abstract=="笔试时间通知":
        status=sendMailTestInformation(freshMember)
    else:# 程序不应该运行到这里
        return HttpResponse("error")
    if status:
        emailRecord.status=1
        emailRecord.save()
        return HttpResponse("成功")
    else :
        emailRecord.status=2
        emailRecord.save()
        return HttpResponse("失败")
# def individualEdit(request):
def freshSMSRecord(request):
    SMSRecordList=SmsHistory.objects.filter()
    totalCount = FreshMembers.objects.count()
    writtenCount = FreshMembers.objects.filter(aspiration1=u'技术部').count()
    writtenCount = writtenCount+FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部').count()
    interviewCount = FreshMembers.objects.filter(interviewqualification=1).count()
    SMSRecordHtml=get_template('freshReg/manage/SMS_record.html').render(Context({'SMSRecordList':SMSRecordList,'total_count':totalCount,'writen_count':writtenCount,'interview_count':interviewCount},autoescape=False))
    return HttpResponse(SMSRecordHtml)


def freshMailRecord(request):
    if request.method=="GET":#get方式访问，返回该网页
        mailRecordList=EmailHistory.objects.filter()
        totalCount = FreshMembers.objects.count()
        writtenCount = FreshMembers.objects.filter(aspiration1=u'技术部').count()
        writtenCount = writtenCount+FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部').count()
        interviewCount = FreshMembers.objects.filter(interviewqualification=1).count()
        mailRecordHtml=get_template('freshReg/manage/mail_record.html').render(Context({'mailRecordList':mailRecordList,'total_count':totalCount,'writen_count':writtenCount,'interview_count':interviewCount},autoescape=False))
        return HttpResponse(mailRecordHtml)
    else:
        return HttpResponse("error @277")

def manage_login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        if username=='nkumstc' and password=='nkumstc1234':
            request.session['manager']='nkumstc'
            return HttpResponseRedirect("/freshShow/")
        else:
            login=get_template('freshReg/manage/login.html')
            loginHtml=login.render(Context({'errors':True}))
            return HttpResponse(loginHtml)
    else:
        user=request.session.get('manager')
        if user is None:
            login=get_template('freshReg/manage/login.html')
            loginHtml=login.render(Context({'errors':False}))
            return HttpResponse(loginHtml)
        else:
            return HttpResponseRedirect("/freshShow/")

def freshReg_entryWrittenPerformance(request):
    if request.session.get('manager') is None:
        return HttpResponseRedirect("/manage/login/")

    freshManList = FreshMembers.objects.filter(aspiration1=u'技术部',register_year=CURRENT_YEAR) | FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部',register_year=CURRENT_YEAR)
    totalCount = FreshMembers.objects.filter(register_year=CURRENT_YEAR).count()
    writtenCount = FreshMembers.objects.filter(aspiration1=u'技术部',register_year=CURRENT_YEAR).count()
    writtenCount = writtenCount+FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部').count()
    interviewCount = FreshMembers.objects.filter(interviewqualification=1,register_year=CURRENT_YEAR).count()
    entryWritten = get_template('freshReg/manage/writtenscore.html')
    entryHtml=entryWritten.render(Context({'freshMemberList':freshManList,'total_count':totalCount,'writen_count':writtenCount,'interview_count':interviewCount}))
    return HttpResponse(entryHtml)

@csrf_exempt
def freshReg_performWrittenPerformance(request):
    if request.session.get('manager') is None:
            return HttpResponseRedirect("/manage/login/")
    freshManList = request.POST
    for freshMan in freshManList:
        freshManRecord = freshManList.getlist(freshMan)
        freshManNow = FreshMembers.objects.get(id = freshMan)
        if freshManNow!= None :
            if freshManRecord[0]!='':
                freshManNow.writtenscore = freshManRecord[0]
            else:
                freshManNow.writtenscore = 0
        freshManNow.save()
    return HttpResponse("信息储存成功！")

def freshShow(request):
    if request.session.get('manager') is None:
            return HttpResponseRedirect("/manage/login/")

    freshManList = FreshMembers.objects.filter(register_year=CURRENT_YEAR)
    totalCount = FreshMembers.objects.filter(register_year=CURRENT_YEAR).count()

    writtenCount = FreshMembers.objects.filter(aspiration1=u'技术部',register_year=CURRENT_YEAR).count()
    writtenCount = writtenCount+FreshMembers.objects.exclude(aspiration1=u'技术部',register_year=CURRENT_YEAR).filter(aspiration2=u'技术部',register_year=CURRENT_YEAR).count()

    interviewCount = FreshMembers.objects.filter(interviewqualification=1,register_year=CURRENT_YEAR).count()
    showAllFresh = get_template('freshReg/manage/show_all_fresh.html')
    showHtml = showAllFresh.render(Context({'freshMemberList':freshManList,'total_count':totalCount,'writen_count':writtenCount,'interview_count':interviewCount,'PERIOD':PERIOD,'PERIOD_TIME':PERIOD_TIME}))
    return HttpResponse(showHtml)

def freshInterviewQualification(request):
    if request.session.get('manager')  is None:
            return HttpResponseRedirect("/manage/login/")

    freshManList = FreshMembers.objects.filter(register_year=CURRENT_YEAR)
    totalCount = FreshMembers.objects.filter(register_year=CURRENT_YEAR).count()

    writtenCount = FreshMembers.objects.filter(aspiration1=u'技术部',register_year=CURRENT_YEAR).count()
    writtenCount = writtenCount+FreshMembers.objects.exclude(aspiration1=u'技术部',register_year=CURRENT_YEAR).filter(aspiration2=u'技术部',register_year=CURRENT_YEAR).count()
    
    interviewCount = FreshMembers.objects.filter(interviewqualification=1,register_year=CURRENT_YEAR).count()

    freshIQ = get_template('freshReg/manage/interviewqualification.html')
    freshIQHtml = freshIQ.render(Context({'freshMemberList':freshManList,'total_count':totalCount,'writen_count':writtenCount,'interview_count':interviewCount}))
    return HttpResponse(freshIQHtml)

def freshSearch(request):
    studentid = request.POST['searchID']
    if check_input(studentid,'studentID'):
        freshManSearch = FreshMembers.objects.filter(student_id=studentid,register_year=CURRENT_YEAR)
        writtenCount = FreshMembers.objects.filter(aspiration1=u'技术部',register_year=CURRENT_YEAR).count()
        writtenCount = writtenCount+FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部',register_year=CURRENT_YEAR).count()
        interviewCount = FreshMembers.objects.filter(interviewqualification=1,register_year=CURRENT_YEAR).count()
        freshSearch = get_template('freshReg/manage/individual_edit.html')
        totalCount = FreshMembers.objects.filter(register_year=CURRENT_YEAR).count()
        freshSearchHtml = freshSearch.render(Context({'freshMemberList':freshManSearch,'total_count':totalCount,'writen_count':writtenCount,'interview_count':interviewCount}))
        return HttpResponse(freshSearchHtml)
    else:
        #这个应该返回到原来页面可能比较合理
        return HttpResponse('学号格式输入错误！')

def freshInterviewQualification_edit(request):
    if request.session.get('manager') is None :
            return HttpResponseRedirect("/manage/login/")

    amount = request.POST['amount']
    # 非技术部的writtenscore 默认填零吧
    freshManList = FreshMembers.objects.filter(register_year = CURRENT_YEAR).order_by('-writtenscore')
    qualifiedFreshMan = []
    for i in range(min(int(amount),freshManList.count())):
        qualifiedFreshMan.append(freshManList[i])
    totalCount = FreshMembers.objects.count()
    writtenCount = FreshMembers.objects.filter(aspiration1=u'技术部').count()
    writtenCount = writtenCount+FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部').count()
    interviewCount = FreshMembers.objects.filter(interviewqualification=1).count()
    qualification = get_template('freshReg/manage/interviewqualification.html')
    qualificationHtml = qualification.render(Context({'freshMemberList':qualifiedFreshMan,'total_count':totalCount,'writen_count':writtenCount,'interview_count':interviewCount}))
    return HttpResponse(qualificationHtml)

def freshInterviewQualification_result(request):#面试资格录入
    if request.session.get('manager') is None:
            return HttpResponseRedirect("/manage/login/")

    techFreshMemberList = FreshMembers.objects.filter(aspiration1=u'技术部',register_year = CURRENT_YEAR) | FreshMembers.objects.exclude(aspiration1=u'技术部').filter(aspiration2=u'技术部',register_year = CURRENT_YEAR)
    for techFreshMan in techFreshMemberList:
        techFreshNow = techFreshMan        
        exist = request.POST[str(techFreshMan.id)]
        if exist!=None:
            techFreshNow.interviewqualification=exist
            techFreshNow.save()
    return HttpResponse(u'面试资格修改成功！')

def finalResult(request):
    if request.method=="GET":#访问的是网页
        if request.session.get('manager') is None:
                return HttpResponseRedirect("/manage/login/")
        regularFreshList = FreshMembers.objects.filter(interviewqualification=1, register_year=CURRENT_YEAR)
        totalCount = FreshMembers.objects.filter(register_year=CURRENT_YEAR).count()
        writtenCount = FreshMembers.objects.filter(aspiration1=u'技术部',register_year=CURRENT_YEAR).count()
        writtenCount = writtenCount+FreshMembers.objects.exclude(aspiration1=u'技术部',).filter(aspiration2=u'技术部',register_year=CURRENT_YEAR).count()
        interviewCount = FreshMembers.objects.filter(interviewqualification=1, register_year=CURRENT_YEAR).count()
        qualification = get_template('freshReg/manage/final_result.html')
        qualificationHtml = qualification.render(Context({'freshMemberList':regularFreshList,'total_count':totalCount,'writen_count':writtenCount,'interview_count':interviewCount}))
        return HttpResponse(qualificationHtml)
    else :#提交的表单
        freshMemberList = FreshMembers.objects.filter(interviewqualification=1,register_year=CURRENT_YEAR)
        for freshMember in freshMemberList:
            freshMember.finalaspiration=request.POST[str(freshMember.id)]
            if freshMember.finalaspiration=="淘汰":
                freshMember.memberqualifiction=0
            else:
                freshMember.memberqualifiction=1
            freshMember.save()
        return HttpResponse("已保存")
             












@csrf_exempt
def login_result(request): # 登陆的结果
    password =  request.POST['password']
    if password=='':
        return HttpResponse('登陆失败！请填写密码')
    email =  request.POST['email']
    if email=='':
        return HttpResponse('登陆失败！请填写邮箱')
    u=User()
    u.email=email
    u.password=password
    try:
       user=User.objects.get(email=email) # user是指从数据库里面查找的邮箱为email的用户
    except User.DoesNotExist:
        return HttpResponse("账户不存在")
    if user.password==hashlib.sha1(u.password).hexdigest(): # u是登陆之时填写的用户
        if user.effective == 1:
            result=get_template('login_result.html') # 比较数据库的用户的密码和填写的密码是否一致
            resultHtml=result.render(Context())
            request.session['user']=user
            return HttpResponseRedirect("/index/")
        else:
            return HttpResponse("您的帐号已被删除或封停,具体情况请联络技术部负责人予以解决!")
    else:
        return HttpResponse("密码错误")



@csrf_exempt
def change_password(request):  #修改密码
    user = request.session.get('user')
    if user is None :
        return HttpResponse("请先登陆！")
    result = get_template('change_password.html')
    result_html = result.render(Context({'return_value_old':True,'return_value_new':True}))
    return HttpResponse(result_html)

@csrf_exempt
def change_password_result(request):  #修改密码的结果
    u = request.session.get('user')
    old_password = request.POST['old_password']
    old_password = hashlib.sha1(old_password).hexdigest() 
    new_password = request.POST['new_password']
    confirm_password = request.POST['password_confirm']
    result = get_template('change_password.html')

    if u is None :
        return HttpResponse("请先登陆！")
    if new_password != confirm_password:
        bad_result_html = result.render(Context({'return_value_old':True,'return_value_new':False}))
        return HttpResponse(bad_result_html)

    bad_result_html = result.render(Context({'return_value_old':False,'return_value_new':False}))
    if old_password==False or new_password==False or confirm_password==False:
        return HttpResponse(bad_result_html)
    if u.password != old_password:
        if new_password != confirm_password:
            return HttpResponse(bad_result_html)
        else:
            bad_result_html = result.render(Context({'return_value_old':False,'return_value_new':True}))
            return HttpResponse(bad_result_html)
    user = User.objects.get(email = u.email)
    user.password = hashlib.sha1(new_password).hexdigest()
    user.save()
    request.session['user'] = user
    return HttpResponseRedirect("/index/")

@csrf_exempt
def reset_password_request(request):   #在登陆页面点击找回密码
    result = get_template('reset_password.html')
    result_html = result.render(Context({'return_value_email':True}))
    return HttpResponse(result_html)

@csrf_exempt
def reset_password(request):  #发送重置邮件获取验证码
    email = request.POST['email']
    #email="754884172@qq.com"
    try:
        user = User.objects.get(email = email)
        #return HttpResponse(user);
        subject = u'南微软通讯录信息录入通知'
        msg_t = get_template("mail_confirm.html")
        success = 1
        code = ''
        while True:    # 防止号码重复
            code = getstr(8)
            try:#改用exist函数
                Code.objects.get(code=code)
            except Code.DoesNotExist:
                break
        if send_mail([email], subject, msg_t.render(Context({'code':code}))):
            c = Code()
            c.code = code
            c.use = User.objects.get(email = email)  
            #old_code = Code.objects.get(user = c.user)
            #old_code.effective = 0
            #old_code.save()
            #c.type = CODE_TYPE['invite'] # CODE_TYPE ？？？#
            c.start_time = datetime.now()
            c.effective = 1
            try:                     #设定有效时间为五分钟，因为进位问题写的很恶心。。望跟进
                c.end_time = c.start_time + timedelta(minutes=5) 
                c.save()
            except :
                c.effective = 0
                c.end_time = c.start_time
                return HttpResponse("时间运算出错啦，请联系系统管理员!")
        else:
            success = 0 
        if success:
            return HttpResponse("邮件发送成功，请您查收！")      
        else:
            return HttpResponse("邮件发送失败，请重试，为我们的失误感到万分抱歉！")
    except User.DoesNotExist:
        bad_result = get_template('reset_password.html')
        bad_result_html = bad_result.render(Context({'return_value_email':False}))
        return HttpResponse(bad_result_html)
    
@csrf_exempt
def reset_password_change(request): #重设密码
    result = get_template('reset_password_2.html')
    result_html = result.render(Context({'return_value_notempty':True,'return_value_notdiff':True,'return_value_wrongstr':True}))
    return HttpResponse(result_html)

@csrf_exempt
def reset_password_result(request): #返回重设密码的结果
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']
    code_confirm = request.POST['code']
    bad_result = get_template('reset_password_2.html')
    if password is None:
        bad_result_html = bad_result.render(Context({'return_value_notempty':False}))
        return HttpResponse(bad_result_html)
    if password_confirm != password:
        bad_result_html = bad_result.render(Context({'return_value_notdiff':True}))
    try:
        code=Code.objects.get(code = code_confirm)
        if code.effective==0:   #判定验证码是否有效
            bad_result_html = bad_result.render(Context({'return_value_wrongstr':False}))
            return HttpResponse(bad_result_html)
        time = datetime.now()
        if time > code.end_time:
            code.effective=0
            bad_result_html = bad_result.render(Context({'return_value_wrongstr':False}))
            return HttpResponse(bad_result_html)
        email = code.use.email
        user = User.objects.get(email = email)
        user.password = hashlib.sha1(password).hexdigest()
        code.effective = 0
        user.save()
        request.session['user'] = user
        return HttpResponseRedirect("/login/")
    except Code.DoesNotExist: #判定验证码是否存在
        bad_result_html = bad_result.render(Context({'return_value_wrongstr':False}))
        return HttpResponse(bad_result_html)

def get_paginator(obj,page): # 这个函数不用管它
    page_size = 10 #每页显示的数量
    after_range_num = 5
    before_range_num = 6 
    context = {}
    try:
        page = int(page)
        if page <1 :
            page = 1 
    except ValueError:
        page = 1 
    paginator = Paginator(obj,page_size)
    try:
        obj = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        obj = paginator.page(1)
    
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+before_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+before_range_num]
    
    context["page_objects"]=obj
    context["page_range"]=page_range
    return context

def logout(requst):# 注销，从session里面删除user对象，并跳转回登陆页面
    user=requst.session.get('user')
    if user is None:
        return HttpResponse("请先登录！")
    del requst.session['user']
    return HttpResponseRedirect("/login/")

def getstr(n):#获得指定长度随机字符串
    st = ''
    while len(st) < n:
        temp = chr(97+random.randint(0,25))
        if st.find(temp) == -1 :
            st = st.join(['',temp])
    return st

def send_code(request):
    user=request.session.get('user')
    if user is None:
        return HttpResponse("请先登录！")
    elif User.objects.get(id = user.id).authority & AUTHORITY['admin'] == 0: # 这个地方最好以后能改成try形式
        return HttpResponse("您不具有管理员资格！")
    else:
        s_c=get_template('send_code.html',)
        s_cHtml=s_c.render(Context())
        return HttpResponse(s_cHtml)

@csrf_exempt
def send_code_result(request):
    user=request.session.get('user')
    if user is None:
        return HttpResponse("请先登录！")
    elif User.objects.get(id = user.id).authority & AUTHORITY['admin'] == 0: # 这个地方最好以后能改成try形式
        return HttpResponse("您不具有管理员资格！")
    else:
        pass
    email_list_raw = request.POST['email_list']
    subject = u'南微软通讯录信息录入通知'
    msg_t = get_template("mail_invite.html")
    email_list = email_list_raw.split('\n')
    success = 1
    for email_addr in email_list:
        code = ''
        while True:
            code = getstr(8)
            try:
                Code.objects.get(code=code)
            except Code.DoesNotExist:
                break
        if send_mail([email_addr], subject, msg_t.render(Context({'code':code}))):
            c = Code()
            c.code = code
            c.use = User.objects.get(id=0)  # a special user means nobody
            c.type = CODE_TYPE['invite']
            c.start_time = datetime.now()
            c.effective = 1
            c.end_time = datetime.now().replace(year=9999) # forever effective
            c.save()
        else:
            success = 0
            break
    if success:
        return HttpResponse("发送邀请码邮件成功!")
    else:
        return HttpResponse("操作失败!")
 
def register(request):
    result = get_template('result.html')
    result_html = result.render(Context({'result':'活动已结束'}))
    return HttpResponse(result_html)

def RegisterToMicrosoft(request):# 编程之美注册
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    passwd=request.POST['password']
    passwd_repeat=request.POST['passwd_repeat']
    email=request.POST['email']
    name=request.POST['name']
    realname=request.POST['real_name']
    gender=request.POST['gender']
    college=request.POST['college']
    graduateyear=request.POST['graduateyear']
    major=request.POST['major']
    mobile=request.POST['mobile']
    student_id=request.POST['student_id']
    tsize=request.POST['tsize']
    degree=request.POST['degree']
    data={
        'lang':'chs',
        'passwd':passwd,
        'passwd_repeat':passwd_repeat,
        'email':email,
        'name':name,
        'realname':realname,
        'gender':gender,
        'college':college,
        'graduateyear':graduateyear,
        'major':major,
        'mobile':mobile,
        'student_id':student_id,
        'joinus':"yes",
        'become_fte':"yes",
        'join_maillist':"no",
        'tsize':tsize,
        'degree':degree
    }    

    for i in data:
        if data[i]=="":
            result=get_template('result.html')
            resultHtml=result.render(Context({'result':'注册资料没有填写完整，注册失败！<a href="/register">点击返回</a>'},autoescape=False))#防止将'<'、 '/'和'>'自动转义，下同
            return HttpResponse(resultHtml)           
    if passwd != passwd_repeat:        
        result=get_template('result.html')
        resultHtml=result.render(Context({'result':'注册失败！两次输入密码不一致 <a href="/register">点击返回</a>'},autoescape=False))     
        return HttpResponse(resultHtml)        


    headers = {'Content-type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0',
                'accept':"*/*"
                }
    conn = httplib.HTTPConnection("programming2015.cstnet.cn")
    params = urllib.urlencode(data)
    conn.request("POST", "/api/user/register.json", params, headers)#提交



    response = conn.getresponse()
    res = response.read()#type of 'res':string  content:{"code":int,"errorMessage":""} or {"response":{"message":"success","url":"\/register\/status"},"code":0}

    index=res.find("code")#在返回的信息中寻找code字符串，找到后在index中加6即为返回的值
    if index==-1:#code ,可能微软注册页面返回的信息已经更改，需要重写代码
        result=get_template('result.html')
        resultHtml=result.render(Context({'result':'出现错误，请联系管理员'}))     
        return HttpResponse(resultHtml)        
    index=index+6
    if res[index]=="0":#注册成功
        conn.close()
        user=Reg()
        user.email=email
        user.name=name
        user.realname=realname
        user.gender=gender
        user.graduateyear=graduateyear
        user.major=major
        user.mobile=mobile
        user.student_id=student_id
        user.degree=degree
        user.status='no'

        #抽奖
        award0=Reg.objects.get(email=0)#无奖品
        award1=Reg.objects.get(email=1)#奖品1
        award2=Reg.objects.get(email=2)#奖品2
        award3=Reg.objects.get(email=3)#奖品3
        award4=Reg.objects.get(email=4)#奖品4
        award5=Reg.objects.get(email=5)#奖品5


        award0num=award0.student_id#奖品的数目
        award1num=award1.student_id
        award2num=award2.student_id
        award3num=award3.student_id
        award4num=award4.student_id
        award5num=award5.student_id
        ram=random.randint(0,award4num+award5num+award3num+award2num+award1num+award0num)

        if ram<=award0num:
            award0.student_id=award0num-1
            award0.save()
            user.save()
            result=get_template('result.html')
            resultHtml=result.render(Context({'result':'注册成功，很遗憾没有抽中奖品。<br>后续会有第二次抽奖，结果公布在微信公众号nkumstc，<a href="http://programming2015.cstnet.cn/login">点击登陆编程之美</a>',
                                                'meta':'http-equiv="refresh" content="5;url=http://mp.weixin.qq.com/s?__biz=MzAxNzI0MTcyOQ==&mid=204230207&idx=1&sn=9d220563ca0387631a7bc3b586b0239b#rd" '},autoescape=False))     
            return HttpResponse(resultHtml)  
        if ram <=award1num+award0num:           
            award1.student_id=award1num-1            
            user.award=award1.name
            user.save()
            str=award1.name
            award1.save()
            result=get_template('result.html')
            
            resultHtml=result.render(Context({'result':'注册成功，恭喜抽中'+str+'  <br>领奖时间于19号微信号公布通知，微信公众号nkumstc <a href="http://programming2015.cstnet.cn/login">点击登陆编程之美</a>',
                                                 'meta':'http-equiv="refresh" content="5;url=http://mp.weixin.qq.com/s?__biz=MzAxNzI0MTcyOQ==&mid=204230207&idx=1&sn=9d220563ca0387631a7bc3b586b0239b#rd"'},autoescape=False))     
            return HttpResponse(resultHtml)
        if ram<=award2num+award1num+award0num:
            award2.student_id=award2num-1            
            user.award=award2.name
            user.save()
            str=award2.name
            award2.save()
            
            result=get_template('result.html')
            resultHtml=result.render(Context({'result':'注册成功，恭喜抽中'+str+' <br>领奖时间于19号微信号公布通知，微信公众号nkumstc <a href="http://programming2015.cstnet.cn/login">点击登陆编程之美</a>',
                                                 'meta':'http-equiv="refresh" content="5;url=http://mp.weixin.qq.com/s?__biz=MzAxNzI0MTcyOQ==&mid=204230207&idx=1&sn=9d220563ca0387631a7bc3b586b0239b#rd"'},autoescape=False))     
            return HttpResponse(resultHtml)
        if  ram<=award3num+award2num+award1num+award0num:
            award3.student_id=award3num-1
            user.award=award3.name
            user.save()
            str=award3.name
            award3.save()
            result=get_template('result.html')
            resultHtml=result.render(Context({'result':'注册成功，恭喜抽中'+str+'  <br>领奖时间于19号微信号公布通知，微信公众号nkumstc <a href="http://programming2015.cstnet.cn/login">点击登陆编程之美</a>',
                                                 'meta':'http-equiv="refresh" content="5;url=http://mp.weixin.qq.com/s?__biz=MzAxNzI0MTcyOQ==&mid=204230207&idx=1&sn=9d220563ca0387631a7bc3b586b0239b#rd"'},autoescape=False))     
            return HttpResponse(resultHtml)
        if  ram<=award4num+award3num+award2num+award1num+award0num:
            award4.student_id=award4num-1
            user.award=award4.name
            user.save()
            str=award4.name
            award4.save()
            result=get_template('result.html')
            resultHtml=result.render(Context({'result':'注册成功，恭喜抽中'+str+'  <br>领奖时间于19号微信号公布通知，微信公众号nkumstc <a href="http://programming2015.cstnet.cn/login">点击登陆编程之美</a>',
                                                 'meta':'http-equiv="refresh" content="5;url=http://mp.weixin.qq.com/s?__biz=MzAxNzI0MTcyOQ==&mid=204230207&idx=1&sn=9d220563ca0387631a7bc3b586b0239b#rd"'},autoescape=False))     
            return HttpResponse(resultHtml)
        if  ram<=award5num+award4num+award3num+award2num+award1num+award0num:
            award5.student_id=award5num-1
            user.award=award5.name
            user.save()
            str=award5.name
            award5.save()
            result=get_template('result.html')
            resultHtml=result.render(Context({'result':'注册成功，恭喜抽中'+str+'  <br>领奖时间于19号微信号公布通知，微信公众号nkumstc <a href="http://programming2015.cstnet.cn/login">点击登陆编程之美</a>',
                                                 'meta':'http-equiv="refresh" content="5;url=http://mp.weixin.qq.com/s?__biz=MzAxNzI0MTcyOQ==&mid=204230207&idx=1&sn=9d220563ca0387631a7bc3b586b0239b#rd"'},autoescape=False))     
            return HttpResponse(resultHtml)


        user.save()
        result=get_template('result.html')
        resultHtml=result.render(Context({'result':'注册成功。<a href="http://programming2015.cstnet.cn/login">点击登陆</a>'},autoescape=False))     
        return HttpResponse(resultHtml)        
    
    else:#注册失败
        conn.close()
        index_start=res.find("errorMessage");
        if index_start==-1:#找不到errorMessage ,可能微软注册页面返回的信息已经更改，需要重写代码
            result=get_template('result.html')
            resultHtml=result.render(Context({'result':'出现错误，请联系管理员'}))     
            return HttpResponse(resultHtml)         
    
        index_start+=14
        index_end=res.find("\"",index_start+1)
        substring=res[index_start+1:index_end]    
        temp='注册失败！'+substring
        temp= temp+' <a href="/register">点击返回</a> '
        result=get_template('result.html')
        resultHtml=result.render(Context({'result':temp},autoescape=False))     
        return HttpResponse(resultHtml)
def rules(request):    
    result = get_template('rules.html')
    result_html = result.render(Context())
    return HttpResponse(result_html)
def intro(request):    
    result = get_template('intro.html')
    result_html = result.render(Context())
    return HttpResponse(result_html)
def query(request):    
    result = get_template('query.html')
    result_html = result.render(Context())
    return HttpResponse(result_html)
def query_result(request):
    if request.POST['email'] and  request.POST['student_id']:

        email=request.POST['email']    
        studentid=request.POST['student_id']
        try:        
            user = Reg.objects.get(email = email)
            if user.student_id==int(studentid):
                status="已领取"
                if user.status=='no':
                    status="未领取"
                query_result=get_template('query_result.html')
                query_result_html=query_result.render(Context({'student_id':user.student_id,'email':user.email,'name':user.realname,'award':user.award,'final_award':user.final_award,'status':status}))
                return HttpResponse(query_result_html)
            else:
                bad_result = get_template('result.html')
                bad_result_html = bad_result.render(Context({'result':'用户不存在 <a href="/query">点击返回</a>'},autoescape=False))
                return HttpResponse(bad_result_html)

        except Reg.DoesNotExist:
            bad_result = get_template('result.html')
            bad_result_html = bad_result.render(Context({'result':'用户不存在 <a href="/query">点击返回</a>'},autoescape=False))
            return HttpResponse(bad_result_html)
    else:
        bad_result = get_template('result.html')
        bad_result_html = bad_result.render(Context({'result':'输入错误 <a href="/query">点击返回</a>'},autoescape=False))
        return HttpResponse(bad_result_html)
def get_award(request):
    if request.POST['email'] and  request.POST['password']:
        email=request.POST['email']
        user = Reg.objects.get(email = email)
        if request.POST['password']=='nkumstc1234' and user.status=='no':           
            
            user.status="yes"
            user.save()
            result=get_template('result.html')
            result_html=result.render(Context({'result':'领取成功',
                                                'meta':'http-equiv="refresh" content="2;url=/query"'},autoescape=False))
            return HttpResponse(result_html)
        else:
            result=get_template('result.html')
            result_html=result.render(Context({'result':'领取失败',
                                                'meta':'http-equiv="refresh" content="2;url=/query"'},autoescape=False))
            return HttpResponse(result_html)
    else:
        result=get_template('result.html')
        result_html=result.render(Context({'result':'同学别闹了抓紧去学习吧:)'},autoescape=False))
        return HttpResponse(result_html)
def change_number(request):
    user=Reg.objects.get(email = '0')
    num=user.student_id+20
    user.student_id=num
    user.save()  
    result=get_template('result.html')
    result_html=result.render(Context({'result':'award0:'+str(num),
                                                'meta':'http-equiv="refresh" content="1;url=/query"'},autoescape=False))
    return HttpResponse(result_html)

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
        p=re.compile(r'^\d{7}$')
        m=p.match(str)
        if m==None:
            return 0
        else:
            return 1



            









