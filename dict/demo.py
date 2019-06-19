"""
客户端界面简述
"""

while True:
    print("第一界面")
    cmd = input(">>>:")
    if cmd == "go":
        while True:
            print("第二界面")
            cmd = input(">>>:")
            if cmd == "out":
                break
