import maya.cmds as cmds
import maya.mel as mm

def centerPivot(*args):
	objects = cmds.ls(selection=True)
	if not objects:
		return
	for obj in objects:
		cmds.xform(obj, cp=1)

	if cmds.checkBox("closeCheck", q=True, v=True):
		cmds.deleteUI("xformDialog", window=True)

def sendPivotToLowestPoint(*args):
	objects = cmds.ls(selection=True)
	if not objects:
		return

	axis = cmds.upAxis(q=True, axis=True)

	for obj in objects:
		bbox = cmds.xform(obj, q=True, bb=True)
		
		if axis == 'y':
			# Y is up
			lowestPoint = [(bbox[0] + bbox[3]) * 0.5, bbox[1], (bbox[2] + bbox[5]) * 0.5]
			cmds.xform(obj, cp=1)
			piv = cmds.xform(obj, q=True, ws=True, rp=True)
			piv[1] = lowestPoint[1]
		else:
			# Z is up
			lowestPoint = [(bbox[0] + bbox[3]) * 0.5, (bbox[1] + bbox[4]) * 0.5, bbox[2]]
			cmds.xform(obj, cp=1)
			piv = cmds.xform(obj, q=True, ws=True, rp=True)
			piv[2] = lowestPoint[2]

		cmds.xform(obj, ws=True, pivots=piv)
	if cmds.checkBox("closeCheck", q=True, v=True):
		cmds.deleteUI("xformDialog", window=True)

def snapObjectToGrid(*args):
	objects = cmds.ls(selection=True)
	if not objects:
		cmds.warning("No objects selected.")
	axis = cmds.upAxis(q=True, axis=True)
	for obj in objects:
		bbox = cmds.xform(obj, q=True, bb=True)        
		if axis == 'y':
			# Y is up
			min_val = bbox[1]
			if min_val > 0:
				cmds.move(0, -abs(min_val), 0, obj, relative=True)
			else:
				cmds.move(0, abs(min_val), 0, obj, relative=True)
		else:
			# Z is up
			min_val = bbox[2]
			if min_val > 0:
				cmds.move(0, 0, -abs(min_val), obj, relative=True)
			else:
				cmds.move(0, 0, abs(min_val), obj, relative=True)

	if cmds.checkBox("closeCheck", q=True, v=True):
		cmds.deleteUI("xformDialog", window=True)

def sendPivottoOrigin(*args):
	selection = cmds.ls(selection=True)
	mm.eval("FreezeTransformations;")
	for s in selection:
		cmds.xform(s, pivots=(0, 0, 0))

	if cmds.checkBox("closeCheck", q=True, v=True):
		cmds.deleteUI("xformDialog", window=True)

def sendObjectCenterToPivot(*args):
	sel = cmds.ls(sl=True)
	if sel:
		originalPivot = cmds.xform(sel[0], q=True, ws=True, rp=True)
		mm.eval("FreezeTransformations;")
		bbox = cmds.xform(sel[0], q=True, bb=True)
		center = [(bbox[0]+bbox[3])*0.5, (bbox[1]+bbox[4])*0.5, (bbox[2]+bbox[5])*0.5]
		pivot = cmds.xform(sel[0], q=True, ws=True, rp=True)
		offset = [pivot[i] - center[i] for i in range(3)]
		cmds.xform(sel[0], ws=True, t=offset)
		cmds.xform(sel[0], ws=True, sp=originalPivot, rp=originalPivot)
		mm.eval("FreezeTransformations;")
	if cmds.checkBox("closeCheck", q=True, v=True):
		cmds.deleteUI("xformDialog", window=True)

def sendObjectLowestPointToPivot(*args):
	sel = cmds.ls(sl=True)
	if sel:
		# Determine the up axis
		axis = cmds.upAxis(q=True, axis=True)
		
		originalPivot = cmds.xform(sel[0], q=True, ws=True, rp=True)
		mm.eval("FreezeTransformations;")
		bbox = cmds.xform(sel[0], q=True, bb=True)
		
		if axis == 'y':
			# Y is up
			lowestPoint = [(bbox[0] + bbox[3]) * 0.5, bbox[1], (bbox[2] + bbox[5]) * 0.5]
		else:
			# Z is up
			lowestPoint = [(bbox[0] + bbox[3]) * 0.5, (bbox[1] + bbox[4]) * 0.5, bbox[2]]
		
		pivot = cmds.xform(sel[0], q=True, ws=True, rp=True)
		offset = [pivot[i] - lowestPoint[i] for i in range(3)]
		cmds.xform(sel[0], ws=True, t=offset)
		cmds.xform(sel[0], ws=True, sp=originalPivot, rp=originalPivot)
		mm.eval("FreezeTransformations;")
	if cmds.checkBox("closeCheck", q=True, v=True):
		cmds.deleteUI("xformDialog", window=True)

if cmds.window("xformDialog", exists=True):
	cmds.deleteUI("xformDialog")

win = cmds.window("xformDialog", title="Xform Action", widthHeight=(300,280))
col = cmds.columnLayout(adj=True)
cmds.button(label="Center pivot", c=centerPivot)
cmds.separator(h=3, style="none")
cmds.button(label="Send pivot to the lowest point", c=sendPivotToLowestPoint)
cmds.separator(h=3, style="none")
cmds.button(label="Place object on grid", c=snapObjectToGrid)
cmds.separator(h=3, style="none")
cmds.button(label="Send pivot to origin", c=sendPivottoOrigin)
cmds.separator(h=3, style="none")
cmds.button(label="Send object's center to pivot", c=sendObjectCenterToPivot)
cmds.separator(h=3, style="none")
cmds.button(label="Place object on pivot", c=sendObjectLowestPointToPivot)
cmds.separator(h=10, style="none")
cmds.checkBox("closeCheck", label="Close window on button press", value=True)
cmds.showWindow(win)
