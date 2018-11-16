import maya.cmds as mc
import AngleDriver
import BendTwist_createJoint
import BendTwist_gimmick
import createExpand
import CreateSpacer
import CreateWeighted
import duplicate_skinJnt
import TwistBend_createJoint
import TwistBend_gimmick

def give_duplicate_skinJnt(*args):
	duplicate_skinJnt.duplicate()

def give_BendTwist_createJoint(*args):
	BendTwist_createJoint.createBendTwist()

def give_TwistBend_createJoint(*args):
	TwistBend_createJoint.createTwistBend()

def gimmick(*args):
	BendTwist_gimmick.cntBendJnt()

def give_weighted(*args):
	a = mc.textField(stt, q=True, text=True)
	b = mc.textField(end, q=True, text=True)
	c = mc.textField(drv, q=True, text=True)
	d = mc.intField(num, q=True, v=True)
	CreateWeighted.preparation(give_sst=a, give_tar=b, give_sdv=c, give_many=d)

def give_AngleDriver(*args):
	AngleDriver.AngleD()

def give_CreateWeighted(*args):
	CreateWeighted.mirrorswt()

def give_Spacer(*args):
	a = mc.radioCollection(rc1, q=True, select=True)
	b = mc.radioCollection(rc2, q=True, select=True)
	CreateSpacer.Preparation(give_rc1=a, give_rc2=b)

def give_Expand(*args):
	a = mc.checkBox('cb1', q=True, v=True)
	b = mc.checkBox('cb2', q=True, v=True)
	c = mc.checkBox('cb3', q=True, v=True)
	d = mc.checkBox('cb4', q=True, v=True)
	createExpand.Preparation(give_cb1=a, give_cb2=b, give_cb3=c, give_cb4=d)

def set_drv(*args):
	sub = mc.ls(sl=True)
	mc.textField(drv, e=True, text='{}'.format(sub[0]))

def stt_set(*args):
	sub = mc.ls(sl=True)
	con = mc.listRelatives(sub[0])
	mc.textField(stt, e=True, text='{}'.format(sub[0]))
	mc.textField(end, e=True, text='{}'.format(con[0]))

def end_set(*args):
	sub = mc.ls(sl=True)
	con = mc.listRelatives(sub[0], p=True)
	mc.textField(stt, e=True, text='{}'.format(con[0]))
	mc.textField(end, e=True, text='{}'.format(sub[0]))

def develop(*args):
	reload(AngleDriver)
	reload(BendTwist_createJoint)
	reload(BendTwist_gimmick)
	reload(createExpand)
	reload(CreateSpacer)
	reload(CreateWeighted)
	reload(duplicate_skinJnt)
	reload(TwistBend_createJoint)
	reload(TwistBend_gimmick)

def mainWin():
	global num, drv, stt, end ,cb1, cb2, cb3, cb4, rc1, rb1, rb2, rc2, rb3, rb4
	if mc.window('GMR', ex=True) == True:
		mc.deleteUI('GMR', window=True)

	win = mc.window('GMR', t='GMrigGimmick', widthHeight=(300, 765))
	mc.window('GMR', e=True, widthHeight=(300, 765))

	#skinJoint-----------------------------------------------------------------------------------
	mc.columnLayout(adj=True)
	mc.frameLayout(l='duplicateSkinJoint', cll=True)
	mc.button(l='skinJoint', w=300, h=30, c=give_duplicate_skinJnt)
	mc.setParent('..')
	#----------------------------------------------------------------------------------------------
	mc.separator(h=10)
	#Bend Twist----------------------------------------------------------------------------------
	mc.frameLayout(l='Create Gimmick Joint', cll=True)
	mc.rowLayout(nc=2)
	mc.button(l='Bend->Twist', w=150, h=30, c=give_BendTwist_createJoint)
	mc.button(l='Twist->Bend', w=150, h=30, c=give_TwistBend_createJoint)
	mc.setParent('..')
	mc.button(l='Connect Gimmick Node', w=300, h=30, c=gimmick)
	mc.setParent('..')
	#----------------------------------------------------------------------------------------------
	mc.separator(h=10)
	#CreateWeighted--------------------------------------------------------------------------------
	mc.frameLayout(l='createWeighted', cll=True)
	mc.frameLayout(l='weighted')
	mc.rowLayout(nc=2, cat=[(1, 'left', 0), (2, 'left', 5)])
	mc.text(' Create many weighted : ')
	num = mc.intField('num', w=145)
	mc.setParent('..')
	mc.rowLayout(nc=3, cat=[(1, 'left', 0), (2, 'left', 5)])
	mc.text(' set drover :')
	drv = mc.textField('drv', w=170)
	mc.button(l='set', w=45, h=20, c=set_drv)
	mc.setParent('..')
	mc.setParent('..')

	mc.frameLayout(l='Range to create weighted')
	mc.rowLayout(nc=3, cat=[(1, 'left', 35), (2, 'left', 5)])
	mc.text('start :')
	stt = mc.textField('stt', w=170)
	mc.button(l='set', w=45, h=20, c=stt_set)
	mc.setParent('..')
	mc.rowLayout(nc=3, cat=[(1, 'left', 42), (2, 'left', 5)])
	mc.text('end :')
	end = mc.textField('end', w=170)
	mc.button(l='set', w=45, h=20, c=end_set)
	mc.setParent('..')
	mc.setParent('..')

	mc.rowLayout(nc=2, w=300)
	mc.button(l='weighted', w=150, h=30, c=give_weighted)
	mc.button(l='mirror', w=150, h=30, c=give_CreateWeighted)
	mc.setParent('..')
	mc.setParent('..')
	#----------------------------------------------------------------------------------------------
	mc.separator(h=10)
	#AngleDriver-----------------------------------------------------------------------------------
	mc.frameLayout(l='setAngleDriver', cll=True)
	mc.button(l='setAngleDriver', c=give_AngleDriver)
	mc.setParent('..')
	#----------------------------------------------------------------------------------------------
	mc.separator(h=10)
	#createExpand----------------------------------------------------------------------------------
	mc.frameLayout(l='createExpand', cll=True)
	mc.rowLayout(nc=4, cat=[(1, 'left', 17), (2, 'left', 35), (3, 'left', 35), (4, 'left', 35)])
	cb1 = mc.checkBox('cb1', l='+Y')
	cb2 = mc.checkBox('cb2', l='-Y')
	cb3 = mc.checkBox('cb3', l='+Z')
	cb4 = mc.checkBox('cb4', l='-Z')
	mc.setParent('..')
	mc.button(l='createExpand', c=give_Expand)
	mc.setParent('..')
	#----------------------------------------------------------------------------------------------
	mc.separator(h=10)
	#CreateSpacer----------------------------------------------------------------------------------
	mc.frameLayout(l='CreateSpacer', cll=True)
	mc.frameLayout(l='Type Select')
	mc.rowLayout(nc=2, cat=[(1, 'left', 50), (2, 'left', 65)])
	rc1 = mc.radioCollection()
	rb1 = mc.radioButton('selb', l='select', select=True)
	rb2 = mc.radioButton('hieb', l='hierachy')
	mc.setParent('..')
	mc.setParent('..')

	mc.frameLayout(label='Node Select')
	mc.rowLayout(nc=2, cat=[(1, 'left', 50), (2, 'left', 40)])
	rc2 = mc.radioCollection()
	rb3 = mc.radioButton('trsb', l='Transform', select=True)
	rb4 = mc.radioButton('jntb', l='joint')
	mc.setParent('..')
	mc.setParent('..')

	mc.button(l='create', c=give_Spacer)
	mc.setParent('..')
	#----------------------------------------------------------------------------------------------
	mc.separator(h=10)
	mc.frameLayout(l='reload module')
	mc.button(l='reload', c=develop)

	mc.showWindow(win)

def consoleKey():
	mainWin()