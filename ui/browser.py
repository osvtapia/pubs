import os
from pubs import *
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(600, 600)
        self.setWindowTitle('Browser')
        exit = QtGui.QAction('Quit Browser', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Close the browser') 
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        settings = QtGui.QAction('Settings', self)
        settings.setStatusTip('Settings to style things.')

        self.statusBar()
        menubar = self.menuBar()
        file = menubar.addMenu('File')
        file.addAction(exit)
        options = menubar.addMenu('Options')
        options.addAction(settings)

        self.mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)

        self.optionsWidget = QtGui.QWidget(self)

        files_list = QtGui.QListWidget()

        self.fileBrowserWidget = QtGui.QWidget(self)

        self.dirmodel = QtGui.QFileSystemModel()
        # Don't show files, just folders
        self.dirmodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)

        self.folder_view = QtGui.QTreeView(parent=self);
        self.folder_view.setModel(self.dirmodel)
        self.folder_view.clicked[QtCore.QModelIndex].connect(self.clicked) 
        # Don't show columns for size, file type, and last modified
        self.folder_view.setHeaderHidden(True)
        self.folder_view.hideColumn(1)
        self.folder_view.hideColumn(2)
        self.folder_view.hideColumn(3)


        self.selectionModel = self.folder_view.selectionModel()

        self.filemodel = QtGui.QFileSystemModel()
        
        # Don't show folders, just files
        self.filemodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)

        self.file_view = QtGui.QListView(parent=self);
        self.file_view.setModel(self.filemodel)
        self.file_view.setViewMode(QtGui.QListView.IconMode)     

        splitter_filebrowser = QtGui.QSplitter()
        splitter_filebrowser.addWidget(self.folder_view)
        splitter_filebrowser.addWidget(self.file_view)
        splitter_filebrowser.setStretchFactor(0,2)
        splitter_filebrowser.setStretchFactor(1,4)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(splitter_filebrowser)
        self.fileBrowserWidget.setLayout(hbox)

        vbox_options = QtGui.QVBoxLayout(self.optionsWidget)
        vbox_options.addWidget(files_list)
        #vbox_options.addWidget(group_input)
        self.optionsWidget.setLayout(vbox_options)

        splitter_filelist = QtGui.QSplitter()
        splitter_filelist.setOrientation(QtCore.Qt.Vertical)
        splitter_filelist.addWidget(self.fileBrowserWidget)
        splitter_filelist.addWidget(self.optionsWidget)
        vbox_main = QtGui.QVBoxLayout(self.mainWidget)
        vbox_main.addWidget(splitter_filelist)       
        vbox_main.setContentsMargins(0,0,0,0)
        #self.setLayout(vbox_main)     

    def set_path(self):
        import os
        try:
            import maya.cmds as cmds
            cwd = os.getcwd()
            self.dirmodel.setRootPath(cwd)   
        else:
            self.dirmodel("")  

    def clicked(self, index):
        #get selected path of folder_view
        index = self.selectionModel.currentIndex()
        dir_path = self.dirmodel.filePath(index)
        ###############################################
        #Here's my problem: How do I set the dir_path
        #for the file_view widget / the filemodel?
        ###############################################
        self.filemodel.setRootPath(dir_path)
        self.file_view.setRootIndex(self.filemodel.index(dir_path))