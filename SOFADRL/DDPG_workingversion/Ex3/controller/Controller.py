#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import socket


x = []
y = []
p = []
tmax = 1
stepCount = 0

sock = socket.socket()
port = 12345
sock.bind(('', port))
sock.listen(5)
c, addr = sock.accept()
print "Socket Up and running with a connection from", addr


class controller(Sofa.PythonScriptController):

    def initGraph(self, node):

        self.node = node
        self.pneu1Node = self.node.getChild('pneu1')
        self.pressureConstraint1Node = self.pneu1Node.getChild('cavity')

        # create pointer towards the MechanicalObject
        self.myMechanicalObjectPointer = self.pneu1Node.getObject('tetras')

    def onBeginAnimationStep(self, dt):
        # do whatever you want at the beginning of the step
        global t
        global pressureValue
        global myMOpositions
        global stepCount
        global rcvdData

        t = self.pneu1Node.findData('time').value
        incr = t*1000.0

        self.MecaObject1 = self.pneu1Node.getObject('tetras')
        self.pressureConstraint1 = self.pressureConstraint1Node.getObject(
            'SurfacePressureConstraint')

        myMOpositions = self.myMechanicalObjectPointer.findData(
            'position').value
        pressureValue = self.pressureConstraint1.findData('value').value[0][0]

        # print type(str(c.recv(1024).decode()))
        if stepCount == 0:
            rcvdData = c.recv(1024).decode()

            if str(rcvdData) == "reset":
                # break
                # self.pneu1Node.getRootContext().animate = False
                #print 'Im in'
                self.pneu1Node.reset()
                c.send(str(myMOpositions[23][0]).encode())

            else:
                #print 'Im out'
                p = float(rcvdData)
                pressureValue = p
                self.pressureConstraint1.findData(
                    'value').value = str(pressureValue)


        # debugging...
        # if str(rcvdData) != "reset":
            # print 'Im out';
            #print (str(rcvdData))

        # DRL Patch communication
        # receive reward
        # rcvdData = c.recv(1024).decode()

        # update action
        # self.pressureConstraint1.findData('value').value = str()

        # p.append(pressureValue)

    # called on each animation step
    # def onBeginAnimationStep(self, dt):
        # do whatever you want at the beginning of the step
        # t = self.rootNode.findData('time').value
        # return 0

    # called on each animation step

    def onEndAnimationStep(self, dt):
        global stepCount
        global rcvdData
        # print the first value of the DOF 0 (Vec3 : x,y,z) x[0] y[0] z[0]
        # print str(t)
        # print str(myMOpositions[5783][0])+' '+str(myMOpositions[5783][1])+' '+str(myMOpositions[5783][2])

        # sendData = raw_input("N: ")

        # Send back position
        # c.send(sendData.encode())

        p.append(pressureValue)
        x.append(t)
        y.append(myMOpositions[23][0])
        stepCount += 1

        if stepCount > 30:
            stepCount = 0
            #print('11111')
            if str(rcvdData) != "reset":
                # self.pneu1Node.getRootContext().animate = False
                #print('11111')
                c.send(str(myMOpositions[23][0]).encode())
                
                # plt.figure()

                # plt.subplot(211)
                # plt.plot(x, y)
                # plt.yscale('linear')
                # plt.ylabel('Displacement/mm')
                # plt.grid(True)

                # l = [2*x for x in p]
                # plt.subplot(212)
                # plt.plot(x, p)
                # plt.yscale('linear')
                # plt.ylabel('Pressure/MPa')
                # plt.xlabel('time')
                # plt.grid(True)

                # plt.show()

        return 0
