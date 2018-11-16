import maya.cmds as mc
import sys
import TwistBend_gimmick

xyz = 'XYZ'
she = 'XY', 'XZ', 'YZ'

def cntBendJnt():
	global many, j, get, jcnt, jnt, baim, bant

	many = []
	baim = []
	j = 0
	
	get = mc.ls(typ='joint')
	exi = mc.ls(typ='aimConstraint')
	for i in exi:
		if 'afterSplitTwistDriver' in '{}'.format(i):
			baim.append(i)
	for i in get:
		if 'twist' in '{}'.format(i):
			get2 = mc.listRelatives(i, p=True)
			if 'bend' in '{}'.format(get2):
				many.append(get2[0])

	jcnt = len(many) - 1 
	bant = len(baim)
	BtoT()

def BtoT():
	global jnt
	ben = many[j]
	tjo = mc.listRelatives(ben)
	twi = tjo[0]
	if '_L' in '{}'.format(ben):
		a = ben.split('_bend_L')
		for i in get:
			if a[0] in i:
				if '_L' in '{}'.format(i):
					if 'bend' not in '{}'.format(i):
						if 'twist' not in '{}'.format(i):
							jnt = i
	elif '_R' in '{}'.format(ben):
		a = ben.split('_bend_R')
		for i in get:
			if a[0] in i:
				if '_R' in '{}'.format(i):
					if 'bend' not in '{}'.format(i):
						if 'twist' not in '{}'.format(i):
							jnt = i
	else:
		a = ben.split('_bend')
		for i in get:
			if a[0] in i:
				if '_L' not in '{}'.format(i):
					if '_R' not in '{}'.format(i):
						if 'bend' not in '{}'.format(i):
							if 'twist' not in '{}'.format(i):
								jnt = i
	
	if bant >= 1:
		for i in baim:
			if jnt in i:
				roop()

	#create node
	aim = mc.createNode('aimConstraint', n='{}_afterSplitTwistDriver'.format(jnt))
	mc.select('{}'.format(aim), r=True)
	mc.addAttr(ln='bend', nc=3, at='double3')
	mc.addAttr(ln='twist', nc=3, at='double3')
	for i in range(3):
		mc.addAttr(ln='bend{}'.format(xyz[i]), at='doubleAngle', p='bend', k=True)
		mc.addAttr(ln='twist{}'.format(xyz[i]), at='doubleAngle', p='twist', k=True)

	oc1 = mc.createNode('orientConstraint', n='{}_afterSplitTwist'.format(jnt))
	oc2 = mc.createNode('orientConstraint', n='{}_rot'.format(jnt))
	oc3 = mc.createNode('orientConstraint', n='{}_twistRot'.format(jnt))
	pb1 = mc.createNode('pairBlend', n='{}_weightedTwist'.format(jnt))
	mc.addAttr(ln='inRot2', nc=3, at='double3', w=False)
	for i in range(3):
		mc.addAttr(ln='inRot2{}'.format(xyz[0]), at='doubleAngle', p='inRot2', w=False)

	pb2 = mc.createNode('pairBlend', n='{}_rotSafeRot'.format(jnt))
	pb3 = mc.createNode('pairBlend', n='{}_twistRotSafeRot'.format(jnt))

	grp = mc.group('{}'.format(oc1),'{}'.format(oc2),'{}'.format(oc3), n='{}_BendTwist'.format(jnt))
	mc.parent('{}'.format(aim), '{}'.format(jnt))
	mc.parent('{}'.format(grp), '{}'.format(jnt))
	mc.setAttr('{}.visibility'.format(grp), 0)


	#setAttr
	mc.setAttr('{}.target[0].targetTranslateX'.format(aim), 1)
	mc.setAttr('{}.worldUpType'.format(aim), 4)
	mc.setAttr('{}.interpType'.format(oc2), 2)
	mc.setAttr('{}.interpType'.format(oc3), 2)
	mc.setAttr('{}.rotateMode'.format(pb2), 2)
	mc.setAttr('{}.rotateMode'.format(pb3), 2)
	mc.setAttr('{}.rotInterpolation'.format(pb2), 1)
	mc.setAttr('{}.rotInterpolation'.format(pb3), 1)
	for i in range(3):
		mc.setAttr('{0}.translate{1}'.format(aim, xyz[i]), 0)


	#connectAttr
	mc.connectAttr('{}.constraintRotate'.format(aim), '{}.bend'.format(aim))
	mc.connectAttr('{}.constraintRotate'.format(aim), '{}.constraintJointOrient'.format(oc1))
	mc.connectAttr('{}.constraintRotate'.format(oc1), '{}.twist'.format(aim))
	mc.connectAttr('{}.matrix'.format(aim), '{}.target[0].targetParentMatrix'.format(aim))
	mc.connectAttr('{}.matrix'.format(aim), '{}.target[0].targetParentMatrix'.format(oc1))
	mc.connectAttr('{}.bend'.format(aim), '{}.target[0].targetJointOrient'.format(oc2))
	mc.connectAttr('{}.twist'.format(aim), '{}.inRotate1'.format(pb1))
	mc.connectAttr('{}.inRot2'.format(pb1), '{}.inRotate2'.format(pb1))
	mc.connectAttr('{}.outRotate'.format(pb1), '{}.target[0].targetRotate'.format(oc2))
	mc.connectAttr('{}.constraintRotate'.format(oc2), '{}.inRotate2'.format(pb2))
	mc.connectAttr('{}.constraintRotate'.format(oc2), '{}.constraintJointOrient'.format(oc3))
	mc.connectAttr('{}.rotate'.format(jnt), '{}.target[0].targetRotate'.format(oc3))
	mc.connectAttr('{}.constraintRotate'.format(oc3), '{}.inRotate2'.format(pb3))
	mc.connectAttr('{}.twistWeight'.format(twi), '{}.weight'.format(pb1))
	for i in range(3):
		mc.connectAttr('{0}.rotate{1}'.format(jnt, xyz[i]), '{0}.rotate{1}'.format(aim, xyz[i]))
		mc.connectAttr('{0}.translate{1}'.format(jnt, xyz[i]), '{0}.translate{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.scale{1}'.format(jnt, xyz[i]), '{0}.scale{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.shear{1}'.format(jnt, she[i]), '{0}.shear{1}'.format(ben, she[i]))
		mc.connectAttr('{0}.scale{1}'.format(ben, xyz[i]), '{0}.scale{1}'.format(twi, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb2, xyz[i]), '{0}.rotate{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb3, xyz[i]), '{0}.rotate{1}'.format(twi, xyz[i]))

	roop()

def roop():
	global j

	if j < jcnt:
		j+=1
		BtoT()

	TwistBend_gimmick.cntTwistJnt()