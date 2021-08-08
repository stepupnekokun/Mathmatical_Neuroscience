import numpy as np
import random
import matplotlib.pyplot as plt

sigma=1.0
reidai=10000

n=list([3,3])
x=np.array([[0.6,0.1],[0.1,0.2]])
# y=np.array([[-1.02,-0.83,0.50],[0.20,2.82,0.58]])
x_alpa=list([[0 for i in range(2)]for i in range(reidai)])
sg=list([0 for i in range(reidai)])
st=list([0 for i in range(reidai)])
sp=list([0 for i in range(reidai)])
zg=list([0 for i in range(reidai)])
zp=list([0 for i in range(reidai)])
zt=list([0 for i in range(reidai)])
sita=random.random()
fp_under=0
cd_over_g=0
cd_over_t=0
cd_over_p=0
fp_over_g=0
fp_over_t=0
fp_over_p=0

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

def sita_gene(sita):
    if random.random()<0.5:
        sita+=0.01
    else:
        sita-=0.01
    return sita

def fp_gene(fp_over,fp_under):
    fp_under=reidai-fp_under
    fp=fp_over/fp_under
    return fp

def cd_gene(cd_over,cd_under):
    cd=cd_over/cd_under
    return cd

for cnt in range(reidai):
    ans=0
    y=np.array([[random.random() for j in range(3)]for i in range(2)]) 
    for i in range(2):
        if random.random()<0.5:
            x_alpa[cnt][i]=0
        else:
            x_alpa[cnt][i]=1 
    sg[cnt]=sg_gene(y)
    st[cnt]=st_gene(y)
    sp[cnt]=sp_gene(y)
    zg[cnt]=out(sg[cnt],sita)
    zt[cnt]=out(st[cnt],sita)
    zp[cnt]=out(sp[cnt],sita)
    # print(sita)
    print(zg[cnt],":",sg[cnt])
    # print(zt[cnt],":",st[cnt])
    # print(zp[cnt],":",sp[cnt])

    if x_alpa[cnt][0]+x_alpa[cnt][1]==2 and zg[cnt]==1:
        cd_over_g+=1
    if x_alpa[cnt][0]+x_alpa[cnt][1]==2 and zt[cnt]==1:
        cd_over_t+=1
    if x_alpa[cnt][0]+x_alpa[cnt][1]==2 and zp[cnt]==1:
        cd_over_p+=1

    if x_alpa[cnt][0]+x_alpa[cnt][1]!=2 and zg[cnt]==1:
        fp_over_g+=1
    if x_alpa[cnt][0]+x_alpa[cnt][1]!=2 and zt[cnt]==1:
        fp_over_t+=1
    if x_alpa[cnt][0]+x_alpa[cnt][1]!=2 and zp[cnt]==1:
        fp_over_p+=1

    if x_alpa[cnt][0]+x_alpa[cnt][1]==2:
        fp_under+=1

    if cd_over_g>=1:
        cd = cd_gene(cd_over_g,fp_under)
        fp = fp_gene(fp_over_g,fp_under)
        plt.plot(cd,fp,marker=".",linestyle="-")
    sita=sita_gene(sita)
    
    

plt.xlim(0,0.2)
plt.ylim(0,1)
plt.tick_params(labelsize=10)
plt.show()


