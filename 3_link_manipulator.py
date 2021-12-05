# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 12:28:22 2021

@author: aluni
"""
"""
Before Running the command it is expected from you to read through the
command syntax from python API for coppeliasim. 
"""
# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.


import math
import sim
import time

print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
    print ('Connected to remote API server')
else:
        print ('Failed connecting to remote API server')
        print ('Program ended')

res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
if res==sim.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
else:
        print ('Remote API function call returned with error code: ',res)

time.sleep(2)

#Getting object handlle
opMode=sim.simx_opmode_blocking
errorCode,base=sim.simxGetObjectHandle(clientID,"Base",opMode)
errorCode,link1=sim.simxGetObjectHandle(clientID,"Link1",opMode)
errorCode,link2=sim.simxGetObjectHandle(clientID,"Link2",opMode)
errorCode,link3=sim.simxGetObjectHandle(clientID,"Link3",opMode)
errorCode,dummy=sim.simxGetObjectHandle(clientID,"Dummy",opMode)
errorCode,target=sim.simxGetObjectHandle(clientID,"Target",opMode)

errorCode,J1=sim.simxGetObjectHandle(clientID,"Revolute_joint1",opMode)
errorCode,J2=sim.simxGetObjectHandle(clientID,"Revolute_joint2",opMode)
errorCode,J3=sim.simxGetObjectHandle(clientID,"Revolute_joint3",opMode)

#Getting tip and target positions
errorCode, tip_position= sim.simxGetObjectPosition(clientID,dummy,base,sim.simx_opmode_oneshot_wait)
errorCode, target_position= sim.simxGetObjectPosition(clientID,target,base,sim.simx_opmode_oneshot_wait)

"""
Note that the coppeliasim coordinate system isn't configured according to
the DH convention. Hence, observe that the formula is changed. ye in 
coppeliasim is xe according to the DH convention and similarly, ze is ye
according to DH convention. The actual calculation doesn't change just the 
naming of variable changes to resemble the coordinate system in coppeliasim
"""
a1 = 0.8; #Link 1 length
a2 = 0.6; #Link 2 length
a3 = 0.4; #Link 3 length
ye = target_position[1]; #Target Position
ze = target_position[2]; #Target Position
ze = ze- 0.425;
g = 70; #end-effector orientation with respect to horizontal axis
g = math.radians(g)

#Finding joint 3 position
y3 = ye - a3*math.cos(g)
z3 = ze - a3*math.sin(g)

#Elbow down config
theta1a = (math.atan(z3/y3)-math.acos((y3**2+z3**2+a1**2-a2**2)/(2*a1*math.sqrt(y3**2+z3**2))))
theta2a = (math.pi - math.acos((a1**2+a2**2-y3**2-z3**2)/(2*a1*a2)))
theta3a = (g) - theta1a - theta2a 

#For Elbow-up configuration uncomment the following equations:
#theta1b = theta1a + 2*g
#theta2b = -theta2a
#theta3b = g - theta1b - theta2b
    
print ("Joint angle 1 = ",theta1a)
print ("Joint angle 2 = ",theta2a)
print ("Joint angle 3 = ",theta3a)

"""
For smoother simulation let's give only 1% of the joint values every loop
"""
#joint 1
for i in range(1,100+1):
  J1a = i*0.01*theta1a;
  errorcode = sim.simxSetJointPosition(clientID,J1,J1a,sim.simx_opmode_oneshot_wait)
#joint 2  
for i in range(1,100+1):
  J2a = i*0.01*theta2a;
  errorcode = sim.simxSetJointPosition(clientID,J2,J2a,sim.simx_opmode_oneshot_wait)
#joint 3  
for i in range(1,100+1):
  J3a = i*0.01*theta3a;
  errorcode = sim.simxSetJointPosition(clientID,J3,J3a,sim.simx_opmode_oneshot_wait)    

sim.simxFinish(clientID)