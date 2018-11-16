import maya.cmds as mc

def duplicate():
    xyz = 'xyz'
    shi = ['xy', 'xz', 'yz']

    jnt = mc.ls(sl=True)
    b = jnt[0]
    e = b.replace('bind', 'skin')
    mc.duplicate(jnt[0], n=e)
    a = mc.listRelatives(e, ad=True, f=True)
    b = mc.listRelatives(jnt[0], ad=True, f=True)
    f = mc.getAttr('{}.radius'.format(e))
    mc.setAttr('{}.radius'.format(e), f*1.5)
    cnt = 0

    for i in a:
        c = i.split('|')
        d = c[-1]
        e = d.replace('bind', 'skin')

        mc.rename(i, e)
        f = mc.getAttr('{}.radius'.format(d))
        mc.setAttr('{}.radius'.format(e), f*1.5)
        for j in range(3):
            mc.connectAttr('{0}.t{1}'.format(b[cnt], xyz[j]), '{0}.t{1}'.format(e, xyz[j]))
            mc.connectAttr('{0}.r{1}'.format(b[cnt], xyz[j]), '{0}.r{1}'.format(e, xyz[j]))
            mc.connectAttr('{0}.s{1}'.format(b[cnt], xyz[j]), '{0}.s{1}'.format(e, xyz[j]))
            mc.connectAttr('{0}.sh{1}'.format(b[cnt], shi[j]), '{0}.sh{1}'.format(e, shi[j]))

        a = mc.listRelatives(e, ad=True, f=True)
        cnt+=1