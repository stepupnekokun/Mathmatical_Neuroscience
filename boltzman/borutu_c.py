import random
import numpy as np

x_n=4
val_n=3
w_n=4
c_e=0
t=1

w=[[0 for l in range(w_n)] for k in range(w_n)]
x_count=[0 for k in range(8)]
x_freq=[0 for k in range(8)]
p=[0 for k in range(8)]


def set_state():
    x_state=[[1,0,0,0],
             [1,0,0,1],
             [1,0,1,0],
             [1,0,1,1],
             [1,1,0,0],
             [1,1,0,1],
             [1,1,1,0],
             [1,1,1,1]]
    return x_state
def set_neuron():
    x=[0 for k in range(x_n)]
    x[0]=1
    return x
def set_weight():
    for k in range(w_n):
        for l in range(k+1,w_n):
            w[k][l]+=(2*x_state[3][k]-1.0)*(2*x_state[6][l]-1.0)
            w[l][k]=w[k][l]
        w[k][k]=0
    return w
def act_dy(i):
    u=0
    for l in range(x_n):
        u+=w[i][l]*x[i]
    return u
def update(u,i):
    return 1 if random.random()>1/(1+np.exp(-u/t)) else 0
def state_cnt():
    for cnt in range(8):
        if x_state[cnt]==x:
            x_count[cnt]+=1
    return x_count
def frequency():
    for f in range(8):
        x_freq[f]=x_count[f]/learn
    return x_freq

x_state=set_state()
x=set_neuron()
w=set_weight()

for learn in range(1,1000001):
    i=random.randint(1,3)
    u=act_dy(i)
    x[i]=update(u,i)
    x_count=state_cnt()
    x_freq=frequency()

for k in range(8): 
    e=-(w[0][1]*x_state[k][1]+w[0][2]*x_state[k][2]+w[0][3]*x_state[k][3]+w[1][2]*x_state[k][1]*x_state[k][2]+w[1][3]*x_state[k][1]*x_state[k][3]+w[2][3]*x_state[k][2]*x_state[k][3])    
    c_e+=np.exp(-e/t)

for k in range(8):
    c=1/c_e
    e=-(w[0][1]*x_state[k][1]+w[0][2]*x_state[k][2]+w[0][3]*x_state[k][3]+w[1][2]*x_state[k][1]*x_state[k][2]+w[1][3]*x_state[k][1]*x_state[k][3]+w[2][3]*x_state[k][2]*x_state[k][3])
    p[k]=c*np.exp(-e/t)

print(x_count)
print(x_freq)
print(p)
