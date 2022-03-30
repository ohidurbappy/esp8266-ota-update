from flask import Flask, redirect, render_template,request,make_response, url_for,flash
from hashlib import md5
import os
import time

app=Flask(__name__)
app.secret_key='superSecr3t'


if not os.path.exists('./uploads'):
    os.mkdir('./uploads')

static = os.path.join(os.path.dirname(__file__), 'static')

def get_checksum(data):
    return md5(data).hexdigest()


def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

@app.route('/')
def index():
    files=os.listdir('./uploads')
    files=sorted(files,reverse=True)
    return render_template('index.html',files=files)


@app.route('/update')
def update():
    current_version_checksum=request.args.get('checksum','')
    files=os.listdir('./uploads')
    files=sorted(files)
    newest_file=files[-1]

    new_version_data=read_file('./uploads/'+newest_file)
    new_version_checksum=get_checksum(new_version_data.encode('utf-8'))

    if current_version_checksum==new_version_checksum:
        return make_response("No update available", 404)

    new_version_data=f"""checksum="{new_version_checksum}"
{new_version_data}    
"""
    return new_version_data

@app.route('/file/<file>')
def show_file(file):
    read_only=True
    files=os.listdir('./uploads')
    files=sorted(files,reverse=True)
    try:
        file_data=read_file(f'./uploads/{file}')
        file_checksum=get_checksum(file_data.encode('utf-8'))
    except FileNotFoundError:
        flash(f'File {file} not found')
        return redirect(url_for('index'))
    return render_template('index.html',file_data=file_data,filename=file,read_only=read_only,files=files,checksum=file_checksum)

@app.route('/upload', methods=['POST'])
def upload():
    data=request.form.get('data','').strip()
    data=data.replace('\n','')
    if data=='':
        flash("No data provided")
        return redirect(url_for('index'))
    filename=time.strftime('%Y%m%d%H%M%S')
    with open(f'./uploads/{filename}', 'w',encoding='utf-8') as f:
        f.write(data)
    
    return redirect(url_for('show_file',file=filename))



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
