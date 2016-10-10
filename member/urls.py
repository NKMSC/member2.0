# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()
urlpatterns = patterns('',
   (r'^statics/(?P<path>.*)','django.views.static.serve',{'document_root':'member/statics/', 'show_indexes': True}),
  #  (r'^statics/(?P<path>.*)','django.views.static.serve',{'document_root':'member/statics'}), 
    # Examples:
    url(r'^$', 'member.views.login', name='home'),
    # url(r'^member/', include('member.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^test/$','member.views.test'),
    #用于通讯录项目
    url(r'^reg/$','member.views.reg'),
    url(r'^login/$','member.views.login'),
    url(r'^index/$','member.views.index'),
    url(r'^depart/(.+)/$','member.views.depart'),
    url(r'^reg_result/$','member.views.reg_result'),
    url(r'^reg_result/index/$','member.views.index'),
    url(r'^login_result/$','member.views.login_result'),
    url(r'^index/(.+)/$','member.views.index_of_others'),
    url(r'^edit/$','member.views.edit'),
    url(r'^edit_result/$','member.views.edit_result'),
    url(r'^logout/$','member.views.logout'),
    url(r'^send_code/$','member.views.send_code'),
    url(r'^send_code_result/$','member.views.send_code_result'),
    url(r'^change_password/$','member.views.change_password'),
    url(r'^change_password_result/$','member.views.change_password_result'),
    url(r'^reset_password_request/$','member.views.reset_password_request'),
    url(r'^reset_password/$','member.views.reset_password'),
    url(r'^reset_password_change/$','member.views.reset_password_change'),
    url(r'^reset_password_result/$','member.views.reset_password_result'),
    

    #用于纳新注册管理
    url(r'^freshReg_result/$','member.views.freshReg_result'),
    url(r'^freshReg_request/$','member.views.freshReg_request'),
    url(r'^freshReg_request_register/$','member.views.freshReg_request_register'),
    url(r'^freshReg_request_check/$','member.views.freshReg_request_check'),
    url(r'^freshReg_request_check_result/$','member.views.freshReg_request_check_result'),
    url(r'^freshReg_entryWrittenPerformance/$','member.views.freshReg_entryWrittenPerformance'),
    url(r'^freshReg_performWrittenPerformance/$','member.views.freshReg_performWrittenPerformance'),
    url(r'^freshInterviewQualification/$','member.views.freshInterviewQualification'),
    url(r'^freshInterviewQualification_result/$','member.views.freshInterviewQualification_result'),
    url(r'^freshInterviewQualification_edit/$','member.views.freshInterviewQualification_edit'),
    url(r'^finalResult/$','member.views.finalResult'),
    url(r'^freshShow/$','member.views.freshShow'),
    url(r'freshSearch/$','member.views.freshSearch'),
    url(r'^manage/login/$','member.views.manage_login'),
    url(r'^manage/mailrecord/$','member.views.freshMailRecord'),
    url(r'^manage/resendmail$','member.views.resendEmail'),
    url(r'^manage/sendEmailList$','member.views.sendEmailList'),
    url(r'^manage/sendSMSList$','member.views.sendSMSList'),
    url(r'^manage/SMSrecord/$','member.views.freshSMSRecord'),
    url(r'^manage/resendSMS$','member.views.resendSMS'),
    #url(r'^manage/temp$','member.views.temp_sendmail'),

    #用于编程之美注册
    #url(r'^createsuperuser$','member.views.createsuperuser'),
    # url(r'^register/$','member.views.register'),
    # url(r'^RegisterToMicrosoft$','member.views.RegisterToMicrosoft'),
    # url(r'^rules$','member.views.rules'),
    # url(r'^intro$','member.views.intro'),
    # url(r'^query$','member.views.query'),
    # url(r'^query_result/$','member.views.query_result'),
    # url(r'^get_award/$','member.views.get_award'),  
    # url(r'^nku1234567/$','member.views.change_number'),     

    #编程之美2016
    url(r'^beautyOfCoding/award_confirmed$','beautyOfcoding.views.award_confirmed'),   
    url(r'^beautyOfCoding/getLottery$','beautyOfcoding.views.getLottery'),
    url(r'^beautyOfCoding/lottery_confirmed$','beautyOfcoding.views.lottery_confirmed'),
    url(r'^beautyOfCoding/manage_lottery_deliver$','beautyOfcoding.views.manage_lottery_deliver'),
    url(r'^beautyOfCoding/award_front/$','beautyOfcoding.views.award_front'),                       
)

