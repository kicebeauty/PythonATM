from atmclass import Mysql


select = '''     select * from userinfo;      '''
allinfo = Mysql().select_allback(select)
for i in allinfo:
    print(i)





