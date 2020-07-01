## 定义用户类
class Account:
    def __init__(self, idnum: int,name: str, passwd: str, balance: float):
        self.idnum = idnum
        self.name = name
        self.passwd = passwd
        self.balance = float(balance)
    def take_money(self, money: float) -> None:
        self.balance = (self.balance / 1000 - float(money)) * 1000
    def save_money(self, money: float) -> None:
        self.balance = (self.balance / 1000 + float(money)) * 1000
    def query_balance(self) -> float:
        return (self.balance) / 1000
    def query_id(self) -> int:
        return self.idnum
    def query_name(self) -> str:
        return self.name
    def query_passwd(self) -> str:
        return self.passwd
    def query_dict(self) -> dict:
        dic = {}
        dic[self.idnum] = [self.name, self.passwd, self.balance]
        return dic
    def __str__(self) -> str:  # 当需要对象作为str类型时，将返回以下字符串
        return '账户号：' + str(self.idnum) + '，' + '用户名：' + self.name  + '，' + '密码：***'  + '，' + '余额：' + str(self.balance)
# 使用Add_User进行列表的对象构造
## Python不支持重载构造函数
class Add_User(Account):
    def __init__(self, dic: dict):
        for key, value in dic.items():
            pass
        super().__init__(key, value[0], value[1], value[2])

## 业务流水
class Statement:
    def __init__(self, spath: str):
        import os
        self.spath = spath
        if 'statement' in os.listdir(os.path.dirname(__file__)):
            pass
        else:
            os.mkdir(self.spath)
    ## 密码修改日志
    def pwappend(self, account: str, result: str) -> None:
        import time
        with open(self.spath + account + '.dat', 'a', encoding='utf8') as pwf:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            pwf.write(f'账号：{account}\t{time_str}\t{result}\n')
    ## 余额变更日志
    def balappend(self, account: str, operation: str, balchange: str, balance: str, sfile: str) -> None:
        import time
        if operation == '存入：':
            symb = '+'
        elif operation == '取出：':
            symb = '-'
        with open(self.spath + account + '.dat', 'a', encoding='utf8') as pwf:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            pwf.write(f'账号：{account}\t{time_str}\t{operation}{symb}{balchange}元\t当前余额：{balance}\n')
    def transbal(self, account: str, target_account: str, operation: str, trans_type: str, trans_balance: str, balance: str):
        import time
        with open(self.spath + account + '.dat', 'a', encoding='utf8') as pwf:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            pwf.write(f'账号：{account}\t{time_str}\t{operation}{trans_balance}元\t{trans_type}{target_account}\t当前余额：{balance}\n')
    ## 余额变更错误日志
    def balerror(self, account: str, operation: str):
        import time
        with open(self.spath + account + '.dat', 'a', encoding='utf8') as pwf:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            pwf.write(f'账号：{account}\t{time_str}\t{operation}失败\n')
        

## 文件读取，将字典分别转换为不同用途的列表
class Dict2List:
    def __init__(self):
        pass
    #将所有对象按info的顺序添加到容器中
    def user(self, info: dict) -> list:
        user = []
        dic = {}
        for i in info: 
            dic[i] = info[i]
            user.append(Add_User(dic))
        return user
    # 获取账户ID，添加到用户名列表：
    def idnum(self, info: dict) -> list:
        idnum = [i for i in info]
        return idnum
    # 获取用户姓名，添加到用户名列表：
    def name(self, info: dict) -> list:
        name = [self.user(info)[i].query_name() for i in range(len(info))]
        return name
    # 获取密码，添加到密码列表：
    def passwd(self, info: dict) -> list:
        passwd = [self.user(info)[i].query_passwd() for i in range(len(info))]
        return passwd
    # 获取余额，添加到余额列表：
    def balance(self, info: dict) -> list:
        balance = [self.user(info)[i].query_balance() for i in range(len(info))]
        return balance

## json配置文件读取、写入类方法
class Jsonoperate:
    '''
    传入文件地址，调用jread()方法读取json文件，返回全量字典
    调用jwrite()方法将字典写入到json文件
    '''
    def __init__(self, jpath):
        self.jpath = jpath
    def jread(self) -> dict:
        import json, time
        from pathlib import Path
        cwd = Path.cwd()
        jsonfile = Path.joinpath(cwd, 'userinfo.json')
        if jsonfile.exists() and jsonfile.stat().st_size > 100:
            jsondict = json.load(open(self.jpath, 'r', encoding='utf8'))
            return jsondict
        else:
            print('userinfo.json文件错误，正在恢复出厂配置......')
            time.sleep(3)
            default_info = {'10001': ['admin', '0192023a7bbd73250516f069df18b500', 5000000.00], 
                                '10002': ['黄俊', 'e10adc3949ba59abbe56e057f20f883e', 1000000.00], 
                                '10003': ['guest', 'fcf41657f02f88137a1bcf068a32c0a3', 500000.00]}
            self.jwrite(default_info)
            return default_info
    def jwrite(self, info: dict):
        import json
        json.dump(info, open(self.jpath, 'w', encoding='utf8'), ensure_ascii=False, indent=1)

## 密码或余额变动类方法
class Change:
    def __init__(self, jpath: str): ## 需传入用户信息文件地址接口
        self.jpath = jpath
    ## 密码修改写入
    def pw(self, user_id: str, new_passwd: str) -> None: 
        from atmfunction import encrypt
        try:
            info = Jsonoperate(self.jpath).jread()
            check = [i for i in info]
            for i in check:
                if user_id == i:
                    info[i][1] = encrypt(new_passwd)
            print(info)
            Jsonoperate(self.jpath).jwrite(info)
            info_check = Jsonoperate(self.jpath).jread()    ## 检查密码是否真实写入
            if info_check[user_id][1] == encrypt(new_passwd):
                print('修改密码成功，请重新登录！')
                return 'success'
            else:
                print('数据写入错误，请稍后再试......')
                return 'failure'
        except:
            print('数据写入错误，请联系黄俊......\n')
    ## 余额修改写入
    def bal(self, user_id: str, balance: float) -> None:
        try:
            info = Jsonoperate(self.jpath).jread()
            check = [i for i in info]
            for i in range(len(info)):
                if user_id == check[i]:
                    info[check[i]][2] = balance
            Jsonoperate(self.jpath).jwrite(info)
            if info[user_id][2] == balance:
                return 'success'
            else:
                return 'failure'
        except:
            print('数据写入错误，请联系黄俊......\n')
    def bal_check(self, account: str, right_value: str) -> bool: 
        '''
        left_value为文件中读取的值
        right_value为需要对比的值
        '''
        left_value = Jsonoperate(self.jpath).jread()[account][2]
        if left_value == right_value:
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




