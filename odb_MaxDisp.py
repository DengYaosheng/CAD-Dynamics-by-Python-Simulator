# -*- coding: utf-8 -*-
from abaqus import *
from abaqusConstants import *
import visualization
import displayGroupOdbToolset as dgo

# 提取最大应力，并在工作目录下建立Result_U1U2U3.txt保存信息
f = open('Result_U1U2U3.txt','w')
mat="{:^16s}\t{:^16}\t{:^16}\t{:^16}\t{:^16s}\t"
w1=mat.format('step','max_U1','max_U2','max_U3','frame')
fenge = '-' * 100
f.write(w1)
f.write('\n%s\n'%fenge)
vp = session.viewports[session.currentViewportName]
odb = vp.displayedObject
if type(odb) != visualization.OdbType: 
    raise 'Please open an .odb file.'
maxValue_U1 = None
maxValue_U2 = None
maxValue_U3 = None
stressOutputExists = FALSE
GuanDi=odb.rootAssembly.instances['TANK-1'].nodeSets['SET-8']
frame_tik = -1
for step in odb.steps.values():
    print 'searching step:', step.name
    for frame in step.frames:
        try: 
            stress = frame.fieldOutputs['U'].getSubset(region=GuanDi)
            stressOutputExists = TRUE
        except KeyError:
            continue
        max_Mises_U1,max_Mises_U2,max_Mises_U3 = -0.1,-0.1,-0.1
        for stressValue in stress.values:
            # U1
            if (not maxValue_U1 or
                    abs(stressValue.data[0]) > abs(maxValue_U1.data[0])):
                    maxValue_U1 = stressValue
            if (abs(stressValue.data[0])>max_Mises_U1):
                w_v1 = stressValue.data[0]
                max_Mises_U1 = abs(w_v1)

            # U2
            if (not maxValue_U2 or
                    abs(stressValue.data[1]) > abs(maxValue_U2.data[1])):
                    maxValue_U2 = stressValue
            if (abs(stressValue.data[1])>max_Mises_U2):
                w_v2 = stressValue.data[1]
            	max_Mises_U2 = abs(w_v2)

            # U3
            if (not maxValue_U3 or
                    abs(stressValue.data[2]) > abs(maxValue_U3.data[2])):
                    maxValue_U3 = stressValue
            if (abs(stressValue.data[2])>max_Mises_U3):
                w_v3 = stressValue.data[2]
                max_Mises_U3 = abs(w_v3)

        frame_tik = frame_tik + 1
        mat="{:^16}\t{:^16.4f}\t{:^16.4f}\t{:^16.4f}\t{:^16}\t"
        ss = mat.format(step.name,w_v1,w_v2,w_v3,frame_tik)
        f.write('%s\n'%ss)
    print 'MaxDisp_U1: %.4f'% maxValue_U1.data[0]
    print 'MaxDisp_U2: %.4f'% maxValue_U2.data[1]
    print 'MaxDisp_U3: %.4f'% maxValue_U3.data[2]
    print "For more information, see 'Result_U1U2U3.txt' on work directory"
    f.write('%s\n'%fenge)
    f.write('%s\nMaxDisp_U1: %.4f\nMaxDisp_U2: %.4f\nMaxDisp_U3: %.4f'%(step.name,
        maxValue_U1.data[0],maxValue_U2.data[1],maxValue_U3.data[2]))
    f.write('\n%s\n'%fenge)
f.close()
if not stressOutputExists:
    raise Exception('Current odb file have no Disp result') 
