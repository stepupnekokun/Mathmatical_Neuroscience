import random
import matplotlib.pyplot as plt
import time
import numpy as np

n1=2
n2=3
in_n = 4
x=list([])
s=list([])
w=list([])
u=list([])
rj=list([])
bs=list([])
bw=list([])
myu = 0.8
learn = 10000

# 正規分布N(0,0.01)で乱数生成
def nrand():
    n = random.normalvariate(0,0.1)
    return n 

# シグモイド関数
def sigmoid(sigmon):
    return 1.0/(1.0+np.exp(-(sigmon) ) )

# 配列の大きさ決め（層決め）
# 入力層
for i in range(n1):
    x.append(i)
    
#中間層
for i in range(n2):
    s.append([nrand(),nrand()] )
    bs.append(nrand())
    u.append(i)
    w.append(nrand())
    bw.append(nrand())
    

for cnt in range(learn):

    # 入力値の決定（教師データ、正解データ）
    for j in range(n1):
        x[j] = random.randint(0,1)
    y=x[0]^x[1]

    # 中間層の出力
    for j in range(n2):
        sigmon=bs[j]
        for k in range(n1):
            sigmon+=x[k]*s[j][k]
        u[j]=sigmoid(sigmon)


    # 出力層の出力
    sigmon=bw[0]
    for j in range(n2):
        sigmon+=w[j]*u[j]
    z = sigmoid(sigmon)


    # 学習
    r=0
    r=(y-z)*(1.0-z)*z

    # 出力層学習
    for j in range(n2):
        bw[j]+=myu*r*1
        w[j]+=myu*r*u[j]

    # 中間層学習
    for j in range(n2):
        rj=r*w[j]*u[j]*(1.0-u[j])
        bs[j]+=myu*rj*1
        for k in range(n1):
            s[j][k]+=myu*rj*x[k]

    
    # 二乗誤差
    e = ((y-z)*(y-z))*0.5

    print(cnt,"教師データ:",x,"正解データ：",y,"出力値：",z,"誤差:",e)
    # グラフに描画

    plt.plot(cnt,e,marker=".")
    # if cnt==6000:
    #     plt.xlim(4000,6000)
    #     plt.xlabel("number of iterations")
    #     plt.ylabel("E")
    #     plt.tick_params(labelsize=10)
    #     plt.savefig('XOR4000_6000.png')
    #     plt.show()




plt.xlim(0,learn)
plt.xlabel("number of iterations")
plt.ylabel("E")
plt.tick_params(labelsize=10)
plt.savefig('backpropagation4.png')
plt.show()

time.sleep(10)