import maya.cmds as mc

xyz = 'XYZ'
she = ['XY', 'XZ', 'YZ']

def AngleD():
	exps = list(range(0))

	jnt = mc.ls(sl=True)
	mc.addAttr(ln='bendH', sn='bh', k=True, at='doubleAngle')
	mc.addAttr(ln='bendV', sn='bv', k=True, at='doubleAngle')
	mc.addAttr(ln='aimVector', nc=3, at='double3')
	for i in range(3):
		mc.addAttr(ln='aimVector{}'.format(xyz[i]), at='double', p='aimVector')

	spc = mc.group(em=True, n='{}_driver'.format(jnt[0]))
	mc.parent(spc, jnt[0])
	for i in range(3):
		mc.setAttr('{0}.translate{1}'.format(spc, xyz[i]), 0)
		mc.setAttr('{0}.rotate{1}'.format(spc, xyz[i]), 0)


	#createNode
	vep = mc.createNode('vectorProduct', n='{}_vectorProduct'.format(jnt[0]))
	exp = mc.expression(n='{}_Exp'.format(jnt[0]), o='{}'.format(jnt[0]))
	mc.expression(exp, e=True, uc='none', ae=0)


	#setAttr
	mc.setAttr('{}.input1X'.format(vep), 1.0)
	mc.setAttr('{}.operation'.format(vep), 3)
	mc.setAttr('{}.normalizeOutput'.format(vep), True)

	#connectAttr
	mc.connectAttr('{}.matrix'.format(spc), '{}.matrix'.format(vep))
	mc.connectAttr('{0}.output[0]'.format(exp), '{}.bendH'.format(jnt[0]))
	mc.connectAttr('{0}.output[1]'.format(exp), '{}.bendV'.format(jnt[0]))
	for i in range(3):
		mc.connectAttr('{0}.output{1}'.format(vep, xyz[i]), '{0}.aimVector{1}'.format(jnt[0], xyz[i]))
		mc.connectAttr('{0}.aimVector{1}'.format(jnt[0], xyz[i]), '{0}.input[{1}]'.format(exp, i))
		mc.connectAttr('{0}.translate{1}'.format(jnt[0], xyz[i]), '{0}.translate{1}'.format(spc, xyz[i]))
		mc.connectAttr('{0}.rotate{1}'.format(jnt[0], xyz[i]), '{0}.rotate{1}'.format(spc, xyz[i]))
		mc.connectAttr('{0}.scale{1}'.format(jnt[0], xyz[i]), '{0}.scale{1}'.format(spc, xyz[i]))
		mc.connectAttr('{0}.shear{1}'.format(jnt[0], she[i]), '{0}.shear{1}'.format(spc, she[i]))


	#expression
	exps.append('vector $x_vec = <<1., .0, .0>>;')
	exps.append('vector $y_vec = <<.0, 1., .0>>;')
	exps.append('vector $z_vec = <<.0, .0, 1.>>;')
	exps.append('vector $vec = <<' + jnt[0] + '.aimVectorX, ')
	exps.append(jnt[0] + '.aimVectorY, ' + jnt[0] + '.aimVectorZ>>;')
	exps.append('float $aim = dot($x_vec, $vec) + 1;')
	exps.append(jnt[0] + '.bendH = atan2(dot($z_vec, $vec), $aim) * -2.;')
	exps.append(jnt[0] + '.bendV = atan2(dot($y_vec, $vec), $aim) * 2.;')
	imp = ''.join(exps)
	mc.expression(exp, e=True, s='{}'.format(imp))
