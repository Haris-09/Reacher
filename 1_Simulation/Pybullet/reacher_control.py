import pybullet as p
import time

p.connect(p.GUI)

planeId = p.loadURDF("utils/plane.urdf")

reacherId = p.loadURDF("reacher-urdf/PoppyErgoJr/robots/PoppyErgoJr.urdf")

gravId = p.addUserDebugParameter("gravity", -10, 10, -10)
jointIds = []
paramIds = []

p.setPhysicsEngineParameter(numSolverIterations=10)
p.changeDynamics(reacherId, -1, linearDamping=0, angularDamping=0)

for j in range(p.getNumJoints(reacherId)):
  p.changeDynamics(reacherId, j, linearDamping=0, angularDamping=0)
  info = p.getJointInfo(reacherId, j)
  #print(info)
  jointName = info[1]
  jointType = info[2]
  if (jointType == p.JOINT_PRISMATIC or jointType == p.JOINT_REVOLUTE):
    jointIds.append(j)
    paramIds.append(p.addUserDebugParameter(jointName.decode("utf-8"), -4, 4, 0))

p.setRealTimeSimulation(1)
while (1):
  p.setGravity(0, 0, p.readUserDebugParameter(gravId))
  for i in range(len(paramIds)):
    c = paramIds[i]
    targetPos = p.readUserDebugParameter(c)
    p.setJointMotorControl2(reacherId, jointIds[i], p.POSITION_CONTROL, targetPos, force=5 * 240.)
