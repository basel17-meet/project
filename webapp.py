from flask import Flask , url_for , flash , redirect , request , render_template , g
from flask import session as login_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from database_setup import Base , User , Post


app = Flask(__name__)

app.secret_key = "FUUUUCKFUCKFUCKFUCKFUCK"


engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

@app.route('/')
def main():
	if 'id' in login_session:
		if(session.query(User).filter_by(id=login_session['id']).first() is not None):
			usr = session.query(User).filter_by(id=login_session['id']).first()
			posts=session.query(Post).all()
			return render_template('main.html' , user = usr , current_id=login_session['id'], Post=posts)
		else :
			return render_template('main.html' , user=None , current_id=-1)
	else :
		return render_template('main.html' , user=None , current_id=-1)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form ['username']
		pasword = request.form ['password']
		if session.query(User).filter_by(username = username).first() is not None:
			user = session.query(User).filter_by(username = username).first()
			if user.password == pasword:
				login_session['username'] = user.username
				login_session['id'] = user.id
				return redirect(url_for('main'))
			else :
				flash ("The username or password you entered do not exist, try again or sign up if you don't have an account!")
				return redirect(url_for('login'))

	else:
		return render_template('login.html')
	


@app.route('/profile/<int:user_id>', methods = ['GET','POST'])
def profile(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	Posts = session.query(Post).filter_by(userid=user_id).all()
	if login_session['id'] is not None:
		return render_template('profile.html' , user=user , current_id=login_session['id'], Posts=Posts)
	else :
		return render_template('profile.html' , user=user , Posts=Posts)

@app.route("/post/<int:post_id>")
def product(post_id):
	post = session,query(Post).filter_by(id=post_id).one()
	return render_template('Post.html' , post = post)


@app.route('/signup/', methods = ['GET' ,'POST'])
def signup():
	if request.method == 'POST':
		usr = User(name = request.form['name'], email = request.form['email'], username  = request.form['username'], password = request.form['password'])
		if usr.name == "" or usr.email == "" or usr.username == "" or usr.password == "":	
			flash ("Please fill in all the forms")
			return redirect(url_for('signup'))
		else:
			session.add(usr)
			session.commit()
			login_session['username'] = usr.username
			login_session['id'] = usr.id
			return redirect(url_for('main'))



	else:
		return render_template('signup.html')

@app.route('/uploader/' , methods = ['GET' , 'POST'])
def upload():
	if request.method == 'POST':
		pst =Post(user =login_session['username'] , user_id =login_session['id'], title = request.form['title'] , descreption = request.form['descreption'] , file = request.form['file'])
		if (user == None):
			flash("Please login to upload") 
			return redirect(url_for('upload'))
		elif title =="" or descreption =="" or file is None:
			flash ("Please fill in all the args")
			return redirect(url_for('upload'))


		else :
			session.add(pst)
			session.commit()
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('main'))
	else :
		if(session.query(User).filter_by(id=login_session['id']).first() is not None):
			user = session.query(User).filter_by(id=login_session['id']).first()
			return render_template('uploader.html' , user=user)	
		return render_template('uploader.html')	

 
@app.route('/profile/edit' , methods = ['GET' , 'POST'])
def edit():
	if request.method == 'POST':
		usr = User(name = request.form['name'], email = request.form['email'], username  = request.form['username'], password = request.form['password'] , id=login_session['id'].one())
		if usr.name == "" or usr.email == "" or usr.username == "" or usr.password == "":	
			flash ("Please fill in all the forms")
		else :
			user = session.query(User).filter_by(id=login_session['id']).one()
			user = usr
	else :
		return render_template('edit.html')


@app.route('/logout')
def logout():
	login_session.pop('id' , None)
	return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
