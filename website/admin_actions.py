from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user


import base64
import imghdr
import random
from datetime import datetime, timedelta
import datetime as dt

from . import DateToolKit as dtk
from .db import db
from .db import dbORM
from . import encrypt
from . import ScreenGoRoute
from . import function_pool
from . import id_generator

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("User"), None


today = dt.datetime.now().date()


admin_actions = Blueprint('admin_actions', __name__)
aa = admin_actions

@aa.route("/create-task", methods=['POST'])
@login_required
def createTask():

    if dbORM.get_all("UserTLFY")[f"{current_user.id}"]['user_type'] == "admin" :
        image = request.files['task_image']

        if image:
            filename = str(secure_filename(image.filename))
            task_temp_id = id_generator.generateTID()

            task_data = {
                "name": request.form['task_name'],
                "task_link": request.form['task_link'],
                "task_type": request.form['task_type'],
                "points": f"{request.form['task_points']}",
                "description": request.form['description'],
                "image_name": f"{filename}",
                "image_raw": f"{task_temp_id}",
                "datestamp": f"{function_pool.getDateTime()[0]}",
                "users_id": "[]",
                "timestamp": f"{function_pool.getDateTime()[1]}",
                "users_id_done": "[]",
                "expiry_date": f"{dt.date.today() + timedelta(days=int(random.choice(['4', '5', '6', '3', '2', '1'])))}",
                "task_owner": "Tasklify",
                "task_device": request.form['task_device']
            }

            dbORM.add_entry("TaskTLFY", encrypt.encrypter(str(task_data)))
            dbORM.update_entry(
                "TaskTLFY", 
                f"{dbORM.find_one('TaskTLFY', 'image_raw', str(task_temp_id))}", 
                str(
                    {
                        "image_raw": f"{function_pool.encode_image(image)}"
                    }
                ), 
                dnd=True
            )

        else:
            filename = "Default_TT_logo.png"

            task_data = {
                "name": request.form['task_name'],
                "task_link": request.form['task_link'],
                "task_type": request.form['task_type'],
                "points": f"{request.form['task_points']}",
                "description": request.form['description'],
                "image_name": filename,
                "image_raw": "Default-Logo",
                "datestamp": f"{function_pool.getDateTime()[0]}",
                "users_id": "[]",
                "timestamp": f"{function_pool.getDateTime()[1]}",
                "users_id_done": "[]",
                "expiry_date": f"{dt.date.today() + timedelta(days=int(random.choice(['4', '5', '6', '3', '2', '1'])))}",
                "task_owner": "Tasklify",
                "task_device": request.form['task_device']
            }

            dbORM.add_entry("TaskTLFY", encrypt.encrypter(str(task_data)))
        
    flash(f"Created Task successfully.", category="Success")
    
    return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@aa.route("/all-withdrawals")
def showAllWithdrawals():
    u = dbORM.get_all("UserTLFY")[f'{current_user.id}']
    all_t = dbORM.get_all("WithdrawTLFY")
    all_t_list = []
    for _tx, _ty in all_t.items():
        all_t_list.append(_ty)

    return render_template("AllWithdrawals.html", WhichDevice=function_pool.which_device, DeviceType=function_pool.detectDeviceType(request), CUser=u, WithdrawalRequests=dbORM.find_all("WithdrawTLFY", "status", "Pending"), DTK=dtk, Thousandify=function_pool.thousandify, Alltime_NGN=function_pool.calculate_total_net(), active_tab="Review", tabs=['Review', 'Successful', 'Failed'], len=len)

@aa.route("/filter-withdrawal-list/<string:filter_>")
def filterWList(filter_):
    u = dbORM.get_all("UserTLFY")[f'{current_user.id}']
    # all_t = dbORM.get_all("WithdrawTLFY")
    # all_t_list = []
    # for _tx, _ty in all_t.items():
    #     all_t_list.append(_ty)

    if filter_ == "Review":
        all_t_list = dbORM.find_all("WithdrawTLFY", "status", "Pending")
        # all_t_list = []

    elif filter_ == "Successful":
        all_t_list = dbORM.find_all("WithdrawTLFY", "status", "success")
        # all_t_list = []

    elif filter_ == "Failed":
        all_t_list = dbORM.find_all("WithdrawTLFY", "status", "failed")
        # all_t_list = []


    return render_template("AllWithdrawals.html", WhichDevice=function_pool.which_device, DeviceType=function_pool.detectDeviceType(request), CUser=u, WithdrawalRequests=all_t_list, DTK=dtk, Thousandify=function_pool.thousandify, Alltime_NGN=function_pool.calculate_total_net(), active_tab=filter_, tabs=['Review', 'Successful', 'Failed'], len=len)

@aa.route("/sign-withdrwal", methods=['POST'])
@login_required
def sign_statement():
    withdrawal_id = request.form['withdrawal_id']
    theWithdrawal = dbORM.get_all("WithdrawTLFY")[f'{withdrawal_id}']
    statement = request.form['sign_statement']

    dbORM.update_entry(
        "WithdrawTLFY", 
        f"{dbORM.find_one('WithdrawTLFY', 'id', withdrawal_id)}", 
        encrypt.encrypter(str(
            {
                "status": statement
            }
        )), 
        dnd=False
    )

    if statement == "failed":
        theUser = dbORM.get_all("UserTLFY")[f"{dbORM.find_one('UserTLFY', 'user_id', theWithdrawal['user_wallet_address'])}"]
        dbORM.update_entry(
            "UserTLFY", 
            f"{dbORM.find_one('UserTLFY', 'user_id', theWithdrawal['user_wallet_address'])}", 
            encrypt.encrypter(str(
                {
                    "wallet_balance": f"{float(theUser['wallet_balance']) + (float(theWithdrawal['amount']) / float(function_pool.CurrencyExchange()))}"
                }
            )), 
            dnd=False
        )

    return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@aa.route("/sign-receipt", methods=['POST'])
def signR():
    theRecept = dbORM.get_all("RReceipt")[f'{dbORM.find_one("RReceipt", "id", request.form["Reciept_id"])}']
    theUser = dbORM.get_all("AgentTLFY")[f"{dbORM.find_one('AgentTLFY', 'agent_email', theRecept['username'])}"]
    if request.form['sign_statement'] == 'success' :
        dbORM.update_entry(
            "TaskTLFY", 
            f"{dbORM.find_one('TaskTLFY', 'id', theRecept['task_id'])}", 
            encrypt.encrypter(str(
                {
                    "task_type": "AD"
                }
            )), 
            dnd=False
        )
    else:
        dbORM.delete_entry("TaskTLFY", f"{dbORM.find_one('TaskTLFY', 'task_owner', theRecept['username'])}")

    dbORM.delete_entry("RReceipt", f'{dbORM.find_one("RReceipt", "id", request.form["Reciept_id"])}')
    return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@aa.route("/unsign-user/<string:user_id>")
@login_required
def unSignuser(user_id):
    dbORM.update_entry(
        "UserTLFY", 
        f"{dbORM.find_one('UserTLFY', 'id', user_id)}", 
        encrypt.encrypter(str(
            {
                "referral_earning": f"0"
            }
        )), 
        dnd=False
    )
    return redirect(url_for("admin_actions.viewUserList"))

@aa.route("/sign-user/<string:user_id>")
@login_required
def Signuser(user_id):
    dbORM.update_entry(
        "UserTLFY", 
        f"{dbORM.find_one('UserTLFY', 'id', user_id)}", 
        encrypt.encrypter(str(
            {
                "referral_earning": f"2"
            }
        )), 
        dnd=False
    )
    return redirect(url_for("admin_actions.viewUserList"))

@aa.route("/delete-task/<string:task_id>")
@login_required
def selete_dask(task_id):
    dbORM.delete_entry("TaskTLFY", task_id)
    return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@aa.route("/user-list")
@login_required
def viewUserList():
    u = dbORM.get_all("UserTLFY")[f'{current_user.id}']
    all_u = dbORM.get_all("UserTLFY")
    all_u_list = []
    for _ux, _uy in all_u.items():
        all_u_list.append(_uy)

    client_count = dbORM.find_all("UserTLFY", "user_type", "client")
    registered_count = dbORM.find_all("UserTLFY", "referral_earning", "2")
    clients_paid = []

    for _c in range(len(client_count)):
        for _r in range(len(registered_count)):
            if _r == _c:
                clients_paid.append(_r)

            # break
    
    if u['user_type'] == 'client':
        return redirect(url_for("views.dashboard"))
    else:
        return render_template("UserList.html", CUser=u, AllUsers=all_u_list, client_count=len(dbORM.find_all("UserTLFY", "user_type", "client")), admin_count=len(dbORM.find_all("UserTLFY", "user_type", "admin")), clients_paid=len(clients_paid), tabs=['all', 'clients', 'admins', 'registered', 'to-review', 'not-registered'], active_tab="all", clients_net_value=function_pool.thousandify(function_pool.calculate_net_value(dbORM.find_all("UserTLFY", "user_type", "client"))))
    
@aa.route("/filter-user-list/<string:filter_>")
def filterUserList(filter_):
    u = dbORM.get_all("UserTLFY")[f'{current_user.id}']

    clients = dbORM.find_all("UserTLFY", "user_type", "client")
    admins = dbORM.find_all("UserTLFY", "user_type", "admin")
    registered_clients = dbORM.find_all("UserTLFY", "referral_earning", "2")
    clients_paid = []

    for _c in range(len(clients)):
        for _r in range(len(registered_clients)):
            if _r == _c:
                clients_paid.append(_r)

    if filter_ == "clients":
        all_u_list = clients

    elif filter_ == "admins":
        all_u_list = admins

    elif filter_ == "registered":
        all_u_list = registered_clients

    elif filter_ == "to-review":
        all_u_list = dbORM.find_all("UserTLFY", "referral_earning", "1")

    elif filter_ == "not-registered":
        all_u_list = dbORM.find_all("UserTLFY", "referral_earning", "0")

    else:
        all_u = dbORM.get_all("UserTLFY")
        all_u_list = []
        for _ux, _uy in all_u.items():
            all_u_list.append(_uy)
    

    if u['user_type'] == 'client':
        return redirect(url_for("views.dashboard"))
    else:
        return render_template("UserList.html", CUser=u, AllUsers=all_u_list, client_count=len(clients), admin_count=len(admins), clients_paid=len(clients_paid), active_tab=filter_, tabs=['all', 'clients', 'admins', 'registered', 'to-review', 'not-registered'], clients_net_value=function_pool.thousandify(function_pool.calculate_net_value(dbORM.find_all("UserTLFY", "user_type", "client"))))

@aa.route("/remove-user/<string:user_id>")
def removeUser(user_id):
    dbORM.delete_entry("UserTLFY", user_id)
    flash(f"Removed User successfully.", category="Success")

    return redirect(url_for("admin_actions.viewUserList"))