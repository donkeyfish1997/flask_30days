from flask import Flask, redirect, render_template, request, session, url_for
import json
import os
import time

app = Flask(__name__)
app.secret_key = b'1qaz@WSX'


@app.route('/', methods=['POST', 'GET'])
def index():
    if session.get('username') is None:
        session['username'] = ''
        session['member'] = []

    return render_template('index.html', user=session['username'], USERS=session['member'])


@app.route('/register', methods=['POST', 'GET'])
def register():
    with open('./member.json', 'r') as file_object:
        member = json.load(file_object)
    if request.method == 'POST':
        if request.values['send'] == '送出':
            if request.values['userid'] in member:
                for find in member:
                    if member[find]['nick'] == request.values['username']:
                        return render_template('register.html', alert='this account and nickname are used.')
                return render_template('register.html', alert='this account is used.', nick=request.values['username'])
            else:
                for find in member:
                    if member[find]['nick'] == request.values['username']:
                        return render_template('register.html', alert='this nickname are used.',
                                               id=request.values['userid'], pw=request.values['userpw'])
                member[request.values['userid']] = {'password': request.values['userpw'],
                                                    'nick': request.values['username']}
                with open('./member.json', 'w') as f:
                    json.dump(member, f)

                basepath = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
                os.mkdir(os.path.join(basepath, request.values['userid']))
                return render_template('index.html')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        with open('./member.json', 'r') as file_object:
            member = json.load(file_object)
            session['member'] = list(member)

        if request.values['userid'] in member:
            if member[request.values['userid']]['password'] == request.values['userpw']:
                session['username'] = request.values['userid']
                print(session['member'], session['username'])

                return redirect(url_for('index'))
            else:
                return render_template('login.html', alert="Your password is wrong, please check again!")
        else:
            return render_template('login.html', alert="Your account is unregistered.")
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        if request.values['send'] == '確定':
            session.pop('username', None)

        return redirect(url_for('index'))
    return render_template('logout.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    basepath = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    dirs = os.listdir(os.path.join(basepath, session.get('username')))
    dirs.insert(0, 'New Folder')
    dirs.insert(0, 'Not Choose')

    if request.method == 'POST':
        flist = request.files.getlist("file[]")
        if flist[0].filename == '':
            return render_template('upload.html', alert='請選擇上傳檔案', dirs=dirs)

        for f in flist:
            format = f.filename[f.filename.index('.'):]
            fileName = time.time()

            if format in ('.jpg', '.png', '.PNG', '.jpeg', '.HEIC', '.jfif'):
                format = '.jpg'
            else:
                format = '.mp4'

            if request.values['folder'] == '0':
                return render_template('upload.html', alert='Please choose a folder or creat a folder', dirs=dirs)

            elif request.values['folder'] == '1':
                if not os.path.isdir(os.path.join(basepath, session.get('username'), request.values['foldername'])):    #如果不是自料夾的話
                    os.mkdir(os.path.join(basepath, session.get('username'), request.values['foldername']))
                    os.mkdir(os.path.join(basepath, session.get('username'), request.values['foldername'], 'video'))
                    os.mkdir(os.path.join(basepath, session.get('username'), request.values['foldername'], 'photo'))

                if format == '.mp4':
                    upload_path = os.path.join(basepath, session.get('username'), request.values['foldername'], 'video',
                                               str(fileName).replace('.', '') + str(format))
                else:
                    upload_path = os.path.join(basepath, session.get('username'), request.values['foldername'], 'photo',
                                               str(fileName).replace('.', '') + str(format))
            else:   #選擇已存在資料夾
                if format == '.mp4':
                    upload_path = os.path.join(basepath, session.get('username'), dirs[int(request.values['folder'])],
                                               'video', str(fileName).replace('.', '') + str(format))
                else:
                    upload_path = os.path.join(basepath, session.get('username'), dirs[int(request.values['folder'])],
                                               'photo', str(fileName).replace('.', '') + str(format))

            f.save(upload_path)

        return redirect(url_for('upload'))
    return render_template('upload.html', dirs=dirs)


if __name__ == '__main__':
    app.run(host='localhost', port='5000', debug=True)
