import maya.cmds as mc
import Console

xyz = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
swt = 0
def preparation(give_sst='', give_tar='', give_sdv='', give_many=''):
    global sdv, sst, tar, atn, atr, many, tar_trs

    sst = give_sst
    tar = give_tar
    sdv = give_sdv
    many = give_many

    tar_trs = mc.getAttr('{}.tx'.format(tar))
    atr = mc.listAttr(sdv, c=True)
    if many != 0:
        tar_trs = tar_trs / many
        atn = 1.0000 / many
    else:
        tar_trs = 0
    
    check()

def check():
    global atn, many, sdv, tar_trs, atr, exi, chk

    chk = mc.listRelatives('{}'.format(sdv), p=True)
    kep = mc.listRelatives('{}'.format(chk[0]))
    exi = 0

    if 'weighted' in '{}'.format(kep):
        cnt = len(kep)
        rem = list(range(0))

        for i in range(cnt):
            if 'weighted' in kep[i]:
                rem.append(kep[i])

        exi = len(rem)
    if 'weight' in '{}'.format(atr):
        atr_cnt = len(atr)
        wgt_atr = list(range(0))
        for i in range(atr_cnt):
            if 'weight' in atr[i]:
                wgt_atr.append(atr[i])

    if exi >= 1:
        for i in range(exi):
            mc.setAttr('{}.tx'.format(rem[i]), tar_trs*(i))

    if many < exi:
        for i in range(exi - many):
            rmv = exi - i - 1
            mc.delete(rem[rmv])
            if 'weight{}'.format(xyz[rmv]) in wgt_atr[rmv]:
                mc.deleteAttr('{0}.{1}'.format(sdv, wgt_atr[rmv]))
            
        mirror()

    nameEdit()

def nameEdit():
    global nme, ene

    nme = sdv
    ene = ''
    if '_L' in sdv:
        nme = sdv.replace('_L', '')
        ene = 'L'
    if '_R' in sdv:
        nme = sdv.replace('_R', '')
        ene = 'R'

    create()

def create():

    wgt = list(range(0))
    for i in range(many):
        f = i + exi

        cjo = mc.joint(n='{0}_weighted_{1}{2}'.format(nme, xyz[f], ene), rad=0.3, p=(0, 0, 0))
        pbd = mc.createNode('pairBlend', n='{0}_ifTwistWeightedBlend_{1}{2}'.format(sdv,xyz[f], ene))
        if 'weight{0}{1}'.format(xyz[f], ene) not in atr:
            mc.addAttr('{}'.format(sdv), ln='weight{0}{1}'.format(xyz[f], ene), min=0, max=1, dv=1)
        mc.parent('{}'.format(cjo), '{}'.format(chk[0]))
        mc.setAttr('{}.translate'.format(cjo), 0, 0, 0)
        mc.setAttr('{}.translateX'.format(cjo), tar_trs*(f))
        mc.setAttr('{}.jointOrient'.format(cjo), 0, 0, 0)
        mc.setAttr('{0}.weight{1}{2}'.format(sdv, xyz[f], ene), atn*f)
        mc.connectAttr('{0}.weight{1}{2}'.format(sdv, xyz[f], ene), '{}.weight'.format(pbd))
        mc.connectAttr('{}.rotateX'.format(sdv), '{}.inRotate2.inRotateX2'.format(pbd))
        mc.connectAttr('{}.outRotateX'.format(pbd), '{}.rotateX'.format(cjo))
        mc.select(cl=True)
        wgt.append(cjo)
        if f == many:
            break

    if exi >= 1:
        mc.delete('{}'.format(cjo))
        wgt.remove(cjo)

    mirror()

def mirrorswt():
    global swt, coa, k, j
    swt = 1
    con = list(range(0))
    coa = list(range(0))
    k = 0
    j = 0
    jnt = mc.ls(typ='joint')

    for i in jnt:
        if 'weighted' in '{}'.format(i):
            con.append(i)

    for i in con:    
        if 'weighted_AL' in '{}'.format(i):
            coa.append(i)
            k = k + 1 

    mirror()

def mirror():
    global tar_trs, sdv, j, swt

    if swt == 0:
        return
    elif swt == 1:
        if j == len(coa):
            return

    cob = mc.listRelatives(coa[j], p=True)
    coc = mc.listRelatives(cob[0])

    for i in coc:
        if 'weighted' in '{}'.format(i):
            if 'weighted_BL' in '{}'.format(i):
                tar_trs = mc.getAttr('{}.tx'.format(i))
                tar_trs = tar_trs * -1
        else:
            sdv = i.replace('_L', '_R')

    j = j + 1
    check()

