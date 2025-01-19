from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename


# from datetime import datetime
from datetime import datetime, timedelta
import base64
import random
import imghdr
import datetime as dt

from . import DateToolKit as dtk
from .db import db
from . import function_pool
from .db import dbORM
from . import encrypt
from . import ScreenGoRoute
from . import id_generator

if dbORM == None:
    User, Notes = None, None
else:
    User, Notes = dbORM.get_all("UserTLFY"), None




client_actions = Blueprint('client_actions', __name__)
ca = client_actions

@ca.route("/task/<string:rad_id_two>/<string:tid>/<string:rad_id_one>")
@login_required
def vT(tid, rad_id_one, rad_id_two):
    try:
        theTask = dbORM.get_all("TaskTLFY")[f'{tid}']

        if str(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) == "0" or int(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) <= 0:
            dbORM.delete_entry("TaskTLFY", tid)

            return ScreenGoRoute.go_to("1", _redirect=True, request=request)
        else:
            try:
                rr = f"data:{function_pool.getMIME(theTask['image_raw'])};base64,{theTask['image_raw']}"
                ipe = "false"
            except Exception as e:
                ipe = "true"
            return render_template("ViewTask.html", ToInt=int, WhichDevice=function_pool.which_device, DeviceType=function_pool.detectDeviceType(request), ImagePassError=function_pool.checkImagePassError, LengthFunc=len, PythonEval=eval, getMIME=function_pool.get_mime_type, CUser=User[f'{current_user.id}'], Task=theTask, DTK=dtk, Thousandify=function_pool.thousandify, TaskIsDone=0, image_pass_error=ipe, _from="none")
    except:
        flash("Task not found.", category="Error occurred")
        return redirect(url_for("views.dashboard"))

@ca.route("/share/task/<string:token>/<string:task_id>")
@login_required
def shareText(token, task_id):
    try:
        theTask = dbORM.get_all("TaskTLFY")[f'{task_id}']
        if theTask['task_owner'] == dbORM.get_all("UserTLFY")[f'{current_user.id}']['email'] :
            flash("Go to Agent Dashboard > Your Ads to see your ads.", category="Important")
            return redirect(url_for("views.dashboard"))
        else:
            if str(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) == "0" or int(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) <= 0:
                dbORM.delete_entry("TaskTLFY", task_id)

                return ScreenGoRoute.go_to("1", _redirect=True, request=request)
            else:
                try:
                    rr = f"data:{function_pool.getMIME(theTask['image_raw'])};base64,{theTask['image_raw']}"
                    ipe = "false"
                except Exception as e:
                    ipe = "true"
                return render_template("ViewTask.html", ToInt=int, WhichDevice=function_pool.which_device, DeviceType=function_pool.detectDeviceType(request), ImagePassError=function_pool.checkImagePassError, LengthFunc=len, PythonEval=eval, getMIME=function_pool.get_mime_type, CUser=User[f'{current_user.id}'], Task=theTask, DTK=dtk, Thousandify=function_pool.thousandify, TaskIsDone=0, image_pass_error=ipe, _from="none")
    except:
        flash("Task not found.", category="Error occurred")
        return redirect(url_for("views.dashboard"))

@ca.route("/my-task/<string:rad_id_two>/<string:tid>/<string:rad_id_one>")
@login_required
def vMT(tid, rad_id_one, rad_id_two):
    try:
        theTask = dbORM.get_all("TaskTLFY")[f'{tid}']

        if str(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) == "0" or int(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) <= 0:
            dbORM.delete_entry("TaskTLFY", tid)

            return ScreenGoRoute.go_to("1", _redirect=True, request=request)
        else:
            try:
                rr = f"data:{function_pool.getMIME(theTask['image_raw'])};base64,{theTask['image_raw']}"
                ipe = "false"
            except Exception as e:
                ipe = "true"
            return render_template("ViewMyTask.html", ImagePassError=function_pool.checkImagePassError, LengthFunc=len, PythonEval=eval, getMIME=function_pool.get_mime_type, CUser=User[f'{current_user.id}'], Task=theTask, DTK=dtk, Thousandify=function_pool.thousandify, TaskIsDone=0, image_pass_error=ipe, _from="none", Agent=dbORM.get_all("AgentTLFY")[f'{dbORM.find_one("AgentTLFY", "user_id", current_user.id)}'])
    except:
        flash("Go to Agent Dashboard > Your Ads to see your ads.", category="Important")
        return redirect(url_for("views.dashboard"))

@ca.route("/delete-my-task/<string:task_id>")
@login_required
def delete_my_task(task_id):
    dbORM.delete_entry("TaskTLFY", task_id)
    flash(f"Deleted Ad successfully.", category="Success")

    return redirect(url_for("client_actions.viewAgentDashboard"))

@ca.route("/task/<string:rad_id_two>/<string:tid>/<string:rad_id_one>/from_TaskPage")
@login_required
def vT2(tid, rad_id_one, rad_id_two):
    theTask = dbORM.get_all("TaskTLFY")[f'{tid}']

    if str(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) == "0" or int(dtk.calculate_difference(theTask['datestamp'], theTask['expiry_date'])) <= 0:
        dbORM.delete_entry("TaskTLFY", tid)

        return ScreenGoRoute.go_to("1", _redirect=True, request=request)
    else:
        try:
            rr = f"data:{function_pool.getMIME(theTask['image_raw'])};base64,{theTask['image_raw']}"
            ipe = "false"
        except Exception as e:
            ipe = "true"
        return render_template("ViewTask.html", ToInt=int, WhichDevice=function_pool.which_device, DeviceType=function_pool.detectDeviceType(request), ImagePassError=function_pool.checkImagePassError, LengthFunc=len, PythonEval=eval, getMIME=function_pool.get_mime_type, CUser=User[f'{current_user.id}'], Task=theTask, DTK=dtk, Thousandify=function_pool.thousandify, TaskIsDone=0, image_pass_error=ipe, _from="taskpage")


    
@ca.route("/dashboard/update-status")
def update_status():
    
    u = dbORM.get_all("UserTLFY")[f"{current_user.id}"]
    dbORM.update_entry(
        "UserTLFY", 
        f"{dbORM.find_one('UserTLFY', 'id', str(current_user.id))}", 
        encrypt.encrypter(str(
            {
                "referral_earning": f"1"
            }
        )), 
        dnd=False
    )

    return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@ca.route("/task/<string:rad_id>/<string:task_id>")
@login_required
def viewTask(rad_id, task_id):
    # try:
    theTask = dbORM.get_all("TaskTLFY")[f'{task_id}']

    def is_done():
        pool = []
        for p in range(41):
            pool.append(p)

        return random.choice(pool)

    if int(current_user.id) in eval(theTask['users_id_done']):
        return ScreenGoRoute.go_to("1", _redirect=True, request=request)
    else:
        participating_users_id = eval(theTask['users_id'])
        if int(current_user.id) in participating_users_id:
            new_participating_users_id = participating_users_id
            new_participating_users_id.append(int(current_user.id))

            dbORM.update_entry(
                "TaskTLFY", 
                f"{dbORM.find_one('TaskTLFY', 'id', task_id)}", 
                encrypt.encrypter(str(
                    {
                        "users_id": f"{new_participating_users_id}"
                    }
                )), 
                dnd=False
            )

        try:
            rr = f"data:{function_pool.getMIME(theTask['image_raw'])};base64,{theTask['image_raw']}"
            ipe = "false"
        except Exception as e:
            ipe = "true"

        return render_template("ViewTask.html", ToInt=int, WhichDevice=function_pool.which_device, DeviceType=function_pool.detectDeviceType(request), ImagePassError=function_pool.checkImagePassError, LengthFunc=len, PythonEval=eval, getMIME=function_pool.get_mime_type, CUser=User[f'{current_user.id}'], Task=theTask, DTK=dtk, Thousandify=function_pool.thousandify, TaskIsDone=is_done(), image_pass_error=ipe, _from="none")
    # except Exception as e:
        
    #     return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@ca.route("/upload-reciept", methods=['POST'])
@login_required
def UploadReciept():
    _ = {"username": request.form['username'], "task_id": request.form['task_id']}
    dbORM.add_entry("RReceipt", encrypt.encrypter(str(_)))
    dbORM.update_entry(
        "RReceipt",
        f"{dbORM.find_one('RReceipt', 'username', request.form['username'])}",
        str(
            {"image_raw": f"{function_pool.encode_image(request.files['image'])}"}
        ),
        dnd=True
    )
    return redirect(url_for("client_actions.update_status"))

@ca.route("/withdrawTaskBalance/<string:task_id>/<string:rad_id>")
@login_required
def WithdrawTaskPoint(task_id, rad_id):

    theTask = dbORM.get_all("TaskTLFY")[f'{task_id}']

    dbORM.update_entry(
        "UserTLFY", 
        f"{dbORM.find_one('UserTLFY', 'id', str(current_user.id))}", 
        encrypt.encrypter(str(
            {
                "wallet_balance": f"{float(dbORM.get_all('UserTLFY')[current_user.id]['wallet_balance']) + float(theTask['points'])}"
            }
        )), 
        dnd=False
    )

    # participating_users_id = eval(theTask['users_id'])
    # if int(current_user.id) in participating_users_id:
    participating_users_id_done = eval(theTask['users_id_done'])
    participating_users_id_done.append(int(current_user.id))

    dbORM.update_entry(
        "TaskTLFY", 
        f"{dbORM.find_one('TaskTLFY', 'id', task_id)}", 
        encrypt.encrypter(str(
            {
                "users_id_done": f"{participating_users_id_done}"
            }
        )), 
        dnd=False
    )

    flash(f"Task completed and TT {theTask['points']} earned.", category="Success")

    return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@ca.route("/withdrawBalance", methods=['POST'])
@login_required
def withdrawBalance():
    _ = {
        'user_wallet_address': dbORM.get_all("UserTLFY")[f'{current_user.id}']["user_id"],
        'dob': dbORM.get_all("UserTLFY")[f'{current_user.id}']["dob"],
        'tid': f"{id_generator.generateTID()}-{id_generator.generateTID()}-{id_generator.generateTID()}",
        'username': dbORM.get_all("UserTLFY")[f'{current_user.id}']["username"],
        'user_first_name': dbORM.get_all("UserTLFY")[f'{current_user.id}']["first_name"],
        'user_last_name': dbORM.get_all("UserTLFY")[f'{current_user.id}']["last_name"],
        'timestamp': f"{function_pool.getDateTime()[1]}",
        'datestamp': f"{function_pool.getDateTime()[0]}",
        'status': "Pending",
        'amount': f"{round(float(request.form['amount']) * float(request.form['CEx']), 2)}",
        'bank': request.form['bank'],
        'account_number': request.form['account_number']
    }
    dbORM.add_entry("WithdrawTLFY", encrypt.encrypter(str(_)))

    dbORM.update_entry(
        "UserTLFY", 
        f"{dbORM.find_one('UserTLFY', 'id', str(current_user.id))}", 
        encrypt.encrypter(str(
            {
                "wallet_balance": f"{float(dbORM.get_all('UserTLFY')[current_user.id]['wallet_balance']) - float(request.form['amount'])}"
            }
        )), 
        dnd=False
    )
    flash(f"Withdrawal Request made successfully.", category="Success")


    return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@ca.route("/send-points", methods=['POST'])
@login_required
def sendPoints():
    amount = request.form['amount']
    recipient_address = request.form['rec_wallet_address']

    try:
        theUser = dbORM.get_all("UserTLFY")[f"{dbORM.find_one('UserTLFY', 'user_id', recipient_address)}"]
        dbORM.update_entry(
            "UserTLFY", 
            f"{dbORM.find_one('UserTLFY', 'user_id', recipient_address)}", 
            encrypt.encrypter(str(
                {
                    "wallet_balance": f"{float(theUser['wallet_balance']) + float(amount)}"
                }
            )), 
            dnd=False
        )
        u = dbORM.get_all("UserTLFY")[f"{current_user.id}"]
        dbORM.update_entry(
            "UserTLFY", 
            f"{dbORM.find_one('UserTLFY', 'id', str(current_user.id))}", 
            encrypt.encrypter(str(
                {
                    "wallet_balance": f"{float(u['wallet_balance']) - float(amount)}"
                }
            )), 
            dnd=False
        )
        flash(f"Sent TT {amount} to {recipient_address}.", category="Success")

    except:
        pass
        flash(f"User with wallet address not found.", category="Error occurred")


    return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@ca.route("/delete-account/<string:user_id>")
def deleteAccount(user_id):
    dbORM.delete_entry("UserTLFY", user_id)
    
    flash(f"Deleted account.", category="Success")

    return redirect(url_for("views.welcome"))

@ca.route("/all-tasks")
def viewAllTasks():
    u = dbORM.get_all("UserTLFY")[f'{current_user.id}']
    all_t = dbORM.get_all("TaskTLFY")
    all_t_list = []
    for _tx, _ty in all_t.items():
        all_t_list.append(_ty)

    return render_template("TaskList.html", WhichDevice=function_pool.which_device, DeviceType=function_pool.detectDeviceType(request), CUser=u, AllTasks=all_t_list, active_tab="All", tabs=['All', 'Android', 'iOS', 'Desktop', '< TT 100.0', '< TT 500.0', '< TT 1,000', '< TT 1,500', '< TT 5,000'], len=len)

@ca.route("/filter-task/<string:filter_>")
def filterUserList(filter_):
    u = dbORM.get_all("UserTLFY")[f'{current_user.id}']
    t = dbORM.get_all("TaskTLFY")
    def getRangeData(n1, n2):
        all_t_list = []
        for x in range(n1, n2):
            try:
                all_t_list.append(t[f'{dbORM.find_one("TaskTLFY", "points", x)}'])
            except:
                pass

        return all_t_list

    if filter_ == "< TT 100.0":
        all_t_list = getRangeData(1, 100)

    elif filter_ == "< TT 500.0":
        all_t_list = getRangeData(101, 500)

    elif filter_ == "< TT 1,000":
        all_t_list = getRangeData(1001, 1500)

    elif filter_ == "< TT 1,500":
        all_t_list = getRangeData(1501, 2000)

    elif filter_ == "< TT 5,000":
        all_t_list = getRangeData(5001, 5500)

    elif filter_ == "Android":
        all_t_list = dbORM.find_all("TaskTLFY", "task_device", "ADR")

    elif filter_ == "iOS":
        all_t_list = dbORM.find_all("TaskTLFY", "task_device", "IOS")

    elif filter_ == "Desktop":
        all_t_list = dbORM.find_all("TaskTLFY", "task_device", "DEK")

    else:
        all_t = dbORM.get_all("TaskTLFY")
        all_t_list = []
        for _ux, _uy in all_t.items():
            all_t_list.append(_uy)
    
    return render_template("TaskList.html", WhichDevice=function_pool.which_device, DeviceType=function_pool.detectDeviceType(request), CUser=u, AllTasks=all_t_list, active_tab=filter_, tabs=['All', 'Android', 'iOS', 'Desktop', '< TT 100.0', '< TT 500.0', '< TT 1,000', '< TT 1,500', '< TT 5,000'], len=len)

@ca.route("/start-agent-process")
@login_required
def startAgent():
    try:
        u = dbORM.get_all("UserTLFY")[f'{current_user.id}']
        # agents = dbORM.find_one("AgentTLFY", "user_id", u['id'])
        # print("eeeeeeeeeeeeeeerrrr", u['id'])
        Tasks = dbORM.get_all("TaskTLFY")
        tasks_list = dbORM.find_all("TaskTLFY", "task_owner", u['email'])

        def checkImagePassError(image_raw):
            try:
                rr = f"data:{function_pool.getMIME(image_raw)};base64,{image_raw}"
                return "false"
            except:
                return "true"

        return render_template("AgentDashboard.html", Tasks=tasks_list, getMIME=function_pool.get_mime_type, ImagePassError=checkImagePassError, CUser=u, DBORM=function_pool.getDBItem, TotalRevenue=0, ToInt=int, ToFloat=float, FloorX=round, ToStr=str, LengthFunc=len, PythonEval=eval)
    except:
        return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@ca.route("/view-agent-dashboard")
@login_required
def viewAgentDashboard():
    try:
        u = dbORM.get_all("UserTLFY")[f'{current_user.id}']
        a = dbORM.get_all("AgentTLFY")[f"{dbORM.find_one('AgentTLFY', 'user_id', current_user.id)}"]
        Tasks = dbORM.get_all("TaskTLFY")
        tasks_list = dbORM.find_all("TaskTLFY", "task_owner", a['agent_email'])

        dbORM.update_entry(
            "UserTLFY", 
            f"{dbORM.find_one('UserTLFY', 'id', current_user.id)}", 
            encrypt.encrypter(str(
                {
                    "wallet_balance": f"{float(a['earnings']) + float(u['wallet_balance'])}"
                }
            )), 
            dnd=False
        )
        revenues = []
        

        if tasks_list != []:
            for task in tasks_list:
                revenues.append(float(len(eval(task['users_id_done']))) * 0.08)
                
        total_revenue = sum(revenues)

        dbORM.update_entry(
            "AgentTLFY", 
            f"{dbORM.find_one('AgentTLFY', 'user_id', current_user.id)}", 
            encrypt.encrypter(str(
                {
                    "earnings": f"{total_revenue}"
                }
            )), 
            dnd=False
        )
        

        def checkImagePassError(image_raw):
            try:
                rr = f"data:{function_pool.getMIME(image_raw)};base64,{image_raw}"
                return "false"
            except:
                return "true"

        return render_template("AgentDashboard.html", Tasks=tasks_list, getMIME=function_pool.get_mime_type, ImagePassError=checkImagePassError, CUser=u, DBORM=function_pool.getDBItem, Agent=a, Thousandify=function_pool.thousandify, TotalRevenue=total_revenue, ToInt=int, ToFloat=float, FloorX=round, ToStr=str, LengthFunc=len, PythonEval=eval)
    except:
        _pos = random.choice([1, 2])
        if _pos == 1:
            flash("Something went wrong while starting your Agent dashboard. Try again.", category="Error occurred")
        else:
            flash("Something went wrong while starting your Agent dashboard. Create new agent account.", category="Error occurred 2")

        return ScreenGoRoute.go_to("1", _redirect=True, request=request)

@ca.route("/create-agent", methods=['POST'])
@login_required
def createAgent():
    _ = {
        "agent_name": request.form['agent_name'].replace("'", ''),
        "agent_email": request.form['agent_email'],
        "agent_number": request.form['agent_number'],
        "user_id": dbORM.get_all('UserTLFY')[f'{current_user.id}']['id'],
        "earnings": "0",
        "tier": "1",
        "tasks_count": "0",
        "tasks_id": "[]"
    }
    dbORM.add_entry("AgentTLFY", encrypt.encrypter(str(_)))
    flash(f"Agent account created.", category="Success")

    return redirect(url_for("client_actions.viewAgentDashboard"))

@ca.route("/transfer-balance-to-nine")
def transferBalanceToNine():
    u = dbORM.get_all("UserTLFY")[f'{current_user.id}']
    a = dbORM.get_all("AgentTLFY")[f"{dbORM.find_one('AgentTLFY', 'user_id', current_user.id)}"]


    return redirect(url_for("client_actions.viewAgentDashboard"))

@ca.route("/create-ad-task", methods=['POST'])
@login_required
def createTask():
    cuid = f"{current_user.id}"
    if dbORM.get_all("AgentTLFY")[f"{dbORM.find_one('AgentTLFY', 'user_id', cuid)}"]['user_id'] == cuid :
        image = request.files['task_image']
        task_plan = request.form['task_plan']

        if task_plan == "basic":
            day = 2
            amount = "600"
        elif task_plan == "advance":
            day = 4
            amount = "1000"
        else:
            day = 5
            amount = "1200"

        if image:
            filename = str(secure_filename(image.filename))
            task_temp_id = id_generator.generateTID()

            task_data = {
                "name": request.form['task_name'].replace("'", ""),
                "task_link": request.form['task_link'],
                "task_type": request.form['task_type'],
                "points": f"{random.choice(['40', '60', '80', '75', '100', '65', '50', '45'])}",
                "description": request.form['description'].replace("'", ""),
                "image_name": f"{filename}",
                "image_raw": f"{task_temp_id}",
                "datestamp": f"{function_pool.getDateTime()[0]}",
                "users_id": f"[]",
                "timestamp": f"{function_pool.getDateTime()[1]}",
                "users_id_done": f"[]",
                "expiry_date": f"{dt.date.today() + timedelta(days=day)}",
                "task_owner": f"{dbORM.get_all('UserTLFY')[f'{current_user.id}']['email']}",
                "task_device": "ADR"
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
                "name": request.form['task_name'].replace("'", ""),
                "task_link": request.form['task_link'],
                "task_type": request.form['task_type'],
                "points": f"{random.choice(['40', '60', '80', '75', '100', '65', '50', '45'])}",
                "description": request.form['description'].replace("'", ""),
                "image_name": filename,
                "image_raw": "Default-Logo",
                "datestamp": f"{function_pool.getDateTime()[0]}",
                "users_id": f"[]",
                "timestamp": f"{function_pool.getDateTime()[1]}",
                "users_id_done": f"[]",
                "expiry_date": f"{dt.date.today() + timedelta(days=day)}",
                "task_owner": f"{dbORM.get_all('UserTLFY')[f'{current_user.id}']['email']}",
                "task_device": "ADR"
            }

            dbORM.add_entry("TaskTLFY", encrypt.encrypter(str(task_data)))

        _name_replaced = request.form["task_name"].replace("'", "")
        theAddedTask = dbORM.get_all("TaskTLFY")[f'{dbORM.find_one("TaskTLFY", "name", _name_replaced)}']
        theAgent = dbORM.get_all("AgentTLFY")[f'{dbORM.find_one("AgentTLFY", "user_id", current_user.id)}']
        agentTaks = eval(theAgent['tasks_id'])
        agentTaks.append(int(theAddedTask['id']))

        dbORM.update_entry(
            "AgentTLFY", 
            f"{dbORM.find_one('AgentTLFY', 'user_id', current_user.id)}", 
            encrypt.encrypter(str(
                {
                    "tasks_id": f"{agentTaks}",
                    "tasks_count": f"{int(theAgent['tasks_count']) + 1}"
                }
            )), 
            dnd=False
        )
        
    
        return render_template("PayLink.html", amount=amount, data={"task_id": theAddedTask['id'], "agent": theAgent, "title": f"Payment for {request.form['task_name']}"})

    return redirect(url_for("client_actions.viewAgentDashboard"))

@ca.route("/delete-ad-task/<string:task_id>")
@login_required
def deleteTask(task_id):
    dbORM.delete_entry("TaskTLFY", task_id)
    flash(f"Deleted Ad successfully.", category="Success")
    
    return redirect(url_for("client_actions.viewAgentDashboard"))