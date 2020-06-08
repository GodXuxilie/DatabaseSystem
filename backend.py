from gevent import monkey
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timedelta
import supportFunction as sf
import re
import json

#开了10个线程，用于处理不同任务
executor = ThreadPoolExecutor(10)
#猴子魔法，使多个路由之间不互相阻塞
monkey.patch_all()
#类型集合
types_in_database = sf.types_modified_in_database
#过滤错误输入信息
pattern_for_id = re.compile(r'^([0-9]{1,11})$')
pattern_for_gender = re.compile(r'^(M|F)$')
pattern_for_age = re.compile(r'^[0-9]{0,3}$')
pattern_for_passwd = re.compile(r'^(.{1,70}$)')

#导入flask
from flask import Flask, render_template, redirect,request, jsonify,session
#本代码中所有重定向可能都得改成返回重定向字符串，由前端进行重定向
app = Flask(__name__)
app.config.update(
    DEBUG=True
)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    #这里的逻辑应该是检查一下用户有没有登录，有的话就是搜索主页
    #没有的话就重定向到登录界面
    if session.get('user'):
        #这个网页中应该有自动向server请求推荐列表的脚本
        return render_template('index.html',userName = session.get('user'))
    else:
        return redirect('/login')

#这个地址要求是前端重定向到的
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if not session.get('user'):
            return render_template('login.html')
    if request.method == 'POST':
        login_id = request.form.get('username')
        login_passwd = request.form.get('passwd')
        if login_id != None and login_passwd != None:
            userInfo = (login_id,login_passwd)
            state = sf.validate_userInfo(userInfo)
            if state == 'Not exist':
                #前端应提示用户名不存在，然后重定向到/login
                return 'Not Exist'
            elif state == 'success':
                session['user'] = userInfo[0]
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=10)
                #前端应重定向到/页面
                return 'success'
            else:
                return 'fail'
        else:
            return 'fail'
    else:
        return redirect('/')

#这个地址要求是前端重定向到的
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        if not session.get('user'):
            return redirect('/login')
        #return render_template('register.html')
    if request.method == 'POST':
        print('point1')
        #try:
        register_name = re.match(pattern_for_id,request.form.get('username'))
        register_passwd = re.match(pattern_for_passwd,request.form.get('passwd'))
        register_gender = re.match(pattern_for_gender,request.form.get('gender'))
        register_age = re.match(pattern_for_age,request.form.get('age'))
        register_jobid = re.match(pattern_for_id,request.form.get('jobid'))
        register_zipcode = re.match(pattern_for_id,request.form.get('zipCode'))
        register_type = request.form.get('types')
        types = register_type.split(',')
        #except Exception:
        #    return redirect('/')
        flag_of_types = True
        if types:
            for type in types:
                if type not in types_in_database:
                    flag_of_types = False
                    break
        else:
            flag_of_types = False
        print('point1.5')
        print(request.form.get('age'))
        print(register_name,',',register_gender,',',register_age,',',register_jobid,',',register_zipcode,',',register_passwd,',',flag_of_types)
        if(register_name != None and register_gender != None and register_age and register_jobid and register_zipcode and register_passwd and flag_of_types == True):
            print('point2')
            userInfo = (register_name.group(0),register_passwd.group(0))
            state = sf.validate_userInfo(userInfo)
            if state == 'Not exist':
                #这个人没注册过                
                print('point3')
                userInfo = (userInfo[0],register_gender.group(0),\
                    register_age.group(0),register_jobid.group(0),\
                        register_zipcode.group(0),userInfo[1],\
                            types)
                #executor.submit(sf.add_userInfo, userInfo)
                state = sf.add_userInfo(userInfo)
                #把两者加入数据库
                #return redirect('/login')
                if state == 'success':
                    print('tologin')
                    return 'tologin'
                else:
                    return 'failed'
            else:
                #这个人已经注册过
                print('existed')
                return 'Existed'
        else:
            #这个人输入的注册信息不合法
            print('invalid')
            return 'invalid'
    else:
        return redirect('/')

@app.route('/list')
def get_recommend_list():
    userName = session.get('user')
    userName = re.match(pattern_for_id,userName)
    socket = request.environ.get('wsgi.websocket')
    if userName != None:
        if socket:
            #有socket 
            #这里的逻辑其实应该是，开一个线程，在其中用websocket和前端通信（还没写）
            #这边立刻返回个success之类的，防止前端阻塞
            #executor.submit(sf.get_list_from_dataset,socket,userName.group(0))
            sf.get_list_from_dataset(socket,userName.group(0))
            return 'success'
        else:
            return 'error'
    else:
        return 'redirectToIndex'


#已被废弃
'''
@app.route('/query',methods=['POST'])
def get_rocommend_list_with_query():
    userName = session.get('user')
    query = request.form.get('query')
    if userName:
        #这里的逻辑其实应该是，开一个线程，在其中用websocket和前端通信（还没写）
        #这边立刻返回个success之类的，防止前端阻塞
        executor.submit(sf.get_list_from_dataset_with_query, (userName,query))
        return 'done'
    else:
        return redirect('/login')
'''

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user', None)
        session.clear()
    return 'successful_logout'
#server运行
if __name__ == "__main__":
    # app.run()
    #默认的server
    http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    #print('running')
    http_server.serve_forever()
    