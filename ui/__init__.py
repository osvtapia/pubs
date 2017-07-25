#sip module
try:
    from PySide import QtGui
    from PySide import QtCore
    import shiboken

    def wrapinstance(ptr, base=None):
        """
        Utility to convert a pointer to a Qt class instance (PySide/PyQt compatible)
        :param ptr: Pointer to QObject in memory
        :type ptr: long or Swig instance
        :param base: (Optional) Base class to wrap with (Defaults to QObject, which should handle anything)
        :type base: QtGui.QWidget
        :return: QWidget or subclass instance
        :rtype: QtGui.QWidget
        """
        if ptr is None:
            return None
        ptr = long(ptr) #Ensure type
        if globals().has_key('shiboken'):
            if base is None:
                qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
                metaObj = qObj.metaObject()
                cls = metaObj.className()
                superCls = metaObj.superClass().className()
                if hasattr(QtGui, cls):
                    base = getattr(QtGui, cls)
                elif hasattr(QtGui, superCls):
                    base = getattr(QtGui, superCls)
                else:
                    base = QtGui.QWidget
            return shiboken.wrapInstance(long(ptr), base)
        else:
            return None

    _uiType = "PySide"
except:
    #PyQt modules
    from PyQt4 import QtGui
    from PyQt4 import QtCore
    import sip

    _uiType = "PyQt"
else:
    pass

#import maya modules
import os

try:
    if _uiType == "PyQt":
        raise 
    from maya import OpenMaya
    from maya import OpenMayaAnim
    from maya import OpenMayaUI 
    from maya import cmds
    from maya import mel
    def getMayaWindow():
        #Get the maya main window as a QMainWindow instance
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        return wrapinstance(long(ptr), QtGui.QMainWindow)
except:
    from maya import OpenMaya
    from maya import OpenMayaAnim
    from maya import OpenMayaUI 
    from maya import cmds
    from maya import mel
    def getMayaWindow():
        #Get the maya main window as a QMainWindow instance
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        return sip.wrapinstance(long(ptr), QtCore.QObject)
else:
    pass