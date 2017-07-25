'''
japeto UI classes 
'''
from pubs.ui import *

#Japeto modules
from pubs.ui import widgets, models, fields
import pubs.pGraph as pGraph
reload(widgets)
reload(models)
reload(widgets)

class CentralTabWidget(QtGui.QTabWidget):
    def __init__(self, graph = pGraph.PGraph('null'), parent = None):
        super(CentralTabWidget, self).__init__(parent)
        self._graph = graph
        
        #-------------------------------------------------
        #SETUP TAB
        #-------------------------------------------------
        setupWidget = QtGui.QWidget()
        self._setupWidgetLayout = QtGui.QHBoxLayout()
        self._setupTreeFilter = QtGui.QLineEdit()
        self._setupTreeView = QtGui.QTreeView()
        self._setupTreeView.setAlternatingRowColors(True)
        self._setupTreeView.setDragEnabled(True)
        self._setupTreeView.setAcceptDrops(True)
        
        #file view
        #self._fileView = widgets.FileView()
        
        #fields
        self._setupAttrsWidget = QtGui.QFrame()
        self._setupAttrsLayout = QtGui.QVBoxLayout(self._setupAttrsWidget)
        self._setupAttrsWidget.setFrameShape(QtGui.QFrame.Panel)
        self._setupAttrsWidget.setFrameShadow(QtGui.QFrame.Sunken)
        #self._setupAttrsWidget.setMaximumWidth(200)
        self._setupAttrsWidget.setMinimumWidth(200)
        
        #bring it all together
        #splitter
        splitter = QtGui.QSplitter()
        
        splitter.addWidget(self._setupTreeView)
        splitter.addWidget(self._setupAttrsWidget)
        splitter.setStretchFactor(0,4)
        splitter.setStretchFactor(1,4)

        #self._setupWidgetLayout.addWidget(splitter)
        self._setupWidgetLayout.addWidget(self._setupTreeView)
        self._setupWidgetLayout.addWidget(self._setupAttrsWidget)
        setupWidget.setLayout(self._setupWidgetLayout)
        
        #-------------------------------------------------
        #MODEL AND PROXY MODEL
        #-------------------------------------------------
        #model for scenegraph
        self._model = models.LayerGraphModel(self._graph)

        self._setupTreeView.setModel(self._model)
        
        self.addTab(setupWidget, 'Setup')
        self._setupTreeView.expandAll()
        
        #set selections
        if self._graph.getNodes():
            self._setupTreeView.setCurrentIndex(self._model.index(0,0))
            self._populateSetupAttrsLayout(self._model.index(0,0))
        
        self._setupTreeView.clicked.connect(self._populateSetupAttrsLayout)

        #CONTEXT MENU
        self._setupTreeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self._setupTreeView, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.showCustomContextMenu)

    
    def showCustomContextMenu(self, pos):
        '''
        Show the context menu at the position of the curser
        
        :param pos: The point where the curser is on the screen
        :type pos: QtCore.QPoint
        '''
        index = self._setupTreeView.indexAt(pos)

        if not index.isValid():
            return

        node = self._model.itemFromIndex(index)
        #If node is disabled, return
        if not node.isActive():
            return
        
        #construct menus
        mainMenu = QtGui.QMenu(self)
        
        executeNodeAction = mainMenu.addAction('Execute')
        QtCore.QObject.connect(executeNodeAction, QtCore.SIGNAL('triggered()'), self._executeSelectedNode)
        
        #main menu actions
        mainMenu.addSeparator()
        removeNodeAction = mainMenu.addAction('Remove Node')
        QtCore.QObject.connect(removeNodeAction, QtCore.SIGNAL('triggered()'), self._removeSelectedNode)
        
        mainMenu.popup(QtGui.QCursor.pos())

    def _executeSelectedNode(self):
        '''
        Runs the selected item in the setup view
        '''
        node = self._selectedNode()
        attributes = dict()
        
        if node:
            attrs = node.getAttributes()
            if attrs:
                for attr in attrs:
                    attributes[attr.getName()] = attr.value()
                
                    node.execute(**attributes)
                    return
            node.execute()
 
    def _selectedNode(self):
        '''
        Returns the selected node
        '''
        index = self._setupTreeView.currentIndex()
        
        if not index.isValid():
            return None
        
        return self._model.itemFromIndex(index)
    
    def _removeSelectedNode(self):        
        index = self._setupTreeView.currentIndex()
        
        node = self._selectedNode()

        #self._model.removeRows(index.row(), 1, self._model)
        if node:
            self._model.beginRemoveRows( index.parent(), index.row(), index.row()+1-1 )
            self._graph.removeNode(node)
            #node.parent().removeChild(node)
            self._model.endRemoveRows()
            del node
        
    def _populateSetupAttrsLayout(self, index):
        '''
        Populates the attributes for the given node
        
        :param index: QModelIndex of the node you want to get attributes for
        :type index: QtCore.QModelIndex
        '''
        #Check if there are any items in the layout
        if self._setupAttrsLayout.count():
            self.clearLayout(self._setupAttrsLayout)

        #check to see if the index passed is valid
        if not index.isValid():
            return None
        
        #get the node
        node = self._model.itemFromIndex(index)

        #go through the attributes on the node and create appropriate field
        labelWidth = 80
        for attr in node.getAttributes():
            if attr.getName() == 'position':
                field = fields.VectorField('{0}:'.format(attr.getName()), value = attr.value(), attribute = attr)
            elif attr.getType() == "str":
                field = fields.LineEditField('{0}:'.format(attr.getName()), value = str(attr.value()), attribute = attr)
            elif attr.getType() == "bool":
                field = fields.BooleanField('{0}:'.format(attr.getName()), value = attr.value(), attribute = attr)
            elif attr.getType() == "int":
                field = fields.IntField('{0}:'.format(attr.getName()), value = attr.value(), attribute = attr)
            elif attr.getType() == "float":
                field = fields.IntField('{0}:'.format(attr.getName()), value = attr.value(), attribute = attr)
            elif attr.getType() == "list":
                field = fields.ListField('{0}:'.format(attr.getName()), value = attr.value(), attribute = attr)
            elif attr.getType() == "code":
                field = fields.TextEditField('{0}:'.format(attr.getName()), value = attr.value(), attribute = attr)
            elif attr.getType() == "file":
                field = fields.FileBrowserField(label = '{0}:'.format(attr.getName()), filter = "",value = attr.value(), attribute = attr)
            elif attr.getType() == "dir":
                field = fields.DirBrowserField(label = '{0}:'.format(attr.getName()), value = attr.value(), attribute = attr)
            
            #add the field to the layout
            field.label().setMinimumWidth(labelWidth)
            field.label().setMaximumWidth(labelWidth)
            field.label().setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self._setupAttrsLayout.addWidget(field)
        #add stretch to push all item up
        self._setupAttrsWidget.setLayout(self._setupAttrsLayout)
        self._setupAttrsLayout.addStretch()
     
    def clearLayout(self, layout):
        '''
        Clears a layout of any items with in the layout
        
        :param layout: Layout that you wish to clear
        :type layout: QtGui.QLayout
        '''
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
    
            if isinstance(item, QtGui.QWidgetItem):
                item.widget().close()
                # or
                # item.widget().setParent(None)
            elif isinstance(item, QtGui.QSpacerItem):
                pass
                # no need to do extra stuff
            else:
                self.clearLayout(item.layout())
    
            # remove the item from layout
            layout.removeItem(item)  
            
    def getAttrFieldValues(self):
        for i in reversed(range(self._setupAttrsLayout.count())):
            item = self._setupAttrsLayout.itemAt(i)
            if isinstance(item, QtGui.QWidgetItem):
                print item.widget().value()

#-------------------------------
#MAIN WINDOW
#-------------------------------
class MainWindow(QtGui.QMainWindow):
    def __init__(self, graph = pGraph.PGraph('null'), parent = None):
        '''
        This is the main window used for pubs

        :param graph: The graph which the ui will use for the setup view
        :type graph: ml_graph.MlGraph
        
        :param parent: The parent for the ui
        :type parent: QtGui.QWidget
        '''
        super(MainWindow, self).__init__(parent)
        #load in the style sheet
        
        #set the window title and central widget
        self.setWindowTitle('PUBS UI')
        tabWidget = CentralTabWidget(graph)
        self.setCentralWidget(tabWidget)
        
        #add menu bar to window
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        newTemplateAction = fileMenu.addAction('New Template')
        loadTemplateAction = fileMenu.addAction('Load Template')
        saveTemplateAction = fileMenu.addAction('Save Template')
        QtCore.QObject.connect(newTemplateAction, QtCore.SIGNAL('triggered()'), self._newTemplate)
        QtCore.QObject.connect(loadTemplateAction, QtCore.SIGNAL('triggered()'), self._loadTemplate)
        #QtCore.QObject.connect(saveTemplateAction, QtCore.SIGNAL('triggered()'), self._saveTemplate)
        
        self.setMinimumSize(880,550)
        self.setMaximumSize(1000, 1200)
              
    def _loadTemplate(self):
        '''
        Load all the templates into the dialog
        '''
        self.loadTemplateDialog = widgets.LoadTemplateDialog(self)
        self.loadTemplateDialog.show()

        self.loadTemplateDialog.finished.connect(self.setTemplate)
    
    def _newTemplate(self):
        '''
        Load all the templates into the dialog
        '''
        self.inheritTemplateDialog = widgets.InheritTemplateDialog(self)
        self.inheritTemplateDialog.show()

        self.inheritTemplateDialog.finished.connect(self.setNewTemplate)
    
               
    def setTemplate(self, *args):
        '''
        sets the template to the template chosen in the templateDialog
        '''
        #get the template chosen
        template = str(self.loadTemplateDialog.template)
        templateFile = self.loadTemplateDialog.templateFile
        #import the file and initialize
        if template != 'None':
            tabWidget = self.centralWidget()
            #get data from the file
            data = dict()
            #run the data we got from file       
            execfile(templateFile, data)
            #newNodeCmd = '%s("%s")' % (template.title(), template) #<-- Construct template
            tabWidget._graph = data[template.title()](template)
            del(data) #<-- delete globals data
            tabWidget._graph.initialize()
            tabWidget._model = models.LayerGraphModel(tabWidget._graph)
            #tabWidget._proxyModel.setSourceModel(tabWidget._model)
            tabWidget._setupTreeView.setModel(tabWidget._model)
            tabWidget._setupTreeView.expandAll()
            
    def closeEvent(self, e):
        # Write window size and position to config file
        #self.settings.setValue("size", self.size())
        #self.settings.setValue("pos", self.pos())
        super(MainWindow,self).closeEvent(e)

def launch(dock = False):
    if cmds.control('Pubs UI',exists=True):
        cmds.delete('Pubs UI',control=True)
    wnd = MainWindow(parent=getMayaWindow())
    wnd.show()
    wnd.raise_()
    return wnd