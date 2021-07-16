import numpy as np
import random

sigma=1.0
sita=0.0

n=list([3,3])
x=np.array([[0.6,0.1],[0.1,0.2]])
# y=np.array([[-1.02,-0.83,0.50],[0.20,2.82,0.58]])
sg=list([0 for i in range(100)])
st=list([0 for i in range(100)])
sp=list([0 for i in range(100)])
zg=list([0 for i in range(100)])
zp=list([0 for i in range(100)])
zt=list([0 for i in range(100)])


def sg_gene(y):
    a=0
    for i in range(2):
        for j in range(n[i]):
            if i==0:
                a+=1-2*y[i][j]+2*y[i][j]*(x[0][i]+x[1][i])-(x[0][i]+x[1][i])*(x[0][i]+x[1][i])
                a+=1-2*y[i][j]+2*y[i][j]*(x[i][0]+x[i][1])-(x[i][0]+x[i][1])*(x[i][0]+x[i][1])
            elif i==1:
                a+=1-2*y[i][j]+2*y[i][j]*(x[0][i]+x[1][i])-(x[0][i]+x[1][i])*(x[0][i]+x[1][i])
                a+=1-2*y[i][j]+2*y[i][j]*(x[i][0]+x[i][1])-(x[i][0]+x[i][1])*(x[i][0]+x[i][1])
    b=a/2*sigma*sigma

    c=0
    for j in range(2):
        x2=x[0][j]+x[1][j]
        c+=x2*np.exp(b)

    for i in range(2):
        x1=x[i][0]+x[i][1]
        c+=x1*np.exp(b)
            
    hg=c/x[1][1]
    return 1/hg

def st_gene(y):
    d=0
    for i in range(2):
        for j in range(n[i]):
            d+=1-2*y[i][j]
    e=np.exp(d/2*sigma*sigma)
    f=x[0][0]/x[1][1]
    ht=f*e+1
    return 1/ht

def sp_gene(y):
    g=0
    for j in range(n[1]):
        g+=1-2*y[1][j]
    h=np.exp(g/2*sigma*sigma)
    o=x[1][0]/x[1][1]
    hp=o*h+1
    hp1=1/hp

    p=0
    for j in range(n[0]):
        p+=1-2*y[0][j]
    q=np.exp(p/2*sigma*sigma)
    r=(x[0][1]+x[0][1])/(x[1][0]+x[1][1])
    hp=r*q+1
    hp2=1/hp
    return hp1*hp2

def out(s,sita):
    if s>sita:
        z=1
    elif s<sita:
        z=0
    return z

for cnt in range(100):
    y=np.array([[random.random() for j in range(3)]for i in range(2)]) 
    sg[cnt]=sg_gene(y)
    st[cnt]=st_gene(y)
    sp[cnt]=sp_gene(y)
    zg[cnt]=out(sg[cnt],sita)
    zt[cnt]=out(st[cnt],sita)
    zp[cnt]=out(sp[cnt],sita)
    # print(zg[cnt],":",sg[cnt])
    # print(zt[cnt],":",st[cnt])
    print(zp[cnt],":",sp[cnt])
    sita=sita+0.01

# sgの保持ｚとの表
