""" 
COVID-19 MANAGEMENT SYSTEM 😷

============================
CREATION DATE: JULY 07, 2021
LAST UPDATED: JULY 21, 2021

============================
PROGRAMMER: Jxrom (つ▀¯▀)つ

============================
Note: If you find some bugs 🐞 email me pls! thankyou! ⊂(´・ω・｀⊂)
Email: jeromemarbebe@gmail.com
"""

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sqlite3 
import sqlite3 as sql
import pandas as pd
import os
import sys
import resource

progressBarValue = 0 
page_number = 1

# <====================================== LOADING SCREEN ======================================>

class LoadingScreen(QWidget):
	def __init__(self):
		super(LoadingScreen, self).__init__()
		loadUi("loadingscreen.ui", self)

		# <======================= DATABASE CREATION =======================>

		self.connection = sqlite3.connect("patientdata.db")
		self.cursor = self.connection.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS patients(ID_NUMBER INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, SEX TEXT, AGE TEXT, CONTACT TEXT, CITY TEXT, STATUS TEXT, USERNAME TEXT, PASSWORD TEXT, Q1 TEXT , Q2 TEXT , Q3 TEXT, Q4 TEXT, Q5 TEXT)")
		self.cursor.close()

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		# TIMER
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.appProgress)
		# time interval in Milliseconds for the progressbar to change value
		self.timer.start(100)

		self.show()

# <====================================== PROGRESS BAR ======================================>

	def appProgress(self):
		global progressBarValue
		
		#Apply progressBarValue to the progressBar
		self.progressBar.setValue(progressBarValue)

		if progressBarValue > 100:
			self.timer.stop()
			self.close()
			self.GotoLoginScreen()
		elif progressBarValue < 25:
			QtCore.QTimer.singleShot(0, lambda: self.loadingstatus.setText(" Connecting to Database"))
		elif progressBarValue < 50:
			QtCore.QTimer.singleShot(0, lambda: self.loadingstatus.setText("     Loading Database"))
		elif progressBarValue < 75:
			QtCore.QTimer.singleShot(0, lambda: self.loadingstatus.setText("        Please Wait.."))

		progressBarValue += 1

	def GotoLoginScreen(self):
		self.window = LoginScreen()
		self.window.show()

# <====================================== LOGIN SCREEN ======================================>

class LoginScreen(QWidget):
	def __init__(self):
		super(LoginScreen, self). __init__()
		loadUi("login_design.ui", self)

		global username
		global password

		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		# <======================= BUTTON CONNECTION =======================>

		self.Admin_PushButton.clicked.connect(self.AdminButton)
		self.Admin_PushButton.clicked.connect(self.close)
		self.Login_PushButton.clicked.connect(self.UserLoginButton)
		self.Create_Button.clicked.connect(self.ShowCreateNew)

	# <======================= BUTTON FUNCTIONS =======================>

	def AdminButton(self):
		self.window = AdminDashboard()
		
		username = self.UserName_LineEdit.text()
		password = self.Password_LineEdit.text()
		
		# ADMIN USERNAME: admin
		# ADMIN PASSWORD: admin
		if username == 'admin' and password == 'admin':
			self.window.show()

		elif username == ' ' and password == ' ':
			print("Please Enter Password")
		else:
			self.ErrorDialog()
			self.window = LoginScreen()
			self.window.show()

	def UserLoginButton(self):
		check_username = self.UserName_LineEdit.text()
		check_password = self.Password_LineEdit.text()

		username = check_username
		password = check_password

		print("try:", username, password)

	# <=================== CHECK USERNAME/PASSWORD ===================>

		if check_username == "" and check_password == "":
				self.MissingDialog()
		elif check_username == "" or check_password == "":
				self.MissingDialog()

		self.connection = sqlite3.connect('patientdata.db')
		self.cursor = self.connection.cursor()
		self.cursor.execute("SELECT USERNAME, PASSWORD from patients") # QUERY
		
		for (user_name, user_password) in self.cursor:
			if check_username == user_name and check_password == user_password:
				print("USERNAME: ", check_username)
				print("PASSWORD: ", check_password)
				self.ShowUser()
				break
			else:
				print("ALL DATA HAS BEEN CHECKED")
				
		self.connection.commit()
		self.cursor.close()
		self.connection.close()

 	# <=============== INVALID INPUT DIALOG ===============>

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("images/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Invalid Username or Password!")
		msg.setInformativeText('Please Retry')
		msg.setWindowTitle("Invalid Input")
		msg.exec_()

	def MissingDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("images/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Invalid Credentials or Missing Input!")
		msg.setInformativeText('Please Retry')
		msg.setWindowTitle("Invalid Input")
		msg.exec_()
	
	# <=============== DEFINE FORMS ===============>

	def ShowUser(self):
		self.window = UserLogin()
		self.window.show()

	def ShowCreateNew(self):
		self.window = CreateNewAcc()
		self.window.show()

# <====================================== ADMIN DASHBOARD ======================================>

class AdminDashboard(QMainWindow):
	def __init__(self):
		super(AdminDashboard, self). __init__()
		loadUi("admindashboard.ui", self)

		self.setFixedSize(788, 524)

	# <======================= BUTTON CONNECTION =======================>

		self.Add_PushButton.clicked.connect(self.AddButton)
		self.Delete_PushButton.clicked.connect(self.DeleteButton)
		self.Update_PushButton.clicked.connect(self.UpdateButton)
		self.Refresh_PushButton.clicked.connect(self.RefreshButton)
		self.Search_PushButton.clicked.connect(self.SearchButton)
		self.Print_PushButton.clicked.connect(self.PrintButton)

	# <======================== BUTTONS FUNCTIONS ========================>

	def AddButton(self):
		self.window = AddPatient()
		self.window.show()
		self.RefreshButton()

	def DeleteButton(self):
		self.window = DeletePatient()
		self.window.show()

	def SearchButton(self):
		self.window = SearchPatient()
		self.window.show()

	def UpdateButton(self):
		self.window = UpdatePatient()
		self.window.show()

# <======================== PRINT FUNCTION TO OPEN A EXCEL FILE ========================>

	def PrintButton(self):
		Dashboard_Window = QtWidgets.QMainWindow()
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/printbutton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		Dashboard_Window.setWindowIcon(icon)

		print_messagebox = QMessageBox.question(Dashboard_Window, 'Print', "Do you want to print table data?", QMessageBox.Yes | QMessageBox.No)
		if print_messagebox == QMessageBox.Yes: 
				connection = sql.connect('patientdata.db')

				df = pd.read_sql(sql = "SELECT * from patients", con = connection)
				df.to_excel('patientsdata.xlsx')
				print(df)
				os.system('start excel.exe patientsdata.xlsx')
				
		else:
				print('Nothing Happened')

	# <======================== LOAD DATA FROM THE DATABASE ========================>

	def RefreshButton(self):
		self.connection = sqlite3.connect("patientdata.db")
		query = "SELECT * FROM patients"
		result = self.connection.execute(query)
		self.DashBoard_Widget.setRowCount(0)
		for row_number, row_data in enumerate(result):
			self.DashBoard_Widget.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.DashBoard_Widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
		self.connection.close()

# <====================================== ADD PATIENT FORM ======================================>

class AddPatient(QWidget):
	def __init__(self):
		super(AddPatient, self). __init__()
		loadUi("addpatient.ui", self)

		self.setFixedSize(260, 441)
		self.RegisterPatient_PushButton.clicked.connect(self.addpatient_db)

	# <================================ ADD STUDENT IN DATABASE ================================>

	def addpatient_db(self):
		name = ""
		sex = ""
		age = ""
		contact = ""
		city = ""
		status = ""

		name = self.Name_LineEdit.text()
		sex = self.Sex_LineEdit.text()
		age = self.Age_LineEdit.text()
		contact = self.Contact_LineEdit.text()
		city = self.City_LineEdit.text()
		status = self.Status_LineEdit.text()

		try:
			self.connection = sqlite3.connect("patientdata.db")
			self.cursor = self.connection.cursor()
			self.cursor.execute("INSERT INTO patients (NAME, SEX, AGE, CONTACT, CITY, STATUS) VALUES (?, ?, ?, ?, ?, ?)", (name, sex, age, contact, city, status))
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
			self.Added_msgbox()
		except:
			self.ErrorDialog()
	
	# <=============== INVALID INPUT DIALOG ===============>

	def Added_msgbox(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient successfully added to the database")
		msg.setWindowTitle("Add Patient")
		msg.exec_()

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient could not add to the database")
		msg.setWindowTitle("Error")
		msg.exec_()

# <====================================== DELETE PATIENT FORM ======================================>

class DeletePatient(QWidget):
	def __init__(self):
		super(DeletePatient, self). __init__()
		loadUi("deletepatient.ui", self)

		self.setFixedSize(354, 173)

	# <======================= BUTTON CONNECTION =======================>

		self.DeleteUserPatient.clicked.connect(self.deletepatient_db)

	# <======================= DELETE PATIENT FROM DATABASE =======================>

	def deletepatient_db(self):
		del_idnumber = ""
		del_idnumber = self.IDLineEdit.text()

		try:
			self.connection = sqlite3.connect("patientdata.db")
			self.cursor = self.connection.cursor()
			self.cursor.execute("DELETE from patients WHERE ID_NUMBER="+str(del_idnumber))
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
			self.Deleted_msgbox()
		except Exception:
			self.ErrorDialog()

	# <=============== INVALID INPUT DIALOG ===============>

	def Deleted_msgbox(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient successfully deleted to the database")
		msg.setWindowTitle("Delete Patient")
		msg.exec_()

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient could not delete to the database")
		msg.setWindowTitle("Error")
		msg.exec_()

class UpdatePatient(QWidget):
	def __init__(self):
		super(UpdatePatient, self). __init__()
		loadUi("updatepatient.ui", self)

		self.setFixedSize(299, 279)

	# <======================= BUTTON CONNECTION =======================>

		self.UpdateButton.clicked.connect(self.updatepatient_db)	

	# <======================= UPDATE PATIENT FROM DATABASE =======================>

	def updatepatient_db(self):
		update_IDNumber = ""
		update_Status = ""

		update_IDNumber = self.ID_NumberLineEdit.text()
		update_Status = self.StatusLineEdit.text()

		try:
			query = "UPDATE patients SET STATUS = ? WHERE ID_NUMBER = ?"
			parameters = (update_Status, update_IDNumber)
			self.connection = sqlite3.connect("patientdata.db")
			self.cursor = self.connection.cursor() 
			self.cursor.execute(query, parameters)
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
			self.Update_msgbox()
		except Exception:
			self.ErrorDialog()

	# <=============== INVALID INPUT DIALOG ===============>

	def Update_msgbox(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient successfully updated to the database")
		msg.setWindowTitle("Update Patient")
		msg.exec_()

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient could not update in the database")
		msg.setWindowTitle("Error")
		msg.exec_()	

class SearchPatient(QWidget):
	def __init__(self):
		super(SearchPatient, self). __init__()
		loadUi("searchpatient.ui", self)

		self.setFixedSize(354, 173)

	# <======================= BUTTON CONNECTION =======================>

		self.SearchButton.clicked.connect(self.searchpatient_db)

	# <======================= SEARCH PATIENT FROM DATABASE =======================>

	def searchpatient_db(self):
		
		searchpatient = ""
		searchpatient = self.SearchID_LineEdit.text()
		try:
			self.connection = sqlite3.connect("patientdata.db")
			self.cursor = self.connection.cursor()
			result = self.cursor.execute("SELECT * from patients WHERE ID_NUMBER="+str(searchpatient))
			row = result.fetchone()
			self.searchresult = "ID Number: " + str(row[0]) + '\n' + "Name: " + str(row[1]) + '\n' + "Sex: " + str(row[2]) + '\n' \
			"Age: " + str(row[3]) + '\n' + "Contact: " + str(row[4]) + '\n'+ "City: " + str(row[5]) + '\n' + "Status: " + str(row[6]) 
			self.InformationDialog()
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
		except Exception:
			self.ErrorDialog()

	# <=============== INVALID INPUT DIALOG ===============>

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient could not find in the database")
		msg.setWindowTitle("Error")
		msg.exec_()

	def InformationDialog(self):
		info_msg = QMessageBox()
		info_icon = QtGui.QIcon()
		info_icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		info_msg.setWindowIcon(info_icon)
		info_msg.setInformativeText(self.searchresult)
		info_msg.setWindowTitle("Search Result")
		info_msg.exec_()

class UserLogin(QMainWindow):
	def __init__(self):
		super(UserLogin, self). __init__()
		loadUi("userdashboard.ui", self)
		self.setFixedSize(788, 567)

		self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
		self.stackedWidget.setGeometry(QtCore.QRect(180, 140, 591, 381))
		self.stackedWidget.setObjectName("stackedWidget")
		self.page = QtWidgets.QWidget()
		self.page.setObjectName("page")
		self.label_6 = QtWidgets.QLabel(self.page)
		self.label_6.setGeometry(QtCore.QRect(0, 0, 591, 381))
		self.label_6.setStyleSheet("image: url(stackedwidgets_pic/coronavirus-prevention-infographic_23-2148523347.jpg)")
		self.label_6.setText("")
		self.label_6.setPixmap(QtGui.QPixmap("stackedwidgets_pic/coronavirus-prevention-infographic_23-2148523347.jpg"))
		self.label_6.setScaledContents(True)
		self.label_6.setObjectName("label_6")
		self.stackedWidget.addWidget(self.page)
		self.page_2 = QtWidgets.QWidget()
		self.page_2.setObjectName("page_2")
		self.label_7 = QtWidgets.QLabel(self.page_2)
		self.label_7.setGeometry(QtCore.QRect(0, 0, 591, 381))
		self.label_7.setText("")
		self.label_7.setPixmap(QtGui.QPixmap("stackedwidgets_pic/wiw2020-quote.png"))
		self.label_7.setScaledContents(True)
		self.label_7.setObjectName("label_7")
		self.stackedWidget.addWidget(self.page_2)
		self.page_3 = QtWidgets.QWidget()
		self.page_3.setObjectName("page_3")
		self.label_8 = QtWidgets.QLabel(self.page_3)
		self.label_8.setGeometry(QtCore.QRect(0, 0, 591, 381))
		self.label_8.setText("")
		self.label_8.setPixmap(QtGui.QPixmap("stackedwidgets_pic/20180705-I-quote-vaccines.png"))
		self.label_8.setScaledContents(True)
		self.label_8.setObjectName("label_8")
		self.stackedWidget.addWidget(self.page_3)

	# <======================= BUTTON CONNECTION =======================>

		self.next_Button.clicked.connect(self.ShowCurrentFeed)
		self.UserInfo_Button.clicked.connect(self.UserInfoButton)
		self.HealthStatus_Button.clicked.connect(self.HealthDeclarationButton)
		self.VaccinationArea_Button.clicked.connect(self.VaccinationAreasButton)
		self.InfectedAreas_Button.clicked.connect(self.InfectedAreasButton)
		self.Logout_Button.clicked.connect(self.LogoutButton)

	# <===================== FUNCTION TO SHOW CURRENT SLIDE IN FEED =====================>

	def ShowCurrentFeed(self):
		global page_number
		pages = [self.page, self.page_2, self.page_3]
		self.stackedWidget.setCurrentWidget(pages[page_number])
		page_number = page_number + 1
		if page_number == 3:
				page_number = 0
		print(page_number)

	# <===================== FUNCTION TO SHOW WINDOW FORM =====================>

	def UserInfoButton(self):
		self.window = ShowPersonalStatus()
		self.window.show()

	def HealthDeclarationButton(self):
		self.window = HealthDeclaration()
		self.window.show()

	def VaccinationAreasButton(self):
		self.window = VaccinationAreas()
		self.window.show()

	def InfectedAreasButton(self):
		self.window = InfectedAreas()
		self.window.show()

	def LogoutButton(self):
		print("LOGOUT")
		self.QuestionDialog()
		
	# <=============== QUESTION INPUT DIALOG ===============>

	def QuestionDialog(self):
		message = QMessageBox.question(self, "Logout", 
									   "Do you want to logout?",
									   QMessageBox.Yes | 
									   QMessageBox.No)
		if message == QMessageBox.Yes:
			self.label.setText("")
			self.close()
	
		else:
			self.show()

# <================================ SHOW PERSONAL STATUS ================================>

class ShowPersonalStatus(QWidget):
	def __init__(self):
		super(ShowPersonalStatus, self). __init__()
		loadUi("userinfo.ui", self)

		self.setFixedSize(470, 320)

	# <======================= BUTTON CONNECTION =======================>

		self.SearchUser.clicked.connect(self.setInfo)
		
	# <======================= SET INFO FUNCTION =======================>

	def setInfo(self):
		global idnumber

		# ERROR HANDLINFG: IF THE USER INPUT STRING

		try:
			idnumber = int(self.ID_NumberLineEdit.text())
		
			self.SetImage()
			self.SetName()
			self.SetSex()
			self.SetAge()
			self.SetContact()
			self.SetCity()
		except Exception:
			self.MissingUserDialog()
		
	# <======================= SET IMAGE FUNCTION =======================>

	def SetImage(self):
		self.connection = sqlite3.connect('patientdata.db')
		self.cursor = self.connection.cursor()
		query = "SELECT SEX from patients WHERE ID_NUMBER = %d" % (idnumber)
		self.cursor.execute(query)

		self.sex = []
		for i in self.cursor.fetchone():
			self.sex.append(i)
			self.result = str(self.sex[0])
			print("RESULT IMAGE:", self.result)

			if self.result == "Male":
				self.label_2.setStyleSheet(u"image: url(icons/user.png)")
			elif self.result == "Female":
				self.label_2.setStyleSheet(u"image: url(icons/usergirl.png)")


# <========================== SET VALUE TO PERSONAL INFORMATION WINDOW ==========================>

	def SetName(self):
		self.connection = sqlite3.connect('patientdata.db')
		self.cursor = self.connection.cursor()
		query = "SELECT NAME from patients WHERE ID_NUMBER = %d" % (idnumber)
		self.cursor.execute(query)
		
		self.name = []
		for i in self.cursor.fetchone():
			self.name.append(i)
			self.result = str(self.name[0])
			print(self.result)

		self.Name_Label.setText(self.result)

	def SetAge(self):
		self.connection = sqlite3.connect('patientdata.db')
		self.cursor = self.connection.cursor()
		query = "SELECT AGE from patients WHERE ID_NUMBER = %d" % (idnumber)
		self.cursor.execute(query)
	
		self.age = []
		for i in self.cursor.fetchone():
			self.age.append(i)
			self.result = str(self.age[0])
			print(self.result)

		self.Age_Label.setText(self.result)

	def SetSex(self):
		self.connection = sqlite3.connect('patientdata.db')
		self.cursor = self.connection.cursor()
		query = "SELECT SEX from patients WHERE ID_NUMBER = %d" % (idnumber)
		self.cursor.execute(query)
		
		self.sex = []
		for i in self.cursor.fetchone():
			self.sex.append(i)
			self.result = str(self.sex[0])
			print(self.result)

		self.Sex_Label.setText(self.result)

	def SetContact(self):
		self.connection = sqlite3.connect('patientdata.db')
		self.cursor = self.connection.cursor()
		query = "SELECT CONTACT from patients WHERE ID_NUMBER = %d" % (idnumber)
		self.cursor.execute(query)
		
		self.contact = []
		for i in self.cursor.fetchone():
			self.contact.append(i)
			self.result = str(self.contact[0])
			print(self.result)

		self.Contact_Label.setText(self.result)

	def SetCity(self):
		self.connection = sqlite3.connect('patientdata.db')
		self.cursor = self.connection.cursor()
		query = "SELECT CITY from patients WHERE ID_NUMBER = %d" % (idnumber)
		self.cursor.execute(query)
		
		self.city = []
		for i in self.cursor.fetchone():
			self.city.append(i)
			self.result = str(self.city[0])
			print(self.result)

		self.City_Label.setText(self.result)

	# <=============== MISSING INPUT DIALOG ===============>

	def MissingUserDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient could not find in the database")
		msg.setWindowTitle("Error")
		msg.exec_()	

# <========================== HEALTH DECLARATION WINDOW ==========================>

class HealthDeclaration(QWidget):
	def __init__(self):
		super(HealthDeclaration, self). __init__()
		loadUi("healthdeclaration.ui", self)

		self.setFixedSize(469, 321)
		self.userimage.setStyleSheet(u"image: url(icons/patient status.png)")

	# <======================= BUTTON CONNECTION =======================>

		self.SearchUser.clicked.connect(self.setUserInfo)

	# <======================= SET INFO FUNCTIONS =======================>

	def setUserInfo(self):
		global idnumber
		try:
			idnumber = int(self.ID_NumberLineEdit.text())
			self.SetImage()
		except Exception:
			self.MissingUserDialog()

	# <======================= SET IMAGE FUNCTION =======================>

	def SetImage(self):
		self.connection = sqlite3.connect('patientdata.db')
		self.cursor = self.connection.cursor()
		query = "SELECT STATUS from patients WHERE ID_NUMBER = %d" % (idnumber)
		self.cursor.execute(query)

		self.status = []
		for i in self.cursor.fetchone():
			self.status.append(i)
			self.result = str(self.status[0])
			print("RESULT IMAGE:", self.result)

			if self.result == "Positive":
				self.userimage.setStyleSheet(u"image: url(icons/positive.png)")
				self.userlabel.setText("                   Positive!")
				self.userlabel_2.setText("Please Seek Medical Attention!")
			elif self.result == "Negative":
				self.userimage.setStyleSheet(u"image: url(icons/negative.png)")
				self.userlabel.setText("                   Negative!")
				self.userlabel_2.setText("              Please Stay at Home")
			elif self.result == "Under Observation":
				self.userimage.setStyleSheet(u"image: url(icons/stay.png)")
				self.userlabel.setText("       Under Observation")
				self.userlabel_2.setText("              Please Stay at Home!")
			elif self.result == "":
				self.userimage.setStyleSheet(u"image: url(icons/patient status.png)")
				self.userlabel.setText("                   Status")
				self.userlabel_2.setText("")

	# <======================= MISSING DIALOG FUNCTIONS =======================>

	def MissingUserDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient could not find in the database")
		msg.setWindowTitle("Error")
		msg.exec_()		

# <========================== VACCINATION AREA WINDOW ==========================>

class VaccinationAreas(QWidget):
	def __init__(self):
		super(VaccinationAreas, self).__init__()
		loadUi("vaccinationareas.ui", self)

		self.setFixedSize(630, 410)
		
	# <========================== SEARCH FILTER ==========================>

		vaccinationcities = ('Quezon City', 'Caloocan City', 'Rizal City', 'Muntinlupa City', 'Pasig City', 'Davao City',
			'Cebu City', 'Baguio City', 'Pasay City', 'Bacolod City')
		model = QStandardItemModel(len(vaccinationcities), 1)
		model.setHorizontalHeaderLabels(['Cities'])

		for row, cities in enumerate(vaccinationcities):
			item = QStandardItem(cities)
			model.setItem(row, 0, item)

		filter_proxy_model = QSortFilterProxyModel()
		filter_proxy_model.setSourceModel(model)
		filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
		filter_proxy_model.setFilterKeyColumn(0)

		self.City_LineEdit.textChanged.connect(filter_proxy_model.setFilterRegExp)
		self.cities_TableView.setModel(filter_proxy_model)

# <========================== INFECTED AREAS WINDOW ==========================>

class InfectedAreas(QWidget):
	def __init__(self):
		super(InfectedAreas, self).__init__()
		loadUi("infectedareas.ui", self)

		self.setFixedSize(630, 416)

	# <========================== BUTTON CONNECTION ==========================>

		self.refresh_button.clicked.connect(self.RefreshButton)

	# <========================== LOAD DATA FROM THE DATABASE ==========================>

	def RefreshButton(self):
		self.connection = sqlite3.connect("patientdata.db")
		query = "SELECT CITY FROM patients"
		result = self.connection.execute(query)
		self.DashBoard_Widget.setRowCount(0)
		for row_number, row_data in enumerate(result):
			self.DashBoard_Widget.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.DashBoard_Widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
		self.connection.close()

# <========================== INFECTED AREAS WINDOW ==========================>

class CreateNewAcc(QWidget):
	def __init__(self):
		super(CreateNewAcc, self). __init__()
		loadUi("new_account.ui", self)

		self.setFixedSize(560, 490)
		self.Proceed_Button.clicked.connect(self.RegisterButton)
		self.Next_PushButton.clicked.connect(self.NextButton)
		self.Register_PushButton.clicked.connect(self.ProceedBtnCheckRadio)
		self.Register_PushButton.clicked.connect(self.close)

	# <======================== PROCEED BUTTONS ========================>

	def ProceedtoVac(self):
		self.stackedWidget.setCurrentWidget(self.page_2)

	def NextButton(self):
		self.stackedWidget.setCurrentWidget(self.page_3)

# <======================== REGISTRATION BUTTON ========================>

	def RegisterButton(self):
		name = ""
		sex = ""
		age = ""
		contact = ""
		city = ""
		status = ""
		username = ""
		password = ""

		name = self.Name_LineEdit.text()
		sex = self.Sex_LineEdit.text()
		age = self.Age_LineEdit.text()
		contact = self.Contact_LineEdit.text()
		city = self.City_LineEdit.text()
		username = self.UserNameReg_LineEdit.text()
		password = self.PasswordReg_LinedEdit.text()
		
		if name == "" and sex == "" and age == "" and contact == "" and contact == "" and city == "" and username == "" and password == "":
			self.MissingDialog()
			self.stackedWidget.setCurrentWidget(self.page)
			print("Could not add")

		elif name == "" or sex == "" or age == "" or contact == "" or contact == "" or city == "" or username == "" or password == "":
			self.MissingDialog()
			self.stackedWidget.setCurrentWidget(self.page)
			print("Could not add")

		else: 
			self.connection = sqlite3.connect("patientdata.db")
			self.cursor = self.connection.cursor()
			self.cursor.execute("INSERT INTO patients (NAME, SEX, AGE, CONTACT, CITY, STATUS, USERNAME, PASSWORD) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, sex, age, contact, city, status, username, password))	
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
			self.ProceedtoVac()

# <========================== REGISTER BUTTON FUNCTION ==========================>

	def ProceedBtnCheckRadio(self):
		username = ""
		username = self.UserNameReg_LineEdit.text()
		print("USERNAME: ", username)

		YES = "YES"
		NO = "NO"

	# <========================== CHECK RADIO BUTTONS - SET TO DATABASE ==========================>

		try:
			if self.Question1_Yes.isChecked():
				query = "UPDATE patients SET Q1 = ? WHERE USERNAME = ?"
				parameters = (YES, username)
					
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()
			elif self.Question1_No.isChecked():
				query = "UPDATE patients SET Q1 = ? WHERE USERNAME = ?"
				parameters = (NO, username)
					
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()

			if self.Question2_Yes_2.isChecked():
				query = "UPDATE patients SET Q2 = ? WHERE USERNAME = ?"
				parameters = (YES, username)
					
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()
			elif self.Question2_No_2.isChecked():
				query = "UPDATE patients SET Q2 = ? WHERE USERNAME = ?"
				parameters = (NO, username)
					
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()

			if self.Question3_Yes_3.isChecked():
				query = "UPDATE patients SET Q3 = ? WHERE USERNAME = ?"
				parameters = (YES, username)
					
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()
			elif self.Question3_No_3.isChecked():
				query = "UPDATE patients SET Q3 = ? WHERE USERNAME = ?"
				parameters = (NO, username)
					
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()

			if self.Question4_Yes.isChecked():
				query = "UPDATE patients SET Q4 = ? WHERE USERNAME = ?"
				parameters = (YES, username)
				
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()
			elif self.Question4_No.isChecked():
				query = "UPDATE patients SET Q4 = ? WHERE USERNAME = ?"
				parameters = (NO, username)
				
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()

			if self.Question5_Yes.isChecked():
				query = "UPDATE patients SET Q5 = ? WHERE USERNAME = ?"
				parameters = (YES, username)
					
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()
			elif self.Question5_No.isChecked():
				query = "UPDATE patients SET Q5 = ? WHERE USERNAME = ?"
				parameters = (NO, username)
					
				self.connection = sqlite3.connect("patientdata.db")
				self.cursor = self.connection.cursor()

				self.cursor.execute(query, parameters)	
				self.connection.commit()
				self.cursor.close()
				self.connection.close()

			self.Added_msgbox()
		except:
			self.ErrorDialog()

		self.connection = sqlite3.connect("patientdata.db")
		self.cursor = self.connection.cursor()

		result = self.cursor.execute("SELECT ID_NUMBER from patients WHERE USERNAME = ?", (username, ) )
			
		row = result.fetchone()	
		self.searchresult = "ID Number: " + str(row[0])
		self.InformationDialog()
		self.connection.commit()
		self.cursor.close()
		self.connection.close()
	
	# <========================== INFORMATION DIALOG ==========================>

	def InformationDialog(self):
		info_msg = QMessageBox()
		info_icon = QtGui.QIcon()
		info_icon.addPixmap(QtGui.QPixmap("icons/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		info_msg.setWindowIcon(info_icon)
		info_msg.setText(self.searchresult)
		info_msg.setWindowTitle("ID NUMBER")
		info_msg.exec_()

	# <======================== DIALOG FUNCTIONS FOR REGISTRATION BUTTON ========================>

	def Added_msgbox(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Registration Sucess")
		msg.setInformativeText("＼(^o^)／")
		msg.setWindowTitle("Registration")
		msg.exec_()

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/covid19"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Patient could not add to the database")
		msg.setWindowTitle("Error")
		msg.exec_()

	def MissingDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("images/covid19.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Please fill up all text box!")
		msg.setInformativeText("╥﹏╥")
		msg.setWindowTitle("Missing Input")
		msg.exec_()
	
# EXECUTE MAIN APPLICATION
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	window = LoadingScreen()
	sys.exit(app.exec_())