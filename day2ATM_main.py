#-*- coding:utf8 -*-
# from atmfunction import *
import atmfunction
import os, time
# Method No.3
## 本程序采用面对对象编程

## 主程序块
if __name__ == '__main__':  # 程序主入口
    # 循环判定
    while True:
        print('\n')
        os.system('cls')    # Windows下使用，清除屏幕信息
        # os.system('clear')    # Linux下使用，清除屏幕信息
        print('*' * 20 + ' 欢迎来到WoniuATM ' + '*' * 20)
        print('*' * 21 + ' 请选择操作菜单 ' + '*' * 21)
        print('*' * 7 + ' 1：注册   2：登录    3：退卡   4：修改密码 ' + '*' * 7)
        # global user
        user_exist = False
        first_choice = input('请输入你的操作选项：')
        # 进入注册流程，注册后将更新info表
        if first_choice == '1':
            reg_user = atmfunction.register()
            if reg_user != None:
                print('%s，恭喜你注册成功，请重新登录！' % reg_user)
                time.sleep(3)
                continue
            else:
                print('注册失败，请重试~')
                time.sleep(3)
                continue
        # 进入登录流程
        elif first_choice == '2':
            user = atmfunction.login()
            if user != None:    # 当登录返回对象，则继续，返回None则跳出
                opt = atmfunction.menu(user)
                if opt == 'exit_safe':  # 如果menu()函数返回exit_safe，表示登录成功
                    break   # 跳出menu，回到主菜单
                else:
                    continue
            else:
                continue
                # break
        elif first_choice == '3':
            break
        elif first_choice == '4':
            print('\n请先登录！3s后跳转登录\n')
            time.sleep(3)
            atmfunction.passwd_change()
            time.sleep(3)
        else:   # 高级账户
            super_user = atmfunction.login(first_choice)
            if super_user == 1:
                from atmclass import Mysql
                print('以下是本机注册所有账户信息！')
                for i in Mysql().select_allback('select * from userinfo'):
                    print('账户id：' + i['account'] + '\t姓名：' + i['name'] + '\t电话：' + i['phone'] + '\t余额：' + str(i['balance'] / 1000))
                print('5s后返回主菜单，请及时确认！')
                time.sleep(5)
            else:
                print('你在试什么呢？净瞎整，老老实实登录去......')
                time.sleep(3)

    os.system('cls')
    print('\n已退出程序，欢迎您再次使用WoniuATM~~~\n')

