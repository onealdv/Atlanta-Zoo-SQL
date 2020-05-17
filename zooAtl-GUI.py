# V2.0 GROUP #58

#Animal Detail Page



import pymysql
import datetime
import sys
import re
from PyQt5.QtWidgets import (
   QApplication,
    QMainWindow,
    qApp,
    QAction,
    QWidget,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QSplitter,
    QGroupBox,
    QFormLayout,
    QPushButton,
    QComboBox,
    QTableView,
    QMessageBox,
    QDateEdit,
    QTimeEdit,
    QRadioButton,
    QDialogButtonBox,
    QDialog,
    QTableWidget,
    QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,
    QGridLayout,
    QSpinBox,
    QCalendarWidget
    )
from PyQt5.QtGui import (
    QIcon,
    QIntValidator)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QVariant,
    QCoreApplication
)


class LoginWindow(QWidget): #every window is a new class
    def __init__(self):
        super(LoginWindow,self).__init__()
        self.setWindowTitle("Login")

        #defining different elements
        unlabel = QLabel("Email")
        pwlabel = QLabel("Password")
        self.usernameText = QLineEdit() #textbox
        self.passwordText = QLineEdit()
        self.passwordText.setEchoMode(QLineEdit.Password)
        loginButton = QPushButton("Login")
        registerButton = QPushButton("Register")

        #put into grid layout
        grid = QGridLayout()
        grid.addWidget(unlabel,1,0)
        grid.addWidget(pwlabel,2,0) #2,0 is the grid coordinate position
        grid.addWidget(self.usernameText,1,1)
        grid.addWidget(self.passwordText,2,1)
        grid.addWidget(loginButton,3,0,1,2) #the extra 1 and 2 is button takes up 1 row and 2 columns width
        grid.addWidget(registerButton,4,0,1,2)

        self.setLayout(grid)

        loginButton.clicked.connect(lambda: self.LoginValidation(self.usernameText.text(),self.passwordText.text()))
        # loginButton.clicked.connect(self.login_box)
        registerButton.clicked.connect(self.Register)

    def LoginValidation(self, email, password):
        curs = connection.cursor()
        if email != '' and password !='':
            query = f"select role from user where email = '{email}' && password = md5('{password}')"
            curs.execute(query)
            result = curs.fetchone()

            if result is not None:
                usercurs = connection.cursor()
                usercurs.execute(f"select * from user where email = '{email}'")
                uname = usercurs.fetchone()['username']

                print("Logged in as " + email) #change to message box
                if 'staff' in result.values():
                    self.Login('staff', uname)
                    self.login_box('staff')
                if 'visitor' in result.values():
                    self.Login('visitor', uname)
                    self.login_box('visitor')
                if 'admin' in result.values():
                    self.Login('admin', uname)
                    self.login_box('admin')
            else:
                self.login_box("fail")
                print("Failed to find login") #change to message box
        else:
            self.login_box("empty")

    def Login(self, role, username):
        print("CONGRATS YOU ARE Login")
        if role == 'visitor':
            self.visitwin = VisitorWindow(self, username)
        elif role == 'staff':
            self.visitwin = StaffWindow(self, username)
        elif role =='admin':
            self.visitwin = AdminWindow(self)
        self.visitwin.show()
        self.close()

    def login_box(self,status):
        if status == "empty":
            logger = QMessageBox.information(self,
                                "Login",
                                "Please enter something",
                                QMessageBox.Ok)
        elif status =="visitor":
            logger = QMessageBox.information(self,
                                "Login",
                                "Welcome visitor",
                                QMessageBox.Ok)
        elif status =="admin":
            logger = QMessageBox.information(self,
                                "Login",
                                "Welcome admin",
                                QMessageBox.Ok)
        elif status =="staff":
            logger = QMessageBox.information(self,
                                "Login",
                                "Welcome staff",
                                QMessageBox.Ok)
        else:
            logger = QMessageBox.information(self,
                                "Login",
                                "Failed to login",
                                QMessageBox.Ok)

    def Register(self):
        self.regwindow = RegistrationWindow(self)
        self.regwindow.show()
        self.close()

class RegistrationWindow(QWidget):
    def __init__(self,main): #main allows the window to know where it came from
        super(RegistrationWindow,self).__init__()
        self.setWindowTitle("Register")
        self.main = main

        emaillabel = QLabel("Email")
        unlabel = QLabel("Username")
        pwlabel = QLabel("Password")
        pw2label = QLabel("Confirm Password")
        self.emailText = QLineEdit()
        self.usernameText = QLineEdit() #textbox
        self.passwordText = QLineEdit()
        self.passwordText.setEchoMode(QLineEdit.Password)
        self.password2Text = QLineEdit()
        self.password2Text.setEchoMode(QLineEdit.Password)
        visitorButton = QPushButton("Register Visitor")
        # visitorButton.clicked.connect(self.mbox("Success"))
        staffButton = QPushButton("Register Staff")
        # staffButton.clicked.connect(self.mbox("Success"))
        backbutton = QPushButton("Back")

        grid = QGridLayout()
        grid.addWidget(emaillabel,1,0)
        grid.addWidget(unlabel,2,0)
        grid.addWidget(pwlabel,3,0) #The grid coordinate position (Row, Col, Row Length, Col Length)
        grid.addWidget(pw2label,4,0)
        grid.addWidget(self.emailText,1,1)
        grid.addWidget(self.usernameText,2,1)
        grid.addWidget(self.passwordText,3,1)
        grid.addWidget(self.password2Text,4,1)
        grid.addWidget(visitorButton,5,0,1,2) #the extra 1 and 2 is button takes up 1 row and 2 columns width
        grid.addWidget(staffButton,6,0,1,2)
        grid.addWidget(backbutton,7,0,1,2)

        self.setLayout(grid)

        visitorButton.clicked.connect(lambda: self.register(self.emailText.text(),self.usernameText.text(),self.passwordText.text(),self.password2Text.text(),"visitor"))
        staffButton.clicked.connect(lambda: self.register(self.emailText.text(),self.usernameText.text(),self.passwordText.text(),self.password2Text.text(),"staff"))
        backbutton.clicked.connect(self.back)


    def register(self, email, username, password, password2, role):

        try:
            if len(password) < 8:
                self.mbox("Password must be 8 characters")
                return False
            elif password != password2:
                self.mbox("Passwords entered are not equal")
                return False
            elif not self.isValidEmail(email):
                self.mbox("Invalid Email")
                return False
            else:
                curs = connection.cursor()

                curs.execute("insert into user values (%s,md5(%s),%s,%s)",(username,password,email,role))
                if role == 'staff':
                    curs.execute("insert into staff values (%s)",(username))
                elif role == 'visitor':
                    curs.execute("insert into visitor values (%s)",(username))
                connection.commit()
                print(f"Successfully added {username}")
                self.main.show()
                self.close()
                self.mbox("Success")
        except:
            self.mbox("User already registered")


    def isValidEmail(self, email):
        if len(email) > 5:
            if re.match(r"[^@]+@[^@]+\.[^@]+", email) != None:
                return True
            return False

    def mbox(self, message):
        logger = QMessageBox.information(self,
                    "Registration",
                    message,
                    QMessageBox.Ok)


    def back(self):
        self.main.show() #shows previous window
        self.close()



#To make the staff and admin window, just copy this class and change / create the required buttons
class VisitorWindow(QWidget):
    def __init__(self,main, username): #main allows the window to know where it came from
        super(VisitorWindow,self).__init__()
        self.setWindowTitle("Visitor Window")
        self.main = main
        self.username = username

        #Rename the buttons
        title = QLabel("Atlanta Zoo")
        searchExhibit = QPushButton("Search Exhibit")
        searchShow = QPushButton("Search Show")
        searchAnimal = QPushButton("Search Animal")
        viewExHist = QPushButton("View Exhibit History ")
        viewShowHist = QPushButton("View Show History")
        logout = QPushButton("Logout")

        grid = QGridLayout()
        grid.addWidget(title,1,1,1,2) #The grid coordinate position (Row, Col, Row Length, Col Length)
        grid.addWidget(searchExhibit,2,0)
        grid.addWidget(searchShow,2,1)
        grid.addWidget(searchAnimal,2,2)
        grid.addWidget(viewExHist,4,0)
        grid.addWidget(viewShowHist,4,1)
        grid.addWidget(logout,6,0)

        self.setLayout(grid)

        searchExhibit.clicked.connect(lambda: self.searchFor('exhibit'))
        searchShow.clicked.connect(lambda: self.searchFor('show_'))
        searchAnimal.clicked.connect(lambda: self.searchFor('animal'))
        viewExHist.clicked.connect(lambda: self.history('exhibit', self.username))
        viewShowHist.clicked.connect(lambda: self.history('show', self.username))
        # staffButton.clicked.connect(lambda: self.register(self.emailText.text(),self.usernameText.text(),self.passwordText.text(),"staff"))
        logout.clicked.connect(self.back)

    def searchFor(self, searching):
        if searching == 'show_':
            self.searchFor = visitorShowWin(self, self.username)
        elif searching =='animal':
            self.searchFor = searchingsAnimal(self, self.username, 'visitor')
        else:
            self.searchFor = visitorExWin(self, self.username)
        self.searchFor.show()
        self.close()

    def history(self, history, username):
        if history == 'exhibit':
            self.hist = ExhibitHistory(self, self.username)
        elif history == 'show':
            self.hist = ShowHistory(self,self.username)
        self.hist.show()
        self.close()

    def back(self):
        self.login = LoginWindow()
        self.login.show()
        self.close()

class visitorExWin(QWidget):
    def __init__(self, main, username):
        super(visitorExWin,self).__init__()
        self.setWindowTitle("Exhibits")
        self.main = main
        self.username = username
        self.rowlist = []

        showname = QLabel("Name")
        numanimal = QLabel("Num Animals")
        sizelabel = QLabel("Size")
        waterlabel = QLabel("Water Feature")

        info = QLabel("Water Feature : 0 is No and 1 is Yes")

        self.nameinput = QLineEdit()
        self.nummin = QSpinBox()
        self.nummax = QSpinBox()
        self.sizemin = QSpinBox()
        self.sizemax = QSpinBox()

        self.sizemin.setRange(0,100000)
        self.sizemax.setRange(0,100000)


        self.waterInput = QComboBox()
        self.waterVal = ''
        self.waterInput.addItems(["--", "Yes", "No"])
        self.waterInput.currentIndexChanged.connect(self.boolchange)

        numgroup = QGroupBox("")
        layout = QFormLayout()
        layout.addRow(QLabel("Min:"), self.nummin)
        layout.addRow(QLabel("Max:"), self.nummax)
        numgroup.setLayout(layout)

        sizegroup = QGroupBox("")
        layout = QFormLayout()
        layout.addRow(QLabel("Min:"), self.sizemin)
        layout.addRow(QLabel("Max:"), self.sizemax)
        sizegroup.setLayout(layout)

        searchbutton = QPushButton("Search")
        backbutton = QPushButton("Back")
        grid = QGridLayout()

        checkcolumn = "select * from exhibit;"
        curs = connection.cursor()
        curs.execute(checkcolumn)
        length = 0
        for row in curs:
            length += 1

        self.table = QTableWidget(length, 4, self) #change 500 to length of rows
        self.table.setHorizontalHeaderLabels(['Name', 'Size', 'Num Animals', 'Water Feature'])
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.cellClicked.connect(self.viewClicked)

        x = 0
        grid.addWidget(showname, x, 0)
        grid.addWidget(self.nameinput, x+1 , 0)
        grid.addWidget(waterlabel, x, 1)
        grid.addWidget(self.waterInput, x+1, 1)


        grid.addWidget(numanimal, x+3 , 0)
        grid.addWidget(numgroup, x+4, 0)


        grid.addWidget(sizelabel, x+3, 1)
        grid.addWidget(sizegroup, x+4, 1)
        grid.addWidget(info, x+5, 0)
        grid.addWidget(searchbutton, x+5, 1)
        grid.addWidget(self.table, x+6, 0, 2, 2)
        grid.addWidget(backbutton, x+8, 0)
        self.setLayout(grid)




        self.loaddata(self.nameinput, self.nummin,self.nummax,self.sizemin,self.sizemax, self.waterVal, True)
        searchbutton.clicked.connect(lambda: self.loaddata(self.nameinput, self.nummin,self.nummax,self.sizemin,self.sizemax, self.waterVal, False))


        backbutton.clicked.connect(self.back)
    def boolchange(self,i):
        self.waterVal = self.waterInput.currentText()

    def loaddata(self, exhibitname, numMin, numMax, sizeMin, sizeMax, waterVal, initialload):
        self.table.setSortingEnabled(False)
        sqlquery = "select a.exhibitName, a.size, b.Num_Animals, a.waterFeature from exhibit as a right join (select exhibitName, count(*) as Num_Animals from animal group by exhibitName) as B on a.exhibitName = b.exhibitName where "
        exhibitname = exhibitname.text()
        water = waterVal
        numMin = numMin.text()
        numMax = numMax.text()
        sizeMin = sizeMin.text()
        sizeMax = sizeMax.text()


        if exhibitname != '' and exhibitname != None:
            sqlquery += "exhibitName like '" + exhibitname + "%' && "

        if initialload == False:
            if numMin != '' and numMin != None:
                sqlquery += "Num_Animals >= '" + numMin + "' && "
            if numMax != '' and numMax != None and numMax !='0':
                sqlquery += "Num_Animals <= '" + numMax + "' && "

            if sizeMin != '' and sizeMin != None:
                sqlquery += "size >= '" + sizeMin + "' && "
            if sizeMax != '' and sizeMax != None and sizeMax !='0' :
                sqlquery += "size <= '" + sizeMax + "' && "


            if water != '' and water != None and water != '--':
                if water == "Yes":
                    water = '1'
                elif water == "No":
                    water = '0'
                sqlquery += "waterFeature = '" + water + "' && "

        if sqlquery.endswith("&& "):
            sqlquery = sqlquery[:-3]
        if sqlquery.endswith("where "):
            sqlquery = sqlquery[:-6]

        sqlquery += ";"
        print(sqlquery)
        curs = connection.cursor()
        curs.execute(sqlquery)
        rows = []
        first_row = curs.fetchone()
        self.table.clearContents()
        if first_row is not None:
            column_headers = [str(k).strip() for k, v in first_row.items()]
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            for i, row in enumerate(rows):
                for j, field in enumerate(row):
                    item = QTableWidgetItem(field)
                    self.table.setItem(i, j, item)
        self.table.setSortingEnabled(True)

    def viewClicked(self, row, col):
        self.item = self.table.item(row ,col)
        self.colhead = self.table.horizontalHeaderItem(col)
        #put each cell to rowlist
        colsize = self.table.columnCount()
        i = 0
        rowlist = []
        while i < colsize:
            entry = []
            entry.append(self.table.horizontalHeaderItem(i).text())
            entry.append(self.table.item(row, i).text())
            rowlist.append(entry)
            i+=1

        self.rowlist = rowlist
        print("Went to exhibit detail")
        # go to exhibit detail
        exhibitname = rowlist[0][1]
        print(self.rowlist)
        self.exhibitdetail = ExhibitDetail(self, self.username, self.rowlist, exhibitname)
        self.exhibitdetail.show()
        self.close()

    def mbox(self,message):
        logger = QMessageBox.information(self,
                    "Log",
                    message,
                    QMessageBox.Ok)
    def exhibitchange(self,i):
        self.exhibitvalue = self.exhibitInput.currentText()
    def back(self):
        self.VisitorWindow = VisitorWindow(self, self.username)
        self.VisitorWindow.show()
        self.close()


class visitorShowWin(QWidget):
    def __init__(self, main, username):
        super(visitorShowWin,self).__init__()
        self.setWindowTitle("Shows")
        self.main = main
        self.username = username
        self.rowlist = []

        showname = QLabel("Name")
        exhibit = QLabel("Exhibit")
        datelabel = QLabel("Date")

        self.shownameInput = QLineEdit()
        self.exhibitInput = QComboBox()
        self.exhibitvalue = ''
        self.exhibitInput.addItems(["--","Birds","Jungle","Mountainous","Pacific","Sahara"])
        self.exhibitInput.currentIndexChanged.connect(self.exhibitchange)#change to dropdown
        self.dateInput = QDateEdit() #not working

        searchbutton = QPushButton("Search")
        logbutton = QPushButton("Log Visit")
        backbutton = QPushButton("Back")
        grid = QGridLayout()

        checkcolumn = "select * from show_;"
        curs = connection.cursor()
        curs.execute(checkcolumn)
        length = 0
        for row in curs:
            length += 1

        self.table = QTableWidget(length, 3, self) #change 500 to length of rows
        self.table.setHorizontalHeaderLabels(['Name', 'Exhibit', 'Date'])
        self.table.setSelectionBehavior(QTableView.SelectRows)

        x = 0
        grid.addWidget(showname, x, 0)
        grid.addWidget(exhibit, x+1 , 0)
        grid.addWidget(datelabel, x+2, 0)
        grid.addWidget(self.shownameInput, x, 1)
        grid.addWidget(self.exhibitInput, x+1, 1)
        grid.addWidget(self.dateInput, x+2, 1)
        grid.addWidget(searchbutton, x+3, 1)
        grid.addWidget(self.table, x+5, 0, 2, 2)
        grid.addWidget(logbutton, x+7, 1)
        grid.addWidget(backbutton, x+7, 0)
        self.setLayout(grid)

        self.loaddata(self.shownameInput, self.exhibitvalue,self.dateInput, True)
        searchbutton.clicked.connect(lambda: self.loaddata(self.shownameInput, self.exhibitvalue,self.dateInput, False))
        self.table.cellClicked.connect(self.viewClicked)
        logbutton.clicked.connect(lambda: self.LogVisit(self.rowlist))
        backbutton.clicked.connect(self.back)

    def loaddata(self, name, exhibit, date, initialload):
        self.table.setSortingEnabled(False)
        sqlquery = "select showName, exhibitName, dateAndTime from show_ where "
        name = name.text()
        date = date.text()
        #format date

        if name != '' and name != None:
            sqlquery += "showName like '" + name + "%' && "
        if exhibit != '' and exhibit != None and exhibit != '--':
            sqlquery += "exhibitName like '" + exhibit + "%' && "
        if initialload == False:
            if date != '' and date != None and date != '2000/01/01': #working on this
                datesplitted = date.split('/')
                datedashed = datesplitted[0] + '/' + datesplitted[1] + '/' + datesplitted[2]
                sqlquery += "dateAndTime like '" + datedashed + "%'"

        if sqlquery.endswith("&& "):
            sqlquery = sqlquery[:-3]
        if sqlquery.endswith("where "):
            sqlquery = sqlquery[:-6]

        sqlquery += ";"
        print(sqlquery)
        curs = connection.cursor()
        curs.execute(sqlquery)
        rows = []
        first_row = curs.fetchone()
        self.table.clearContents()
        if first_row is not None:
            column_headers = [str(k).strip() for k, v in first_row.items()]
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            for i, row in enumerate(rows):
                for j, field in enumerate(row):
                    item = QTableWidgetItem(field)
                    self.table.setItem(i, j, item)
        self.table.setSortingEnabled(True)

    def viewClicked(self, row, col):
        self.item = self.table.item(row ,col)
        self.colhead = self.table.horizontalHeaderItem(col)
        #put each cell to rowlist
        colsize = self.table.columnCount()
        rowlist = []
        i = 0
        while i < colsize:
            entry = []
            entry.append(self.table.horizontalHeaderItem(i).text())
            entry.append(self.table.item(row, i).text())
            rowlist.append(entry)
            i+=1

        if col == 1:
            self.rowlist = rowlist
            print("Went to exhibit detail")
            # go to exhibit detail
            exhibitname = rowlist[1][1]
            self.exhibitdetail = ExhibitDetail(self, self.username, self.rowlist, exhibitname)
            self.exhibitdetail.show()
            self.close()
        else:
            self.rowlist = rowlist

    def LogVisit(self, selectedrow):
        if len(selectedrow) > 0:
            uname = self.username
            dateAndTime = datetime.datetime.today().strftime('%m/%d/%y %')

            #To compare dates
            datetoday = datetime.datetime.today()
            showdate = datetime.datetime.strptime(selectedrow[2][1],'%m/%d/%y %')

            if datetoday >= showdate:
                print(selectedrow)
                showname = selectedrow[0][1]
                exhibitInput = selectedrow[1][1]

                print(f"insert into showvisitor values ({uname},{showname}, {dateAndTime}) ;")
                print(f"insert into exhibitvisitor values ({uname},{exhibitInput}, {dateAndTime}) ;")

                curs = connection.cursor()
                curs.execute("insert into showvisitor values (%s,%s,%s) ;", (uname, showname, dateAndTime))
                curs.execute("insert into exhibitvisitor values (%s,%s,%s) ;", (uname, exhibitInput, dateAndTime))
                connection.commit()
                print("Success adding History")
            else:
                self.mbox("Show has not started yet")
        else:
            self.mbox("No show selected")

    def mbox(self,message):
        logger = QMessageBox.information(self,
                    "Log",
                    message,
                    QMessageBox.Ok)
    def exhibitchange(self,i):
        self.exhibitvalue = self.exhibitInput.currentText()
    def back(self):
        self.VisitorWindow = VisitorWindow(self, self.username)
        self.VisitorWindow.show()
        self.close()

class ExhibitDetail(QWidget):
    def __init__(self, main, username, rowlist, exhibitname): #USERNAME
        super(ExhibitDetail, self).__init__()
        self.main = main
        self.setWindowTitle("Exhibit Detail")
        self.exhibitname = exhibitname
        self.username = username

        grid = QGridLayout()

        curs = connection.cursor()
        curs.execute(f"select a.exhibitName as 'Exhibit Name', a.waterFeature as 'Water Feature', a.size as 'Size', b.Num_Animals as 'Num Animals' from exhibit as a right join (select exhibitName, count(*) as Num_Animals from animal group by exhibitName) as B on a.exhibitName = b.exhibitName where a.exhibitName = '{self.exhibitname}'; ")


        numanimals = 0
        #For the labels
        x = 0
        for row in curs:
            print(row)
            for tupl in row.items():
                tupl = list(tupl)
                grid.addWidget(QLabel(tupl[0] +": "), x, 0)
                if tupl[0] == 'Water Feature':
                    if tupl[1] == 1:
                        tupl[1] = "Yes"
                    else:
                        tupl[1] = "No"
                if tupl[0] == 'Num Animals': #get the # of rows to make table
                    numanimals = tupl[1]
                if type(tupl[1]) is int:
                    tupl[1] = str(tupl[1])
                grid.addWidget(QLabel(tupl[1]), x, 1)
                x += 1

        logbutton = QPushButton("Log Visit")
        backbutton = QPushButton("Back")
        self.table = QTableWidget(numanimals, 2, self)
        self.table.setHorizontalHeaderLabels(['Name', 'Species'])

        #Populate Table
        curs.execute(f"select * from animal where exhibitName = '{self.exhibitname}';")
        rows = []
        first_row = curs.fetchone()
        rows.append([str(v).strip() for k, v in first_row.items()])
        for row in curs:
            rows.append([str(v).strip() for k, v in row.items()])

        for i, row in enumerate(rows):
            for j, field in enumerate(row):
                item = QTableWidgetItem(field)
                self.table.setItem(i, j, item)

        grid.addWidget(logbutton,x+1, 1)
        grid.addWidget(backbutton,x+1,0)
        grid.addWidget(self.table,x+2,0,2,2)
        self.setLayout(grid)

        logbutton.clicked.connect(self.LogVisit)
        backbutton.clicked.connect(self.back)


    def LogVisit(self):
        uname = self.username
        dateAndTime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        print(f"insert into exhibitvisitor values ({uname},{self.exhibitname}, {dateAndTime}) ;")
        curs = connection.cursor()
        curs.execute("insert into exhibitvisitor values (%s,%s,%s) ;", (uname, self.exhibitname, dateAndTime))
        connection.commit()
        print("Success adding Exhibit Visit")

    def back(self):
        self.main.show()
        self.close()

#here

class ShowHistory(QWidget):
    def __init__(self, main, username):
        super(ShowHistory, self).__init__()

        self.main = main
        self.setWindowTitle("Show History")
        self.username = username
        self.rowlist = []

        grid = QGridLayout()

        query = f"select a.username, a.showName,a.dateandtime, b.exhibitName from showvisitor as a left join  (select showName,exhibitName from show_) as b on a.showName = b.showName where username = '{self.username}';"
        curs = connection.cursor()
        curs.execute(query)

        #length check
        length = 0
        for row in curs:
            length += 1

        namelabel = QLabel("Name")
        datelabel = QLabel("Date")
        exhibitlabel = QLabel("Exhibit")

        self.nametext = QLineEdit()
        self.datetext = QDateEdit()
        self.exhibitInput = QComboBox()
        self.exhibitvalue = ''
        self.exhibitInput.addItems(["--","Birds","Jungle","Mountainous","Pacific","Sahara"])
        self.exhibitInput.currentIndexChanged.connect(self.exhibitchange)

        searchbutton = QPushButton("Search")
        backbutton = QPushButton("Back")

        self.table = QTableWidget(length, 3, self) #change 500 to length of rows
        self.table.setHorizontalHeaderLabels(['Name', 'Time', 'Exhibit'])
        self.table.setSelectionBehavior(QTableView.SelectRows)

        grid.addWidget(namelabel, 1, 0)
        grid.addWidget(datelabel, 2, 0)
        grid.addWidget(exhibitlabel, 2, 2)
        grid.addWidget(self.nametext, 1, 1)
        grid.addWidget(self.exhibitInput, 2,3)
        grid.addWidget(self.datetext, 2,1)
        grid.addWidget(searchbutton, 3,3)
        grid.addWidget(self.table,4,0,3,4)
        grid.addWidget(backbutton,7,0)

        self.setLayout(grid)

        self.loaddata(self.nametext, self.datetext, self.exhibitvalue, True)
        searchbutton.clicked.connect(lambda: self.loaddata(self.nametext, self.datetext, self.exhibitvalue, False))
        backbutton.clicked.connect(self.back)

    def exhibitchange(self,i):
        self.exhibitvalue = self.exhibitInput.currentText()

    def loaddata(self, name, date, exhibitName, initialload):
        self.table.setSortingEnabled(False)
        sqlquery = f"select a.showName,a.dateandtime, b.exhibitName from showvisitor as a left join  (select showName,exhibitName from show_) as b on a.showName = b.showName where a.username = '{self.username}' && "
        name = name.text()
        date = date.text()

        if name != '' and name != None:
            sqlquery += "a.showName like '" + name + "%' && "
        if not initialload:
            if date != '' and date != None and date != 'YYYY-MM-DD':
                sqlquery += "a.dateandtime like '" + date + "%' && "
        if exhibitName != '' and exhibitName != None and exhibitName != '--':
            sqlquery += "b.exhibitName =  '" + exhibitName + "' && "

        if sqlquery.endswith("&& "):
            sqlquery = sqlquery[:-3]
        if sqlquery.endswith("where "):
            sqlquery = sqlquery[:-6]

        sqlquery += ";"
        print(sqlquery)
        curs = connection.cursor()
        curs.execute(sqlquery)
        rows = []
        first_row = curs.fetchone()
        self.table.clearContents()
        if first_row is not None:
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            for i, row in enumerate(rows):
                for j, field in enumerate(row):
                    item = QTableWidgetItem(field)
                    self.table.setItem(i, j, item)
        self.table.setSortingEnabled(True)

    def mbox(self,title, message):
        logger = QMessageBox.information(self,
                    title,
                    message,
                    QMessageBox.Ok)

    def back(self):
        self.VisitorWindow = VisitorWindow(self, self.username)
        self.VisitorWindow.show()
        self.close()
class ExhibitHistory(QWidget):
    def __init__(self, main, username):
        super(ExhibitHistory, self).__init__()

        self.main = main
        self.setWindowTitle("Exhibit History")
        self.username = username
        self.rowlist = []

        grid = QGridLayout()

        query = f"select a.exhibitName as 'Exhibit Name', a.dateandtime as 'Date', b.num as 'Number of Visits' from exhibitvisitor as a right join (select exhibitName, count(*) as num from exhibitvisitor group by exhibitName) as b on a.exhibitName = b.exhibitName where a.username = '{self.username}';"
        curs = connection.cursor()
        curs.execute(query)

        #length check
        length = 0
        for row in curs:
            length += 1

        namelabel = QLabel("Name")
        datelabel = QLabel("Date")
        numlabel = QLabel("Number of Visits")

        self.nametext = QLineEdit()
        self.datetext = QDateEdit()
        self.lower = QSpinBox()
        self.upper = QSpinBox()

        form_group_box2 = QGroupBox("")
        layout = QFormLayout()
        layout.addRow(QLabel("Min:"), self.lower)
        layout.addRow(QLabel("Max:"), self.upper)
        form_group_box2.setLayout(layout)

        searchbutton = QPushButton("Search")
        backbutton = QPushButton("Back")

        self.table = QTableWidget(length, 3, self) #change 500 to length of rows
        self.table.setHorizontalHeaderLabels(['Name', 'Time', 'Number of Visits'])
        self.table.setSelectionBehavior(QTableView.SelectRows)

        grid.addWidget(namelabel, 0, 0)
        grid.addWidget(numlabel, 0, 2)
        grid.addWidget(datelabel, 1, 0)
        grid.addWidget(self.nametext, 0, 1)
        grid.addWidget(form_group_box2, 1, 2)
        grid.addWidget(self.datetext, 1,1)
        grid.addWidget(searchbutton, 2,1)
        grid.addWidget(self.table,3,0,3,4)
        grid.addWidget(backbutton,6,0)

        self.setLayout(grid)

        self.loaddata(self.nametext, self.datetext, self.lower, self.upper, True)
        searchbutton.clicked.connect(lambda: self.loaddata(self.nametext, self.datetext, self.lower, self.upper, False))
        self.table.cellClicked.connect(self.viewClicked)
        backbutton.clicked.connect(self.back)

    def loaddata(self, name, date, lower, upper, initialload):
        self.table.setSortingEnabled(False)
        sqlquery = f"select a.exhibitName, a.dateandtime, b.num from exhibitvisitor as a right join (select exhibitName, count(*) as num from exhibitvisitor group by exhibitName) as b on a.exhibitName = b.exhibitName where "
        name = name.text()
        date = date.text()
        lower = lower.text()
        upper = upper.text()

        if name != '' and name != None:
            sqlquery += "a.exhibitName = '" + name + "' && "
        if not initialload:
            if date != '' and date != None and date != 'YYYY-MM-DD':
                sqlquery += "a.dateandtime like '" + date + "%' && "
        if upper != '' and upper != None and upper != '0':
            sqlquery += "b.num <= '" + upper + "' && "
        if lower != '' and lower != None and lower != '0':
            sqlquery += "b.num >= '" + lower + "' && "

        if sqlquery.endswith("&& "):
            sqlquery = sqlquery[:-3]
        if sqlquery.endswith("where "):
            sqlquery = sqlquery[:-6]

        sqlquery += ";"
        print(sqlquery)
        curs = connection.cursor()
        curs.execute(sqlquery)
        rows = []
        first_row = curs.fetchone()
        self.table.clearContents()
        if first_row is not None:
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            for i, row in enumerate(rows):
                for j, field in enumerate(row):
                    item = QTableWidgetItem(field)
                    self.table.setItem(i, j, item)
        self.table.setSortingEnabled(True)

    def viewClicked(self, row, col):
        self.item = self.table.item(row ,col)
        self.colhead = self.table.horizontalHeaderItem(col)
        #put each cell to rowlist
        colsize = self.table.columnCount()
        rowlist = []
        i = 0
        while i < colsize:
            entry = []
            entry.append(self.table.horizontalHeaderItem(i).text())
            entry.append(self.table.item(row, i).text())
            rowlist.append(entry)
            i+=1

        self.rowlist = rowlist
        print("Went to exhibit detail")
        # go to exhibit detail
        print(self.rowlist)
        exhibitname = self.rowlist[0][1]
        self.exhibitdetail = ExhibitDetail(self, self.username, self.rowlist, exhibitname)
        self.exhibitdetail.show()
        self.close()


    def back(self):
        self.VisitorWindow = VisitorWindow(self, self.username)
        self.VisitorWindow.show()
        self.close()

'''
class searchForWindow(QWidget) is a usable class when need to make a "Search for 'something'"" window
Functions:
- Make_label
    - just makes labels
- back
    - goes to previous main window
- showsearch(answerdict,tableName)
    - Parameter: answerdict is a dictionary value that maps keys to the answers
    of the user input. {column name: user input answers, column name 2: user input 2, ... }
    - Parameter: tableName is the name of the table in the database.
    - called in the .connect button
    i.e, searchbutton.clicked.connect(lambda: self.showsearch(answerdict,tableName))
- show_information box
    - not used fo rnow
- selection change
    - for the .currentIndexChanged() dropdown list
'''
class searchForWindow(QWidget): #visitor search for show search for exhibit
    def __init__(self, tableName, username):
        super(searchForWindow, self).__init__()
        self.setWindowTitle(tableName)
        cursor = connection.cursor()
        cursor.execute(f"select * from {tableName}")
        grid = QGridLayout()
        self.username = username

        #Variables initialized
        n = 1
        answerlist = []
        keylist = []
        booleanoption = ["Yes", "No"]

        #To get the column names from each table and make a user input UI according to its type
        for key in cursor.fetchone():
            grid.addWidget(self.make_label(key),n,0)
            curs = connection.cursor()
            curs.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{tableName}' and column_name = '{key}';")
            queryresult = curs.fetchone()
            if queryresult is not None:
                if 'tinyint' in queryresult.values(): #If boolean type (This still doesnt work)
                    self.cb = QComboBox()
                    self.boolval = ''
                    self.cb.addItems(booleanoption)
                    grid.addWidget(self.cb,n,1)
                    self.cb.currentIndexChanged.connect(self.selectionchange)
                    answerlist.append(self.boolval)
                elif 'datetime' in queryresult.values(): #If datetime type (This still doesnt work)
                    self.cal= QCalendarWidget()
                    grid.addWidget(self.cal,n,1)
                    answerlist.append('')
                elif 'int' in queryresult.values(): #If int
                    self.onlyInt = QLineEdit()
                    self.onlyInt.setValidator(QIntValidator())
                    grid.addWidget(self.onlyInt,n,1)
                    answerlist.append(self.onlyInt)
                else: #if everything else (text)
                    self.textbox = QLineEdit()
                    grid.addWidget(self.textbox,n,1)
                    answerlist.append(self.textbox)
            keylist.append(key)
            n += 1

        #Buttons in the window
        searchbutton = QPushButton("Search")
        backbutton = QPushButton("Back")

        #Puts button in the grid layout where n is the amount of columns
        grid.addWidget(searchbutton,n,1)
        grid.addWidget(backbutton,n,0)
        self.setLayout(grid)

        #This is what happens when the buttons are clicked. The searchubutton is still work in progress to
        answerdict = dict(zip(keylist,answerlist))
        searchbutton.clicked.connect(lambda: self.showsearch(self, answerdict,tableName))
        backbutton.clicked.connect(self.back)

    def selectionchange(self,i):
        self.boolval = self.cb.currentText()


    def make_label(self,key):
        label = QLabel(key)
        return label

    def back(self):
        self.visitor = VisitorWindow(self, self.username)
        self.visitor.show() #shows previous window
        self.close()

    def showsearch(self, main, answerdict, tableName):
        self.main = main
        print(answerdict)
        sqlquery = "select * from " + tableName + " where "
        keys = list(answerdict.keys())
        for key in keys:
            if key == 'waterFeature':
                if answerdict[key].text() == "N":
                    answerdict[key] = '0';
                elif answerdict[key].text() == "Y":
                    answerdict[key] = '1';
            try:
                answerdict[key] = answerdict[key].text()
            except:
                pass
            if answerdict[key] != None and answerdict[key] != '':
                sqlquery += key + " = '" + answerdict[key] +"' && "
        if sqlquery.endswith("&& "):
            sqlquery = sqlquery[:-3]
            sqlquery += ";"
        print(sqlquery)
        try:
            curs = connection.cursor()
            curs.execute(sqlquery)
            rows = []
            first_row = curs.fetchone()
            column_headers = [str(k).strip() for k, v in first_row.items()]
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            dlg = TableDialog(self, column_headers, rows, tableName, self.username)
            self.close()
            dlg.exec()
        except:
            self.notfound()
            self.close()
            self.back = searchForWindow(tableName, self.username)
            self.back.show()

    def notfound(self):
        logger = QMessageBox.information(self,
                            "Login",
                            "Entry Not Found",
                            QMessageBox.Ok)

class TableDialog(QDialog): #This is to show the table popup
    def __init__(self, main, column_headers, rows, tableName, username):
        super(TableDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("")
        self.main =main

        table = QTableWidget(len(rows), len(rows[0]), self)
        table.setHorizontalHeaderLabels(column_headers)

        for i, row in enumerate(rows):
            for j, field in enumerate(row):
                item = QTableWidgetItem(field)
                table.setItem(i, j, item)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.clicked.connect(lambda: self.back(tableName))
        self.table.cellClicked.connect(self.viewClicked)

        vbox_layout = QVBoxLayout()
        table.setSortingEnabled(True)
        vbox_layout.addWidget(table)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)

    def back(self, tableName):
        self.close()
        self.back = searchForWindow(tableName, self.username)
        self.back.show()

class StaffWindow(QWidget):
    def __init__(self, main, username): #main allows the window to know where it came from
        super(StaffWindow,self).__init__()
        self.setWindowTitle("Staff Window")
        self.main = main
        self.username = username

        #Rename the buttons
        title = QLabel("Atlanta Zoo")
        searchAnimal = QPushButton("Search Animal")
        viewShow = QPushButton("View Show")
        logout = QPushButton("Logout")

        grid = QGridLayout()
        grid.addWidget(title,1,1,1,2) #The grid coordinate position (Row, Col, Row Length, Col Length)
        grid.addWidget(searchAnimal,2,0)
        grid.addWidget(viewShow,2,1)
        grid.addWidget(logout,2,2)

        self.setLayout(grid)

        searchAnimal.clicked.connect(lambda: self.searchFor(username))
        viewShow.clicked.connect(lambda: self.showstaff(username))
        logout.clicked.connect(self.back)

    def searchFor(self, username):
        self.searchFor = searchingsAnimal(self, username, 'staff')
        self.searchFor.show()
        self.close()

    def back(self):
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def showstaff(self, username):
        self.username = username
        query = f"select showName, dateAndTime, exhibitName from show_ where username = '{username}';"
        curs = connection.cursor()
        curs.execute(query)
        rows = []
        first_row = curs.fetchone()
        if first_row is not None:
            column_headers = [str(k).strip() for k, v in first_row.items()]
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            dlg = ShowTableDialog(self, column_headers, rows)
            dlg.exec()
        else:
            self.notfound()
    def notfound(self):
        logger = QMessageBox.information(self,
                            "Login",
                            "Shows Not Found",
                            QMessageBox.Ok)

class searchingsAnimal(QWidget):
    def __init__(self, main, username, role):
        super(searchingsAnimal,self).__init__()
        self.setWindowTitle("Atlanta Zoo - Animals")
        self.main = main
        self.username = username
        self.rowlist = []
        self.role = role

        animalName = QLabel("Name")
        animalSpecies = QLabel("Species")
        age = QLabel("Age")
        type_ = QLabel("Type")
        exhibitName = QLabel("Exhibit")

        self.animalNameInput = QLineEdit()
        self.animalSpeciesInput = QLineEdit()
        self.ageminInput = QSpinBox()
        self.agemaxInput = QSpinBox()

        self.typeInput = QComboBox()
        self.typevalue = ''
        self.typeInput.addItems(["--","Bird","Mammal","Amphibian","Reptile","Fish", "Invertebrate"])
        self.typeInput.currentIndexChanged.connect(self.typechange)

        self.exhibitInput = QComboBox()
        self.exhibitvalue = ''
        self.exhibitInput.addItems(["--","Birds","Jungle","Mountainous","Pacific","Sahara"])
        self.exhibitInput.currentIndexChanged.connect(self.exhibitchange)

        form_group_box2 = QGroupBox("")
        layout = QFormLayout()
        layout.addRow(QLabel("Min:"), self.ageminInput)
        layout.addRow(QLabel("Max:"), self.agemaxInput)
        form_group_box2.setLayout(layout)

        searchbutton = QPushButton("Search")
        backbutton = QPushButton("Back")
        grid = QGridLayout()

        self.table = QTableWidget(500, 5, self)
        self.table.setHorizontalHeaderLabels(['Name', 'Species', 'Age', 'Type', 'Exhibit'])
        self.table.setSelectionBehavior(QTableView.SelectRows)

        x = 0
        y = 0
        grid.addWidget(animalName, x, 0)
        grid.addWidget(animalSpecies, x+1, 0)
        grid.addWidget(age, x+2, y)
        grid.addWidget(type_, x+4, 0)
        grid.addWidget(exhibitName, x+5, 0)
        grid.addWidget(self.animalNameInput, x, 1)
        grid.addWidget(self.animalSpeciesInput, x+1, 1)
        grid.addWidget(form_group_box2, x+2, 1)
        grid.addWidget(self.typeInput, x+4, 1)
        grid.addWidget(self.exhibitInput, x+5, 1)
        grid.addWidget(searchbutton, x+6, 1)
        grid.addWidget(self.table, x+8, 0, 2, 3)
        grid.addWidget(backbutton, x+10, 0)
        self.setLayout(grid)



        self.loaddata(self.animalNameInput, self.animalSpeciesInput, self.ageminInput, self.agemaxInput, self.typevalue, self.exhibitvalue)
        searchbutton.clicked.connect(lambda: self.loaddata(self.animalNameInput, self.animalSpeciesInput, self.ageminInput, self.agemaxInput, self.typevalue, self.exhibitvalue))
        self.table.cellClicked.connect(self.viewClicked)
        backbutton.clicked.connect(self.back)

    def loaddata(self, animalName, animalSpecies, agemin, agemax, type_, exhibitName):
        self.table.setSortingEnabled(False)
        sqlquery = "select animalName, animalSpecies, age, type_, exhibitName from animal where "
        animalName = animalName.text()
        animalSpecies = animalSpecies.text()
        agemin = agemin.text()
        agemax = agemax.text()
        #exhibitName = exhibitName.text()
        if animalName != '' and animalName != None:
            sqlquery += "animalName like '" + animalName + "%' && "
        if animalSpecies != '' and animalSpecies != None:
            sqlquery += "animalSpecies like '" + animalSpecies + "%' && "
        if agemin != '' and agemin != None:
            sqlquery += "age >= '" + agemin + "' && age <= '" + agemax + "' && "
        if type_ != '' and type_ != None and type_ != '--':
            sqlquery += "type_ like '" + type_ + "%' && "
        if exhibitName != '' and exhibitName != None and exhibitName != '--':
            sqlquery += "exhibitName like '" + exhibitName + "%' "

        if sqlquery.endswith("&& "):
            sqlquery = sqlquery[:-3]
        if sqlquery.endswith("where "):
            sqlquery = sqlquery[:-6]
        if sqlquery.endswith("&& age = '0' "):
            sqlquery = sqlquery[:-13]
        if sqlquery.endswith("where age = '0' "):
            sqlquery = sqlquery[:-16]

        sqlquery += ";"
        print(sqlquery)
        curs = connection.cursor()
        curs.execute(sqlquery)
        rows = []
        first_row = curs.fetchone()
        self.table.clearContents()
        if first_row is not None:
            column_headers = [str(k).strip() for k, v in first_row.items()]
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            for i, row in enumerate(rows):
                for j, field in enumerate(row):
                    item = QTableWidgetItem(field)
                    self.table.setItem(i, j, item)
        else:
            print("No data found")
        self.table.setSortingEnabled(True)

    def viewClicked(self, row, col):
        self.item = self.table.item(row ,col)
        self.colhead = self.table.horizontalHeaderItem(col)
        if self.item is not None:
            colsize = self.table.columnCount()
            rowlist = []
            i = 0
            while i < colsize:
                entry = []
                entry.append(self.table.horizontalHeaderItem(i).text())
                entry.append(self.table.item(row, i).text())
                rowlist.append(entry)
                i+=1
            print(rowlist)
            if self.role == 'staff':
                self.AnimalCare = AnimalCare(self, rowlist, self.username)
                self.AnimalCare.show()
                self.close()
            elif self.role == 'visitor':
                print(rowlist)
                self.exhibitdetail = AnimalDetail(self, self.username, rowlist)
                self.exhibitdetail.show()
                self.close()

    def exhibitchange(self,i):
        self.exhibitvalue = self.exhibitInput.currentText()

    def typechange(self,i):
        self.typevalue = self.typeInput.currentText()

    def back(self, username):
        if self.role == 'staff':
            self.StaffWindow = StaffWindow(self, self.username)
            self.StaffWindow.show()
            self.close()
        elif self.role == 'visitor':
            self.VisitorWindow = VisitorWindow(self, self.username)
            self.VisitorWindow.show()
            self.close()


class ShowTableDialog(QDialog): #This is to show the table popup
    def __init__(self, main, column_headers, rows):
        super(ShowTableDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("")
        self.main =main

        table = QTableWidget(len(rows), len(rows[0]), self)
        table.setHorizontalHeaderLabels(column_headers)

        for i, row in enumerate(rows):
            for j, field in enumerate(row):
                item = QTableWidgetItem(field)
                table.setItem(i, j, item)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        vbox_layout = QVBoxLayout()
        table.setSortingEnabled(True)
        vbox_layout.addWidget(table)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)


class AnimalCare(QWidget):
    def __init__(self, main, datalist, username):
        super(AnimalCare,self).__init__()
        self.setWindowTitle("Animal Care")
        self.main = main
        self.username = username

        title = QLabel("Animal Care")
        logbutton = QPushButton("Log Notes")
        backbutton = QPushButton("Back")
        textbox = QPlainTextEdit()
        grid = QGridLayout()
        x = 0
        for entry in datalist:
            y = 0
            grid.addWidget(QLabel(entry[0]+": "),x,y)
            grid.addWidget(QLabel(entry[1]),x,y+1)
            x+=1

        self.tablelength = len(datalist)
        self.table = QTableWidget(500, 3, self) #change 500 to length of rows
        self.table.setHorizontalHeaderLabels(['Staff Member', 'Note', 'Time'])
        grid.addWidget(logbutton,x,1)
        grid.addWidget(backbutton,x,0)
        grid.addWidget(textbox ,x+1,0,2,2)
        grid.addWidget(self.table,x+3,0,2,2)
        try:
            self.loaddata(datalist)
        except:
            pass
        self.setLayout(grid)


        logbutton.clicked.connect(lambda: self.LogVisit(datalist, textbox))
        backbutton.clicked.connect(lambda: self.back(username))

    #by seperating the loaddata function, you can update the table when the button is clicked
    def loaddata(self, datalist):
        self.table.setSortingEnabled(False)
        aname = datalist[0][1]
        aspecies = datalist[1][1]

        sqlquery = "select username,notetext,dateandtime from AnimalCare where animalName = '" + aname + "'&& animalSpecies = '" + aspecies + "';"
        print(sqlquery)
        curs = connection.cursor()
        curs.execute(sqlquery)
        rows = []
        first_row = curs.fetchone()
        column_headers = [str(k).strip() for k, v in first_row.items()]
        rows.append([str(v).strip() for k, v in first_row.items()])
        for row in curs:
            rows.append([str(v).strip() for k, v in row.items()])

        for i, row in enumerate(rows):
            for j, field in enumerate(row):
                item = QTableWidgetItem(field)
                self.table.setItem(i, j, item)
        self.table.setSortingEnabled(True)
    def back(self, username):
        self.searchFor = searchingsAnimal(self, username, 'staff')
        self.searchFor.show()
        self.close()

    # YOU CAN USE VARIABLES OUTSIDE OF FUNCTION BY USING SELF.VARIABLE
    def LogVisit(self, datalist, textbox):
        aname = datalist[0][1]
        aspecies = datalist[1][1]
        staffuser = self.username
        dateAndTime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') #change to currentdatetime
        notetext = textbox.toPlainText()

        curs = connection.cursor()
        curs.execute("insert into AnimalCare values (%s,%s,%s,%s,%s)", (aname,aspecies,staffuser,dateAndTime,notetext))
        connection.commit()
        self.loaddata(datalist)
        print("Success adding Notes")


class AnimalDetail(QWidget):
    def __init__(self, main, username, datalist):
        super(AnimalDetail,self).__init__()
        self.setWindowTitle("Animal Detail")
        self.main = main
        self.username = username
        self.datalist = datalist

        print(self.datalist)
        title = QLabel("Animal Detail")
        logbutton = QPushButton("Log Notes")
        backbutton = QPushButton("Back")
        textbox = QPlainTextEdit()
        grid = QGridLayout()
        x = 0
        for entry in self.datalist:
            y = 0
            grid.addWidget(QLabel(entry[0]+": "),x,y)
            grid.addWidget(QLabel(entry[1]),x,y+1)
            x+=1

        # self.tablelength = len(datalist)
        # self.table = QTableWidget(500, 3, self) #change 500 to length of rows
        # self.table.setHorizontalHeaderLabels(['Staff Member', 'Note', 'Time'])
        # grid.addWidget(logbutton,x,1)
        # grid.addWidget(backbutton,x,0)
        #grid.addWidget(textbox ,x+1,0,2,2)
        #grid.addWidget(self.table,x+3,0,2,2)
        #try:
        #     self.loaddata(datalist)
        # except:
        #     pass
        self.setLayout(grid)


        # logbutton.clicked.connect(lambda: self.LogVisit(datalist, textbox))
        # backbutton.clicked.connect(lambda: self.back(username))

    #by seperating the loaddata function, you can update the table when the button is clicked
    # def loaddata(self, aname, aspecies):
    #     self.table.setSortingEnabled(False)
    #     sqlquery = "select username,notetext,dateandtime from AnimalCare where animalName = '" + aname + "'&& animalSpecies = '" + aspecies + "';"
    #     print(sqlquery)
    #     curs = connection.cursor()
    #     curs.execute(sqlquery)
    #     rows = []
    #     first_row = curs.fetchone()
    #     column_headers = [str(k).strip() for k, v in first_row.items()]
    #     rows.append([str(v).strip() for k, v in first_row.items()])
    #     for row in curs:
    #         rows.append([str(v).strip() for k, v in row.items()])

    #     for i, row in enumerate(rows):
    #         for j, field in enumerate(row):
    #             item = QTableWidgetItem(field)
    #             self.table.setItem(i, j, item)
    #     self.table.setSortingEnabled(True)
    def back(self, username):
        self.searchFor = searchingsAnimal(self, username, 'staff')
        self.searchFor.show()
        self.close()

    # # YOU CAN USE VARIABLES OUTSIDE OF FUNCTION BY USING SELF.VARIABLE
    # def LogVisit(self, datalist, textbox):
    #     aname = datalist[0][1]
    #     aspecies = datalist[1][1]
    #     staffuser = self.username
    #     dateAndTime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') #change to currentdatetime
    #     notetext = textbox.toPlainText()

    #     curs = connection.cursor()
    #     curs.execute("insert into AnimalCare values (%s,%s,%s,%s,%s)", (aname,aspecies,staffuser,dateAndTime,notetext))
    #     connection.commit()
    #     self.loaddata(datalist)
    #     print("Success adding Notes")

class AdminWindow(QWidget):
    def __init__(self,main):
        super(AdminWindow,self).__init__()
        self.setWindowTitle("Admin Window")
        self.main = main

        title = QLabel("Atlanta Zoo")
        viewVisitor = QPushButton("View Visitor")
        viewStaff = QPushButton("View Staff")
        searchShow = QPushButton("Search Show")
        searchAnimal = QPushButton("Search Animal")
        addAnimal = QPushButton("Add Animal")
        addShow = QPushButton("Add Show")
        logout = QPushButton("Logout")

        grid = QGridLayout()
        grid.addWidget(title,1,1,1,2)
        grid.addWidget(viewVisitor,2,0)
        grid.addWidget(viewStaff,2,1)
        grid.addWidget(searchShow,2,2)
        grid.addWidget(searchAnimal,4,0)
        grid.addWidget(addAnimal,4,1)
        grid.addWidget(addShow,4,2)
        grid.addWidget(logout,6,0)

        self.setLayout(grid)

        viewVisitor.clicked.connect(lambda: self.viewing('visitor'))
        viewStaff.clicked.connect(lambda: self.viewing('staff'))
        searchShow.clicked.connect(lambda: self.searchfor('show'))
        searchAnimal.clicked.connect(lambda: self.searchfor('animal'))
        addAnimal.clicked.connect(lambda: self.adding('animal'))
        addShow.clicked.connect(lambda: self.adding('show'))
        logout.clicked.connect(self.back)

    def viewing(self,role):
        self.view = ViewUsers(self, role)
        self.view.show()
        self.close()

    def searchfor(self, typee):
        if typee == 'show':
            self.searching = searchingShow(self,typee, 'admin')
        elif typee == 'animal':
            self.searching = searchingAnimal(self,typee)
        self.searching.show()
        self.close()

    def adding(self,typee):
        if typee == 'animal':
            self.adds = AddAnimal(self, typee)
        elif typee == 'show':
            self.adds = AddShow(self,typee)
        self.adds.show()
        self.close()

    def back(self):
        self.login = LoginWindow()
        self.login.show()
        self.close()

class ViewUsers(QWidget):
    def __init__(self, main, role):
        super(ViewUsers,self).__init__()
        self.setWindowTitle(f"View {role}")
        self.main = main
        self.selectedrow = []
        self.role = role

        grid = QGridLayout()
        title = QLabel(f"View {role}")
        delbutton = QPushButton(f"Delete {role}")
        backbutton = QPushButton("Back")

        self.table = QTableWidget(10, 2, self) #change 500 to length of rows
        self.table.setHorizontalHeaderLabels(['Username', "Email"])
        grid.addWidget(backbutton,0, 0)
        grid.addWidget(self.table,1, 0, 2, 2)
        grid.addWidget(delbutton, 3, 0 ,2, 1)


        self.loaddata(role)
        self.setLayout(grid)

        self.table.cellClicked.connect(self.viewClicked)
        delbutton.clicked.connect(lambda: self.delUser(self.selectedrow))
        backbutton.clicked.connect(self.back)

    def loaddata(self, role):
        self.table.setSortingEnabled(False)
        sqlquery = "select username, email from user where role = '" + role + "'"
        curs = connection.cursor()
        curs.execute(sqlquery)

        rows = []
        first_row = curs.fetchone()
        self.table.clearContents()
        if first_row is not None:

            column_headers = [str(k).strip() for k, v in first_row.items()]
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            for i, row in enumerate(rows):
                for j, field in enumerate(row):
                    item = QTableWidgetItem(field)
                    self.table.setItem(i, j, item)
        else:
            print("Empty Table")
        self.table.setSortingEnabled(True)

    def delUser(self, selectedrow):
        if len(selectedrow) > 0:
            print(selectedrow)
            uname = selectedrow[0][1]
            email = selectedrow[1][1]

            query = f"delete from user where username = '{uname}' && email = '{email}';"
            curs = connection.cursor()
            curs.execute(query)
            connection.commit()
            self.loaddata(self.role)
            print(f"Deleted User {uname}")
            self.selectedrow = [] #reset datalist
        else:
            self.mbox()

    def viewClicked(self, row, col):
        self.item = self.table.item(row ,col)
        self.colhead = self.table.horizontalHeaderItem(col)

        if self.item is not None:
            #put each cell to selectedrow
            colsize = self.table.columnCount()
            selectedrow = []
            i = 0
            while i < colsize:
                entry = []
                entry.append(self.table.horizontalHeaderItem(i).text())
                entry.append(self.table.item(row, i).text())
                selectedrow.append(entry)
                i+=1
            self.selectedrow = selectedrow
        # else:
            # print("Clicking on Empty Cell")

    def mbox(self):
        logger = QMessageBox.information(self,
                    "Remove",
                    "No User selected",
                    QMessageBox.Ok)

    def back(self):
        self.AdminWindow = AdminWindow(self)
        self.AdminWindow.show()
        self.close()

class searchingShow(QWidget):
    def __init__(self, main, username, role):
        super(searchingShow,self).__init__()
        self.setWindowTitle("Atlanta Zoo - Shows")
        self.main = main
        self.username = username
        self.rowlist = []

        showname = QLabel("Name")
        exhibit = QLabel("Exhibit")
        datelabel = QLabel("Date")

        self.shownameInput = QLineEdit()
        self.dateInput = QDateEdit()
        self.exhibitInput = QComboBox()
        self.exhibitvalue = ''
        self.exhibitInput.addItems(["--","Birds","Jungle","Mountainous","Pacific","Sahara"])
        self.exhibitInput.currentIndexChanged.connect(self.exhibitchange)

        searchbutton = QPushButton("Search")
        removebutton = QPushButton("Remove Show")
        backbutton = QPushButton("Back")
        logbutton = QPushButton("Log Visit")
        grid = QGridLayout()

        self.table = QTableWidget(500, 3, self)
        self.table.setHorizontalHeaderLabels(['Name', 'Exhibit', 'Date'])
        self.table.setSelectionBehavior(QTableView.SelectRows)

        x = 0
        grid.addWidget(showname, x, 0)
        grid.addWidget(exhibit, x+1 , 0)
        grid.addWidget(datelabel, x+2, 0)
        grid.addWidget(self.shownameInput, x, 1)
        grid.addWidget(self.exhibitInput, x+1, 1)
        grid.addWidget(self.dateInput, x+2, 1)
        grid.addWidget(searchbutton, x+3, 1)
        grid.addWidget(self.table, x+5, 0, 2, 2)
        if role == 'admin':
            grid.addWidget(removebutton, x+7, 1)
        elif role == 'visitor':
            grid.addWidget(logbutton, x+7, 1)
        grid.addWidget(backbutton, x+7, 0)
        self.setLayout(grid)

        self.loaddata(self.shownameInput, self.exhibitvalue,self.dateInput, True)
        searchbutton.clicked.connect(lambda: self.loaddata(self.shownameInput, self.exhibitvalue,self.dateInput, False))
        self.table.cellClicked.connect(self.viewClicked)
        removebutton.clicked.connect(lambda: self.delShow(self.rowlist))
        logbutton.clicked.connect(lambda: self.LogVisit(self.rowlist))
        backbutton.clicked.connect(self.back)

    def exhibitchange(self,i):
        self.exhibitvalue = self.exhibitInput.currentText()

    def loaddata(self, name, exhibit, date, initialload):
        self.table.setSortingEnabled(False)
        sqlquery = "select showName, exhibitName, dateAndTime from show_ where "
        name = name.text()
        date = date.text()
        if name != '' and name != None:
            sqlquery += "showName like '" + name + "%' && "
        if exhibit != '' and exhibit != None != '--' :
            sqlquery += "exhibitName like '" + exhibit + "%' && "
        if not initialload:
            if date != '' and date != None and date != 'YYYY-MM-DD':
                sqlquery += "dateAndTime like '" + date + "%'"

        if sqlquery.endswith("&& "):
            sqlquery = sqlquery[:-3]
        if sqlquery.endswith("where "):
            sqlquery = sqlquery[:-6]

        sqlquery += ";"
        curs = connection.cursor()
        curs.execute(sqlquery)
        rows = []
        first_row = curs.fetchone()
        self.table.clearContents()
        if first_row is not None:
            column_headers = [str(k).strip() for k, v in first_row.items()]
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            for i, row in enumerate(rows):
                for j, field in enumerate(row):
                    item = QTableWidgetItem(field)
                    self.table.setItem(i, j, item)
        else:
            print("Empty Table")
        self.table.setSortingEnabled(True)

    def viewClicked(self, row, col):
        self.item = self.table.item(row ,col)
        self.colhead = self.table.horizontalHeaderItem(col)
        if self.item is not None:
            #put each cell to rowlist
            colsize = self.table.columnCount()

            i = 0
            while i < colsize:
                entry = []
                entry.append(self.table.horizontalHeaderItem(i).text())
                entry.append(self.table.item(row, i).text())
                self.rowlist.append(entry)
                i+=1

    def delShow(self, selectedrow):
        if len(selectedrow) > 0:
            showName = selectedrow[0][1]
            dateTime = selectedrow[2][1]

            query = f"delete from show_ where showName = '{showName}' && dateAndTime = '{dateTime}';"
            curs = connection.cursor()
            curs.execute(query)
            connection.commit()
            print(f"Deleted show {showName}")
            self.loaddata(self.shownameInput, self.exhibitvalue, self.dateInput, True)

            self.rowlist = []
        else:
            self.mbox()

    def mbox(self):
        logger = QMessageBox.information(self,
                    "Remove",
                    "Fail to remove",
                    QMessageBox.Ok)

    def back(self):
        self.AdminWindow = AdminWindow(self)
        self.AdminWindow.show()
        self.close()

class searchingAnimal(QWidget):
    def __init__(self, main, username):
        super(searchingAnimal,self).__init__()
        self.setWindowTitle("Atlanta Zoo - Animals")
        self.main = main
        self.username = username
        self.rowlist = []

        animalName = QLabel("Name")
        animalSpecies = QLabel("Species")
        age = QLabel("Age")
        type_ = QLabel("Type")
        exhibitName = QLabel("Exhibit")

        self.animalNameInput = QLineEdit()
        self.animalSpeciesInput = QLineEdit()
        self.ageminInput = QSpinBox()
        self.agemaxInput = QSpinBox()

        self.typeInput = QComboBox()
        self.typevalue = ''
        self.typeInput.addItems(["--","Bird","Mammal","Amphibian","Reptile","Fish", "Invertebrate"])
        self.typeInput.currentIndexChanged.connect(self.typechange)

        self.exhibitInput = QComboBox()
        self.exhibitvalue = ''
        self.exhibitInput.addItems(["--","Birds","Jungle","Mountainous","Pacific","Sahara"])
        self.exhibitInput.currentIndexChanged.connect(self.exhibitchange)

        form_group_box2 = QGroupBox("")
        layout = QFormLayout()
        layout.addRow(QLabel("Min:"), self.ageminInput)
        layout.addRow(QLabel("Max:"), self.agemaxInput)
        form_group_box2.setLayout(layout)

        searchbutton = QPushButton("Search")
        removebutton = QPushButton("Remove Animal")
        backbutton = QPushButton("Back")
        grid = QGridLayout()

        self.table = QTableWidget(500, 5, self)
        self.table.setHorizontalHeaderLabels(['Name', 'Species', 'Age', 'Type', 'Exhibit'])
        self.table.setSelectionBehavior(QTableView.SelectRows)

        x = 0
        y = 0
        grid.addWidget(animalName, x, 0)
        grid.addWidget(animalSpecies, x+1, 0)
        grid.addWidget(age, x+2, y)
        grid.addWidget(type_, x+4, 0)
        grid.addWidget(exhibitName, x+5, 0)
        grid.addWidget(self.animalNameInput, x, 1)
        grid.addWidget(self.animalSpeciesInput, x+1, 1)
        grid.addWidget(form_group_box2, x+2, 1)
        grid.addWidget(self.typeInput, x+4, 1)
        grid.addWidget(self.exhibitInput, x+5, 1)
        grid.addWidget(searchbutton, x+6, 1)
        grid.addWidget(self.table, x+8, 0, 2, 3)
        grid.addWidget(removebutton, x+10, 1)
        grid.addWidget(backbutton, x+10, 0)
        self.setLayout(grid)



        self.loaddata(self.animalNameInput, self.animalSpeciesInput, self.ageminInput, self.agemaxInput, self.typevalue, self.exhibitvalue)
        searchbutton.clicked.connect(lambda: self.loaddata(self.animalNameInput, self.animalSpeciesInput, self.ageminInput, self.agemaxInput, self.typevalue, self.exhibitvalue))
        self.table.cellClicked.connect(self.viewClicked)
        removebutton.clicked.connect(lambda: self.delAnimal(self.rowlist))
        backbutton.clicked.connect(self.back)

    def loaddata(self, animalName, animalSpecies, agemin, agemax, type_, exhibitName):
        self.table.setSortingEnabled(False)
        sqlquery = "select animalName, animalSpecies, age, type_, exhibitName from animal where "
        animalName = animalName.text()
        animalSpecies = animalSpecies.text()
        agemin = agemin.text()
        agemax = agemax.text()
        #exhibitName = exhibitName.text()
        if animalName != '' and animalName != None:
            sqlquery += "animalName like '" + animalName + "%' && "
        if animalSpecies != '' and animalSpecies != None:
            sqlquery += "animalSpecies like '" + animalSpecies + "%' && "
        if agemin != '' and agemin != None:
            sqlquery += "age >= '" + agemin + "' && age <= '" + agemax + "' && "
        if type_ != '' and type_ != None and type_ != '--':
            sqlquery += "type_ like '" + type_ + "%' && "
        if exhibitName != '' and exhibitName != None and exhibitName != '--':
            sqlquery += "exhibitName like '" + exhibitName + "%' "

        if sqlquery.endswith("&& "):
            sqlquery = sqlquery[:-3]
        if sqlquery.endswith("where "):
            sqlquery = sqlquery[:-6]
        if sqlquery.endswith("&& age = '0' "):
            sqlquery = sqlquery[:-13]
        if sqlquery.endswith("where age = '0' "):
            sqlquery = sqlquery[:-16]

        sqlquery += ";"
        print(sqlquery)
        curs = connection.cursor()
        curs.execute(sqlquery)
        rows = []
        first_row = curs.fetchone()
        self.table.clearContents()
        if first_row is not None:
            column_headers = [str(k).strip() for k, v in first_row.items()]
            rows.append([str(v).strip() for k, v in first_row.items()])
            for row in curs:
                rows.append([str(v).strip() for k, v in row.items()])

            for i, row in enumerate(rows):
                for j, field in enumerate(row):
                    item = QTableWidgetItem(field)
                    self.table.setItem(i, j, item)
        else:
            print("No data found")
        self.table.setSortingEnabled(True)

    def viewClicked(self, row, col):
        self.item = self.table.item(row ,col)
        self.colhead = self.table.horizontalHeaderItem(col)

        if self.item is not None:
            #put each cell to rowlist
            colsize = self.table.columnCount()
            rowlist = []
            i = 0
            while i < colsize:
                entry = []
                entry.append(self.table.horizontalHeaderItem(i).text())
                entry.append(self.table.item(row, i).text())
                rowlist.append(entry)
                i+=1
        # else:
        #     print("Clicking on Empty Cell")

        # if col == 1:
        #     self.rowlist = rowlist
        #     print("Went to exhibit detail")
        #     # go to exhibit detail
        # else:
        #     self.rowlist = rowlist

    def exhibitchange(self,i):
        self.exhibitvalue = self.exhibitInput.currentText()

    def typechange(self,i):
        self.typevalue = self.typeInput.currentText()

    def delAnimal(self, selectedrow):
        if len(selectedrow) > 0:
            print(selectedrow)
            animalName = selectedrow[0][1]
            animalSpecies = selectedrow[1][1]
            age = selectedrow [2][1]

            query = f"delete from animal where animalName = '{animalName}' && animalSpecies = '{animalSpecies}' && age = '{age}';"
            curs = connection.cursor()
            curs.execute(query)
            connection.commit()
            self.loaddata(self.animalNameInput, self.animalSpeciesInput, self.ageInput, self.typeInput, self.exhibitInput)
            print(f"Deleted animal {animalName}")
            self.selectedrow = []
        else:
            self.mbox()

    def mbox(self):
        logger = QMessageBox.information(self,
                    "Remove",
                    "Fail to remove",
                    QMessageBox.Ok)

    def back(self):
        self.AdminWindow = AdminWindow(self)
        self.AdminWindow.show()
        self.close()

class AddAnimal(QWidget):
    def __init__(self, main, typee):
        super(AddAnimal, self).__init__()
        self.main = main
        self.setWindowTitle("Add Animal")

        firstlabel = QLabel("Name")
        secondlabel = QLabel("Species")
        thirdlabel = QLabel("Type")
        fourthlabel = QLabel("Age")
        fifthlabel = QLabel("Exhibit")

        self.firstText = QLineEdit()
        self.secondText = QLineEdit()
        self.fourthText = QSpinBox()


        self.typeInput = QComboBox()
        self.typevalue = ''
        self.typeInput.addItems(["--","Bird","Mammal","Amphibian","Reptile","Fish", "Invertebrate"])
        self.typeInput.currentIndexChanged.connect(self.typechange)

        self.exhibitInput = QComboBox()
        self.exhibitvalue = ''
        self.exhibitInput.addItems(["--","Birds","Jungle","Mountainous","Pacific","Sahara"])
        self.exhibitInput.currentIndexChanged.connect(self.exhibitchange)

        addAnimalButton = QPushButton("Add Animal")
        backbutton = QPushButton("Back")

        grid = QGridLayout()
        grid.addWidget(firstlabel,1,0)
        grid.addWidget(secondlabel,2,0)
        grid.addWidget(thirdlabel,3,0)
        grid.addWidget(fourthlabel,4,0)
        grid.addWidget(fifthlabel,5,0)
        grid.addWidget(self.firstText,1,1)
        grid.addWidget(self.secondText,2,1)
        grid.addWidget(self.typeInput,3,1)
        grid.addWidget(self.fourthText,4,1)
        grid.addWidget(self.exhibitInput,5,1)
        grid.addWidget(addAnimalButton,6,1)
        grid.addWidget(backbutton,6,0)

        self.setLayout(grid)

        addAnimalButton.clicked.connect(lambda: self.addValue(self.firstText.text(), self.secondText.text(), self.typevalue, self.fourthText.value(), self.exhibitvalue))
        backbutton.clicked.connect(self.back)

    def addValue(self, name, species, type_, age, exhibit):
        if name != '' and name != None:
            if species != '' and species != None:
                if type_ != '' and type_ != None and type_ != '--':
                    if age !='' and age != None:
                        if exhibit != '' and exhibit != None and exhibit != '--':
                            sqlquery = f"insert into animal (animalName, animalSpecies, type_, age, exhibitName) values ('{name}', '{species}', '{type_}', '{age}', '{exhibit}')"
                            curs = connection.cursor()
                            curs.execute(sqlquery)
                            connection.commit()
                            msg = f"animal: {name} \nspecies: {species} \nage: {age}"
                            self.mbox("Addded Animal", msg)
                        else:
                            self.mbox("Error", "Fail to add animal. Insufficient information.")
                    else:
                        self.mbox("Error", "Fail to add animal. Insufficient information.")
                else:
                    self.mbox("Error", "Fail to add animal. Insufficient information.")
            else:
                self.mbox("Error", "Fail to add animal. Insufficient information.")
        else:
            self.mbox("Error", "Fail to add animal. Insufficient information.")


    def mbox(self, title, message):
        logger = QMessageBox.information(self,
                    title,
                    message,
                    QMessageBox.Ok)
    def typechange(self,i):
        self.typevalue = self.typeInput.currentText()

    def exhibitchange(self,i):
        self.exhibitvalue = self.exhibitInput.currentText()

    def back(self):
        self.admin = AdminWindow(self)
        self.admin.show()
        self.close()

class AddShow(QWidget):
    def __init__(self, main, typee):
        super(AddShow, self).__init__()
        self.main = main
        self.setWindowTitle("Add Show")

        firstlabel = QLabel("Name")
        secondlabel = QLabel("Exhibit")
        thirdlabel = QLabel("Staff")
        fourthlabel = QLabel("Date")
        fifthlabel = QLabel("Time")

        self.firstText = QLineEdit()
        self.exhibitInput = QComboBox()
        self.exhibitvalue = ''
        self.exhibitInput.addItems(["--","Birds","Jungle","Mountainous","Pacific","Sahara"])
        self.exhibitInput.currentIndexChanged.connect(self.exhibitchange)
        self.thirdText = QLineEdit()
        self.fourthText = QDateEdit()
        self.fifthText = QTimeEdit()

        addShowButton = QPushButton("Add Show")
        backbutton = QPushButton("Back")

        grid = QGridLayout()
        grid.addWidget(firstlabel,1,0)
        grid.addWidget(secondlabel,2,0)
        grid.addWidget(thirdlabel,3,0)
        grid.addWidget(fourthlabel,4,0)
        grid.addWidget(fifthlabel,5,0)
        grid.addWidget(self.firstText,1,1)
        grid.addWidget(self.exhibitInput,2,1)
        grid.addWidget(self.thirdText,3,1)
        grid.addWidget(self.fourthText,4,1)
        grid.addWidget(self.fifthText,5,1)
        grid.addWidget(addShowButton,6,0)
        grid.addWidget(backbutton,6,1)

        self.setLayout(grid)

        addShowButton.clicked.connect(lambda: self.addValue(self.firstText.text(), self.exhibitvalue, self.thirdText.text(), self.fourthText.text(), self.fifthText.text()))
        backbutton.clicked.connect(self.back)

    def addValue(self, name, exhibit, staff, date, time):
        if name != '' and name != None:
            if exhibit != '' and exhibit != None and exhibit != '--':
                if staff != '' and staff != None:
                    if date !='' and date != None:
                        if time != '' and time != None:
                            dateAndTime = date + " " + time
                            sqlquery = f"insert into show_ (showName, username, exhibitName, dateAndTime) values ('{name}', '{staff}', '{exhibit}', '{dateAndTime}')"
                            print(sqlquery)
                            curs = connection.cursor()
                            curs.execute(sqlquery)
                            connection.commit()
                            msg = f"show: {name} \nDate and Time: {dateAndTime}"
                            self.mbox("Addded Show", msg)
                        else:
                            self.mbox("Error", "Fail to add show. Insufficient information.")
                    else:
                        self.mbox("Error", "Fail to add show. Insufficient information.")
                else:
                    self.mbox("Error", "Fail to add show. Insufficient information.")
            else:
                self.mbox("Error", "Fail to add show. Insufficient information.")
        else:
            self.mbox("Error", "Fail to add show. Insufficient information.")

    def mbox(self, title, message):
        logger = QMessageBox.information(self,
                    title,
                    message,
                    QMessageBox.Ok)

    def exhibitchange(self,i):
        self.exhibitvalue = self.exhibitInput.currentText()

    def back(self):
        self.admin = AdminWindow(self)
        self.admin.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    global connection
    connection = pymysql.connect(host='localhost',user='root',db = 'zooAtl',password = '',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    main = LoginWindow()
    main.show()
    sys.exit(app.exec_())
