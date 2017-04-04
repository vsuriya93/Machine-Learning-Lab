import os
from flask import Flask,request,send_file
from flask import render_template
from werkzeug import secure_filename
app = Flask(__name__,static_folder="images",static_url_path="")

app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploadedi
app.config['ALLOWED_EXTENSIONS'] = set(['zip'])

def load_details(name_file,assignment_file):
    f=open(name_file)
    g=open(assignment_file)
    final_names= [x.strip() for x in f.readlines()]
    assignments=[x.strip() for x in g.readlines()]
    final_assignment={}
    for x in assignments:
	key,value=x.split(':')
	final_assignment[key]=value
	
    return final_names,final_assignment

names,assignments=load_details("names","assignments")

@app.route("/")
def hello():
    return render_template('main.html',assignments=assignments.keys())

@app.route('/submit', methods=['GET', 'POST'])
def submit():
	if request.form['submit']=="Go to Submission Page":
		return render_template("temp.html",student_name=names,assignments=assignments.keys())
	elif request.form['submit']=="Request Assignment":
		assignment_number = request.form.get("assignment_number")
		if assignments[assignment_number]=="False":
			error="Assignment Closed"
			return render_template("upload.html",message=error)
		else:
			path="send_assignments/"+assignment_number+".zip"
			return send_file(path,as_attachment=True)
@app.route('/assignment_upload', methods=['GET', 'POST'])
def assignment_upload():
	if request.method=="POST":
		student_name = request.form.get("student_name")
		assignment_number = request.form.get("assignment_number")
		file=request.files["student_assignment"]
		if assignments[assignment_number]=="False":
			error="Assignment Closed"
			return render_template("upload.html",message=error)
		
		elif file.filename=="":
			error="No File Uploaded"
			return render_template("upload.html",message=error)
		elif file.filename.split('.')[1]!="zip":
			error="Invalid File Format"	
			return render_template("upload.html",message=error)
		print assignments[assignment_number]
		upload_file_name=secure_filename(file.filename)
		path=app.config['UPLOAD_FOLDER']+student_name+'/'+assignment_number+'/'
		file.save(os.path.join(path+upload_file_name))
			
	return render_template("upload.html",message="File Upload Successful")
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0',debug=True)
