import maya.cmds as mc

xyz = 'XYZ'
she = 'XY', 'XZ', 'YZ'

def createBendTwist():

	#create joint
	jnt = mc.ls(sl=True)
	jnt_rot = [0.0, 0.0, 0.0]
	for i in range(len(jnt)):
		mc.select(jnt[i])
		tar = mc.listRelatives('{}'.format(jnt[i]))
		par = mc.listRelatives('{}'.format(jnt[i]), p=True)
		jnt_trs = mc.getAttr('{}.worldMatrix[0]'.format(jnt[i]))
		jnt_rad = mc.getAttr('{}.radius'.format(jnt[i]))
		tar_trs = mc.getAttr('{}.translateX'.format(tar[0]))
		for j in range(3):
			jnt_rot[j] = mc.getAttr('{0}.jointOrient{1}'.format(jnt[i], xyz[j]))

		a = jnt[i]
		if '_L' in '{}'.format(a):
			b = a.replace('_L', '')
			jnt[i] = b
			ben = mc.joint(n='{}_bend_L'.format(jnt[i]), rad=jnt_rad * 0.7, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
			twi = mc.joint(n='{}_twist_L'.format(jnt[i]), rad=jnt_rad * 0.7, p=(tar_trs, 0, 0))
		elif '_R' in '{}'.format(a):
			b = a.replace('_R', '')
			jnt[i] = b
			ben = mc.joint(n='{}_bend_R'.format(jnt[i]), rad=jnt_rad * 0.7, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
			twi = mc.joint(n='{}_twist_R'.format(jnt[i]), rad=jnt_rad * 0.7, p=(tar_trs, 0, 0))
		else:
			ben = mc.joint(n='{}_bend'.format(jnt[i]), rad=jnt_rad * 0.7, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
			twi = mc.joint(n='{}_twist'.format(jnt[i]), rad=jnt_rad * 0.7, p=(tar_trs, 0, 0))

		mc.joint('{}'.format(ben), e=True, oj='xyz', sao='yup')
		for j in range(3):
			mc.setAttr('{0}.jointOrient{1}'.format(twi, xyz[j]), 0)

		tar_trs = tar_trs / 2
		mc.setAttr('{}.translateX'.format(twi), tar_trs)
		mc.addAttr('{}'.format(twi), ln='twistWeight', min=0, max=1, dv=1, k=True)
		if par is not None:
			mc.parent('{}'.format(ben), '{}'.format(par[0]))
		elif par is None:
			mc.parent('{}'.format(ben), w=True)
		
		for j in range(3):
			mc.setAttr('{0}.jointOrient{1}'.format(ben, xyz[j]), jnt_rot[j])
