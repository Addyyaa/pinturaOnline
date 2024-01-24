import time

def print_after_previous_line(text):
    # 使用 ANSI 转义码清除光标位置到行尾的内容
    print('\033[K' + text)

# 示例

    # 在之前的打印信息后面输出
print('Hello, World!')
for i in range(4):
    print_after_previous_line('Hello, World!')
    time.sleep(1)

