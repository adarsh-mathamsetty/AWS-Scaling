from flask import Flask,request, make_response,render_template

import time
import boto3
import string
import hashlib

app = Flask(__name__)

s3=boto3.resource('s3', aws_access_key_id='AKIAIFB7PYV2I3OHGOPA', aws_secret_access_key='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', region_name='us-east-2')
bucket=s3.Bucket('bucket1files')
bucket1=s3.Bucket('addydetails')

@app.route('/')
def index():
 # return app.send_static_file('home.html') 
        return app.send_static_file('index.html')


@app.route('/logout')
def logout():
  #return app.send_static_file('home.html')
        return app.send_static_file('index.html')

"""@app.route('/login', methods=['POST'])
def login():

  username= request.form['uname']
  password= request.form['psw']
  for obj in bucket.objects.all():
    data = obj.get()["Body"].read()
    splits=string.split(data,',')
    
    for vals in splits:
      values=str(vals)
      value=string.split(values,' ')
      
      if(username==value[0] and password==value[1]):
        return app.send_static_file('index.html')
    return "Invalid credentials" """

@app.route('/upload', methods=['POST'])
def upload():
  f= request.files['file']
  comment = request.form.get('comment')
  file_name=f.filename
  content=f.read()
   
start = time.time()
  end = time.time()
  total = end-start
  totalstr = str(total)  
  return "uploaded succesfully"+ totalstr

@app.route('/download', methods=['POST', 'GET'])
def download():
  file_name = request.args.get('dwnfile', '')
  for obj in bucket.objects.all():
    if file_name == obj.key:
      data = obj.get()["Body"].read()
      response = make_response(data)
      response.headers["Content-Disposition"] = "attachment; filename=" + file_name
      return response
  return "File Not Found"


@app.route('/delete', methods=['POST','GET'])
def delete():
  filename = request.args.get('delfile', '')
  for obj in bucket.objects.all():
    if filename == obj.key:
          obj.delete()
          return 'Deleted'
  return "File not Found"

@app.route('/list1', methods=['POST','GET'])
def list1():

        
  lists=''
  for obj in bucket.objects.all():
    lists=lists+obj.key+"<br>"
    print(obj.key)
    size = obj.size
    print size
    Modified = obj.last_modified
    print Modified
    
  return lists

@app.route('/view', methods=['POST','GET'])
def img():
 return app.send_static_file('image.html') 
if __name__ == '__main__':
  app.run()
