import pymysql
import predict as rc
from geventwebsocket.websocket import WebSocket,WebSocketError
from concurrent.futures import ThreadPoolExecutor
import databaseInfo as db
import datetime
import re
import json
#开启10个进程
executor = ThreadPoolExecutor(10)
#过滤\n
pattern_for_types = re.compile(r'')
#类型集合
types_in_database = ['Animation',\
    'Children s', \
    'Comedy\n',\
    'Adventure',\
    'Fantasy\n',\
    'Comedy',\
    'Romance\n',\
    'Drama\n',\
    'Action',\
    'Crime',\
    'Thriller\n',\
    'Children s\n',\
    'Action\n',\
    'Drama',\
    'Horror\n',\
    'Sci-Fi\n',\
    'Documentary\n',\
    'War\n',\
    'Adventure\n',\
    'Musical',\
    'Mystery\n',\
    'Sci-Fi',\
    'Horror',\
    'Musical\n',\
    'Crime\n',\
    'Mystery',\
    'Romance',\
    'Thriller',\
    'Film-Noir',\
    'Western\n',\
    'Fantasy',\
    'War',\
    'Documentary',\
    'Animation\n',\
    'Film-Noir\n']

types_modified_in_database = ['Animation',\
    'Children', \
    'Comedy',\
    'Adventure',\
    'Fantasy',\
    'Comedy',\
    'Romance',\
    'Drama',\
    'Action',\
    'Crime',\
    'Thriller',\
    'Children',\
    'Action',\
    'Drama',\
    'Horror',\
    'Sci-Fi',\
    'Documentary',\
    'War',\
    'Adventure',\
    'Musical',\
    'Mystery',\
    'Sci-Fi',\
    'Horror',\
    'Musical',\
    'Crime',\
    'Mystery',\
    'Romance',\
    'Thriller',\
    'Film-Noir',\
    'Western',\
    'Fantasy',\
    'War',\
    'Documentary',\
    'Animation',\
    'Film-Noir']
reverse_types_in_database = {}
types_in_database_to_types = {}
for index in range(len(types_in_database)):
    reverse_types_in_database[types_modified_in_database[index]] = types_in_database[index]
    types_in_database_to_types[types_in_database[index]] = types_modified_in_database[index]
#服务函数
#注册添加信息

def add_userInfo(userInfo):
    #加入数据库
    conn = pymysql.connect(host=db.databaseAddress, user=db.databaseLoginName, password=db.databasePasswd, database=db.databaseName)
    cur = conn.cursor()
    #gender必须是‘男’或‘女’
    sql1 = "Insert INTO User VALUES({},'{}',{},{},'{}','{}') ".format(\
        userInfo[0],userInfo[1],userInfo[2],\
            userInfo[3],userInfo[4],userInfo[5])
    sql2 = "CREATE OR REPLACE VIEW rates AS SELECT MovieID, AVG(Rating) as rating FROM review GROUP BY MovieID"
    try:
        print(sql1)
        cur.execute(sql1)
        print('test1')
        print(sql2)
        cur.execute(sql2)
        print('test2')
        for type in userInfo[6]:
            original_type = reverse_types_in_database[type]
            sql3 = "CREATE OR REPLACE VIEW movie_{} as SELECT MovieID from movie_genre WHERE genre = '{}'".format(type,original_type)
            cur.execute(sql3)
            print('test3')
            sql4 = "SELECT MovieID from movie_{} natural left join rates ORDER BY rating DESC".format(type)
            cur.execute(sql4)
            print('test4')
            data = cur.fetchone()
            date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            sql5 = "INSERT INTO watch_history VALUES({},{},'{}')".format(userInfo[0],data[0],date)
            print(sql5)
            cur.execute(sql5)
            print('test5')
        print('test6')
    except Exception:
        conn.rollback()
        print('添加数据失败')
        return 'failed'
    else:
        conn.commit()
    cur.close()
    conn.close()
    return 'success'

#验证用户是否存在/用户密码是否正确
def validate_userInfo(userInfo):
    #从数据库中按照userInfo[0]取出对应passwd
    conn = pymysql.connect(host=db.databaseAddress, user=db.databaseLoginName, password=db.databasePasswd, database=db.databaseName)
    cur = conn.cursor()
    sql = "SELECT password FROM User where UserID = {}".format(userInfo[0])
    cur.execute(sql)
    data = cur.fetchone()
    print('data:',data)
    if data == None:
        #数据库中没这个人
        return 'Not exist'
    if userInfo[1] == data[0]:
        cur.close()
        conn.close()
        return 'success'
    else:
        cur.close()
        conn.close()
        return 'fail'


#根据用户id获得片单
def get_list_from_dataset(socket,userName):
    userName = int(userName)
    movies = rc.recommend_your_favorite_movie(userName, top_k=60)
    conn = pymysql.connect(host=db.databaseAddress, user=db.databaseLoginName, password=db.databasePasswd, database=db.databaseName)
    cur = conn.cursor()
    result = []
    sql1 = "CREATE OR REPLACE VIEW rates AS SELECT MovieID, AVG(Rating) as rating FROM review GROUP BY MovieID"
    #try:
    cur.execute(sql1)
    for movieID in movies:
        try:
            print(movieID)
            sql2 = "SELECT Title, case when rating is null then 0 else rating END FROM movie natural left join rates WHERE movieID = {} ".format(movieID)
            cur.execute(sql2)
            data1 = cur.fetchone()
            print(data1)
            sql3 = "SELECT case when Genre is null then 'Comedy\n' else Genre END FROM movie natural join movie_genre natural left join rates WHERE movieID = {} ".format(movieID)
            cur.execute(sql3)
            data2 = cur.fetchall()
            print(data2)
            data2 = [i[0] for i in data2]
            if data1[0] != None and data1[1] != None and data2:
                #这里的data2改成,分隔的字符串！
                temp_str = types_in_database_to_types[data2[0]]
                for index in range(1,len(data2)):
                    temp_str = temp_str + ',' + types_in_database_to_types[data2[index]]
                result.append({"title":data1[0],"genre":temp_str,"rate":float(data1[1])})
        except Exception:
            pass
    #except Exception:
    #    conn.rollback()
    #    print('添加数据失败')
    else:
        conn.commit()
    cur.close()
    try:
        conn.close()
    except Exception:
        pass
    try:
        if result:
            string = json.dumps(result)
            socket.send(string)
        else:
            socket.send('nothing')
    except WebSocketError:
        pass #占位置的空操作
    #executor.submit(add_to_history,userName,movies)
    add_to_history(userName,movies)


    '''
    #先根据userName查找出以往的历史
    if '有历史':
        #按照历史获得推荐
        return 'recommend content'
    else:
        #按照没有历史获得推荐
        return 'recommend content'
    '''

def add_to_history(userName,movies):
    conn = pymysql.connect(host=db.databaseAddress, user=db.databaseLoginName, password=db.databasePasswd, database=db.databaseName)
    cur = conn.cursor()
    date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    for movie in movies:
        sql = "INSERT INTO watch_history VALUES({},{},'{}')".format(userName,movie,date)
        cur.execute(sql)
    

#已被废弃
#def get_list_from_dataset_with_query(userName,query):
'''
#先根据userName查找出以往的历史
if '有历史':
    #按照历史、query获得推荐
    #开一个线程，把这次的搜索加到历史中
    return 'recommend content'
else:
    #按照没有历史、只有query获得推荐
    #开一个线程，把这次的搜索加到历史中
    return 'recommend content'
'''