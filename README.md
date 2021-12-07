# Ch3_InverseKinematics

## Problem Statement:

Finding the inverse kinematic solution of a 3-link planar manipulator. Use the found solution to write a python code and simulate in Coppeliasim.

## Pre-requisites:

- Software: Coppeliasim (for simulation), Spyder (for python coding)
- Basic python syntax
- Understanding of the python remote API commands for coppeliasim ( refer: [Remote API Python](https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm))

## Solution:

![3 link planar manipulator](cuboid.png)
 
Assume the link lengths to be a1, a2, and a3, respectively, with corresponding joint angles of ϴ1, ϴ2, and ϴ3.

To find this manipulator's inverse kinematic, we require the position (xe, ye) and orientation of the end-effector(γ).

The orientation of the end-effector has the following relation with the joint angles:

γ = ϴ1 + ϴ2 + ϴ3 ... (1)

From this, we can see that once we find out the joint values for joint 1 and joint 2, we can directly use the above relation to find the value for joint 3.

To find ϴ1 and ϴ2, we need first to find the position of the wrist point. Using simple trigonometry, we can see that:

![x3](1.png)

To find ϴ2, we need to first find β. Using the law of cosine in the triangle made by joints 1, 2, and 3, we get:

![y3](2.png)

![beta](3.png)

To find ϴ1, we need to first find α and δ. We can find α with the help of the wrist point.

![theta2](4.png)

For δ, we can again use the law of cosines:

![alpha](5.png)

![delta](6.png)

Using equations (1), (2), and (3), we can find ϴ3:

![theta1](7.png)

This solution only provides one configuration, i.e., the elbow-down configuration. You can use a similar geometric approach to find joint angles for the elbow-up configuration. The solution for the elbow-up configuration can be found in the python code. 

## Simulation:

### Scene setup:

Open the “scene_setup.ttt” file. For our problem, we make our manipulator by using the “Add > Primitive Shape > Cuboid” for the linkages and “Add > Joint > Revolute”.

![cop](8.png)
 		 
To find inverse kinematics, we need to fix certain variables. For our example let’s set the link lengths as:

a1 = 0.8

a2 = 0.6

a3 = 0.4

Base height = 1

Use these lengths to define the cuboids while setting up your scene. Once you add the base and specify its length, you add a revolute joint and give it the appropriate length and diameter to be visible. The length and diameter of the joint don’t contribute to the simulation’s kinematics and dynamics. After adding the joint, you will observe that the joint is placed at the scene's origin. To move the joint to its intended location, we use the “Object/item shift” and “Object/item rotate” from the toolbar. The rest of the linkages can be set up using the same steps.

To make a simulation where we define where the manipulator should go, we add a “Dummy” from the “Add” tab and move it using “Object/item shift”. This target dummy is the input for our inverse kinematic, and by moving it around, we can see how the manipulator will behave. Since our manipulator moves in a planar motion, we need to keep the target in the same plane as link 3. You can rename the links, joints, and dummy by double-clicking on the name in the “Scene hierarchy” tab and typing the desired names.

Once the scene is set up, open the link properties tab by double clicking on the cuboid logo of the corresponding link under the “Scene hierarchy” tab. Once the “Scene object properties” tab opens, under “Dynamic properties,” click “Show dynamic properties dialog” and deselect “Body is dynamic”. If you don’t deselect this, the link will drop down to the floor due to gravity when running the simulation. Repeat this for all the links.

It is essential to define the hierarchy of the links and joints since it notifies coppeliasim which link moves with respect to a joint. The hierarchy for our simulation is:

Base – Revolute joint 1 – Link 1 – Revolute joint 2 – Link 2 – Revolute Joint 3 – Link 3 – Dummy

Once the hierarchy is set, the only thing remaining now is opening a connection for coppeliasim and spyder to communicate through. We can do so by copying the following command in any of the child scripts:

`simRemoteApi.start(19999)`

To open a child script, right-click on any of the joints or links then “Add > Associated child script > Nonthreaded”. This will add a script-like logo next to the selected link or joint, double click that logo, and paste the above code line as the first line of the code without changing anything else. Now we begin to write the code for simulation.

### Coding:

The code is essentially divided into five parts. Read through the following steps and explanations:

- Open “3_link_manipulator.py”

- Read through the code

- In the first part of the code (lines 20 – 39), we import the necessary libraries and open communication with coppeliasim. Once the communication is established, we store all the object handles and display the object handles sent from coppeliasim to python. We do this to verify whether the communication is proper and if there is any missing object handle

- In the second part of the code (lines 42 – 56), we store the object handles to the appropriate variable name. This is done the simplify the code by using the variable name instead of the object name. In line 56, we store the target position, viz. the target dummy in coppeliasim; this will be our input for inverse kinematics (end-effector position).

- In the third part of the code (line 65 – 72), we define the manipulator parameters and store the target position into "ye" and "ze". Note that instead of "xe", we are using "ye" and instead of "ye", we are using "ze". This is because coppeliasim has a global coordinate system different from our coordinate system, which follows the DH convention. The end-effector orientation (γ) is defined as g, and we arbitrarily set it at 70 degrees (you can change it to any value and observe the change in the simulation)

- The firth part of the code (lines 75 – 81) utilizes our inverse kinematic solution. Note that the change in coordinate system follows in this part of the code too

- Once we find the joint angles necessary for the manipulator to reach the desired position and with the defined orientation, we need to communicate these values back to coppeliasim to move the joints accordingly. In the fifth part of the code, we send these values using the remote API command (`simxSetJointPosition()`)

- If we directly send these values to coppeliasim, the joint will instantly move to its calculated value. But, since we want to see how the manipulator moves, we will use a for loop and only return 1% of the joint value to coppeliasim in every iteration. This will give a smooth simulation.
