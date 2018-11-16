import maya.cmds as mc

def Preparation(give_rc1='', give_rc2=''):
	trs = list(range(0))
	slc = mc.ls(sl=True)
	StoH = give_rc1
	JtoT = give_rc2

	if StoH == 'selb':
		cnt = len(slc)
		for i in range(cnt):
			trs.append(mc.getAttr('{}.wm'.format(slc[i])))

	elif StoH == 'hieb':
		par = mc.listRelatives('{}'.format(slc[0]), ad=True, typ=('transform', 'joint'))
		par.append(slc[0])
		slc = list(range(0))
		cnt = len(par)
		for i in range(cnt):
			slc.append(par[i])
			trs.append(mc.getAttr('{}.wm'.format(slc[i])))


	for i in range(cnt):
		par = mc.listRelatives('{}'.format(slc[i]), p=True)
		if  par is not None:
			if '{}_space'.format(slc[i]) == par[0]:
				continue
		if JtoT == 'trsb':
			spc = mc.createNode('transform', n='{}_space'.format(slc[i]))
		elif JtoT == 'jntb':
			typ = mc.ls('{}'.format(slc[i]), st=True)
			if typ[1] == 'joint':
				rad = mc.getAttr('{}.radius'.format(slc[i]))
				spc = mc.createNode('joint', n='{}_space'.format(slc[i]))
				mc.setAttr('{}.radius'.format(spc), rad*1.3)
			elif typ[1] == 'transform':
				spc = mc.createNode('joint', n='{}_space'.format(slc[i]))
				mc.setAttr('{}.radius'.format(spc), 0.8)
			
		mc.setAttr('{}.t'.format(spc), trs[i][12], trs[i][13], trs[i][14])
		if  par is not None:
			mc.parent(spc, par[0])
		mc.parent(slc[i], spc)
		mc.setAttr('{}.t'.format(slc[i]), 0, 0, 0)
