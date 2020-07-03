## 业务流水
class Statement:
    def __init__(self):
        pass
    ## 事件日志，传入用户id和
    def eventappend(self, user_id: str, event: str) -> bool:
        import time
        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = '''insert into log(account, dt, event) values('%s', '%s', '%s');'''
        n = Mysql().insert_IDback(sql % (user_id, curtime, event))
        if n != 0:
            return True
        else:
            return False
    ## 余额变更日志
    def balappend(self, *args) -> None:
        '''
        参数列表顺序：用户id，事件，变更金额，当前余额
        '''
        import time
        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = '''insert into record(account, dt, event, money, curbalance) values('%s', '%s', '%s', %f, %f);'''
        n = Mysql().insert_IDback(sql % (args[0], curtime, args[1], args[2], args[3]))
        if n != 0:
            return True
        else:
            return False
    def transbal(self, *args):
        '''
        参数列表顺序：账户id，事件名，变更金额，目标/来源，目标账户id，当前余额
        '''
        import time
        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = '''insert into transrecord(account, dt, event, type, taraccount, money, curbalance) values('%s', '%s', '%s', '%s', '%s', %f, %f);'''
        n = Mysql().insert_IDback(sql % (args[0], curtime, args[1], args[2], args[3], args[4], args[5]))
        if n != 0:
            return True
        else:
            return False
    ## 余额变更错误日志
    def balerror(self, user_id: str, event: str) -> bool:
        '''
        参数列表顺序：账户id，变动金额，事件名
        '''
        import time
        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = '''insert into log(account, dt, event) values(%s, %s, %s, %f);'''
        n = Mysql().insert_IDback(sql % (user_id, curtime, event))
        if n != 0:
            return True
        else:
            return False

## 数据库数据更新类
class DBChange:
    def __init__(self):
        pass
    def pw(self, user_id: str, new_passwd: str) -> bool:
        sql = '''update userinfo set passwd = '%s' where account = '%s';'''
        n = Mysql().update(sql % (new_passwd, user_id))
        if n != 0:
            return True
        else:
            return False
    def bal(self, user_id: str, new_balance: str) -> bool:
        sql = '''update userinfo set balance = %f where account = '%s';'''
        n = Mysql().update(sql % (new_balance, user_id))
        if n != 0:
            return True
        else:
            return False
    def register(self, *args) -> bool:
        '''
        参数列表：账户id，用户姓名，密码，手机号
        '''
        sql = '''insert into userinfo(account, name, passwd, phone, balance) values('%s', '%s', '%s', '%s', %f);'''
        n = Mysql().update(sql % (args[0], args[1], args[2], args[3], 0.0))
        if n != 0:
            return True
        else:
            return False

## 定义密码输入加密类
# class Getch:
#     def __init__(self, prompt: str='请输入密码: '):
#         try:
#             self.inmethod = Getch_Windows().pwinput(prompt)
#         except ImportError:
#             self.inmethod = Getch_Linux().pwinput(prompt)
#     def __call__(self):
#         return self.inmethod
## 定义windows中输入类
class Getch_Windows:
    def __init__(self):
        pass
    def pwinput(self, prompt: str = '请输入密码: '):      # 只有按回车键，才会返回实际输入的字符
        import msvcrt, sys
        chars = []
        sys.stdout.write(prompt) # 文字提示用户输入密码
        while True:
            ## getch() 返回的是一个二进制字符，需decode()转换为utf8字符串
            newChar = bytes.decode(msvcrt.getch(), encoding='utf8') # 将用户输入的每一个字符进行操作（每输入一个字符自动确认）
            if newChar in '\r\n':   # 如果是回车键，则返回字符串
                print('')
                return ''.join(chars)   # chars是单个字符列表，此方法将列表转换为一串
            elif newChar ==  '\b':
                if chars:
                    chars.pop() # 按backspace，删除最后一个字符
                    sys.stdout.write('\b \b')   # 显示的字符同样减少一个
            else:
                chars.append(newChar)
                sys.stdout.write('*')   # 将字符显示为*号
    def default_input(self, prompt: str = '请输入密码: '):
        return input(prompt)
## 定义Linux中输入类
# class Getch_Linux:
#     def __init__(self):
#         pass
#     def pwinput(self, prompt: str='请输入密码：'):
#         import termios, sys
#         fd = sys.stdin.fileno()
#         old = termios.tcgetattr(fd)
#         new = termios.tcgetattr(fd)
#         new[3] = new[3] & ~termios.ECHO          # lflags
#         try:
#             termios.tcsetattr(fd, termios.TCSADRAIN, new)
#             passwd = raw_input(prompt)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old)
#         return passwd

class Mysql:
    def __init__(self):
        pass
    ## 创建mysql连接
    def connet(self):
        '''
        创建mysql连接
        '''
        import pymysql
        try:
            connection = pymysql.connect(host = '192.168.13.57', 
                                                        port = 3306,   
                                                        user = 'root', 
                                                        passwd = '123456', 
                                                        db = 'woniuATM', 
                                                        charset = 'utf8', 
                                                        cursorclass = pymysql.cursors.DictCursor)       # cursorclass指定：游标返回的结果以字典形式返回
            cursor = connection.cursor()
        except Exception as e:
            print('数据库连接失败！' + e)
            return False
        finally:
            return cursor, connection
    def select_oneback(self, select: str) -> dict:
        '''
        执行一条select语句，并返回一行结果
        '''
        import pymysql
        try:
            cursor, connection = self.connet()
            cursor.execute(select)
            fetone = cursor.fetchone()
            return fetone
        except:
            return False
        finally:
            cursor.close()
            connection.close()
    ## 执行一条select
    def select_allback(self, select: str) -> dict:
        '''
        执行一条select语句，并返回所有结果
        '''
        import pymysql
        try:
            cursor, connection = self.connet()
            cursor.execute(select)
            fetall = cursor.fetchall()
            return fetall
        except:
            return False
        finally:
            cursor.close()
            connection.close()
    def insert_IDback(self, ins: str) -> int:
        '''
        执行一条insert语句，并返回插入的行号
        '''
        import pymysql
        try:
            cursor, connection = self.connet()
            cursor.execute(ins)
            connection.commit()
            insertid = int(cursor.lastrowid)
            return insertid
        except:
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()
    def update(self, up: str) -> bool:
        '''
        执行一条update语句，返回是否成功
        '''
        import pymysql
        try:
            cursor, connection = self.connet()
            n = cursor.execute(up)
            connection.commit()
            return n
        except:
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()
    def create(self, create: str) -> bool:
        '''
        执行一条create语句，返回是否成功
        '''
        import pymysql
        try:
            cursor, connection = self.connet()
            n = cursor.execute(create)
            connection.commit()
            return n
        except:
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()
    def set_default(self):
        '''
        创建初始用户信息
        '''
        import pymysql
        create_1 = '''
        create table if not exists userinfo(
        id int auto_increment primary key,
        account varchar(5) unique not null,
        name varchar(20) not null,
        passwd varchar(32) not null,
        phone varchar(11) not null,
        balance double not null
        )engine=innodb character set utf8;
        '''
        create_2 = '''
        create table if not exists record(
        id int auto_increment primary key,
        account varchar(5) not null,
        dt datetime not null,
        event varchar(10) not null,
        money double,
        curbalance double
        )engine=innodb character set utf8;
        '''
        create_3 = '''
        create table if not exists transrecord(
        id int auto_increment primary key,
        account varchar(5) not null,
        dt datetime not null,
        event varchar(10) not null,
        type varchar(10),
        taraccount varchar(5),
        money double,
        curbalance double
        )engine=innodb character set utf8;
        '''
        create_4 = '''
        create table if not exists log(
        id int auto_increment primary key,
        account varchar(5) not null,
        dt datetime not null,
        event varchar(10) not null
        )engine=innodb character set utf8;
        '''
        insert_1 = '''
        insert into userinfo(account, name, passwd, phone, balance) values('10001', 'admin', '0192023a7bbd73250516f069df18b500', '13880872992', 5000000.0),
         ('10002', '黄俊', 'e10adc3949ba59abbe56e057f20f883e', '13880872992', 1000000.0),
         ('10003', 'guest', 'fcf41657f02f88137a1bcf068a32c0a3', '13880872992', 500000.0);
        '''
        self.create(create_1)
        self.create(create_2)
        self.create(create_3)
        self.create(create_4)
        self.insert_IDback(insert_1)

if __name__ == "__main__":
    Mysql().set_default()