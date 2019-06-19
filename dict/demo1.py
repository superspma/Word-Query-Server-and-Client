import getpass  # 将输入隐藏  默认Password:
import hashlib  # 转换加密

pwd = getpass.getpass()
print(pwd)

# 生成hash对象
# hash = hashlib.md5()  # 生成对象

# 算法加盐
hash = hashlib.md5(("*#06l_".encode()))
hash.update(pwd.encode())  # 算法加密
pwd = hash.hexdigest()  # 获取加密后的密码
print(pwd)

# pwd = getpass.getpass("PW:")
# print(pwd)
