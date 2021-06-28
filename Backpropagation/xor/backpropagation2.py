import random
import matplotlib.pyplot as plt
import time
import numpy as np

n1=2
n2=2
in_n = 4
x=list([])
s=list([])
w=list([])
u=list([])
rj=list([])
bs=list([])
bw=list([])
myu = 0.8
learn = 100000

# 正規分布N(0,0.01)で乱数生成
def nrand():
    n = random.normalvariate(0,0.1)
    return n 

# シグモイド関数
def sigmoid(sigmon):
    return 1.0/(1.0+np.exp(-(sigmon) ) )

def act_dyn(x,y):
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

    return z


def ans_per(c):
    if c==0:
        x[0]=0
        x[1]=0
    elif c==1:
        x[0]=0
        x[1]=1
    elif c==2:
        x[0]=1
        x[1]=0
    elif c==3:
        x[0]=1
        x[1]=1
    return x


# 配列の大きさ決め（層決め）
# 入力層
for i in range(n1):
    x.append(i)
    s.append([nrand(),nrand()] )
    bs.append(nrand())
#中間層
for i in range(n2):
    u.append(i)
    w.append(nrand())
    bw.append(nrand())
    

for cnt in range(learn):

    # 入力値の決定（教師データ、正解データ）
    for j in range(n1):
        x[j] = random.randint(0,1)
    y=x[0]^x[1]

    z=act_dyn(x,y)

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

    # print(cnt,"教師データ:",x,"正解データ：",y,"出力値：",z,"誤差:",e)
    # グラフに描画
    if cnt!=0 and cnt%10==0:
        for c in range(4):
            x=ans_per(c)
            y=x[0]^x[1]
            z=act_dyn(x,y)
            ansper=abs(y-z)/4
            print(cnt+c,"入力データ:",x,"正解データ：",y,"出力値：",z,"正解率：",ansper)
            plt.plot(cnt+c,ansper,marker=".")
        
    



plt.xlim(10000,50000)
plt.xlabel("number of iterations")
plt.ylabel("correct responses")
plt.tick_params(labelsize=10)
plt.savefig('backpropagation2.png')
plt.show()

time.sleep(10)