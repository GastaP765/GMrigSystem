import maya.cmds as mc
import sys

xyz = 'XYZ'
she = 'XY', 'XZ', 'YZ'


def cntTwistJnt():
	global many, j, get, jcnt, taim, tant

	many = []
	taim = []
	j = 0
	
	get = mc.ls(typ='joint')
	exi = mc.ls(typ='aimConstraint')
	for i in exi:
		if 'beforeSplitTwistDriver' in '{}'.format(i):
			taim.append(i)

	for i in get:
		if 'bend' in '{}'.format(i):
			get2 = mc.listRelatives(i, p=True)
			if 'twist' in '{}'.format(get2):
				many.append(i)

	jcnt = len(many) - 1
	tant = len(taim)
	TtoB()

def TtoB():
	ben = many[j]
	twi = mc.listRelatives(ben, p=True)
	a = ben.split('_bend')
	if '_L' in '{}'.format(twi):
		for i in get:
			if a[0] in i:
				if '_L' in '{}'.format(i):
					if 'bend' not in '{}'.format(i):
						if 'twist' not in '{}'.format(i):
							b = mc.listRelatives(i, typ='joint')
							jnt = i
	elif '_R' in '{}'.format(twi):
		for i in get:
			if a[0] in i:
				if '_R' in '{}'.format(i):
					if 'bend' not in '{}'.format(i):
						if 'twist' not in '{}'.format(i):
							b = mc.listRelatives(i, typ='joint')
							jnt = i
	else:
		for i in get:
			if a[0] in i:
				if '_L' not in '{}'.format(i):
					if '_R' not in '{}'.format(i):
						if 'bend' not in '{}'.format(i):
							if 'twist' not in '{}'.format(i):
								b = mc.listRelatives(i, typ='joint')
								jnt = i
	
	if tant >= 1:
		for i in taim:
			if b[0] in i:
				roop()
	
	par = mc.listRelatives(twi[0], p=True)
	tar = mc.listRelatives(jnt)

	jnt_orix = mc.getAttr('{}.jointOrientX'.format(jnt))
	jnt_oriy = mc.getAttr('{}.jointOrientY'.format(jnt))
	jnt_oriz = mc.getAttr('{}.jointOrientZ'.format(jnt))
	jnt_rot = [-1 * jnt_orix, -1 * jnt_oriy, -1 * jnt_oriz] 

	
	#vectorCalculation
	co1 = mc.createNode('composeMatrix')
	co2 = mc.createNode('composeMatrix')
	inv = mc.createNode('inverseMatrix')
	mlt = mc.createNode('multMatrix')
	dec = mc.createNode('decomposeMatrix')
	trs = mc.createNode('transform')

	mc.connectAttr('{}.translate'.format(tar[0]), '{}.inputTranslate'.format(co1))
	mc.connectAttr('{}.scale'.format(tar[0]), '{}.inputScale'.format(co1))
	mc.connectAttr('{}.rotate'.format(tar[0]), '{}.inputRotate'.format(co1))
	mc.connectAttr('{}.shear'.format(tar[0]), '{}.inputShear'.format(co1))
	mc.connectAttr('{}.scale'.format(jnt), '{}.inputScale'.format(co2))
	mc.connectAttr('{}.jointOrient'.format(jnt), '{}.inputRotate'.format(co2))
	mc.connectAttr('{}.shear'.format(jnt), '{}.inputShear'.format(co2))
	mc.connectAttr('{}.outputMatrix'.format(co2), '{}.inputMatrix'.format(inv))
	mc.connectAttr('{}.outputMatrix'.format(co1), '{}.matrixIn[0]'.format(mlt))
	mc.connectAttr('{}.outputMatrix'.format(inv), '{}.matrixIn[1]'.format(mlt))
	mc.connectAttr('{}.matrixSum'.format(mlt), '{}.inputMatrix'.format(dec))
	mc.connectAttr('{}.outputRotate'.format(dec), '{}.rotate'.format(trs))
	mc.connectAttr('{}.outputTranslate'.format(dec), '{}.translate'.format(trs))
	mc.connectAttr('{}.outputScale'.format(dec), '{}.scale'.format(trs))
	mc.connectAttr('{}.outputShear'.format(dec), '{}.shear'.format(trs))
	mc.parent('{}'.format(trs), '{}'.format(jnt))
	mat = mc.getAttr('{}.matrix'.format(trs))
	mc.delete('{}'.format(co2), '{}'.format(inv), '{}'.format(mlt), '{}'.format(dec), '{}'.format(trs))


	#createNode
	aim = mc.createNode('aimConstraint', n='{}_beforeSplitTwistDriver'.format(tar[0]))
	mc.addAttr(ln='bend', nc=3, at='double3')
	mc.addAttr(ln='twist', nc=3, at='double3')
	for i in range(3):
		mc.addAttr(ln='bend{}'.format(xyz[i]), at='doubleAngle', p='bend')
		mc.addAttr(ln='twist{}'.format(xyz[i]), at='doubleAngle', p='twist')

	oc1 = mc.createNode('orientConstraint', n='{}_beforeSplitTwist'.format(jnt))
	oc2 = mc.createNode('orientConstraint', n='{}_bendRot'.format(jnt))
	oc3 = mc.createNode('orientConstraint', n='{}_twistRot'.format(jnt))
	pb1 = mc.createNode('pairBlend', n='{}_weightedTwist'.format(jnt))
	pb2 = mc.createNode('pairBlend', n='{}_bendRotSafeRot'.format(jnt))
	pb3 = mc.createNode('pairBlend', n='{}_twistRotSafeRot'.format(jnt))

	mc.parent('{}'.format(aim), '{}'.format(jnt))
	mc.parent('{}'.format(oc1), '{}'.format(jnt))
	mc.parent('{}'.format(oc2), '{}'.format(ben))
	mc.parent('{}'.format(oc3), '{}'.format(twi[0]))


	#setAttr
	mc.setAttr('{}.worldUpType'.format(aim), 4)
	mc.setAttr('{}.rotateMode'.format(pb2), 2)
	mc.setAttr('{}.rotateMode'.format(pb3), 2)
	mc.setAttr('{}.rotInterpolation'.format(pb2), 1)
	mc.setAttr('{}.rotInterpolation'.format(pb3), 1)
	mc.setAttr('{}.scaleCompensate'.format(aim), False)
	for i in range(3):
		mc.setAttr('{0}.aimVector{1}'.format(aim, xyz[i]), mat[i])
		mc.setAttr('{0}.target[0].targetTranslate{1}'.format(aim, xyz[i]), mat[i])
		mc.setAttr('{0}.translate{1}'.format(aim, xyz[i]), 0)
		mc.setAttr('{0}.translate{1}'.format(oc1, xyz[i]), 0)
		mc.setAttr('{0}.translate{1}'.format(oc2, xyz[i]), 0)
		mc.setAttr('{0}.translate{1}'.format(oc3, xyz[i]), 0)
		mc.setAttr('{0}.target[0].targetRotate{1}'.format(oc3, xyz[i]), jnt_rot[i])
		mc.setAttr('{0}.constraintJointOrient{1}'.format(oc3, xyz[i]), jnt_rot[i])


	#connectAttr
	mc.connectAttr('{}.constraintRotate'.format(aim), '{}.bend'.format(aim))
	mc.connectAttr('{}.constraintRotate'.format(aim), '{}.constraintJointOrient'.format(oc1))
	mc.connectAttr('{}.matrix'.format(aim), '{}.target[0].targetParentMatrix'.format(aim))
	mc.connectAttr('{}.matrix'.format(aim), '{}.target[0].targetParentMatrix'.format(oc1))
	mc.connectAttr('{}.twist'.format(aim), '{}.inRotate2'.format(pb1))
	mc.connectAttr('{}.constraintRotate'.format(oc1), '{}.twist'.format(aim))
	mc.connectAttr('{}.constraintRotate'.format(oc2), '{}.inRotate2'.format(pb2))
	mc.connectAttr('{}.constraintRotate'.format(oc3), '{}.inRotate2'.format(pb3))
	mc.connectAttr('{}.outRotate'.format(pb1), '{}.constraintJointOrient'.format(oc2))
	mc.connectAttr('{}.outRotate'.format(pb1), '{}.target[0].targetJointOrient'.format(oc3))
	for i in range(3):
		mc.connectAttr('{0}.scale{1}'.format(jnt, xyz[i]), '{0}.scale{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.shear{1}'.format(jnt, she[i]), '{0}.shear{1}'.format(ben, she[i]))
		mc.connectAttr('{0}.scale{1}'.format(par[0], xyz[i]), '{0}.scale{1}'.format(twi[0], xyz[i]))
		mc.connectAttr('{0}.shear{1}'.format(par[0], she[i]), '{0}.shear{1}'.format(twi[0], she[i]))
		mc.connectAttr('{0}.rotate{1}'.format(jnt, xyz[i]), '{0}.rotate{1}'.format(aim, xyz[i]))
		mc.connectAttr('{0}.rotate{1}'.format(jnt, xyz[i]), '{0}.target[0].targetRotate{1}'.format(oc2, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb2, xyz[i]), '{0}.rotate{1}'.format(ben, xyz[i]))
		mc.connectAttr('{0}.outRotate{1}'.format(pb3, xyz[i]), '{0}.rotate{1}'.format(twi[0], xyz[i]))

	roop()

def roop():
	global j

	if j < jcnt:
		j+=1
		TtoB()

	sys.exit()