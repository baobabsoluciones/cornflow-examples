import sys
from PySide2 import QtWidgets, QtCore, QtGui
from cornflow_client import CornFlow, group_variables_by_name, CornFlowApiError

import os
import logging
import gui
import model as md
import logging as log
import pandas as pd
import json


REFERENCE_ID_CODE = 256
EXECUTIONS_CODE = 257
TEXT_LABEL_OK = "QLabel { color : green; }"
TEXT_LABEL_NOK = "QLabel { color : red; }"

class MainWindow_EXCEC():

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.logger = log.getLogger('appLog')
        logFormat = '%(asctime)s %(levelname)s:%(message)s'
        formatter = log.Formatter(logFormat)
        stderr_log_handler = log.StreamHandler()
        stderr_log_handler.setFormatter(formatter)
        _log = log.getLogger()
        _log.handlers = [stderr_log_handler]

        MainWindow = QtWidgets.QMainWindow()

        # set icon
        if getattr(sys, 'frozen', False):
            scriptDir = sys._MEIPASS
            self.examplesDir = scriptDir + 'data/'
        else:
            scriptDir = os.path.dirname(os.path.realpath(__file__))
            self.examplesDir = scriptDir + 'data/'

        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        self.instance_name = ''
        self.instance = None
        self.solution = None
        self.solution_log = None
        self.client = None
        self.token = None
        self.config = dict(threads=1)
        self.ui.solver.insertItems(0, ['PULP_CBC_CMD', 'GUROBI_CMD', 'CPLEX_CMD'])
        self.ui.maxTime.setText(str(100))

        self.update_ui()

        # menu actions:
        self.ui.actionExit.triggered.connect(QtCore.QCoreApplication.exit)

        # below buttons:
        self.ui.chooseFile.clicked.connect(self.choose_file)
        self.ui.send_instance.clicked.connect(self.send_instance)

        self.ui.solve_instance.clicked.connect(self.solve_instance)
        self.ui.get_instances.clicked.connect(self.get_instances)

        self.ui.instances.clicked.connect(self.get_executions)
        self.ui.get_results.clicked.connect(self.get_results)
        self.ui.show_solution.clicked.connect(self.show_solution)

        self.ui.signup.clicked.connect(self.signup)
        self.ui.login.clicked.connect(self.login)
        self.ui.logout.clicked.connect(self.logout)
        self.ui.checkBoxDebug.clicked.connect(self.update_ui)

        self.ui.instances.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # self.ui.instances.customContextMenuRequested[QtCore.QPoint].connect(self.rightMenuShow)
        self.get = QtWidgets.QAction(text='get')
        self.get.triggered.connect(self.get_one_instance)
        self.delete = QtWidgets.QAction(text='delete')
        self.delete.triggered.connect(self.delete_one_instance)
        self.ui.instances.addAction(self.delete)

        self.ui.instances.addAction(self.get)
        self.ui.instances.addAction(self.delete)

        self.ui.solver.activated.connect(self.update_ui)
        self.ui.maxTime.textEdited.connect(self.update_ui)

        self.ui.showLog.clicked.connect(self.show_log)
        self.ui.showStats.clicked.connect(self.show_stats)

        MainWindow.show()
        sys.exit(self.app.exec_())


    def update_ui(self):

        # we update labels with status:
        try:
            self.config['timeLimit'] = float(self.ui.maxTime.text())
        except:
            pass
        self.config['solver'] = self.ui.solver.currentText()

        if self.instance is None:
            self.ui.instCheck.setText('No instance loaded')
            self.ui.instCheck.setStyleSheet(TEXT_LABEL_NOK)
        else:
            self.ui.instCheck.setText('Instance loaded')
            self.ui.instCheck.setStyleSheet(TEXT_LABEL_OK)

        if self.solution is None:
            self.ui.solCheck.setText('No solution loaded')
            self.ui.solCheck.setStyleSheet(TEXT_LABEL_NOK)
        else:
            self.ui.solCheck.setText('Solution loaded')
            self.ui.solCheck.setStyleSheet(TEXT_LABEL_OK)
        if self.token:
            self.ui.loginCheck.setText('Logged-in')
            self.ui.loginCheck.setStyleSheet(TEXT_LABEL_OK)
            self.ui.username.setEnabled(False)
            self.ui.password.setEnabled(False)
            self.ui.server.setEnabled(False)
        else:
            self.ui.loginCheck.setText('Logged-out')
            self.ui.loginCheck.setStyleSheet(TEXT_LABEL_NOK)
            self.ui.username.setEnabled(True)
            self.ui.password.setEnabled(True)
            self.ui.server.setEnabled(True)
        if self.ui.checkBoxDebug.isChecked():
            level = log.DEBUG
        else:
            level = log.INFO
        _log = log.getLogger()
        _log.setLevel(level)
        return 1

    def choose_file(self):
        QFileDialog = QtWidgets.QFileDialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(
            caption="Choose a file to load",
            dir=self.examplesDir,
            options=options)
        try:
            fileName = fileName[0]
        except IndexError:
            return
        if not fileName:
            return False
        self.ui.file_path.setText(fileName)
        self.load_file(fileName)
        self.update_ui()
        return True

    def signup(self):
        if not self.ui.username.text() or not self.ui.password.text():
            return self.show_message('Fill above', "You need to provide a username and a password")
        if not self.ui.server.text():
            return self.show_message('Fill above', "You need to provide a server name")
        config = dict(email = self.ui.username.text(), pwd= self.ui.password.text(), name=self.ui.username.text())
        self.client = CornFlow(url=self.ui.server.text())
        self.client.sign_up(**config)
        self.login()
        return True

    def login(self):
        if not self.ui.username.text() or not self.ui.password.text():
            return self.show_message('Fill above', "You need to provide a username and a password")
        if not self.ui.server.text():
            return self.show_message('Fill above', "You need to provide a server name")
        self.client = CornFlow(url=self.ui.server.text())
        self.token = self.client.login(self.ui.username.text(), self.ui.password.text())
        self.get_instances()
        self.update_ui()

    def logout(self):
        self.token = None
        self.client = None
        self.instance  = None
        self.solution = None
        if self.ui.instances.model():
            self.ui.instances.model().clear()
        if self.ui.executions.model():
            self.ui.executions.model().clear()
        self.update_ui()

    def get_instances(self):
        if not self.token:
            return self.show_message('Login first!', "You need to login before doing anything")

        instances = self.client.get_all_instances()
        if instances is not None:
            instances.sort(key=lambda v: v['created_at'])

        model = QtGui.QStandardItemModel(self.ui.instances)
        for inst in instances:
            item = QtGui.QStandardItem(inst['name'] + ' ' + inst['created_at'])
            item.setData(inst['id'], REFERENCE_ID_CODE)
            # item.setData(inst['executions'], EXECUTIONS_CODE)
            # self.update_row_inst(item, len(inst['executions']))
            model.appendRow(item)
        self.ui.instances.setModel(model)

    @staticmethod
    def update_row_inst(item, has_executions):
        green_brush = get_brush('green')
        red_brush = get_brush('red')
        if has_executions:
            item.setForeground(green_brush)
        else:
            item.setForeground(red_brush)

    def get_one_instance(self):
        item_id = self.ui.instances.currentIndex()
        if not item_id.data(REFERENCE_ID_CODE):
            return
        instance_id = item_id.data(REFERENCE_ID_CODE)
        inst = self.client.get_one_instance(instance_id)
        item = self.ui.instances.model().itemFromIndex(item_id)
        item.setData(inst['executions'], EXECUTIONS_CODE)
        self.update_row_inst(item, len(inst['executions']))
        self.get_executions()

    def delete_one_instance(self):
        item_id = self.ui.instances.currentIndex()
        if not item_id.data(REFERENCE_ID_CODE):
            return
        instance_id = item_id.data(REFERENCE_ID_CODE)
        result = self.client.delete_one_instance(instance_id)
        if result.status_code == 200:
            item = self.ui.instances.model().itemFromIndex(item_id)
            self.ui.instances.model().removeRow(item.row())
        else:
            return self.show_message('Error in response', "The api returned an unexpected status: {}".format(result.status_code))

    def send_instance(self):
        if not self.token:
            return self.show_message('Login first!', "You need to login before doing anything")
        if not self.instance:
            self.show_message(title="Loading needed", text='No instance loaded, so not possible to solve.')
            return

        lpmodel = md.build_model(self.instance, self.instance_name)
        try:
            self.client.create_instance(lpmodel)
        except CornFlowApiError as e:
            return self.show_message('Error in response', "The api returned an error: {}".format(e))
        self.get_instances()
        return True

    def get_executions(self):
        if not self.token:
            return self.show_message('Login first!', "You need to login before doing anything")
        instance = self.ui.instances.currentIndex()
        instance_id = instance.data(REFERENCE_ID_CODE)
        if not instance_id:
            return
        model = QtGui.QStandardItemModel(self.ui.executions)
        details = self.client.get_one_instance(instance_id)
        executions = details['executions']
        for exec in executions:
            config = exec['config']
            name = "{} +{} @ {}".format(config.get('solver', ''),
                                       config.get('timeLimit', 0),
                                       exec['created_at'])
            item = QtGui.QStandardItem(name)
            item.setData(exec['id'], REFERENCE_ID_CODE)
            green_brush = get_brush('green')
            red_brush = get_brush('red')
            yellow_brush = get_brush('yellow')
            colors = \
                {1: green_brush,
                 0: yellow_brush,}
            color = colors.get(exec['state'], red_brush)
            item.setForeground(color)
            model.appendRow(item)
        self.ui.executions.setModel(model)

    def get_results(self):
        execution = self.ui.executions.currentIndex()
        execution_id = execution.data(REFERENCE_ID_CODE)
        if not execution_id:
            return
        # QtCore.Qt.ItemDataRole.DisplayRole
        # QtCore.Qt.DisplayRole
        results = self.client.get_results(execution_id)
        if results['state'] != 1:
            self.solution = None
            self.update_ui()
            return self.show_message('No results', "This execution has no solution (yet?)")
        response = self.client.get_solution(execution_id)
        if not response['data']:
            self.solution = None
            self.update_ui()
            return self.show_message('No results', "This execution has no solution (yet?)")
        model_dict = response['data']
        log_json = self.client.get_api_for_id('execution/', execution_id, 'log')
        self.solution_log = log_json.json()['log']
        self.solution_log['progress'] = self.progress_to_dataframe(log_progress=self.solution_log['progress'])

        self.solution = md.get_solution_from_model(model_dict)
        self.update_ui()

    @staticmethod
    def progress_to_dataframe(log_progress):
        return pd.DataFrame.from_dict(log_progress)

    def show_message(self, title, text, icon='critical'):
        msg = QtWidgets.QMessageBox()
        if icon=='critical':
            msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(text)
        # msg.setInformativeText("No template_in file found in directory.")
        msg.setWindowTitle(title)
        retval = msg.exec_()
        return

    def load_file(self, fileName):

        if not os.path.exists(fileName):
            self.show_message(title="Missing files", text="No template_in.xlsx file found in directory.")
            return
        try:
            model_data = md.read_file(fileName)
        except Exception as e:
            self.show_message(title="Error in file while reading",
                              text="There's been an error reading the input file:\n{}.".format(e))
            return
        self.instance_name = os.path.basename(fileName)
        self.instance = model_data
        self.solution = None

        return True

    def solve_instance(self):
        if not self.token:
            return
        config = self.config
        instance = self.ui.instances.currentIndex()
        if not instance.data(REFERENCE_ID_CODE):
            self.show_message(title="Select instance", text='No instance selected to solve.')
            return

        try:
            self.client.create_execution(instance.data(REFERENCE_ID_CODE), config)
        except CornFlowApiError as e:
            return self.show_message('Error in response', "The api returned an error: {}".format(e))

    def show_solution(self):
        if not self.instance:
            return self.show_message('Error showing solution', "You need to load an instance first!")
        if not self.solution:
            return self.show_message('Error showing solution', "You need to load a solution first!")
        md.graph_solution(self.instance, self.solution, path='path.png')
        self.solutionPicture = QtWidgets.QLabel(text="<img src='path.png' />")
        self.solutionPicture.show()

    def show_log(self):
        if not self.solution_log:
            return self.show_message('No log read', "No log was read from the solution :(")
        self.view = QtWidgets.QTableView()
        model = PandasModel(self.solution_log['progress'])
        self.view.setModel(model)
        self.view.resize(1000, 10000)
        self.view.show()

    def show_stats(self):
        self.wid = QtWidgets.QWidget()
        self.wid.resize(250, 150)
        self.wid.setWindowTitle('Stats!')


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = parent.ui.solution_log
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


class ScrollMessageBox(QtWidgets.QMessageBox):
   def __init__(self, *args, **kwargs):
       QtWidgets.QMessageBox.__init__(self, *args, **kwargs)
       chldn = self.children()
       scrll = QtWidgets.QScrollArea(self)
       scrll.setWidgetResizable(True)
       grd = self.findChild(QtWidgets.QGridLayout)
       lbl = QtWidgets.QLabel(chldn[1].text(), self)
       lbl.setWordWrap(True)
       scrll.setWidget(lbl)
       scrll.setMinimumSize (400,200)
       grd.addWidget(scrll,0,1)
       chldn[1].setText('')
       self.exec_()

def get_brush(colorName):
    a = QtGui.QColor()
    a.setNamedColor(colorName)
    brush = QtGui.QBrush()
    brush.setColor(a)
    return brush


# class ScrollMessageBox(QtWidgets.QMessageBox):
#    def __init__(self, *args, **kwargs):
#         QtWidgets.QMessageBox.__init__(self, *args, **kwargs)
#         scroll = QtWidgets.QScrollArea(self)
#         scroll.setWidgetResizable(True)
#         self.content = QtWidgets.QWidget()
#         scroll.setWidget(self.content)
#         lay = QtWidgets.QVBoxLayout(self.content)
#         for item in l:
#            lay.addWidget(QtWidgets.QLabel(item, self))
#         self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
#         self.setStyleSheet("QScrollArea{min-width:300 px; min-height: 400px}")

if __name__ == "__main__":
    # to compile desktop_app.gui, we need the following:
    # pyuic5 -o filename.py file.ui
    # if we add -x flag we make it executable
    # example: pyuic5 desktop_app/gui.ui -o desktop_app/gui.py
    # for pyside2:
    # Migration to pyside2:
    # https://www.learnpyqt.com/blog/pyqt5-vs-pyside2/
    # pyside2-uic gui.ui -o gui.py
    MainWindow_EXCEC()



