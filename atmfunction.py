from atmclass import Add_User
from atmclass import Jsonoperate
from atmclass import Change
from atmclass import Getch_Windows
from atmclass import Dict2List
from atmclass import Statement
import time, os, sys, msvcrt

## 定义用户信息配置文件
filename = r'./userinfo.json'
spath = r'./statement/'


## 密码输入加密算法，利用msvcrt模块，同时将输入的内容单个append到目标字符串，并以*显示密码
def pwd_input(print_str: str) -> str:
    try:
        return Getch_Windows().pwinput(print_str)
    except:
        print('无法加载星号加密组件，将使用默认输入方式：')
        return Getch_Windows().default_input(print_str)
## md5加密函数
def encrypt(passwd: str) -> str:
    import hashlib
    md = hashlib.md5()
    md.update(passwd.encode())
    return md.hexdigest()
#将所有对象按info的顺序添加到容器中
def user_docker(info: dict) -> list:
    return Dict2List().user(info)
# 获取账户ID，添加到用户名列表：
def id_docker(info: dict) -> list:
    return Dict2List().idnum(info)
# 获取用户姓名，添加到用户名列表：
def name_docker(info: dict) -> list:
    return Dict2List().name(info)
# 获取密码，添加到密码列表：
def passwd_docker(info: dict) -> list:
    return Dict2List().passwd(info)
# 获取余额，添加到余额列表：
def balance_docker(info: dict) -> list:
    return Dict2List().balance(info)

## 密码修改进程
## 密码修改写入，直接调用Change类，避免重复代码
def passwd_change():
    while True:
        change_passwd_user = login()
        if change_passwd_user != None:
            new_passwd1 = pwd_input('\n请输入要修改的新密码：')
            new_passwd2 = pwd_input('请再次输入新密码：')
            if new_passwd1 == new_passwd2:
                result = Change(filename).pw(change_passwd_user.query_id(), new_passwd2)
                if result == 'success':
                    Statement(spath).pwappend(change_passwd_user.query_id(), '修改密码成功')
                elif result == 'failure':
                    Statement(spath).pwappend(change_passwd_user.query_id(), '修改密码失败')
                break
            else:
                print('两次输入的密码不一致，请重新输入~')
                continue

# 注册进程，新注册用户余额为0
## 返回一个Add_User对象
def register() -> object:
    import random
    info = Jsonoperate(filename).jread()
    while True:
        id = str(random.randint(10000, 99999))
        if id not in id_docker(info):
            pass
        else:
            continue
        while True:
            username = input('请输入注册者的姓名（输入exit退回主界面）：')
            if username == '':
                print('\n请输入正确的姓名！\n')
                continue
            elif username == 'exit':
                break
            while True:
                passwd_first = pwd_input('请输入六位数新密码：')  # 调用密码加密输入函数，输入后base64加密储存
                reg_dic = {}
                if passwd_first == '':
                    print('\n请输入密码...\n')
                    continue
                elif len(passwd_first) < 6:
                    print('\n请输入6位密码！\n')
                else:
                    passwd_second = pwd_input('请再次确认输入密码：') # 密码二次确认
                    if passwd_first == passwd_second:
                        passwd = encrypt(passwd_second)
                        reg_dic[id] = [username, passwd, 0.00]
                        info[id] = [username, passwd, 0.00]
                        Jsonoperate(filename).jwrite(info)
                        if id in Jsonoperate(filename).jread():     ## 判断注册账号是否写入文件
                            print(f'您申请的账户id为{id}，3s后返回，请牢记......\n')
                            return Add_User(reg_dic)  # 用新的用户名、密码，构造并返回一个对象
                        else:
                            print('注册失败，请重新注册......')
                            break
                    else:
                        print('两次密码输入不一致，请重新输入：')
                        continue
            break

# 登录进程，返回一个Add_User对象或空
def login(super_user: str = 'default') -> object:
    info = Jsonoperate(filename).jread()
    id_info = id_docker(info)
    passwd_info = passwd_docker(info)
    user_info = user_docker(info)
    if super_user == 'default':
        usrtime, pwdtime = 3, 3 # 账户名最多3次尝试，密码最多3次尝试
        while usrtime:  # 账户名输入3次判定
            user = input('请输入5位数账户号（输入exit退回主界面）：')  #提示输入密码
            if user == 'exit':
                break
            elif user in id_info: # 判断输入是否存在于用户名列表中
                usrtime = 0 # 输入正确，不再循环输入用户名，取消下次循环
                while pwdtime:  #密码输入3次判定
                    pwd = pwd_input('请输入密码：')
                    # 由于写入算法将 ’ 单引号替换了，此处也许替换
                    if encrypt(pwd) == passwd_info[id_info.index(user)]: # 用户名对应密码检测
                        print('正在核对账户信息，请稍后......')
                        time.sleep(2)
                        print('登录成功，欢迎你，%s\n' % user)
                        Statement(spath).pwappend(user_info[id_info.index(user)].query_id(), '登录成功')
                        pwdtime = 0 # 登录成功，取消下次密码输入循环
                        return user_info[id_info.index(user)] # 登录成功，返回登录的对象
                    else:
                        pwdtime -= 1    # 密码循环输入计数器减一
                        if pwdtime == 0:    # 密码输入计数器为0时，退出login进程
                            print('密码输入错误达到三次，程序终止！')
                            Statement(spath).pwappend(user_info[id_info.index(user)].query_id(), '尝试登录失败，密码输入错误达到三次')
                            return # 三次密码输入错误，登录失败，不返回登录的对象
                        count = input('密码错误，是否重新输入？（输入 1 以继续，其他任意键退出：）')  #  提供用户提前退卡功能
                        if count == '1':
                            pass
                        else:
                            print('程序已退出！')
                            return # 用户选择退出登录进程，不返回登录对象
            else:
                print('找不到该用户信息，请重新输入：')
                usrtime -= 1
                if usrtime == 0:
                    print('用户名输入错误三次，程序终止！') 
                    return # 用户名3次输入错误，登录失败，不返回登录的对象
    elif super_user == 'super':
        super_user_name = input('请输入super用户名：')
        super_user_passwd = pwd_input('请输入super密码：')
        if super_user_name == 'admin' and encrypt(super_user_passwd) == '213f2807cf903ce63407c11d8f0f57fe':   # 无聊写的，没有加密，存在super账户泄露风险
            print('\n超级用户登录，欢迎您，superuser！')
            return 1
    else:
        print('恭喜您，发现新大陆！但是你输入的参数有误。')
        time.sleep(3)

def menu_1(user_obj: object) -> str:
    Statement(spath).pwappend(user_obj.query_id(), '查询账户余额')
    return f'用户名：{user_obj.query_name()}，余额为：{user_obj.query_balance():.2f}'
def menu_2(user_obj: object) -> None:
    while True:
        save = input('请输入要存款的金额（输入exit返回主菜单）：')
        try:
            if save == 'exit':
                break
            elif float(save) > 10000:
                print('单笔存款金额不能大于10000，请重新输入！')
                continue
            elif float(save) % 100 == 0:
                user_obj.save_money(save)    # 调用存钱方法
                print('正在存入，请稍后......')
                time.sleep(3)
                Change(filename).bal(user_obj.query_id(), user_obj.query_balance() * 1000)
                print('账号：%s\t存款成功，已存入%.2f，余额%.2f\n' % (user_obj.query_id(), float(save), user_obj.query_balance()))     #控制精度
                if user_obj.query_balance() * 1000 == Jsonoperate(filename).jread()[user_obj.query_id()][2]:
                    Statement(spath).balappend(user_obj.query_id(), '存入：', save, str(user_obj.query_balance()), spath)
                else:
                    Statement(spath).balerror(user_obj.query_id(),'存入')
                break
            else:
                print('请输入100的倍数！')
        except ValueError:
            print('请重新输入有效数字！\n')
            continue
def menu_3(user_obj) -> None:
    while True:
        take = input('请输入要取款的金额（输入exit返回主菜单）：')
        try:
            if take == 'exit':
                break
            elif float(take) > 2000:
                print('单笔取款金额不能大于2000，请重新输入！')
                continue
            elif float(take) % 100 == 0:
                if float(take) <= user_obj.query_balance():
                    user_obj.take_money(take)    # 调用取钱方法
                    print('正在取出，请稍后......')
                    time.sleep(3)
                    Change(filename).bal(user_obj.query_id(), user_obj.query_balance() * 1000)
                    print('账号：%s\t取款成功，已取出%.2f，余额%.2f\n' % (user_obj.query_id(), float(take), user_obj.query_balance())) #控制精度
                    if user_obj.query_balance() * 1000 == Jsonoperate(filename).jread()[user_obj.query_id()][2]:
                        Statement(spath).balappend(user_obj.query_id(), '取出：', take, str(user_obj.query_balance()), spath)
                    else:
                        Statement(spath).balerror(user_obj.query_id(),'取出')
                    break
                else:
                    print('\n余额不足，无法完成取款，请重新输入金额！\n')
                    time.sleep(3)
            else:
                print('请输入100的倍数！\n')
                continue
        except ValueError:
            print('请重新输入有效数字！\n')
            continue
def menu_4(user_obj: object) -> None:
    while True:
        trans_account = input('请输入目标账户号（输入exit退回上一级）：')
        allinfo = Jsonoperate(filename).jread()
        if trans_account in allinfo and trans_account != user_obj.query_id():
            try:
                while True:
                    trans_money = float(input('请输入转账金额：'))
                    if trans_money <= 0:
                        print('金额输入错误，请重试！')
                        continue
                    else:
                        user_obj.take_money(trans_money)
                        allinfo[user_obj.query_id()][2] = user_obj.query_balance() * 1000
                        allinfo[trans_account][2] += trans_money * 1000
                        Jsonoperate(filename).jwrite(allinfo)
                        print('\n正在转出，请等待......\n')
                        time.sleep(3)
                        if Change(filename).bal_check(user_obj.query_id(), user_obj.query_balance() * 1000) and Change(filename).bal_check(trans_account, allinfo[trans_account][2]):
                            print(f'\n您的账户 {user_obj.query_id()} 成功转出到 {trans_account} ，金额：{trans_money}，余额：{user_obj.query_balance()}\n感谢使用WoniuATM~')
                            Statement(spath).transbal(user_obj.query_id(), trans_account, '转出：', '目标账户：', trans_money, user_obj.query_balance())
                            Statement(spath).transbal(trans_account, user_obj.query_id(), '转入：', '来源账户：',trans_money, allinfo[trans_account][2] / 1000)
                        else:
                            print('转账失败，ErrorCode: File cannot be read...')
                        break
                break
            except:
                print('请输入有效的金额~\n')
                continue
        elif trans_account == 'exit':
            break
        else:
            print('不支持本账户自转或目标账户不存在，请确认后重新输入~')
            continue


def menu(user_obj: object) -> None:
    os.system('cls')
    print('*' * 20 + ' 恭喜登录蜗牛银行 ' + '*' * 20)
    while True: # 直接进入循环，注意每个结果后添加break退出循环
        print('\n' + '*' * 21 + ' 请选择操作菜单 ' + '*' * 21)
        print('*' * 0 + ' 1：查询  2：存款 3：取款 4：转账 5：日志 6：返回 7：退出 ' + '*' * 0 + '\n')
        choice = input('请输入你的操作选项：')
        if choice == '1':
            print(menu_1(user_obj)) # 调用查询余额方法
        elif choice == '2':
            menu_2(user_obj)
        elif choice == '3':
            menu_3(user_obj)
        elif choice == '4':
            menu_4(user_obj)
        elif choice == '5':
            with open(spath + user_obj.query_id() + '.dat', 'r', encoding='utf8') as f:
                journal = f.readlines()
                print(''.join(journal))
        elif choice == '6':
            break
        elif choice == '7':   # 用户选择退出系统
            return 'exit_safe'
        else:
            return 'exit_unsafe'    # 先随便返回一个值占位，以后说不定有其他内容




