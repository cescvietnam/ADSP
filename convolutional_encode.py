import numpy as np



def conv_encoder(input):
    output=[]
    state='00'
    G_polys = ('111','101')
    constraint_length = len(G_polys[0])
    Nstates = 2**(constraint_length-1) 
    for n in range(len(input)):
        u1 = int(input[n])
        u2 = int(input[n])
        for m in range(1,constraint_length):
            if int(G_polys[0][m])==1:
                u1=u1^int(state[m-1])
            if int(G_polys[1][m])==1:
                u2=u2^int(state[m-1])
        output=np.hstack((output,[u1,u2]))
        state=bin(int(input[n]))[-1]+state[:-1]
    return output,state
            

