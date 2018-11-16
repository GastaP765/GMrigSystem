import maya.cmds as mc

def createTwistBend():
	#create joint
	jnt = mc.ls(sl=True)
	for i in range(len(jnt)):
		mc.select(jnt[i])
		par = mc.listRelatives('{}'.format(jnt[i]), p=True)
		twi_trs = mc.getAttr('{}.translateX'.format(jnt[i]))
		jnt_trs = mc.getAttr('{}.worldMatrix[0]'.format(jnt[i]))
		jnt_rad = mc.getAttr('{}.radius'.format(jnt[i]))
		par_trs = mc.getAttr('{}.worldMatrix[0]'.format(par[0]))
		jnt_orix = mc.getAttr('{}.jointOrientX'.format(jnt[i]))
		jnt_oriy = mc.getAttr('{}.jointOrientY'.format(jnt[i]))
		jnt_oriz = mc.getAttr('{}.jointOrientZ'.format(jnt[i]))
		twi_trs = twi_trs / 2

		a = jnt[i]
		if '_L' in '{}'.format(a):
			b = a.replace('_L', '')
			jnt[i] = b
			twi = mc.joint(n='{}_twist_L'.format(jnt[i]), rad=jnt_rad * 0.7, p=(par_trs[12],par_trs[13],par_trs[14]))
			ben = mc.joint(n='{}_bend_L'.format(jnt[i]), rad=jnt_rad * 0.7, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
		elif '_R' in '{}'.format(a):
			b = a.replace('_R', '')
			jnt[i] = b
			twi = mc.joint(n='{}_twist_R'.format(jnt[i]), rad=jnt_rad * 0.7, p=(par_trs[12],par_trs[13],par_trs[14]))
			ben = mc.joint(n='{}_bend_R'.format(jnt[i]), rad=jnt_rad * 0.7, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))
		else:
			twi = mc.joint(n='{}_twist'.format(jnt[i]), rad=jnt_rad * 0.7, p=(par_trs[12],par_trs[13],par_trs[14]))
			ben = mc.joint(n='{}_bend'.format(jnt[i]), rad=jnt_rad * 0.7, p=(jnt_trs[12],jnt_trs[13],jnt_trs[14]))

		mc.parent('{}'.format(twi), '{}'.format(par[0]))
		mc.joint('{}'.format(twi), e=True, oj='xyz', sao='yup')
		mc.setAttr('{}.translateX'.format(twi), twi_trs)
		mc.setAttr('{}.translateX'.format(ben), twi_trs)
		mc.setAttr('{}.jointOrientX'.format(twi), 0)
		mc.setAttr('{}.jointOrientY'.format(twi), 0)
		mc.setAttr('{}.jointOrientZ'.format(twi), 0)
		mc.setAttr('{}.jointOrientX'.format(ben), jnt_orix)
		mc.setAttr('{}.jointOrientY'.format(ben), jnt_oriy)
		mc.setAttr('{}.jointOrientZ'.format(ben), jnt_oriz)
