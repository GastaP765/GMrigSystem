import maya.cmds as mc
import ui

xyz = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def Preparation(give_cb1='', give_cb2='', give_cb3='', give_cb4=''):
	global jnt, cnt, many, j, k, py, my, pz, mz

	jnt = mc.ls(sl=True)
	cnt = len(jnt)
	py = give_cb1
	my = give_cb2
	pz = give_cb3
	mz = give_cb4
	many = 0
	j = 0
	k = 0
	
	check()

def check():
	global py, my, pz, mz, many

	if py == 1:
		many+=1
	if my == 1:
		many+=1
	if pz == 1:
		many+=1
	if mz == 1:
		many+=1

	station()

def station():
	global par, py, my, pz, mz

	par = mc.listRelatives(jnt[j], p=True)
	if py == 1:
		py = 0
		PlusY()
	elif my == 1:
		my = 0
		MinusY()
	elif pz == 1:
		pz = 0
		PlusZ()
	elif mz == 1:
		mz = 0
		MinusZ()

def PlusY():
	mc.select(cl=True)
	exp = mc.joint(n='{0}_expand{1}'.format(jnt[j], xyz[k]), rad=0.3)
	grp = mc.group(exp, n='{0}_expSpace{1}'.format(jnt[j], xyz[k]))
	mc.parent(grp, jnt[j])
	mc.setAttr('{}.translate'.format(grp), 0, 1, 0)
	mc.setAttr('{}.rotate'.format(grp), 0, 0, 0)

	roop()

def MinusY():
	mc.select(cl=True)
	exp = mc.joint(n='{0}_expand{1}'.format(jnt[j], xyz[k]), rad=0.3)
	grp = mc.group(exp, n='{0}_expSpace{1}'.format(jnt[j], xyz[k]))
	mc.parent(grp, jnt[j])
	mc.setAttr('{}.translate'.format(grp), 0, -1, 0)
	mc.setAttr('{}.rotate'.format(grp), 0, 0, 0)

	roop()

def PlusZ():
	mc.select(cl=True)
	exp = mc.joint(n='{0}_expand{1}'.format(jnt[j], xyz[k]), rad=0.3)
	grp = mc.group(exp, n='{0}_expSpace{1}'.format(jnt[j], xyz[k]))
	mc.parent(grp, jnt[j])
	mc.setAttr('{}.translate'.format(grp), 0, 0, 1)
	mc.setAttr('{}.rotate'.format(grp), 0, 0, 0)

	roop()

def MinusZ():
	mc.select(cl=True)
	exp = mc.joint(n='{0}_expand{1}'.format(jnt[j], xyz[k]), rad=0.3)
	grp = mc.group(exp, n='{0}_expSpace{1}'.format(jnt[j], xyz[k]))
	mc.parent(grp, jnt[j])
	mc.setAttr('{}.translate'.format(grp), 0, 0, -1)
	mc.setAttr('{}.rotate'.format(grp), 0, 0, 0)

	roop()

def roop():
	global k, j

	if k < many:
		k+=1
		station()

	if j < cnt - 1:
		j+=1
		k = 0
		check()
