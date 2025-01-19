from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from .db import dbORM
from . import DateToolKit as dtk

import base64
import imghdr
from . import encrypt
import random
from . import function_pool
import datetime as dt
from . import id_generator
from datetime import datetime

User, Record = dbORM.get_all("UserTLFY"), None
	
								# <!-- <img src="data:{{ getMIME( Task['image_raw'] ) }};base64,{{ Task['image_raw'] }}" style="background: white; aspect-ratio: 1/1; width: 40px; padding: 20px; object-fit: cover;"> -->


def go_to(screen_id, _redirect=False, **kwargs):
	if _redirect == False:
		u = dbORM.get_all("UserTLFY")[f'{current_user.id}']

		Tasks = dbORM.get_all("TaskTLFY")
		tasks_list = []
		for k, v in Tasks.items():
			tasks_list.append(v)

		tasks_list = list(reversed(tasks_list))

		for tl in tasks_list:
			if str(dtk.calculate_difference(tl['datestamp'], tl['expiry_date'])) == "0" or int(dtk.calculate_difference(tl['datestamp'], tl['expiry_date'])) <= 0:
				dbORM.delete_entry("TaskTLFY", tl['id'])
				tasks_list.remove(tl)

		WithdrawalRequests = dbORM.get_all("WithdrawTLFY")
		withdrawal_requests_list = []
		for k, v in WithdrawalRequests.items():
			withdrawal_requests_list.append(v)

		RecieptRequests = dbORM.get_all("RReceipt")
		reciept_req_list = []
		for k, v in RecieptRequests.items():
			reciept_req_list.append(v)

		reciept_req_list.remove({})
		# try:
		# 	tasks_list.remove({"0": {"id": "1", "name": "", "task_link": "https://tasklify-nine.vercel.app", "task_type": "Link", "points": "0", "description": "", "image_name": "", "image_raw": "", "datestamp": "2024-07-28", "users_id": "[]", "timestamp": "22:15:18", "users_id_done": "[]", "expiry_date": "2024-07-31"}}) 
		# except: 
		# 	pass

		# withdrawal_requests_list = list(reversed(withdrawal_requests_list))

		MyWithdrawalRequests = dbORM.find_all("WithdrawTLFY", "user_wallet_address", u['user_id'])
		my_withdrawal_requests = list(reversed(MyWithdrawalRequests))

		if u['user_type'] == 'client':
			if u['referral_earning'] == '0' :
				_ = []
				for x in range(100):
					_.append(x)
				__ = [1.0, 0.9, 0.8, 0.7, 0.6]
				return render_template("to-payments.html", amount="850", num_list=_, num_list2=__, CUser=u)

		def checkImagePassError(image_raw):
			try:
				rr = f"data:{function_pool.getMIME(image_raw)};base64,{image_raw}"
				return "false"
			except:
				return "true"

		return render_template("dashboard.html",
			CUser = u,		
			Tasks = tasks_list,
			WithdrawalRequests = withdrawal_requests_list,
			MyWithdrawalRequests = my_withdrawal_requests,
			RecieptRequests = reciept_req_list,
			ImagePassError = checkImagePassError,

			ScreenID = screen_id,

			DTK = dtk,
			AgentAccount = dbORM.find_one('AgentTLFY', 'user_id', current_user.id),
			LengthFunc = len,
			ToJoin = function_pool.toJoin,
			DeviceType = function_pool.detectDeviceType(kwargs['request']),
			WhichDevice = function_pool.which_device,
			GetDBItem = function_pool.getDBItem,
			ToString = str,
			RoundFloat = round,
			referral_data = function_pool.referral_data(),
			CurrentDate = function_pool.getDateTime()[0],
			ToFloat = float,
			ToInt = int,
			CurrencyExchange = function_pool.CurrencyExchange(),
			RandomID = id_generator.generateTID,
			PythonEval = function_pool.python_eval,
			ToFloatToInt = function_pool.floatToInt,
			Thousandify = function_pool.thousandify,
			getMIME = function_pool.get_mime_type,
			TimeDifference = function_pool.calcTimeDifference,
			CurrentTime = function_pool.getDateTime()[1],
			HTMLBreak_ = function_pool.HTMLBreak
		)
	else:
		return redirect(url_for("views.dashboard"))
	