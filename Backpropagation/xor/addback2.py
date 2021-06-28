x_check=list([0,0])
for c in range(4):
    if c==0:
        x_check[0]=0
        x_check[1]=0
    elif c==1:
        x_check[0]=0
        x_check[1]=1
    elif c==2:
        x_check[0]=1
        x_check[1]=0
    elif c==3:
        x_check[0]=1
        x_check[1]=1
    print(x_check)