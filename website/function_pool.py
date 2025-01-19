from .db import dbORM
from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
import base64
import imghdr
import datetime as dt
from datetime import datetime, timedelta
from flask_login import login_required, current_user
from . import DateToolKit as dtk
import math as Math
import random
from . import id_generator
from . import encrypt


def encode_image(file_storage):
    image_data = file_storage.read()
    encoded_string = base64.b64encode(image_data).decode("utf-8")

    return encoded_string

def calcTimeDifference(dpt, ct):
	return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]

def getDBItem(model, column, value, f=False):
	
	try:
		if f == True:
			i = dbORM.find_one(model, column, value)
		else:
			i = dbORM.get_all(model)[f'{dbORM.find_one(model, column, value)}']
	except Exception as e:
		i = {}

	return i

def python_eval(exp):

	try:
		return eval(exp)
	except:
		return []

def eddie():
	return "ds"

def loopAppendAndReverse(a, b):
	try:
		for k, v in a.items():
			b.append(v)
		return b[::-1]
	except Exception as e:
		return f"Error occured\nError: {e}"

def toJoin(i, j):
	return f"{i}{j}"

def thousandify(amount):
	amount = "{:,}".format(float(amount))
	return f"{amount}"

def referral_data():
	refs = 0 if (dbORM.get_all("UserTLFY")[f'{current_user.id}']['referral_count']) == "NULL" else (dbORM.get_all("UserTLFY")[f'{current_user.id}']['referral_count'])
	earnings = float(refs) * 1000
	return [f"{refs}", earnings]

def is_test():
	return "True"

def floatToInt(n):
	return f"{Math.ceil(float(n))}"

def getDateTime():
	# Getting Date-Time Info
	current_date = dt.date.today()
	current_time = datetime.now().strftime("%H:%M:%S")

	# Date Format: "YYYY-MM-DD"
	formatted_date = current_date.strftime("%Y-%m-%d")
	date = formatted_date
	time = current_time

	return [date, time]


def HTMLBreak(n):
	breaks = ""

	for x in range(int(n)):
		breaks = breaks + "\n<br>"	

	return breaks

def getOppositeTheme(theme):
	if theme == 'light':
		return 'dark'
	else:
		return 'light'

def oppositeCurrency(currency):
	return "NGN" if currency == "$" else "NGN"

def CurrencyExchange():
	v1 = float(f"0.{dtk.split_date(getDateTime()[0])['Day']}") # initial float
	v2 = float(f"0.{dtk.split_date(getDateTime()[0])['Month']}") # error margin

	return round(v1 * v2, 2)

def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else ''

def checkImagePassError(image_raw):
	try:
		rr = f"data:{getMIME(image_raw)};base64,{image_raw}"
		return "false"
	except:
		return "true"

def calculate_total_net():

	ref = {	
		"ttr": ["Pending", [], 0],
		"ts": ["success", [], 0],
		"tf": ["failed", [], 0]
	}
	for r, e in ref.items():
		# for item in e:
		_list = dbORM.find_all("WithdrawTLFY", "status", e[0])
		if _list != [] or len(_list) > 0:
			for list_item in _list:
				e[1].append(float(list_item['amount']))

	print(ref)

	for r, e in ref.items():
		e[2] = sum(e[1])

	print(ref)


	return [ref['ttr'][2], ref['ts'][2], ref['tf'][2]]

def detectDeviceType(theRequest):
	user_agent = theRequest.user_agent.string.lower()

	if 'android' in user_agent:
		device_type = 'Android'

	elif "iphone" in user_agent:
		device_type = 'iPhone'

	else:
		device_type = 'Desktop'

	return device_type

def which_device(dev_code):
	try:
		if dev_code == "ADR":
			return "Android"
		elif dev_code == "IOS":
			return "iPhone"
		elif dev_code == "DEK":
			return "Desktop"
		else:
			return "JustShow"
	except:
		return "error"

def calculate_net_value(_list):
	single_value = []
	single = []
	for j in _list:
		single.append(j)

	try:
		single.remove({})
	except:
		pass


	for k in single:
		single_value.append(float(k['wallet_balance']))

	# print(single_value)

	return sum(single_value)