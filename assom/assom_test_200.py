# 連想記憶なのに思い出してくれない
# 初めから更新がなされていない

import random
import matplotlib.pyplot as plt

n=1000
m=200
a=25
memories=list([]) 
x=list([])
sgn=list([])
w=list([])
count=list([])
y=list([])


def nrand():
    return 1 if random.random() < 0.5 else -1

def gene_memories():
    memories=[[nrand() for i in range(n) ] for j in range(m) ]
    return memories

def set_weigth():
    for i in range(n):
        for j in range(i+1,n):
            sum=0
            for k in range(m):
                sum+=memories[k][i]*memories[k][j]
            w[i][j]=sum/n
            w[j][i]=w[i][j]
        w[i][i]=0.0

def init_x():
    for i in range(n):
        if i<a:
            x[i]=-memories[0][i]
        else:
            x[i]=memories[0][i]

def sign_function(x):
    for i in range(n):
        u=0.0
        for j in range(n):
            u+=w[i][j]*x[j]  
        if u>0:
            sgn[i]=1
        else:
            sgn[i]=-1
    for i in range(n):
        x[i]=sgn[i]
    return x

def direct_cos(x):
    cos=0.0
    for i in range(n):
        cos+=memories[0][i]*x[i]
    cos=cos/n
    return cos

w=[[0.0 for i in range(n) ] for j in range(n)]
sgn=[0.0 for i in range(n)]
x=[0.0 for i in range(n) ] 
count=[0 for i in range(20) ]
y=[0.0 for i in range(20) ]

while a!=1025:
    memories=gene_memories()
    set_weigth()
    init_x()

    for cnt in range(20):
        cos=direct_cos(x)
        sign_function(x)
        count[cnt]=cnt
        y[cnt]=cos


    plt.plot(count,y,marker=".",linestyle="-")
    a+=25
    
plt.xlim(0,20)
plt.ylim(0.2,1)
plt.tick_params(labelsize=10)
plt.show()
