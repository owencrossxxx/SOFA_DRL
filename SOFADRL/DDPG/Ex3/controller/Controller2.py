#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

x = []
y = []
p = []
tmax = 0.5

class controller(Sofa.PythonScriptController):

    def initGraph(self, node):

            self.node = node
            self.pneu1Node=self.node.getChild('pneu')
            self.pressureConstraint1Node = self.pneu1Node.getChild('cavity')

            # create pointer towards the MechanicalObject
            self.myMechanicalObjectPointer = self.pneu1Node.getObject('tetras')


    #called on each animation step
    def onBeginAnimationStep(self, dt):
        #do whatever you want at the beginning of the step
        global t
        global pressureValue
        global myMOpositions

        t = self.pneu1Node.findData('time').value
        incr = t*1000.0;

        self.MecaObject1=self.pneu1Node.getObject('tetras');
        self.pressureConstraint1 = self.pressureConstraint1Node.getObject('SurfacePressureConstraint')

        myMOpositions = self.myMechanicalObjectPointer.findData('position').value

        if t == 0:
            pressureValue = self.pressureConstraint1.findData('value').value[0][0]
        if t< float(tmax/3) and t > 0:
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] + 0.0001
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            if pressureValue > 0.001:
                pressureValue = 0.001
        if t< float(2*tmax/3) and t> float(tmax/3) :
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] - 0.0002
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            if pressureValue < -0.001:
                pressureValue = -0.001
        if t> float(2*tmax/3):
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] + 0.0003
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            if pressureValue > 0.001:
                pressureValue = 0.001


        return 0




    #called on each animation step
    def onEndAnimationStep(self, dt):
        #access the 'position' state vector
        #t = self.pneu1Node.findData('time').value


        # print the first value of the DOF 0 (Vec3 : x,y,z) x[0] y[0] z[0]
        #print str(t)
        #print str(myMOpositions[5783][0])+' '+str(myMOpositions[5783][1])+' '+str(myMOpositions[5783][2])

        p.append(pressureValue)
        x.append(t)
        y.append(myMOpositions[5783][0])


        if t>= tmax:
            self.pneu1Node.getRootContext().animate = False

            plt.figure()

            plt.subplot(211)
            plt.plot(x, y)
            plt.yscale('linear')
            plt.ylabel('Displacement/mm')
            plt.grid(True)

            #l = [2*x for x in p]
            plt.subplot(212)
            plt.plot(x, p)
            plt.yscale('linear')
            plt.ylabel('Pressure/MPa')
            plt.xlabel('time')
            plt.grid(True)


            plt.show()

        return 0
