"""
输出 9*9 乘法口诀表。
分行与列考虑，共9行9列，i控制行，j控制列。
"""

for i in range(1,20):
    for j in range(1,i+1):
        print('%d*%d=%2ld '%(i,j,i*j),end='')
    print()




