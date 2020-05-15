import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(1, figsize=(24, 12))
SIFS = 10  # us
slot = 20  # us slot time
DIFS = 2 * slot + SIFS
Rb = 12   # 12Mbits/s
Tb = 1 / Rb
CWmin = 32  # %minimal Contention Window
CWmax = 1024  # maximal Contention Window
RTS = round(20 * 8 * Tb)  # 20Byte for RTS
CTS = round(14 * 8 * Tb)  # 14Byte for CTS
ACK = round(14 * 8 * Tb)  # 14Byte for ACK
fair = []
pc = []
for Nnode in range(1, 2):  # number of active nodes
    # Nnode=2
    # assume both nodes are saturated with packets to be sent out
    # node status loop
    thr = []
    print('Nnode=%d' % Nnode)
    cnt = np.zeros(Nnode, dtype=int)
    Ndata = np.zeros(Nnode, dtype=int)
    BC = np.zeros(Nnode, dtype=int)
    ch, cln, sent = [], [], []
    first, Ncln = 1, 0
    Nloop = 1e5
    Npkg = 0
    npkg = 0
    for loop in range(int(Nloop)):
        ch = []
        #        if loop%100==0:
        #            print('loop %d times' %loop)
        if first:
            first = 0
            BC = np.random.randint(CWmin, size=Nnode)  # set back-off counter;
            Ndata = np.random.randint(29, 2347, size=Nnode) * 8 * Tb  # random data length
            #            Ndata=np.random.randint(2047,2048,size=Nnode)*8*Tb #set a data length
            Ndata = Ndata.astype(int)
            #    wait for DIFS to start out
        ch += [0] * DIFS
        [mBC, ind] = np.min(BC), np.argmin(BC)
        cln = []
        for i in range(Nnode):
            once = 1
            if i != ind and BC[i] == mBC:
                cln.append(i)
                cnt[i] += 1
                if once:
                    cnt[ind] += 1
                    once = 0
                    #            for j in range(len(cln)):
                    #                print('Collision nodes:')
                    #                print(cln)

        ch += [0] * (mBC * slot)
        #    print(BC)
        BC = BC - mBC  # adjust BO values
        #    print(BC)
        if len(cln) == 0:
            cnt[:Nnode] = 0
            #        print('the Node %d win the channel access' %ind)
            Npkg += 1
            if ind == 0:
                npkg += 1
            sent.append(ind)
            BC[ind] = np.random.randint(CWmin)  # reset the BO
        else:
            Ncln += 1
            BC[ind] = np.random.randint(CWmin * 2 ** np.min([5, cnt[ind]]))  # reset the BO
            for i in range(len(cln)):
                BC[cln[i]] = np.random.randint(CWmin * 2 ** np.min([5, cnt[ind]]))  # reset the BO

        ch += [1] * RTS
        ch += [0] * SIFS
        ch += [1] * CTS
        ch += [0] * SIFS
        ch += [1] * Ndata[ind]
        ch += [0] * SIFS
        ch += [1] * ACK
        #    pc.append(Ncln/Nloop*100)
        #    fair.append(npkg/Npkg)
        thr.append(Ndata[0] / len(ch))

plt.hist(thr)
print('Collision probability is %f%%\n' % (Ncln / Nloop * 100))
# plt.plot(ch)
plt.show()
# plt.plot(range(1,10),pc)
# plt.plot(range(1,10),fair)
plt.grid(True)
fig.savefig('1', dpi=300)
