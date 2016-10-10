from file_path import JSON_FILE_PATH
from django.http import JsonResponse
from django.http import HttpResponse
from os import environ
import random
import json

def getLottery(request):
	debug = not environ.get("APP_NAME","")
	#read present file
	if debug:
		jsonfile = open(JSON_FILE_PATH)
		data = json.load(jsonfile)
	else:
		data = {}

	special = data["special"]
	special_read = data["special"]
	first = data["first"]+special
	first_read = data["first"]
	second = data["second"]+first
	second_read = data["second"]
	third = data["third"]+second
	third_read = data["third"]
	rate = data["rate"]
	total = (third*100)/rate
	present_level = ""

	#remain no present
	if total==0:
		present_level = "None"
	else: #get lottery
		ram = random.randint(1,total)
		if ram==special:
			special_read = special_read-1
			present_level = "special"
		elif ram<=first:
			first_read = first_read-1
			present_level = "first"
		elif ram<=second:
			second_read = second_read-1
			present_level = "second"
		elif ram<=third:
			third_read = third_read-1
			present_level = "third"
		else:
			present_level = "None"

	if debug:  # write to present file
		jsonfile = open(JSON_FILE_PATH,"w")
	else:
		jsonfile = None
	jsonfile.write(json.dumps({"special":special_read,"first":first_read,"second":second_read,"third":third_read,"rate":rate}))

	return HttpResponse(present_level)

