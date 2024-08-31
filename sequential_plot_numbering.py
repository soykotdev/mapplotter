import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QAction, QDialog, QMessageBox
from qgis.core import QgsProject, QgsGeometry, QgsVectorLayer
from qgis.gui import QgsMapTool
from qgis.utils import iface
#Firstly I created the script then converted it the plugin . 
from .ui.sequential_plot_numbering_dialog import Ui_Dialog

class SequentialPlotNumberingTool(QgsMapTool):
    def __init__(self, iface, layer, field_name, start_number):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.iface = iface
        self.layer = layer
        self.field_name = field_name
        self.current_number = start_number
        self.feature_plot_map = {}  # Dictionary to store feature IDs and their plot numbers
        self.undo_stack = []  # Stack to store previous states for undo

    def activate(self):
        self.canvas().setCursor(QCursor(Qt.CrossCursor))

    def canvasReleaseEvent(self, event):
        point = self.toLayerCoordinates(self.layer, event.pos())
        buffer = QgsGeometry.fromPointXY(point).buffer(0.0001, 5)

        self.layer.startEditing()
        for feature in self.layer.getFeatures():
            if buffer.intersects(feature.geometry()):
                feature_id = feature.id()
                if feature_id not in self.feature_plot_map:
                    # Save the current state for undo
                    self.undo_stack.append((feature_id, feature[self.field_name]))

                    feature[self.field_name] = self.current_number
                    self.layer.updateFeature(feature)
                    self.feature_plot_map[feature_id] = self.current_number
                    self.current_number += 1
                break
        self.layer.commitChanges()
        self.iface.mapCanvas().refresh()

    def undo(self):
        if not self.undo_stack:
            return

        self.layer.startEditing()
        feature_id, previous_value = self.undo_stack.pop()
        feature = self.layer.getFeature(feature_id)

        feature[self.field_name] = previous_value
        self.layer.updateFeature(feature)
        del self.feature_plot_map[feature_id]
        self.current_number -= 1

        self.layer.commitChanges()
        self.iface.mapCanvas().refresh()

class SequentialPlotNumberingDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.setupUi(self)
        self.populate_layers()

    def populate_layers(self):
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            self.comboBoxLayer.addItem(layer.name(), layer.id())

        self.comboBoxLayer.currentIndexChanged.connect(self.populate_fields)
        self.populate_fields()

    def populate_fields(self):
        self.comboBoxField.clear()
        layer_id = self.comboBoxLayer.itemData(self.comboBoxLayer.currentIndex())
        layer = QgsProject.instance().mapLayer(layer_id)
        
        if isinstance(layer, QgsVectorLayer):
            fields = layer.fields().names()
            self.comboBoxField.addItems(fields)
        else:
            self.comboBoxField.addItem("No fields available")

class SequentialPlotNumbering:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None
        self.stop_action = None
        self.tool = None
        self.undo_shortcut = None

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icons', 'icon.png')
        stop_icon_path = os.path.join(self.plugin_dir, 'icons', '2.PNG')
        
        self.action = QAction(QIcon(icon_path), "MapPlotter", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

        self.stop_action = QAction(QIcon(stop_icon_path), "Stop MapPlotter", self.iface.mainWindow())
        self.stop_action.triggered.connect(self.stop_tool)
        self.iface.addToolBarIcon(self.stop_action)
        self.stop_action.setVisible(False)

        self.undo_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self.iface.mainWindow())
        self.undo_shortcut.activated.connect(self.undo_last_action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removeToolBarIcon(self.stop_action)
        if self.undo_shortcut:
            self.undo_shortcut.deleteLater()

    def run(self):
        dialog = SequentialPlotNumberingDialog(self.iface)
        if dialog.exec_():
            layer_id = dialog.comboBoxLayer.itemData(dialog.comboBoxLayer.currentIndex())
            field_name = dialog.comboBoxField.currentText()
            start_number = dialog.lineEdit_2.text()

            layer = QgsProject.instance().mapLayer(layer_id)
            if not layer:
                self.iface.messageBar().pushMessage("Error", "Layer not found!", level=3)
                return

            self.tool = SequentialPlotNumberingTool(self.iface, layer, field_name, int(start_number))
            self.iface.mapCanvas().setMapTool(self.tool)
            self.stop_action.setVisible(True)
            self.action.setVisible(False)

    def stop_tool(self):
        if self.tool:
            self.iface.mapCanvas().unsetMapTool(self.tool)
            self.tool = None
        self.stop_action.setVisible(False)
        self.action.setVisible(True)

    def undo_last_action(self):
        if self.tool:
            self.tool.undo()
