#-*- coding: UTF-8 -*-
#
# 具体定义和参数说明参考 云之讯REST开发者文档 .docx
#
import base64
import datetime
import urllib2
import md5
import json
# 返回签名
def getSig(accountSid,accountToken,timestamp):
	sig = accountSid + accountToken + timestamp
	return md5.new(sig).hexdigest().upper()

#生成授权信息
def getAuth(accountSid,timestamp):
	src = accountSid + ":" + timestamp
	return base64.encodestring(src).strip()

#发起http请求
def urlOpen(req,data=None):
	try:
		res = urllib2.urlopen(req,data)
		data = res.read()
		res.close()
	except urllib2.HTTPError, error:
		data = error.read()
		error.close()
	return data

#生成HTTP报文
def createHttpReq(req,url,accountSid,timestamp,responseMode,body):
	req.add_header("Authorization", getAuth(accountSid,timestamp))
	if responseMode:
		req.add_header("Accept","application/"+responseMode)
		req.add_header("Content-Type","application/"+responseMode+";charset=utf-8")
	if body:
		req.add_header("Content-Length",len(body))
		req.add_data(body)
	return req

# 参数意义说明
# accountSid 主账号
# accountToken 主账号token
# clientNumber 子账号
# appId 应用的ID
# clientType 计费方式。0  开发者计费；1 云平台计费。默认为0.
# charge 充值或回收的金额
# friendlyName 昵称
# mobile 手机号码
# isUseJson 是否使用json的方式发送请求和结果。否则为xml。
# start 开始的序号，默认从0开始
# limit 一次查询的最大条数，最小是1条，最大是100条
# responseMode 返回数据个格式。"JSON" "XML"
# chargeType  0 充值；1 回收。
# fromClient 主叫的clientNumber
# toNumber 被叫的号码
# toSerNum 被叫显示的号码
# verifyCode 验证码内容，为数字和英文字母，不区分大小写，长度4-8位
# displayNum 被叫显示的号码
# templateId 模板Id
class RestAPI:

	HOST = "https://api.ucpaas.com"
	PORT = ""
	SOFTVER = "2014-06-30"
	JSON = "json"
	XML = "xml"
	
	#主账号信息查询
	#accountSid  主账号ID
	#accountToken 主账号的Token
	def getAccountInfo(self,accountSid,accountToken,isUseJson=True):
		now = datetime.datetime.now()
		timestamp = now.strftime("%Y%m%d%H%M%S")
		signature = getSig(accountSid,accountToken,timestamp)
		url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "?sig=" + signature
		
		if isUseJson == True:
			responseMode = self.JSON
		else:
			responseMode = self.XML

		req = urllib2.Request(url)
		return urlOpen(createHttpReq(req,url,accountSid,timestamp,responseMode,None))
	
	
	
	#短信验证码（模板短信）
	#accountSid 主账号ID
	#accountToken 主账号Token
	#appId 应用ID
	#toNumber 被叫的号码
	#templateId 模板Id
	#param <可选> 内容数据，用于替换模板中{数字}
	def templateSMS(self,accountSid,accountToken,appId,toNumbers,templateId,param,isUseJson=True):
		now = datetime.datetime.now()
		timestamp = now.strftime("%Y%m%d%H%M%S")
		signature = getSig(accountSid,accountToken,timestamp)
		url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature
		
		if isUseJson == True:
			body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}'%(appId,toNumbers,templateId,param)
			responseMode = self.JSON
		else:
			body = "<?xml version='1.0' encoding='utf-8'?>\
					<templateSMS>\
						<appId>%s</appId>\
						<to>%s</to>\
						<templateId>%s</templateId>\
						<param>%s</param>\
					</templateSMS>\
					"%(appId,toNumbers,templateId,param)
			responseMode = self.XML
		
		req = urllib2.Request(url)
		return urlOpen(createHttpReq(req,url,accountSid,timestamp,responseMode,body))

def sendSMS(toNumber,param,templateId):
	test = RestAPI()

	accountSid = "72ed5c8f96572772b6b7379bdf26ac4a"
	accountToken = "bee12aee398f01ace9e1751cc9e1ded3"
	appId = "d52d103beaf24016a1272f2dd43fb5f9"
	isUseJson = True
	# toNumber="15620941886"
	# templateId="14072"
	# param="liu,10月9日晚7点到8点半,综合教学楼b104"
	return test.templateSMS(accountSid,accountToken,appId,toNumber,templateId,param,isUseJson)

	