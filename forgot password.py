Step-1
database_setup.py

Create DataBase
class Reset_Token(Base):
    __tablename__ = 'reset_tokens'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee_details.id'))
    token = Column(String(32),nullable=False)

step-2
project.py

from database_setup import Reset_Token
import random
import string
from wtforms import FileField, StringField, validators
from flask_mail import Mail, Message
app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'anilpolineni008@gmail.com',
	MAIL_PASSWORD = 'anil@1234',
	MAIL_DEFAULT_SENDER = 'anilpolineni008@gmail.com'
	)
mail = Mail(app)

@app.route('/resetPsw' ,methods=['GET','POST'])
def resetPsw():
	if request.method == "GET":
		return render_template('email.html')
	else:
		email = request.form['email']
		user = session.query(EmployeeDetails).filter_by(email=email).one_or_none()
		if not user:
			flash('email not found','success')
			return redirect(url_for('home'))
		reply , token = sendEmail(email)
		if reply == True:
			reset_token = session.query(Reset_Token).filter_by(employee_id=user.id).one_or_none()
			if not reset_token:
				reset_token = Reset_Token(employee_id=user.id,token=token)
			else:
				reset_token.token = token
			session.add(reset_token)
			session.commit()
			flash('mail sent Successfully',"success")
			return render_template('otp.html',email=email)
		else:
			flash('email sent failed '+str(token),'success')
		return redirect(url_for('home'))

@app.route('/verifytoken/',methods=['POST','GET'])
def verifyToken():
	if request.method == 'POST':
		print('\n'*5,'anil','POST in verifyToken')
		email = request.form['email']
		received_token = request.form['utoken']
		user = session.query(EmployeeDetails).filter_by(email=email).one_or_none()
		if not user:
			flash('email not found','success')
			return redirect(url_for('home'))
		reset_token = session.query(Reset_Token).filter_by(employee_id=user.id).one_or_none()
		if not reset_token:
			flash('Wrong request','success')
			return redirect(url_for('home'))
		sent_token = reset_token.token
		if sent_token != received_token:
			flash('Invalid token psw reset failed',"success")
			return redirect(url_for('home'))
		user.password = request.form['newpsw']
		session.add(user)
		session.commit()
		flash('password reset Successfully','success')
		return redirect(url_for('home'))
	flash('something is wrong',"success")
	return redirect(url_for('home'))

def sendEmail(email):
	try:
		to = email
		subject = "reset your password"
		token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
		flash('token '+token)
		message = "reset ur password by enter OTP  "+token
		print("\n\n\n\n",to,subject,message)

		# image = request.files['file']
		# print("file\n\n\n\n",image)
		msg = Message(subject,
			sender = ('hellostudentsattendance','anilpolineni008@gmail.com'),
		  recipients=[to])
		msg.body = message
		print('ok2') 
		# with app.open_resource("download.jpg") as fp:
		#msg.attach(form.file_.data.filename,
        #'application/octect-stream',
        #form.file_.data.read())
		#print("\n\n\n",msg)
		print('ok3')    
		mail.send(msg)
		print('\n\n\n\n\n\n','ok4')
		return True,token
	except Exception as e:
		return False,(str(e)) 




