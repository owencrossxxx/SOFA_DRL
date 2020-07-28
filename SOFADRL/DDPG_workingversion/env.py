import numpy as np
import socket

sock = socket.socket()
sock.connect(('127.0.0.1',12345))

class ArmEnv(object):
    dt = .1    # refresh rate
    action_bound = [-0.01, 0.05]
    goal = 85
    state_dim = 1
    action_dim = 1

    def __init__(self):
        self.on_goal = 0

    def step(self, action):
        done = False
        a = np.clip(action, *self.action_bound)
        a = str(a[0])
        #print(a)

        sock.send(a.encode())
        s = float(sock.recv(1024).decode())

        print ('pos:',s,'','act:','',a)

        if np.abs(self.goal-s) < 0.5:
            r = 1.
            done = True
        else:
            r = -np.abs(self.goal-s)
            self.on_goal = 0
        
        s = np.array([s])


        return s, r, done


    def reset(self):
        self.goal = 83.01 + np.random.rand()*10
        self.on_goal = 0
        str = "reset"
        sock.send(str.encode())
        s = np.array([float(sock.recv(1024).decode())])

        return s
