from atmclass import Mysql
from atmclass import DBChange
from atmclass import Getch_Windows
from atmclass import Statement
import time, os, sys, msvcrt


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

## 密码修改进程
## 密码修改写入，直接调用Change类，避免重复代码
def passwd_change():
    while True:
        change_passwd_user = login()
        if change_passwd_user != None:
            new_passwd1 = pwd_input('\n请输入要修改的新密码：')
            new_passwd2 = pwd_input('请再次输入新密码：')
            if new_passwd1 == new_passwd2:
                result = DBChange().pw(change_passwd_user.query_id(), new_passwd2)
                if result:
                    Statement().eventappend(change_passwd_user.query_id(), '修改密码成功')
                else:
                    Statement().eventappend(change_passwd_user.query_id(), '修改密码失败')
                break
            else:
                print('两次输入的密码不一致，请重新输入~')
                continue

# 注册进程，新注册用户余额为0
## 返回一个Add_User对象
def register() -> str:
    import random
    select = '''    select account from userinfo    '''
    all_id = [i['account'] for i in Mysql().select_allback(select)]
    flag_loop, flag_passwd, flag_phone, flag_success = True, False, False, False
    while flag_loop:
        id = str(random.randint(10000, 99999))
        if id not in all_id:
            pass
        else:
            continue
        while True:
            username = input('请输入注册者的姓名（输入exit退回主界面）：')
            if username == '':
                print('\n请输入正确的姓名！\n')
                continue
            elif username == 'exit':
                flag_loop = False
                break
            else:
                flag_passwd = True
                break
        while flag_passwd:
            passwd_first = encrypt(pwd_input('请输入新密码：'))  # 调用密码加密输入函数，输入后md5加密储存
            if passwd_first == '':
                print('\n请输入密码...\n')
                continue
            elif len(passwd_first) < 6:
                print('\n请输入6位密码！\n')
            else:
                passwd_second = encrypt(pwd_input('请再次确认密码：')) # 密码二次确认
                if passwd_first == passwd_second:
                    flag_phone = True
                    break
                else:
                    print('两次密码输入不一致，请重新输入：')
                    continue
        while flag_phone:
            phone = input('请输入注册者的11位手机号（输入exit退回主界面）：')
            if len(phone) == 11 and phone.startswith('1'):
                flag_success = True
                break
            elif phone == 'exit':
                flag_loop = False
                break
            else:
                print('输入的手机号错误，请重新输入')
                continue
        if flag_success:
            n = DBChange().register(id, username, passwd_second, phone)
            if n:
                print(f'您申请的账户id为{id}，3s后返回，请牢记......\n')
                # return Add_User(reg_dic)  # 用新的用户名、密码，构造并返回一个对象
                return username
            else:
                print('注册失败，请重新注册......')
                break
        break

# 登录进程，返回一个Add_User对象或空
def login(super_user: str = 'default') -> str:
    if super_user == 'default':
        usrtime, pwdtime = 3, 3 # 账户名最多3次尝试，密码最多3次尝试
        while usrtime:  # 账户名输入3次判定
            account = input('请输入5位数账户id（输入exit退回主界面）：')  #提示输入账号
            if account == 'exit':
                pwdtime = 0
                usrtime = 0
            elif account.isalnum(): # 判断输入是否存在于用户名列表中
                select = '''    select * from userinfo where account = "%s";  '''
                info = Mysql().select_oneback(select % account)
                usrtime = 0 # 输入正确，不再循环输入用户名，取消下次循环
            else:
                print('找不到该用户信息，请重新输入：')
                usrtime -= 1
                if usrtime == 0:
                    print('用户名输入错误三次，程序终止！') 
                    pwdtime = 0     # 不再进入输入密码程序
        while pwdtime:  #密码输入3次判定
                    pwd = encrypt(pwd_input('请输入密码：'))     # 提示输入密码
                    if pwd == info['passwd']: # 用户名对应密码检测
                        print('正在核对账户信息，请稍后......')
                        time.sleep(2)
                        print('登录成功，欢迎你，%s\n' % account)
                        Statement().eventappend(account, '登录成功')
                        # pwdtime = 0 # 登录成功，取消下次密码输入循环
                        return account # 登录成功，返回登录的对象
                    else:
                        pwdtime -= 1    # 密码循环输入计数器减一
                        if pwdtime == 0:    # 密码输入计数器为0时，退出login进程
                            print('密码输入错误达到三次，程序终止！')
                            Statement().eventappend(info['account'], '尝试登录失败，密码输入错误达到三次')
                            return # 三次密码输入错误，登录失败，不返回登录的对象
                        count = input('密码错误，是否重新输入？（输入 0退出，其他任意键继续：）')  #  提供用户提前退卡功能
                        if count != '0':
                            pass
                        else:
                            print('程序已退出！')
                            return # 用户选择退出登录进程，不返回登录对象
    elif super_user == 'super':
        super_user_name = input('请输入super用户名：')
        super_user_passwd = pwd_input('请输入super密码：')
        if super_user_name == 'admin' and encrypt(super_user_passwd) == '213f2807cf903ce63407c11d8f0f57fe':   # 
            print('\n超级用户登录，欢迎您，superuser！')
            return 1
    else:
        print('恭喜您，发现新大陆！但是你输入的参数有误。')

def query_balance(account: str) -> str:
    select = '''    select balance from userinfo where account = "%s"    '''
    user = Mysql().select_oneback(select % account)
    Statement().eventappend(account, '查询账户余额')
    return print('用户名：%s，余额为：%.2f' % (account, user['balance'] / 1000))
def deposits(account: str) -> None:
    while True:
        try:
            save = float(input('请输入要存款的金额（任意字符退回上一级）：'))
            if save > 10000:
                print('单笔存款金额不能大于10000，请重新输入！')
                continue
            elif save % 100 == 0 and save != 0:
                print('正在存入，请稍后......')
                time.sleep(3)
                select = '''    select account, balance from userinfo where account = "%s"    '''
                user_info = Mysql().select_oneback(select % account)
                result = DBChange().bal(account, user_info['balance'] + save * 1000)
                if result:
                    user_info_check = Mysql().select_oneback(select % account)
                    print('账号：%s\t存款成功，已存入%.2f，余额%.2f\n' % (account, save, user_info_check['balance'] / 1000))     #控制精度
                    Statement().balappend(account, '存入', save, user_info_check['balance'])
                else:
                    Statement().balerror(account, '存入失败')
                break
            else:
                print('请输入100的倍数！')
        except ValueError:
            print('请重新输入有效数字！\n')
            continue
def withdraw(account: str) -> None:
    while True:
        try:
            take = float(input('请输入要取款的金额（任意字符退回上一级）：'))
            if take > 2000:
                print('单笔取款金额不能大于2000，请重新输入！')
                continue
            elif take % 100 == 0:
                select = '''    select account, balance from userinfo where account = "%s"    '''
                user_info = Mysql().select_oneback(select % account)
                if take <= user_info['balance']:
                    print('正在取出，请稍后......')
                    time.sleep(3)
                    result = DBChange().bal(account, user_info['balance'] - take * 1000)
                    user_info_check = Mysql().select_oneback(select % account)
                    if result:
                        print('账号：%s\t取款成功，已取出%.2f，余额%.2f\n' % (account, take, user_info_check['balance'] / 1000)) #控制精度
                        Statement().balappend(account, '取出', take, user_info_check['balance'])
                    else:
                        Statement().balerror(account, '取出失败')
                    break
                else:
                    print('\n余额不足，无法完成取款，请重新输入金额！\n')
                    time.sleep(3)
                    continue
            else:
                print('请输入100的倍数！\n')
                continue
        except ValueError:
            print('请重新输入有效数字！\n')
            continue
def trans_balance(account: str) -> None:
    while True:
        trans_account = input('请输入目标账户id（输入exit退回上一级）：')
        if trans_account.isalnum():
            select_target = '''     select account, balance from userinfo where account = "%s";      '''
            target_id_first = Mysql().select_oneback(select_target % trans_account)
            origin_id_first = Mysql().select_oneback(select_target % account)
        else:
            print('您输入的目标账户id有误，请重新输入')
            continue
        if target_id_first != None and trans_account != account:
            try:
                while True:
                    trans_money = float(input('请输入转账金额（任意字符退回上一级）：'))
                    if trans_money <= 0:
                        print('金额输入错误，请重试！')
                        continue
                    elif trans_money > origin_id_first['balance']:
                        print('转出金额超出余额，请重新输入')
                        continue
                    else:
                        ## 原账户金额减少，并写入数据库
                        origin_value = DBChange().bal(account, origin_id_first['balance'] - trans_money * 1000)
                        origin_id_second = Mysql().select_oneback(select_target % account)     ## 查询变更后的用户余额
                        ## 目标账户金额增加，并写入数据库
                        target_value = DBChange().bal(trans_account, target_id_first['balance'] + trans_money * 1000)
                        target_id_second = Mysql().select_oneback(select_target % trans_account)
                        ## 判断返回结果，如果都成功，提示转出成功，并进入日志记录
                        if origin_value and target_value:
                            print('\n正在转出，请等待......')
                            time.sleep(3)
                            print('\n您的账户：%s成功转出到：%s ，金额：%.2f，余额：%.2f\n感谢使用WoniuATM~' % (account,  trans_account, trans_money, origin_id_second['balance'] / 1000 ))
                            Statement().transbal(account, '转出', '目标账户', trans_account, trans_money, origin_id_second['balance'] / 1000)
                            Statement().transbal(trans_account, '转入', '来源账户', account, trans_money, target_id_second['balance'] / 1000)
                            break
                        else:
                            print('\n转账失败，请重试\n')
                            continue
                break
            except:
                print('请输入有效的金额~\n')
                continue
        elif trans_account == 'exit':
            break
        else:
            print('不支持本账户自转或目标账户不存在，请确认后重新输入~')
            continue

def query_journal(account: str) -> None:
    start_time = input('请输入起始年月日（格式YYYY-MM-DD，不输入则直接按回车）：')
    end_time = input('请输入结束年月日（格式YYYY-MM-DD，不输入则直接按回车）：')
    journal_type = input('请输入要查看的记录类型（1：存取款\t2：转账\t3：日志）：')
    if journal_type == '1':
        select = '''select * from (select account, dt, event, type, money, taraccount, curbalance from transrecord where account = "%s" order by dt desc limit 10) as a order by a.dt asc limit 10;'''
    elif journal_type == '2':
        select = '''select * from (select account, dt, event from record where account = "%s" order by dt desc limit 10) as a order by a.dt asc limit 10;'''
    elif journal_type == '3':
        select = '''select * from (select account, dt, event, money, curbalance from log where account = "%s" order by dt desc limit 10) as a order by a.dt asc limit 10;'''
    else:
        print('输入错误，请重试！')
        return False
    journal = Mysql().select_allback(select % account)
    if start_time == '' and end_time == '':     # 不输入默认按时间显示最后10行
        # *item = [journal]
        print('')
        for i in journal:
            for j in i:
                if i[j] == None:
                    print(' ',end='\t')
                else:
                    print('%s：%s' % (j, str(i[j])), end='\t')
                # print('%s\t%s\t%s\t%.2f\t%s\t%.2f' % (account, i['dt'], i['event'], str(i['type']), str(i['money']), str(i['targetaccount']), str(i['curbalance'])))
            print('\n')
    elif start_time == '' and end_time != '':       # 输入起始时间，不输入结束时间，默认结束到当日
        for i in journal:
             
            for j in i:
                if i[j] == None:
                    print(' ',end='\t')
                else:
                    print('%s：%s' % (j, str(i[j])), end='\t')
    elif start_time != '' and end_time == '':       # 输入结束时间，不输入起始时间，默认最开始到结束时间所有日志
        pass
    elif start_time == '' and end_time == '':
        pass
    else:
        print('您输入的时间范围内，没有可以显示的内容......')

def menu(account: str) -> None:
    os.system('cls')
    print('*' * 20 + ' 恭喜登录蜗牛银行 ' + '*' * 20)
    while True: # 直接进入循环，注意每个结果后添加break退出循环
        print('\n' + '*' * 21 + ' 请选择操作菜单 ' + '*' * 21)
        print('*' * 0 + ' 1：查询  2：存款 3：取款 4：转账 5：日志 6：返回 7：退出 ' + '*' * 0 + '\n')
        choice = input('请输入你的操作选项：')
        if choice == '1':
            query_balance(account) # 调用查询余额方法
        elif choice == '2':
            deposits(account)
        elif choice == '3':
            withdraw(account)
        elif choice == '4':
            trans_balance(account)
        elif choice == '5':
            result = query_journal(account)
            if result == False:
                continue
        elif choice == '6':
            break
        elif choice == '7':   # 用户选择退出系统
            return 'exit_safe'
        else:
            return 'exit_unsafe'    # 先随便返回一个值占位，以后说不定有其他内容





