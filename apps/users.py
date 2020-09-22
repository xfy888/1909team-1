# 用户模块
from flask import Blueprint,render_template,request,session
from .models import  Reader,ReaderGrade # 项目中一定使用一下模型类！ 否则无法迁移！
from  config import  db
users = Blueprint('users',__name__)

@users.route('/')
def index():
    return render_template('/index.html')



@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method =='GET':
        return render_template('/register.html')
    else:
        # 实现注册功能， 获取表单数据，增加
        grade = request.form.get('reader_grade')
        name = request.form.get('reader_name')
        pwd = request.form.get('reader_pwd')
        phone = request.form.get('reader_phone')
        print(f'级别:{grade},名字{name},密码：{pwd},电话：{phone}')
        reader = Reader(reader_name=name,reader_pass=pwd,phone=phone,grand_id=grade,is_activate=0) #默认未激活！
        db.session.add(reader)
        db.session.commit()
        return render_template('/index.html')



@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('index.html')
    else:
        # 1. 获取资料
        role_id= request.form.get('role_id')
        user_name = request.form.get('user_name')
        user_pwd = request.form.get('user_pwd')
        print(f'roleid:{role_id},name:{user_name},pwd:{user_pwd}')

        # 2.判断角色
        print(type(role_id))
        if role_id =="1":
            #读者用户名和密码
            reader = Reader.query.filter_by(reader_name=user_name,reader_pass=user_pwd).all()
            print(reader)
            #print(f'名字:{reader.reader_name},电话:{reader.phone}')
            #用户登录后，用户资料写入session缓存中，方便在任意页面使用！
            if len(reader)==0:
                return render_template('index.html', msg='用户名或密码错误！')
            else:
                # 用户登录成功,用户对象保存到session中,方便其他方法调用！
                session["user_id"] = reader[0].id
                session["user_name"] = reader[0].reader_name
                if reader[0].is_activate == 0:
                    msg = '请修改密码！'

                return render_template('reader.html', msg=reader[0].reader_name)


        elif role_id=="2":
            #图书管理员
            return render_template('bookManager.html')
        else:
            # 系统管理员
            return render_template('systemManager.html')


@users.route('/userinfo', methods=['GET'])
def user_info():
    '''根据id，或用户名查询，展示用户资料'''
    id = session.get('user_id')
    print(f'用户id:{id}')
    reader = Reader.query.filter_by(id=id).all()
    if len(reader)>0:
        return render_template('userinfo.html',reader=reader[0])
    else:
        return render_template('reader.html',msg='查询无结果！')


