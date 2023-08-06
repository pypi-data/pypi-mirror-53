import numpy as np
import numpy.random as rng

import dynmix

import matplotlib.cm as cm
# import matplotlib.pyplot as plt


def mix_cm(eta, idx):
    if type(eta) in [int, float]:
        assert len(idx) == 2
        return eta * np.array(cm.Set2(idx[0])) + (1 - eta) * np.array(cm.Set2(idx[1]))

    cols = np.array([eta[i] * np.array(cm.Set2(idx[i])) for i in range(len(idx))])
    return np.clip(cols.sum(axis=0), 0, 1)


rng.seed(123)
T = 90
n_a = 12
n_b = 8
n = 22

y_a, theta_a = dynmix.dlm.simulate(T, np.eye(1), np.eye(1), np.eye(1) * 5, np.eye(1) * 2,
                                   theta_init=np.ones(1) * 5, n=n_a)
y_b, theta_b = dynmix.dlm.simulate(T, np.eye(1), np.eye(1), np.eye(1) * 8, np.eye(1) * 2,
                                   theta_init=np.ones(1) * 11, n=n_b)

y_c = np.empty((T, 2))

mixa = np.linspace(0, 1, T)
mixa[:int(T/1.5)] **= 4
mixa[int(T/1.5):] **= 0.8
mixb = 1 - mixa

for t in range(T):
    y_c[t] = mixa[t] * (rng.randn(2) * np.sqrt(5) + theta_a[t]) + mixb[t] * (rng.randn(2) * np.sqrt(8) + theta_b[t])

T -= 20
y_a = y_a[20:]
y_b = y_b[20:]
y_c = y_c[20:]
Y = np.hstack((y_a, y_b, y_c))

# for i in range(n_a):
#     plt.plot(y_a[:,i], color='k')
# for i in range(n_b):
#     plt.plot(y_b[:,i], color='k')
# for i in range(2):
#     plt.plot(y_c[:,], c=cm.Set2(1))
# plt.ylabel('Time-Series')
# plt.xlabel('Time')
# plt.show()

F_list = [np.eye(1), np.eye(1)]
G_list = [np.eye(1), np.eye(1)]

rng.seed(2)
chains = dynmix.dynamic.sampler(Y, F_list, G_list)
