# -*- coding: utf-8 -*-
from file_path import JSON_FILE_PATH
from file_path import JSON_SERVER_OBJECT_NAME
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from beautyOfcoding.models import Lottery
from sae.storage import Bucket
from os import environ
import hashlib
import base64
import random
import json
import re

def getLottery(request):
	try:
	    micro_id64 = request.POST['micro_id']
	    micro_id = int(base64.b64decode(micro_id64))
	    hash_id = hashlib.sha1(str(micro_id)).hexdigest()
	    try:
	    	winner = Lottery.objects.get(hash_id = hash_id)
	    except:
	    	return HttpResponse("同学别刷票了 (╯▔皿▔)╯")

	    #中奖通知确认
	    if winner.present_level == "None": 
	    	noaward_notice = get_template('lottery_beautyOfCoding/noaward_confirm.html')
	    	noaward_noticeHtml = noaward_notice.render(Context())
	    	return HttpResponse(noaward_noticeHtml)
	    else:
	    	award_notice = get_template('lottery_beautyOfCoding/award_confirm.html')
	    	information = {'level':winner.present_level,'micro_id':micro_id64,'no_phoneNumber':False}
	    	award_noticeHtml = award_notice.render(Context(information))
	    	return HttpResponse(award_noticeHtml)
	except:  
		return HttpResponse("非法访问！")

def lottery_confirmed(request):
	try:
		micro_id64 = request.POST['micro_id']
		micro_id = int(base64.b64decode(micro_id64))
		hash_id = hashlib.sha1(str(micro_id)).hexdigest()
		try:
			winner = Lottery.objects.get(hash_id = hash_id)
			if request.POST['phone_number']:
				#check phone number format
				phone_number = request.POST['phone_number']
				if check_input(str(phone_number),'phoneNumber'):
					if winner.phone_number != None :
						return HttpResponse("该奖品已经有申奖号码了")
					winner.phone_number = phone_number
					winner.save()
					##update lottery_remain_information
					debug = not environ.get("APP_NAME","")
					# #read present file
					if debug:
						jsonfile = open(JSON_FILE_PATH)
						data = json.load(jsonfile)
					else:
						bucket = Bucket("nkumstc")
						data = json.loads(bucket.get_object_contents(JSON_SERVER_OBJECT_NAME))

					special_read = data["special"]
					first_read = data["first"]
					second_read = data["second"]
					third_read = data["third"]
					fourth_read = data["fourth"]
					fifth_read = data["fifth"]
					rate = data["rate"]
					#update
					if winner.present_level=="special":
						special_read = special_read-1
					elif winner.present_level=="first":
						first_read = first_read -1
					elif winner.present_level == "second":
						second_read = second_read-1
					elif winner.present_level == "third":
						third_read = third_read-1
					elif winner.present_level == "fourth":
						fourth_read = fourth_read-1
					elif winner.present_level == "fifth":
						fifth_read = fifth_read-1
					else:
						return HttpResponse("bug!")

					if debug:  # write to present file
						jsonfile = open(JSON_FILE_PATH,"w")
						jsonfile.write(json.dumps({"special":special_read,"first":first_read,"second":second_read,"third":third_read,"rate":rate,"fourth":fourth_read,"fifth":fifth_read}))
					else:
						bucket = Bucket("nkumstc")
						content = {"special":special_read,"first":first_read,"second":second_read,"third":third_read,"rate":rate,"fourth":fourth_read,"fifth":fifth_read}
						bucket.put_object(JSON_SERVER_OBJECT_NAME,json.dumps(content))
				else:
					award_notice = get_template('lottery_beautyOfCoding/award_confirm.html')
					information = {'level':winner.present_level,'micro_id':micro_id64,'no_phoneNumber':True}
					award_noticeHtml = award_notice.render(Context(information))
					return HttpResponse(award_noticeHtml)
			else:
				award_notice = get_template('lottery_beautyOfCoding/award_confirm.html')
				information = {'level':winner.present_level,'micro_id':micro_id64,'no_phoneNumber':True}
				award_noticeHtml = award_notice.render(Context(information))
				return HttpResponse(award_noticeHtml)
		except:
			return HttpResponse("同学别刷票了 (╯▔皿▔)╯")
	except:
		return HttpResponse("您可能使用的是windows手机，请换成其他手机或使用电脑浏览器抽奖，如有问题请于俱乐部联系")

	#final result return
	award_confirmed = get_template('lottery_beautyOfCoding/award_confirmed.html')
	award_confirmedHtml = award_confirmed.render(Context())
	return HttpResponse(award_confirmedHtml)

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
def manage_lottery_deliver(request):
	manage = get_template('lottery_beautyOfCoding/manage/show_all_lotteryInformation.html')
	lotteryWinners = Lottery.objects.filter().exclude(present_level="None").exclude(phone_number__isnull=True)
	manageHtml = manage.render(Context({'lotteryWinners':lotteryWinners}))
	return HttpResponse(manageHtml)
def award_confirmed(request):
	if request.GET['micro_id']: #确认参数有效
		micro_id = request.GET['micro_id']
	else:
		return HttpResponse("非法操作！")

	# 确认中奖者真实存在
	try:
		winner = Lottery.objects.get(micro_id=micro_id)
	except Lottery.DoesNotExist:
		return HttpResponse("非法操作！")
	if winner.status == 1: #确认中奖者未领奖
		return HttpResponse("非法操作！")
	#修改状态为 已领奖
	winner.status = 1
	winner.save()
	#返回管理页面
	manage = get_template('lottery_beautyOfCoding/manage/show_all_lotteryInformation.html')
	lotteryWinners = Lottery.objects.filter().exclude(present_level="None")
	manageHtml = manage.render(Context({'lotteryWinners':lotteryWinners}))
	return HttpResponse(manageHtml)
def award_front(request):
	try:
		#验证合法 micro_id
	    assume_micro_id = request.GET['id']
	    check_1 = assume_micro_id[0:13]
	    check_2 = assume_micro_id[::-1][0:19]
	    length = len(assume_micro_id)
	    if check_1 == "2b80b60a10d3a" and check_2 == "05ab236e2f139bbcbd3":
	    	pass
	    else:
	    	return HttpResponse("同学别刷票了 (╯▔皿▔)╯")
	    moreLikely_id = assume_micro_id[len("2b80b60a10d3a"):length-len("05ab236e2f139bbcbd3")]
	    micro_id = int(moreLikely_id)^65535
	    if micro_id>20000:
	    	return HttpResponse("同学别刷票了 (╯▔皿▔)╯")

	    ##update lottery_remain_information
	    debug = not environ.get("APP_NAME","")
	    #read present file
	    if debug:
	    	jsonfile = open(JSON_FILE_PATH)
	    	data = json.load(jsonfile)
	    else:
	    	bucket = Bucket("nkumstc")
	    	data = json.loads(bucket.get_object_contents(JSON_SERVER_OBJECT_NAME))

	    special = data["special"]
	    first = data["first"]+special
	    second = data["second"]+first
	    third = data["third"]+second
	    fourth = data["fourth"]+third
	    fifth = data["fifth"]+fourth
	    rate = data["rate"]
	    total = (fifth*100)/rate
	    present_level = ""

	    ##get lottery
	    #remain no present
	    if total == 0:
	    	present_level = "None"
	    #get lottery  活动开始初期不让有特等奖orz
	    else:
	    	#while (True):
	    	ram = random.randint(1,total)
	    	if ram==special:
	    		present_level = "special"
	    	elif ram<=first:
	    		present_level = "first"
	    		#break
	    	elif ram<=second:
	    		present_level = "second"
	    		#break
	    	elif ram<=third:
	    		present_level = "third"
	    		#break
	    	elif ram<=fourth:
	    		present_level = "fourth"
	    		#break
	    	elif ram<=fifth:
	    		present_level = "fifth"
	    		#break
	    	else:
	    		present_level = "None"
	    		#break

	    #make database record
	    user = Lottery()
	    user.present_level = present_level
	    user.micro_id = micro_id
	    user.status = False
	    user.hash_id = hashlib.sha1(str(micro_id)).hexdigest()
	    try:
	    	user.save()
	    except:
	    	return HttpResponse("同学别刷票了 (╯▔皿▔)╯")

	    micro_id64 = base64.b64encode(str(micro_id))

	    award_front = get_template('lottery_beautyOfCoding/award_front.html')
	    award_frontHtml = award_front.render(Context({"micro_id":micro_id64}))
	    return HttpResponse(award_frontHtml)
	except:
		return HttpResponse("非法访问！")
	