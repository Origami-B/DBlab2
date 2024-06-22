from flask import Flask, render_template, request, abort, redirect, url_for
import config
import numpy as np
import datetime
from db_init import db, db2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, text, func
from models import Bank, Client, Employee, SavingAccount, CreditAccount, Loan, Apply, \
    Account, Department, Own, Checking, User
import time

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

cursor = db2.cursor()


@app.route('/')
def hello_world():
    return redirect(url_for('login'))


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    print('000')
    if request.method == 'GET':
        print('111')
        return render_template('login.html')
    else:
        print('222')
        if request.form.get('type') == 'signup':
            name = request.form.get('name')
            key = request.form.get('password')

            newUser = User(
                username=name,
                userkey=key,
            )

            print(name, key, 'signup')

            db.session.add(newUser)
            db.session.commit()
            return render_template('login.html')
        elif request.form.get('type') == 'login':

            name = request.form.get('name')
            key = request.form.get('password')
            print(name, key, 'login')
            UserNotExist = db.session.query(User).filter_by(username=name).scalar() is None

            if UserNotExist == 1:
                error_title = '登录错误'
                error_message = '用户名不存在'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            user_result = db.session.query(User).filter_by(username=name).first()
            if user_result.userkey == key:
                return render_template('index.html')
            else:
                error_title = '登录错误'
                error_message = '密码错误'
                return render_template('404.html', error_title=error_title, error_message=error_message)
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')


# 支行管理 
@app.route('/bank', methods=['GET', 'POST'])
def bank():
    labels = ['支行号', '支行名', '支行资产', '所在城市']
    result_query = db.session.query(Bank)
    result = result_query.all()
    if request.method == 'GET':
        print(result)
        return render_template('bank.html', labels=labels, content=result)
    else:
        if request.form.get('type') == 'query':
            bank_id = request.form.get('id')
            bank_name = request.form.get('name')
            bank_city = request.form.get('city')
            bank_asset = request.form.get('assets')

            if bank_id != "":
                result_query = result_query.filter(Bank.B_ID == bank_id)
            if bank_name != "":
                result_query = result_query.filter(Bank.B_Name == bank_name)
            if bank_asset != "":
                result_query = result_query.filter(Bank.Assets == bank_asset)
            if bank_city != "":
                result_query = result_query.filter(Bank.City == bank_city)

            result = result_query.all()

            return render_template('bank.html', labels=labels, content=result)

        elif request.form.get('type') == 'update':
            old_num = request.form.get('key')
            bank_name = request.form.get('bank_name')
            bank_asset = request.form.get('bank_asset')
            bank_city = request.form.get('bank_city')
            bank_result = db.session.query(Bank).filter_by(B_ID=old_num).first()
            bank_result.B_Name = bank_name
            bank_result.Assets = bank_asset
            bank_result.City = bank_city
            db.session.commit()

        elif request.form.get('type') == 'delete':
            old_id = request.form.get('key')
            BankName = db.session.query(Bank).filter_by(B_ID=old_id).first().B_Name

            print("***************111", old_id, BankName)

            BankNotExist = db.session.query(Employee).filter(Employee.B_Name==BankName).first() is None

            if BankNotExist != 1:
                error_title = '删除错误'
                error_message = '支行在存在关联员工'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            BankNotExist = db.session.query(Account).filter(Account.B_Name==BankName).first() is None

            if BankNotExist != 1:
                error_title = '删除错误'
                error_message = '支行在存在关联账户'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            BankNotExist = db.session.query(Loan).filter(Loan.B_Name==BankName).first() is None

            if BankNotExist != 1:
                error_title = '删除错误'
                error_message = '支行在存在关联贷款'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            BankNotExist = db.session.query(Checking).filter(Checking.B_Name==BankName).first() is None

            if BankNotExist != 1:
                error_title = '删除错误'
                error_message = '支行在存在关联信息'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            bank_result = db.session.query(Bank).filter(Bank.B_ID==old_id)
            print("***************222", bank_result)
            bank_result.delete()
            db.session.commit()

        elif request.form.get('type') == 'insert':
            bank_id = request.form.get('id')
            bank_name = request.form.get('name')
            bank_asset = request.form.get('estate')
            bank_city = request.form.get('city')

            newBank = Bank(
                B_ID=bank_id,
                B_Name=bank_name,
                Assets=bank_asset,
                City=bank_city
            )

            db.session.add(newBank)
            db.session.commit()

        elif request.form.get('type') == 'static':
            # Call the total_asset function
            total = db.session.query(func.total_asset()).scalar()

            print("Total assets: ", total)

            result = db.session.query(Bank).all()

            return render_template('asset.html', assets=total)

    result = db.session.query(Bank).all()

    return render_template('bank.html', labels=labels, content=result)


# 客户管理
@app.route('/client', methods=['GET', 'POST'])
def client():
    labels1 = ['客户ID', '客户姓名', '客户电话', '客户住址']
    result_query1 = db.session.query(Client)
    result1 = result_query1.all()

    if request.method == 'GET':
        print('get')
        print(result1)
        return render_template('client.html', labels=labels1, content=result1)
    else:
        if request.form.get('type') == 'query1':
            clientID = request.form.get('clientID')
            clientName = request.form.get('name')
            clientPhone = request.form.get('phone')
            clientAddress = request.form.get('address')

            if clientID != '':
                result_query1 = result_query1.filter(Client.C_ID == clientID)
            if clientName != '':
                result_query1 = result_query1.filter(Client.C_Name == clientName)
            if clientPhone != '':
                result_query1 = result_query1.filter(Client.C_Tel == clientPhone)
            if clientAddress != '':
                result_query1 = result_query1.filter(Client.C_Addr == clientAddress)

            result1 = result_query1.all()

            return render_template('client.html', labels=labels1, content=result1)

        elif request.form.get('type') == 'update1':
            clientID = request.form.get('key')
            clientName = request.form.get('name')
            clientPhone = request.form.get('phone')
            clientAddress = request.form.get('address')
            Client_result = db.session.query(Client).filter_by(C_ID=clientID).first()
            Client_result.C_Name = clientName
            Client_result.C_Tel = clientPhone
            Client_result.C_Addr = clientAddress

            db.session.commit()

        elif request.form.get('type') == 'delete1':
            clientID = request.form.get('key')
            print("***************111", clientID)
            client_result = db.session.query(Client).filter(Client.C_ID==clientID)

            # AccountNotExist = db.session.query(Own).filter(Own.C_ID==clientID).first() is None

            # if AccountNotExist != 1:
            #     error_title = '删除错误'
            #     error_message = '客户在存在关联账户'
            #     return render_template('404.html', error_title=error_title, error_message=error_message)

            ApplyNotExist = db.session.query(Apply).filter_by(C_ID=clientID).scalar() is None

            if ApplyNotExist != 1:
                error_title = '删除错误'
                error_message = '客户在存在贷款记录'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            print("***************222", client_result)
            client_result.delete()
            db.session.commit()

        elif request.form.get('type') == 'insert1':
            clientID = request.form.get('clientID')
            clientName = request.form.get('name')
            clientPhone = request.form.get('phone')
            clientAddress = request.form.get('address')

            newClient = Client(
                C_ID=clientID,
                C_Name=clientName,
                C_Tel=clientPhone,
                C_Addr=clientAddress
            )

            db.session.add(newClient)
            db.session.commit()

    result_query1 = db.session.query(Client)
    result1 = result_query1.all()
    return render_template('client.html', labels=labels1, content=result1)


# 员工管理
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    labels1 = ['员工ID', '员工姓名', '员工电话', '员工住址', '雇佣日期', '所在支行', '部门号', '部门名称', '部门类型', '部门经理ID']
    labels2 = ['部门号', '部门名称', '部门类型', '部门经理ID']
    result_query = db.session.query(Employee, Department).filter(Employee.D_ID == Department.D_ID)
    result = result_query.all()

    result_query2 = db.session.query(Department)
    result2 = result_query2.all()

    if request.method == 'GET':
        return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)
    else:
        if request.form.get('type') == 'query1':
            ID = request.form.get('staffID')
            name = request.form.get('name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            date = request.form.get('date')
            Bank = request.form.get('bank')
            departID = request.form.get('departId')
            departName = request.form.get('departName')
            departType = request.form.get('departType')
            ManagerID = request.form.get('ManagerId')

            if ID != '':
                result_query = result_query.filter(Employee.E_ID == ID)
            if name != '':
                result_query = result_query.filter(Employee.E_Name == name)
            if phone != '':
                result_query = result_query.filter(Employee.E_Tel == phone)
            if address != '':
                result_query = result_query.filter(Employee.E_Addr == address)
            if date != '':
                date = date.split('-')
                date = datetime.date(
                    int(date[0]), int(date[1]), int(date[2]))
                result_query = result_query.filter(Employee.Work_Date == date)
            if Bank != '':
                result_query = result_query.filter(Employee.B_Name == Bank)
            if departID != '':
                result_query = result_query.filter(Employee.D_ID == departID)
            if departName != '':
                result_query = result_query.filter(Department.D_Name == departName)
            if departType != '':
                result_query = result_query.filter(Department.D_Type == departType)
            if ManagerID != '':
                result_query = result_query.filter(Department.Manager_ID == ManagerID)

            result = result_query.all()

            return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)

        elif request.form.get('type') == 'query2':
            departID = request.form.get('departId')
            departName = request.form.get('departName')
            departType = request.form.get('departType')
            ManagerID = request.form.get('ManagerId')

            if departID != '':
                result_query2 = result_query2.filter(Employee.D_ID == departID)
            if departName != '':
                result_query2 = result_query2.filter(Department.D_Name == departName)
            if departType != '':
                result_query2 = result_query2.filter(Department.D_Type == departType)
            if ManagerID != '':
                result_query2 = result_query2.filter(Department.Manager_ID == ManagerID)

            result = result_query.all()
            result2 = result_query2.all()

            return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)

        elif request.form.get('type') == 'update1':
            oldID = request.form.get('key')

            phone = request.form.get('phone')
            address = request.form.get('address')
            Bank = request.form.get('bank')
            departID = request.form.get('departId')
            path = request.form.get('path')

            employee_result = db.session.query(Employee).filter_by(E_ID=oldID).first()

            employee_result.D_ID = departID
            employee_result.B_Name = Bank
            employee_result.E_Tel = phone
            employee_result.E_Addr = address
            employee_result.E_Img = path

            print("update employee")
            db.session.commit()

        elif request.form.get('type') == 'update2':
            oldID = request.form.get('key')

            departName = request.form.get('departName')
            departType = request.form.get('departType')
            ManagerID = request.form.get('ManagerId')

            Department_result = db.session.query(Department).filter_by(D_ID=oldID).first()

            Department_result.D_Name = departName
            Department_result.D_Type = departType
            Department_result.Manager_ID = ManagerID

            db.session.commit()

        elif request.form.get('type') == 'delete1':
            oldID = request.form.get('key')
            print("***************")

            # Call the stored procedure
            proc = text("CALL dismiss(:emp_id)")
            print("***************")
            result = db.session.execute(proc, {'emp_id': oldID})

            db.session.commit()

        elif request.form.get('type') == 'delete2':
            oldID = request.form.get('key')

            DepartmentNotExist = db.session.query(Employee).filter_by(D_ID=oldID).scalar() is None

            if DepartmentNotExist != 1:
                error_title = '删除错误'
                error_message = '部门在存在关联员工'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            Department_result = db.session.query(Department).filter_by(D_ID=oldID).first()

            db.session.delete(Department_result)
            db.session.commit()

        elif request.form.get('type') == 'insert1':
            ID = request.form.get('staffID')
            name = request.form.get('name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            date = request.form.get('date')
            Bank = request.form.get('bank')
            departID = request.form.get('departId')
            path = request.form.get('path')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))

            newStaff = Employee(
                E_ID=ID,
                D_ID=departID,
                E_Name=name,
                B_Name=Bank,
                E_Tel=phone,
                E_Addr=address,
                Work_Date=date,
                E_Img = path
            )

            db.session.add(newStaff)
            db.session.commit()
            result = db.session.query(Employee, Department).filter(Employee.D_ID == Department.D_ID).all()
            return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)

        elif request.form.get('type') == 'insert2':
            departID = request.form.get('departId')
            departName = request.form.get('departName')
            departType = request.form.get('departType')
            ManagerID = request.form.get('ManagerId')

            ManagerExist = db.session.query(Employee).filter(Employee.E_ID==ManagerID).first()

            print("**********gggg", ManagerExist)
            if ManagerExist is None:
                error_title = '部门插入错误'
                error_message = '不存在此经理'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            newDepartment = Department(
                D_ID=departID,
                D_Name=departName,
                D_Type=departType,
                Manager_ID=ManagerID,
            )

            db.session.add(newDepartment)
            db.session.commit()

        elif request.form.get('type') == 'imgquery':
            img_id = request.form.get('key')
            employee_result = db.session.query(Employee).filter_by(E_ID=img_id).first()
            print(img_id, employee_result.E_Name)
            return render_template('image.html', ID=img_id, name=employee_result.E_Name, path=employee_result.E_Img)

    result = db.session.query(Employee, Department).filter(Employee.D_ID == Department.D_ID).all()
    result2 = db.session.query(Department).all()
    return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)


# 账户管理
@app.route('/account', methods=['GET', 'POST'])
def account():
    labels1 = ['账户号', '客户ID', '客户姓名', '开户支行', '开户时间', '账户余额', '最近访问时间', '利率', '货币类型']
    labels2 = ['账户号', '客户ID', '客户姓名', '开户支行', '开户时间', '账户余额', '最近访问时间', '透支额度']

    content1_query = db.session.query(Account, SavingAccount, Own, Client).filter(Account.A_ID == SavingAccount.A_ID).filter(Client.C_ID == Own.C_ID).filter(Own.A_ID == Account.A_ID)
    content2_query = db.session.query(Account, CreditAccount, Own, Client).filter(CreditAccount.A_ID == Account.A_ID).filter(Account.A_ID == Own.A_ID).filter(Own.C_ID == Client.C_ID)

    content1 = content1_query.all()
    content2 = content2_query.all()
    print("******************", content1)
    print("******************", content2)

    if request.method == 'GET':
        print("******************", content2)
        return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)
    else:
        if request.form.get('type') == 'squery':
            accID = request.form.get('accId')
            clientID = request.form.get('clientID')
            clientName = request.form.get('clientName')
            BankName = request.form.get('bank')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            interestRate = request.form.get('interest')
            currType = request.form.get('currType')

            if accID != "":
                content1_query = content1_query.filter(Account.A_ID == accID)
            if clientID != "":
                content1_query = content1_query.filter(Client.C_ID == clientID)
            if clientName != "":
                content1_query = content1_query.filter(Client.C_Name == clientName)
            if BankName != "":
                content1_query = content1_query.filter(Account.B_Name == BankName)
            if openDate != "":
                openDate = openDate.split('-')
                openDate = datetime.date(
                    int(openDate[0]), int(openDate[1]), int(openDate[2]))
                content1_query = content1_query.filter(Account.Opening_Date == openDate)
            if balance != "":
                content1_query = content1_query.filter(Account.Balance == float(balance))
            if interestRate != "":
                content1_query = content1_query.filter(SavingAccount.Interest_Rate == float(interestRate))
            if currType != "":
                content1_query = content1_query.filter(SavingAccount.Currency_Type == currType)

            content1 = content1_query.all()

            return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1,
                                    content2=content2)

        elif request.form.get('type') == 'cquery':
            accID = request.form.get('accId')
            clientID = request.form.get('clientID')
            clientName = request.form.get('clientName')
            BankName = request.form.get('bank')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            VisitedDate = request.form.get('VisitDate')
            overDraft = request.form.get('overDraft')

            if accID != "":
                content2_query = content2_query.filter(Account.A_ID == accID)
            if clientID != "":
                content2_query = content2_query.filter(Client.C_ID == clientID)
            if clientName != "":
                content2_query = content2_query.filter(Client.C_Name == clientName)
            if BankName != "":
                content2_query = content2_query.filter(Account.B_Name == BankName)
            if openDate != "":
                openDate = openDate.split('-')
                openDate = datetime.date(
                    int(openDate[0]), int(openDate[1]), int(openDate[2]))
                content2_query = content2_query.filter(Account.Opening_Date == openDate)
            if VisitedDate != "":
                VisitedDate = VisitedDate.split('-')
                VisitedDate = datetime.date(
                    int(VisitedDate[0]), int(VisitedDate[1]), int(VisitedDate[2]))
                content2_query = content2_query.filter(Own.Visited_Date == VisitedDate)
            if balance != "":
                content2_query = content2_query.filter(Account.Balance == float(balance))
            if overDraft != "":
                content2_query = content2_query.filter(CreditAccount.Overdraft == float(overDraft))

            content2 = content2_query.all()

            return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1,
                                    content2=content2)

        elif request.form.get('type') == 'saddAcc':
            accID = request.form.get('accId')
            clientID = request.form.get('clientID')
            BankName = request.form.get('bank')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            interestRate = request.form.get('interest')
            currType = request.form.get('currType')

            openDate = openDate.split('-')
            openDate = datetime.date(
                int(openDate[0]), int(openDate[1]), int(openDate[2]))

            VisitedDate = time.strftime("%Y-%m-%d", time.localtime()).split('-')
            VisitedDate = datetime.date(
                int(VisitedDate[0]), int(VisitedDate[1]), int(VisitedDate[2]))

            CheckingNotExist = db.session.query(Checking).filter(Checking.C_ID==clientID).filter(Checking.
                B_Name==BankName).filter(Checking.A_Type==1).first()

            print("***********hhh", CheckingNotExist)

            if CheckingNotExist is not None:
                error_title = '开户错误'
                error_message = '客户在该银行已存在一个储蓄账户'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            AccountNotExist = db.session.query(Account.A_ID).filter(Account.A_ID==accID).first() is None
            if AccountNotExist != 1:
                error_title = '开户错误'
                error_message = '该账户号已存在'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            AccountNotExist = db.session.query(Account.A_ID).filter(Account.A_ID==accID).first() is None
            if AccountNotExist == 1:
                newAccount = Account(
                    A_ID=accID,
                    B_Name=BankName,
                    Balance=balance,
                    Opening_Date=openDate,
                )

                db.session.add(newAccount)
                db.session.commit()

                newLilAccount = SavingAccount(
                    A_ID=accID,
                    Interest_Rate=interestRate,
                    Currency_Type=currType
                )
                db.session.add(newLilAccount)
                db.session.commit()

            newChecking = Checking(
                C_ID=clientID,
                B_Name=BankName,
                A_Type=1,
                A_ID=accID,
            )
            db.session.add(newChecking)
            db.session.commit()

            newOwn = Own(
                C_ID=clientID,
                Visited_Date=VisitedDate,
                A_ID=accID,
            )

            db.session.add(newOwn)
            db.session.commit()

        elif request.form.get('type') == 'caddAcc':
            accID = request.form.get('accId')
            clientID = request.form.get('clientID')
            BankName = request.form.get('bank')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            overDraft = request.form.get('overDraft')

            openDate = openDate.split('-')
            openDate = datetime.date(
                int(openDate[0]), int(openDate[1]), int(openDate[2]))

            VisitedDate = time.strftime("%Y-%m-%d", time.localtime()).split('-')
            VisitedDate = datetime.date(
                int(VisitedDate[0]), int(VisitedDate[1]), int(VisitedDate[2]))

            CheckingNotExist = db.session.query(Checking).filter(Checking.C_ID==clientID).filter(Checking.
                B_Name==BankName).filter(Checking.A_Type==0).first()

            if CheckingNotExist is not None:
                error_title = '开户错误'
                error_message = '客户在该银行已存在一个信用账户'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            AccountNotExist = db.session.query(Account.A_ID).filter(Account.A_ID==accID).first() is None
            if AccountNotExist != 1:
                error_title = '开户错误'
                error_message = '该账户号已存在'
                return render_template('404.html', error_title=error_title, error_message=error_message)
                
            newAccount = Account(
                A_ID=accID,
                B_Name=BankName,
                Balance=balance,
                Opening_Date=openDate,
            )
            db.session.add(newAccount)
            db.session.commit()

            newLilAccount = CreditAccount(
                A_ID=accID,
                Overdraft=overDraft,
            )
            db.session.add(newLilAccount)
            db.session.commit()

            newChecking = Checking(
                C_ID=clientID,
                B_Name=BankName,
                A_Type=0,
                A_ID=accID,
            )
            db.session.add(newChecking)
            db.session.commit()
            

            newOwn = Own(
                C_ID=clientID,
                Visited_Date=VisitedDate,
                A_ID=accID,
            )
            db.session.add(newOwn)
            db.session.commit()

        elif request.form.get('type') == 'supdate':
            oldAccount = request.form.get('key')
            balance = request.form.get('sBalance')
            interestRate = request.form.get('sInterest')
            currType = request.form.get('sCType')

            SavingAccount_result = db.session.query(SavingAccount).filter_by(A_ID=oldAccount).first()
            Account_result = db.session.query(Account).filter_by(A_ID=oldAccount).first()

            Account_result.Balance = balance
            SavingAccount_result.Interest_Rate = interestRate
            SavingAccount_result.Currency_Type = currType
            db.session.commit()

        elif request.form.get('type') == 'cupdate':
            oldAccount = request.form.get('key')
            balance = request.form.get('cBalance')
            overDraft = request.form.get('cOver')

            CreditAccount_result = db.session.query(CreditAccount).filter_by(A_ID=oldAccount).first()
            Account_result = db.session.query(Account).filter_by(A_ID=oldAccount).first()

            Account_result.Balance = balance
            CreditAccount_result.Overdraft = overDraft
            db.session.commit()

        elif request.form.get('type') == 'sdelete':
            oldAccount = request.form.get('key')

            Account_result = db.session.query(Account).filter_by(A_ID=oldAccount)
            SavingAccount_result = db.session.query(SavingAccount).filter_by(A_ID=oldAccount)
            Own_result = db.session.query(Own).filter_by(A_ID=oldAccount)

            Own_result.delete()
            db.session.commit()

            SavingAccount_result.delete()
            db.session.commit()

            Account_result.delete()
            db.session.commit()

        elif request.form.get('type') == 'cdelete':
            oldAccount = request.form.get('key')

            Account_result = db.session.query(Account).filter_by(A_ID=oldAccount).first()
            CreditAccount_result = db.session.query(CreditAccount).filter_by(A_ID=oldAccount).first()
            Own_result = db.session.query(Own).filter_by(A_ID=oldAccount).first()

            db.session.delete(Own_result)
            db.session.commit()

            db.session.delete(CreditAccount_result)
            db.session.commit()

            db.session.delete(Account_result)
            db.session.commit()

    content1 = db.session.query(Account, SavingAccount, Own, Client).filter(
        Account.A_ID == SavingAccount.A_ID).filter(
        Own.A_ID == Account.A_ID).filter(Client.C_ID == Own.C_ID).all()
    content2 = db.session.query(CreditAccount, Account, Own, Client).filter(
        CreditAccount.A_ID == Account.A_ID).filter(
        Account.A_ID == Own.A_ID).filter(Own.C_ID == Client.C_ID).all()

    return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)


# 贷款管理
@app.route('/debt', methods=['GET', 'POST'])
def debt():
    labels1 = ['贷款号', '发放支行', '贷款金额', '已还金额','贷款状态']
    labels2 = ['还款号', '贷款号', '客户ID', '支付金额', '支付日期']

    content_query1 = db.session.query(Loan)
    content_query2 = db.session.query(Apply)
    result1 = content_query1.all()
    result2 = content_query2.all()

    if request.method == 'GET':
        return render_template('debt.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
    else:
        if request.form.get('type') == 'main_query':
            num = request.form.get('num')
            Bank = request.form.get('bank')
            money = request.form.get('money')
            state = request.form.get('state')

            if num != '':
                content_query1 = content_query1.filter(Loan.L_ID == num)
            if Bank != '':
                content_query1 = content_query1.filter(Loan.B_Name == Bank)
            if money != '':
                content_query1 = content_query1.filter(Loan.L_Amount == money)
            if state != '':
                content_query1 = content_query1.filter(Loan.L_Status == state)

            result1 = content_query1.all()

            return render_template('debt.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)

        elif request.form.get('type') == 'update':
            oldNum = request.form.get('key')
            money = request.form.get('money')
            date = request.form.get('date')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))

            Apply_result = db.session.query(Apply).filter_by(P_ID=oldNum).first()
            Loan_result = db.session.query(Loan).filter_by(L_ID=Apply_result.L_ID).first()
            sum_money = Loan_result.P_already - Apply_result.P_Amount

            if Loan_result.L_Status == 1:
                if sum_money + float(money) <= Loan_result.L_Amount:
                    Loan_result.P_already = sum_money + float(money)
                    Apply_result.P_Amount = money
                    Apply_result.Pay_Date = date

                    db.session.commit()
                    if sum_money + float(money) == Loan_result.L_Amount:
                        Loan_result.L_Status = 2

                        db.session.commit()
                else:
                    error_title = '更新错误'
                    error_message = '支付总金额大于贷款金额'
                    return render_template('404.html', error_title=error_title, error_message=error_message)
            else:
                error_title = '更新错误'
                error_message = '只能更新正在发放的贷款信息'
                return render_template('404.html', error_title=error_title, error_message=error_message)

        elif request.form.get('type') == 'delete':
            oldNum = request.form.get('key')

            loan_result = db.session.query(Loan).filter_by(L_ID=oldNum).first()

            if loan_result.L_Status == 1:
                error_title = '删除错误'
                error_message = '不可删除正在发放的贷款信息'
                return render_template('404.html', error_title=error_title, error_message=error_message)
            elif loan_result.L_Status == 2:
                Apply_result = db.session.query(Apply).filter_by(L_ID=oldNum).delete()
                db.session.commit()
            db.session.delete(loan_result)
            db.session.commit()

        elif request.form.get('type') == 'insert':
            num = request.form.get('num')
            Bank = request.form.get('bank')
            money = request.form.get('money')

            newLoan = Loan(
                L_ID=num,
                B_Name=Bank,
                L_Amount=money,
                L_Status=0,
                P_already=0,
            )

            db.session.add(newLoan)
            db.session.commit()

        elif request.form.get('type') == 'query':
            loanNum = request.form.get('loanNum')
            clientID = request.form.get('clientID')
            payID = request.form.get('payID')
            date = request.form.get('date')
            money = request.form.get('money')

            if loanNum != '':
                content_query2 = content_query2.filter(Apply.L_ID == loanNum)
            if clientID != '':
                content_query2 = content_query2.filter(Apply.C_ID == clientID)
            if payID != '':
                content_query2 = content_query2.filter(Apply.P_ID == payID)
            if date != '':
                content_query2 = content_query2.filter(Apply.Pay_Date == date)
            if money != '':
                content_query2 = content_query2.filter(Apply.P_Amount == money)

            result2 = content_query2.all()

            return render_template('debt.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)

        elif request.form.get('type') == 'give':
            loanNum = request.form.get('loanNum')
            clientID = request.form.get('clientID')
            payID = request.form.get('payID')
            date = request.form.get('date')
            money = request.form.get('money')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))

            Loan_result = db.session.query(Loan).filter_by(L_ID=loanNum).first()

            if Loan_result.L_Status == 0:
                if float(money) <= Loan_result.L_Amount:
                    Loan_result.L_Status = 1
                    Loan_result.P_already = money

                    newApply = Apply(
                        C_ID=clientID,
                        L_ID=loanNum,
                        P_ID=payID,
                        P_Amount=money,
                        Pay_Date=date
                    )
                    db.session.add(newApply)
                    db.session.commit()
                    if float(money) == Loan_result.L_Amount:
                        Loan_result.L_Status = 2

                        db.session.commit()

                else:
                    error_title = '发放错误'
                    error_message = '支付总金额大于贷款金额'
                    return render_template('404.html', error_title=error_title, error_message=error_message)

            elif Loan_result.L_Status == 1:

                sum_money = Loan_result.P_already

                if sum_money + float(money) <= Loan_result.L_Amount:
                    Loan_result.P_already = sum_money + float(money)

                    newApply = Apply(
                        C_ID=clientID,
                        L_ID=loanNum,
                        P_ID=payID,
                        P_Amount=money,
                        Pay_Date=date
                    )

                    db.session.add(newApply)
                    db.session.commit()
                    if sum_money + float(money) == Loan_result.L_Amount:
                        Loan_result.L_Status = 2
                        db.session.commit()

                else:
                    error_title = '发放错误'
                    error_message = '支付总金额大于贷款金额'
                    return render_template('404.html', error_title=error_title, error_message=error_message)
            else:
                error_title = '发放错误'
                error_message = '贷款已发放完毕'
                return render_template('404.html', error_title=error_title, error_message=error_message)

    content_query1 = db.session.query(Loan)
    content_query2 = db.session.query(Apply)
    result1 = content_query1.all()
    result2 = content_query2.all()

    return render_template('debt.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)

@app.route('/404')
def not_found():
    return render_template('404.html', error_title='错误标题', error_message='错误信息')

@app.route('/img')
def img_view():
    return render_template('image.html', ID="缺乏员工信息", name="", path="img/pep.png")

@app.errorhandler(Exception)
def err_handle(e):
    error_message = ''
    error_title = ''
    if (type(e) == IndexError):
        error_title = '填写错误'
        error_message = '日期格式错误! (yyyy-mm-dd)'
    elif (type(e) == AssertionError):
        error_title = '删除错误'
        error_message = '删除条目仍有依赖！'
    elif (type(e) == exc.IntegrityError):
        error_title = '更新/插入错误'
        error_message = str(e._message())
    return render_template('404.html', error_title=error_title, error_message=error_message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)