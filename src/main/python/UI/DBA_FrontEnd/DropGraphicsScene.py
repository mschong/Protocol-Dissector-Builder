from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from UI.DBA_FrontEnd.Field import Field
from UI.DBA_FrontEnd.Connector import Connector
from UI.DBA_FrontEnd.While_Loop import While_Loop
from UI.DBA_FrontEnd.For_Loop import For_Loop
from UI.DBA_FrontEnd.Decision import Decision
from UI.DBA_FrontEnd.GraphicsProxyWidget  import GraphicsProxyWidget
from UI.DBA_FrontEnd.Dialogs.ConnectorTypeDialog import ConnectorTypeDialog
from UI.DBA_FrontEnd.CodeBlock import CodeBlock
from UI.DBA_FrontEnd.Variable import Variable
import json
import sys


class ToolButton(QToolButton):
    def __init__(self, widget, scene):
        super().__init__()
        self.initUI(widget, scene)

    def initUI(self, widget, scene):
        self.widget = widget
        self.scene = scene
        self.setPopupMode(QToolButton.MenuButtonPopup)
        self.setObjectName("Button")
        self.setGeometry(QRect(20, 30, 278, 45))
        self.setText("No Name")
        menu = QMenu()
        self.setMenu(menu)
        action = QWidgetAction(self)
        action.setDefaultWidget(self.widget)
        self.menu().addAction(action)
        

class DropGraphicsScene(QGraphicsScene):
    InsertLine_ON, MoveItem = range(2)

    def __init__(self, parent = None):
        super(DropGraphicsScene, self).__init__(parent)
        self.line = None
        self.myMode = self.MoveItem
        self.myLineColor = Qt.black
        self.proxyWidgetList = []
        self.proxyDefinedFieldList= []
        self.variableList = []
        self.countFields = 0
        self.decision_count = 0
        self.while_count = 0 
        self.forloop_count = 0
        # self.doWhile_count = 0
        self.codeBlock_count = 0
        self.variable_count = 0

    def contextMenuEvent(self, event):
        if(len(self.items(event.scenePos()))):
            menu = QMenu()
            if isinstance(self.items(event.scenePos())[0], Connector):
                change_type_action = menu.addAction("Change Type")
                delete_action = menu.addAction("Delete")

                action = menu.exec_(event.screenPos())

                if(action == delete_action):
                    for item in self.items(event.scenePos()):
                        if(item.scene()):
                            item.startItem().removeConnector(item)
                            item.endItem().removeConnector(item)
                            self.removeItem(item)
                elif action == change_type_action:
                    dialog = ConnectorTypeDialog(self.items(event.scenePos())[0])
                    dialog.exec_()
            else:
                delete_action = menu.addAction("Delete")
                action = menu.exec_(event.screenPos())

                if action == delete_action:
                    for item in self.items(event.scenePos()):
                        if item.scene():
                            item.removeConnectors()
                            i = 0
                            while (i < len(self.proxyWidgetList)):
                                if(isinstance(self.getDefaultWidget(item), Variable) or isinstance(self.getDefaultWidget(item), Field)):
                                    # Deletes the copy of a defined field without affecting the original field
                                    if(self.proxyWidgetList[i] == item and self.proxyWidgetList[i].widget().menu().actions()[0].defaultWidget().getIsCopy() == True):
                                        del self.proxyWidgetList[i]
                                        break
                                    # Deletes the original of a defined field without affecting the copy field
                                    elif(self.proxyWidgetList[i] == item and self.proxyWidgetList[i].widget().menu().actions()[0].defaultWidget().getIsCopy() == False):
                                        del self.proxyWidgetList[i]
                                        break
                                else:
                                    del self.proxyWidgetList[i]
                                    break
                                i = i+1    
                            if(not isinstance(item.widget(), QPushButton)):
                                if(isinstance(self.getDefaultWidget(item), Variable)):
                                    # If there's no other occurrences of the deleted field or variable then it going to be removed from the list of defined variable or field
                                    if(self.countOccurrences(item) == 0):
                                        self.variableList.remove(item.widget().menu().actions()[0].defaultWidget().nameLineEdit.text())
                                    self.variable_count -= 1
                                    i = 0
                                    for widget in self.proxyWidgetList:
                                        if(isinstance(self.getDefaultWidget(widget), Variable)):
                                            self.getDefaultWidget(widget).setVariableNumber(i)
                                            i += 1
                                elif(isinstance(self.getDefaultWidget(item), Field)):
                                     if(self.countOccurrences(item) == 0):
                                        self.proxyDefinedFieldList.remove(item.widget().menu().actions()[0].defaultWidget().table.cellWidget(0,1).text())
                            self.removeItem(item)


    # This function counts how repeats are form the item selected for deletion
    def countOccurrences(self, item):
       i = 0
       counter = 0
       while (i < len(self.proxyWidgetList)):
            if(item.widget().text() == self.proxyWidgetList[i].widget().text()):
                counter = counter + 1
            i = i+1
       return counter

    # The following two functions are only preparing the scene to accept any drag movements
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    # In this function is where we will drop the field to the canvas
    def dropEvent(self, event):
        proxy = GraphicsProxyWidget()
        if(event.mimeData().text() == "Field"):
            field = Field()
            proxy = self.addWidgetToScene(field, event.scenePos(), event.mimeData().text())
            self.proxyDefinedFieldList.append(str(proxy.widget().menu().actions()[0].defaultWidget().table.cellWidget(0,1).text()))
            proxy.setPolygon()
        elif(event.mimeData().text() == "Field (String)"):
            str_field = Field()
            str_field.setDataType("STRING")
            proxy = self.addWidgetToScene(str_field, event.scenePos(), event.mimeData().text())
            self.proxyDefinedFieldList.append(str(proxy.widget().menu().actions()[0].defaultWidget().table.cellWidget(0,1).text()))
            proxy.setPolygon()
        elif(event.mimeData().text() == "Field (Integer)"):
            int_field = Field()
            int_field.setDataType("INT32")
            proxy = self.addWidgetToScene(int_field, event.scenePos(), event.mimeData().text())
            self.proxyDefinedFieldList.append(str(proxy.widget().menu().actions()[0].defaultWidget().table.cellWidget(0,1).text()))
            proxy.setPolygon()
        elif(event.mimeData().text() == "Field (Float)"):
            float_field = Field()
            float_field.setDataType("FLOAT")
            proxy = self.addWidgetToScene(float_field, event.scenePos(), event.mimeData().text())
            self.proxyDefinedFieldList.append(str(proxy.widget().menu().actions()[0].defaultWidget().table.cellWidget(0,1).text()))
            proxy.setPolygon()
        elif(event.mimeData().text() == "Field (Octal)"):
            octal_field = Field()
            octal_field.setBase("OCT")
            proxy = self.addWidgetToScene(octal_field, event.scenePos(), event.mimeData().text())
            self.proxyDefinedFieldList.append(str(proxy.widget().menu().actions()[0].defaultWidget().table.cellWidget(0,1).text()))
            proxy.setPolygon()
        elif(event.mimeData().text() == "Code Block"):
            name = "CodeBlock" + str(self.codeBlock_count)
            self.codeBlock_count = self.codeBlock_count + 1

            code_block = CodeBlock(name)
            proxy = self.addWidgetToScene(code_block, event.scenePos(), event.mimeData().text())
            proxy.setPolygon()
        elif(event.mimeData().text() == "while"):
            name = "While" + str(self.while_count)
            self.while_count = self.while_count + 1

            while_loop = While_Loop(name)
            proxy = self.addWidgetToScene(while_loop, event.scenePos(), event.mimeData().text())
            proxy.setPolygon()            
        elif(event.mimeData().text() == "for"):
            name = "ForLoop" + str(self.forloop_count)
            self.forloop_count += 1
            
            for_loop = For_Loop(name)
            proxy = self.addWidgetToScene(for_loop, event.scenePos(), event.mimeData().text())
            proxy.setPolygon()
        # if(event.mimeData().text() == "do while"):
        #     name = "DoWhile" + str(self.doWhile_count)
        #     self.doWhile_count = self.doWhile_count + 1

        #     do_loop = Do_Loop(name)
        #     proxy = self.addWidgetToScene(do_loop, event.scenePos(), event.mimeData().text())
        #     proxy.setPolygon()            
        elif(event.mimeData().text() == "Decision"):
            name = "Decision"+str(self.decision_count)
            self.decision_count = self.decision_count + 1

            decision = Decision(name)
            proxy = self.addWidgetToScene(decision, event.scenePos(), event.mimeData().text())
            proxy.setPolygon()
        elif(event.mimeData().text() == "End Loop"):
            end_loop = QWidget()
            proxy = self.addWidgetToScene(end_loop, event.scenePos(), event.mimeData().text())
            proxy.setPolygon()
        elif(event.mimeData().text() == "do"):
            do_widget = QWidget()
            proxy = self.addWidgetToScene(do_widget, event.scenePos(), event.mimeData().text())
            proxy.setPolygon()
        elif(event.mimeData().text() == "Variable"):
            varNumber = self.variable_count
            self.variable_count += 1
            variable = Variable(varNumber)
            proxy = self.addWidgetToScene(variable, event.scenePos(), event.mimeData().text())
            self.variableList.append(str(proxy.widget().menu().actions()[0].defaultWidget().nameLineEdit.text()))
            proxy.setPolygon()
        else: 
            for widget in self.proxyWidgetList:
                if(event.mimeData().text() == widget.widget().text()):
                    definedWidgetPos = event.scenePos()
                    if(isinstance(widget.widget().menu().actions()[0].defaultWidget(), Field)):
                        definedWidget = self.prepareDefinedWidgetForDrop(event.mimeData().text(),'Field')
                        proxy = self.addWidgetToScene(definedWidget, definedWidgetPos, 'Defined Field')
                        proxy.setPolygon()
                    else:
                        definedWidget = self.prepareDefinedWidgetForDrop(event.mimeData().text(),'Variable')
                        proxy = self.addWidgetToScene(definedWidget, definedWidgetPos, 'Defined Variable')
                        proxy.setPolygon()

        if ((proxy.scenePos().x() + proxy.size().width()) > self.width()):
            self.updateScene(proxy.size().width(), True)
        if ((proxy.scenePos().y() + proxy.size().height()) > self.height()):
            self.updateScene(proxy.size().height(), False)

        self.proxyWidgetList.append(proxy)
        """if(event.mimeData().text()[0:5] == "Field"):
            self.proxyDefinedFieldList.append(proxy)"""
        event.accept()

    def addWidgetToScene(self, widget, pos, text):

        button = None        
        if(text != "End Loop" and text != "do"):
            if(not(isinstance(widget, Field))):
                if(isinstance(widget, Variable)):
                    button = ToolButton(widget, self)
                    button.setText(text)
                    widget.setButton(button)
                    if(text=='Defined Variable'):
                        variable_name = button.menu().actions()[0].defaultWidget().nameLineEdit.text()
                        button.setText(variable_name)
                        widget.setIsCopy(True)
                    else:
                        variable_text = 'No Name Variable' + ' ' + str(self.variable_count)
                        button.setText(variable_text)
                        button.menu().actions()[0].defaultWidget().nameLineEdit.setText(button.text())
                        widget.setIsCopy(False)
                        widget.setName(variable_text)
                        widget.setScene(self)


                
                else:
                    button = QToolButton()
                    button.setPopupMode(QToolButton.MenuButtonPopup)
                    button.setGeometry(QRect(20, 30, 278, 40)) 
                    button.setText(text)
                    menu = QMenu()
                    button.setMenu(menu)
                    action = QWidgetAction(button)
                    action.setDefaultWidget(widget)
                    button.menu().addAction(action)
                
            if(isinstance(widget, Field)):
                if(text[0:5] == "Field"):
                    self.countFields = self.countFields + 1
                    button = ToolButton(widget, self)
                    field_text = button.text() + ' ' + str(self.countFields)
                    button.setText(field_text)
                    button.menu().actions()[0].defaultWidget().table.cellWidget(0,1).setText(field_text)
                    widget.setName(field_text)
                    widget.setButton(button)
                    widget.setIsCopy(False)
                    widget.setScene(self)
                elif(text == "Defined Field"):
                    self.countFields = self.countFields + 1
                    button = ToolButton(widget, self)
                    field_text = button.widget.table.cellWidget(0,1).text()
                    button.setText(field_text)
                    widget.setButton(button)
                    widget.setIsCopy(True)
                    widget.setScene(self)
                else:
                    self.countFields = self.countFields + 1
                    button = ToolButton(widget, self)
                    button.setText(text)
                    widget.setName(field_text)
                    widget.setButton(button)
                    widget.setIsCopy(False)
                    widget.setScene(self)
        else:
            button = QPushButton()
            button.setGeometry(QRect(20, 30, 278, 40))
            button.setText(text)
        
        
        
        """ A QGraphicsWidget is a QGraphicsItem and A QGraphicsItem is movable. So I will create
        a parent over the field widget so the field can be movable"""
        parent = QGraphicsWidget()
        parent.setCursor(Qt.SizeAllCursor)
        parent.setGeometry((pos.x())-70, (pos.y())-70, 80, 90)
        # parent.setGeometry((pos.x()), (pos.y()), 80, 90)
        parent.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        """ Here we are 'dropping' the item to the scene.
         We needed to create a parent over the widget because if would add the widget to scene 
         the widget would be be positioned at (0,0) and we wouldn't be able o move it"""
        self.addItem(parent)

        # This Proxy will allows us to add the child to the parent and drop the  widget to the canvas
        proxy = GraphicsProxyWidget()
        proxy.setWidget(button)
        proxy.setParentItem(parent)

        return proxy


    def prepareDefinedWidgetForDrop(self, text, typeWidget):
        if(typeWidget == 'Field'):
            definedField = Field()
            for field in self.proxyWidgetList:
                if text == field.widget().text():
                    defined_field_properties = field.widget().menu().actions()[0].defaultWidget().saveMethod()
                    definedField.setName(defined_field_properties.get('Name'))
                    definedField.setAbbreviation(defined_field_properties.get('Abbreviation'))
                    definedField.setDescription(defined_field_properties.get('Description'))
                    definedField.setDataType(defined_field_properties.get('Data Type'))
                    definedField.setBase(defined_field_properties.get('Base'))
                    definedField.setMask(defined_field_properties.get('Mask'))
                    definedField.setValueConstraint(defined_field_properties.get('Value Constraint'))
                    definedField.setSize(defined_field_properties.get('Var Size').get('editText'), defined_field_properties.get('Var Size').get('combobox'))
                    definedField.setID(defined_field_properties.get('ID Value'))
                    definedField.setRequired(defined_field_properties.get('Required'))
            return definedField
        else:
            definedVariable = Variable(self.variable_count)
            self.variable_count += 1
            for variable in self.proxyWidgetList:
                if text == variable.widget().text():
                    defined_variable_properties = variable.widget().menu().actions()[0].defaultWidget().saveMethod()
                    definedVariable.setScope(defined_variable_properties.get('Scope'))
                    definedVariable.setName(defined_variable_properties.get('Name'))
                    definedVariable.setDataType(defined_variable_properties.get('Data Type'))
                    definedVariable.setValue(defined_variable_properties.get('Value'))
            return definedVariable


    def restoreWidgetsToScene(self, dissector):
        nameToProxyDict = {} # Used for filling out the values in connectionsDict
        connectionsDict = {} # Keys and Values are proxywidgets, key widget points to value widget on canvass
        self.variable_count = 0
        if('START' in dissector.keys()):
            dissector.pop('START', None)
        for key in dissector.keys():
            widget = dissector[key]
            widgetType = widget["Type"]
            if(widgetType == "Field"):
                widgetToAdd = Field()
                widgetToAdd.setName(widget["Name"])
                widgetToAdd.setAbbreviation(widget["Abbreviation"])
                widgetToAdd.setDescription(widget["Description"])
                widgetToAdd.setDataType(widget["Data Type"])
                widgetToAdd.setBase(widget["Base"])
                widgetToAdd.setMask(widget["Mask"])
                widgetToAdd.setValueConstraint(widget["Value Constraint"])
                if(widget["Var Size"]["combobox"] == "BITS" or widget["Var Size"]["combobox"] == "BYTES"):
                    widgetToAdd.setSize(widget["Var Size"]['editText'], widget["Var Size"]["combobox"])
                else:
                    widgetToAdd.setSizeofVariable(widget["Var Size"]["editText"], widget["Var Size"]["combobox"])
                widgetToAdd.setID(widget["ID Value"])
                widgetToAdd.setRequired(widget["Required"])
                widgetToAdd.setLittleEndian(widget["LE"])
                widgetText = widget["Name"]

            elif(widgetType == "Decision"):
                widgetToAdd = Decision(key)
                self.decision_count += 1
                widgetText = "Decision"
            elif(widgetType == "while"):
                widgetToAdd = While_Loop(key)
                self.while_count += 1
                widgetText = "while"
            # elif(widgetType == "do while"):
            #     widgetToAdd = Do_Loop(key)
            #     self.doWhile_count += 1
            #     widgetText = "do while"
            elif(widgetType == "for"):
                widgetToAdd = For_Loop(key)
                self.forloop_count += 1
                widgetText = "for"
            elif(widgetType == "do"):
                widgetToAdd = QWidget()
                widgetText = "do"
            elif(widgetType == "End Loop"):
                widgetToAdd = QWidget()
                widgetText = "End Loop"
            elif(widgetType == "CodeBlock"):
                widgetToAdd = CodeBlock(key)
                self.codeBlock_count += 1
                widgetToAdd.setTextBox(widget['Code'])
                widgetText = "Code Block"
            elif(widgetType == "Variable"):
                widgetToAdd = Variable(self.variable_count)
                self.variable_count += 1
                widgetToAdd.setName(widget['Name'])
                widgetToAdd.setValue(widget['Value'])
                widgetToAdd.setScope(widget['Scope'])
                widgetToAdd.setDataType(widget['Data Type'])
                widgetText = 'Defined Variable'


            widgetPosition = QPointF(dissector[key]["Position"]["x"], dissector[key]["Position"]["y"])
            proxy = self.addWidgetToScene(widgetToAdd, widgetPosition, widgetText)

            proxy.setPolygon()
            self.proxyWidgetList.append(proxy)
            if(widgetType == "Field"):
                self.proxyDefinedFieldList.append(proxy)
            elif(widgetType == "Variable"):
                self.variableList.append(proxy)

            nameToProxyDict.update({key: proxy})
            
            if(widgetType == "Field" or widgetType == "do" or widgetType == "End Loop" or widgetType == "CodeBlock" or widgetType == "Variable"):
                if(dissector[key]["next_field"] != "END"):
                    connectionsDict.update({proxy: dissector[key]["next_field"]})

            elif(widgetType == "Decision" or widgetType == "while" or widgetType == "do while" or widgetType == "for"):
                if(widgetType == "for"):
                    widgetToAdd.setExpressions(widget["Expressions"])
                else:
                    widgetToAdd.setCondition(widget["Condition"])
                conditionConnections = {}
                # if field has a true key and it's not None
                if("true" in dissector[key].keys()):
                    if(dissector[key]["true"] != "END"):
                        conditionConnections.update({1: dissector[key]["true"]})
                # if field has a false key and it's not None
                if("false" in dissector[key].keys()):
                    if(dissector[key]["false"] != "END"):
                        conditionConnections.update({0: dissector[key]["false"]})
                connectionsDict.update({proxy: conditionConnections})

        # Placing the endItems in the dictionary values
        for key, value in nameToProxyDict.items():
            for startItem, endItem in connectionsDict.items():
                # if there are more than one next_field and key is one of those fields
                if(type(endItem) is dict and key in endItem.values()):
                    # path 0 innerEndItem is for false, path 1 innerEndItem is for true
                    for path, innerEndItem in endItem.items():
                        if(innerEndItem == key):
                            connectionsDict[startItem][path] = value
                            break
                    continue
                elif(endItem == key):
                    connectionsDict[startItem] = value
                    continue

        self.restoreConnectorsToScene(connectionsDict)

    def restoreConnectorsToScene(self, connectionsDict):
        for startItem, endItem in connectionsDict.items():
            # if there is more than one endItem (false,true)
            if(type(endItem) is dict):
                for path, innerEndItem in endItem.items():
                    connector = Connector(startItem, innerEndItem)
                    if(path == 0):
                        connector.setType("False")
                    else:
                        connector.setType("True")
                    startItem.addConnector(connector)
                    innerEndItem.addConnector(connector)
                    connector.setZValue(-1000.0)
                    self.addItem(connector)
                    connector.updatePosition()
            else:
                connector = Connector(startItem, endItem)
                connector.setColor(self.myLineColor)
                startItem.addConnector(connector)
                endItem.addConnector(connector)
                connector.setZValue(-1000.0)
                self.addItem(connector)
                connector.updatePosition()

    def updateScene(self, widgetSize, isX):
        rec = self.sceneRect()
        if(isX):
            self.setSceneRect(rec.x(), rec.y(), (rec.width() + widgetSize), rec.height())
            
        else:
            self.setSceneRect(rec.x(), rec.y(), rec.width(), (rec.height() + widgetSize))
	
    def setMode(self, mode):
        self.myMode = mode

    def mousePressEvent(self, event):
        if self.myMode == self.InsertLine_ON and event.button() == Qt.LeftButton:
            self.line = QGraphicsLineItem(QLineF(event.scenePos(), event.scenePos()))
            self.line.setPen(QPen(self.myLineColor, 2))
            self.addItem(self.line)

        super(DropGraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.myMode == self.InsertLine_ON and self.line:
            newLine = QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(newLine)

        elif self.myMode == self.MoveItem:
            if(len(self.items(event.scenePos())) and isinstance(self.items(event.scenePos())[0], QGraphicsWidget)):
                movingItem = self.items(event.scenePos())[0]
                if(len(movingItem.childItems()) and movingItem.childItems()[0].isMoving()):
                    pass

            super(DropGraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.line and self.myMode == self.InsertLine_ON:
            startItems = self.items(self.line.line().p1())
            if len(startItems) and startItems[0] == self.line:
                startItems.pop(0)
            endItems = self.items(self.line.line().p2())
            if len(endItems) and endItems[0] == self.line:
                endItems.pop(0)

            self.removeItem(self.line)
            self.line = None

            if len(startItems) and len(endItems) and isinstance(startItems[0], GraphicsProxyWidget) and isinstance(endItems[0], GraphicsProxyWidget) and startItems[0] != endItems[0]:
                startItem = startItems[0]
                endItem = endItems[0]
                connector = Connector(startItem, endItem)
                connector.setColor(self.myLineColor)
                startItem.addConnector(connector)
                endItem.addConnector(connector)
                connector.setZValue(-1000.0)
                self.addItem(connector)
                connector.updatePosition()


        self.line = None
        self.myMode = self.MoveItem
        super(DropGraphicsScene, self).mouseReleaseEvent(event)

    def save_dissector(self):
        dissector = {}
        fieldsForJSONFile = {}
        variableCount = 0
        for proxyWidget in self.proxyWidgetList:
            
            # Saving "end loop" or "do" widgets into a dictionary
            if(isinstance(proxyWidget.widget(), QPushButton)):
                if(proxyWidget.widget().text() == "End Loop"):
                    x_position = proxyWidget.scenePos().x()+70
                    y_position = proxyWidget.scenePos().y()+70
                    position = {'x': x_position, 'y': y_position}
                    endLoop = {'Position': position}
                    endLoop.update({'Type': "End Loop"})

                    end_item = ""
                    for connector in proxyWidget.connectors:
                        if connector.endItem().widget() is proxyWidget.widget():
                            continue
                        end_item = self.getNextWidgetName(connector.endItem())
                        endLoop.update({'next_field': end_item})

                    name = "End_" + end_item
                    dissector.update({name: endLoop})
                    
                    
                elif(proxyWidget.widget().text() == "do"):
                    x_position = proxyWidget.scenePos().x()+70
                    y_position = proxyWidget.scenePos().y()+70
                    position = {'x': x_position, 'y': y_position}
                    doWhile_start = {'Position': position}
                    doWhile_start.update({'Type': "do"})
                    
                    for connector in proxyWidget.connectors:
                        if connector.endItem().widget() is proxyWidget.widget():
                            continue
                        end_item = self.getNextWidgetName(connector.endItem())
                        doWhile_start.update({'next_field': end_item})

                    name = self.getDoWidgetName(proxyWidget)

                    if(self.isStartField(proxyWidget)):
                        dissector.update({'START': name})

                    dissector.update({name: doWhile_start})
                continue # continue proxyWidgetList for-loop


            # if widget isn't a "do" or "End Loop", get default widget
            defaultWidget = self.getDefaultWidget(proxyWidget)
            
            # Saving field information into a dictionary
            if(isinstance(defaultWidget, Field)):
                field = defaultWidget.saveMethod()

                x_position = proxyWidget.scenePos().x()+70
                y_position = proxyWidget.scenePos().y()+70
                position = {'x': x_position, 'y': y_position}

                field.update({'Position': position})
                field.update({'Type': "Field"})

                # Getting "next field"
                for connector in proxyWidget.connectors:
                    # Skip if this widget is the endItem of the connector
                    if(not isinstance(connector.endItem().widget(), QPushButton)):
                        if(self.getDefaultWidget(connector.endItem()) is defaultWidget):
                            continue # continue connector for-loop

                    end_item = self.getNextWidgetName(connector.endItem())
                    field.update({'next_field': end_item})

                if(self.isEndField(field)):
                    field.update({'next_field': "END"})

                if(self.isStartField(proxyWidget)):
                    dissector.update({'START': field['Name']}) 

                dissector.update({field['Name']: field})
                fieldsForJSONFile.update({field['Name']: field})

            # Saving Codeblock into dictionary
            elif(isinstance(defaultWidget, CodeBlock)):
                codeBlock = defaultWidget.saveMethod()
                codeBlockName = defaultWidget.getName()

                x_position = proxyWidget.scenePos().x()+70
                y_position = proxyWidget.scenePos().y()+70
                position = {'x': x_position, 'y': y_position}
                codeBlock.update({'Position': position})
                codeBlock.update({'Type': "CodeBlock"})

                # Getting "next field"
                for connector in proxyWidget.connectors:
                    # Skip if this widget is the endItem of the connector
                    if(not isinstance(connector.endItem().widget(), QPushButton)):
                        if(self.getDefaultWidget(connector.endItem()) is defaultWidget):
                            continue # continue connector for-loop

                    end_item = self.getNextWidgetName(connector.endItem())
                    codeBlock.update({'next_field': end_item})

                if(self.isEndField(codeBlock)):
                    codeBlock.update({'next_field': "END"})
                if(self.isStartField(proxyWidget)):
                    dissector.update({'START': codeBlockName})
                dissector.update({codeBlockName: codeBlock})

            # Saving Variable informatin into dictionary
            elif(isinstance(defaultWidget, Variable)):
                variableProperties = defaultWidget.saveMethod()                
                variableName = "Variable"+str(defaultWidget.getVariableNumber())

                x_position = proxyWidget.scenePos().x()+70
                y_position = proxyWidget.scenePos().y()+70
                position = {'x': x_position, 'y': y_position}
                variableProperties.update({'Position': position})
                variableProperties.update({'Type': "Variable"})

                # Getting "next field"
                for connector in proxyWidget.connectors:
                    # Skip if this widget is the endItem of the connector
                    if(not isinstance(connector.endItem().widget(), QPushButton)):
                        if(self.getDefaultWidget(connector.endItem()) is defaultWidget):
                            continue # continue connector for-loop

                    end_item = self.getNextWidgetName(connector.endItem())
                    variableProperties.update({'next_field': end_item})

                if(self.isEndField(variableProperties)):
                    variableProperties.update({'next_field': "END"})
                if(self.isStartField(proxyWidget)):
                    dissector.update({'START': variableName})
                dissector.update({variableName: variableProperties})

            # Saving Decision information into dictionary
            elif(isinstance(defaultWidget, Decision)):
                decision = self.saveConditionWidget(proxyWidget)
                decision[list(decision.keys())[0]].update({'Type': "Decision"})
                dissector.update(decision)

            # Saving While loop information into dictionary
            elif(isinstance(defaultWidget, While_Loop)):
                whileLoop = self.saveConditionWidget(proxyWidget)
                whileLoop[list(whileLoop.keys())[0]].update({'Type': "while"})
                dissector.update(whileLoop)

            # Saving Do While loop information into dictionary
            # elif(isinstance(defaultWidget, Do_Loop)):
            #     doWhile = self.saveConditionWidget(proxyWidget)
            #     doWhile[list(doWhile.keys())[0]].update({'Type': "do while"})
            #     dissector.update(doWhile)

            elif(isinstance(defaultWidget, For_Loop)):
                forLoop = self.saveConditionWidget(proxyWidget)
                forLoop[list(forLoop.keys())[0]].update({'Type': "for"})
                dissector.update(forLoop)


        return dissector

    # called by self.saveDissector() to save Decision, While, For_Loop
    def saveConditionWidget(self, proxyWidget):
        defaultWidget = self.getDefaultWidget(proxyWidget)
        widget_name = defaultWidget.getName()
        
        if(isinstance(defaultWidget, For_Loop)):
            expressions = defaultWidget.saveMethod()
            widget_properties = {'Expressions': expressions}
        else:
            condition = defaultWidget.saveMethod()
            widget_properties = {'Condition': condition}

        x_position = proxyWidget.scenePos().x()+70
        y_position = proxyWidget.scenePos().y()+70
        position = {'x': x_position, 'y': y_position}
        widget_properties.update({'Position': position})

        for connector in proxyWidget.connectors:
            # Skip if this widget is the endItem of the connector
            if(not isinstance(connector.endItem().widget(), QPushButton)):
                if(self.getDefaultWidget(connector.endItem()) is defaultWidget):
                    continue # continue connector for-loop

            end_item = self.getNextWidgetName(connector.endItem())
            if(connector.getType() == "True"):
                widget_properties.update({'true': end_item})
            elif(connector.getType() == "False"):
                widget_properties.update({'false': end_item})

        if('true' not in widget_properties.keys()):
            widget_properties.update({'true': "END"})
        if('false' not in widget_properties.keys()):
            widget_properties.update({'false': "END"})

        if(self.isStartField(proxyWidget)):
            return {widget_name: widget_properties, 'START': widget_name}
        else:
            return {widget_name: widget_properties}

    # widget must be a GraphicsProxyWidget
    def getDefaultWidget(self, widget):
        return widget.widget().menu().actions()[0].defaultWidget()

    def getAbsolutePosition(self, widget):
        point = widget.mapFromScene(0.0,0.0)
        return({'x': abs(point.x()), 'y': abs(point.y())})
        

    # widget properties is a dictionary
    def isEndField(self, widget_properties):
        return not 'next_field' in widget_properties

    def isStartField(self, proxyWidget):
        for connector in proxyWidget.connectors:
            
            if(not isinstance(connector.endItem().widget(), QPushButton)):
                if(connector.endItem() is proxyWidget):
                    if(not isinstance(self.getDefaultWidget(proxyWidget), While_Loop) and not isinstance(self.getDefaultWidget(proxyWidget), For_Loop)):
                        return False # false if this widget is pointed to by a connector
                    else:
                        if(connector.startItem().widget() == QPushButton):
                            continue
                        else:
                            return False
            else:
                if(connector.endItem() is proxyWidget and connector.getType() != "True"):
                    return False
        return True # true if no connectors are pointed to this widget

    # endItem is connector.endItem()
    def getNextWidgetName(self, endItem):

        # This assumes that "End Loop" is pointing to a loop widget in the dissector pane
        if(isinstance(endItem.widget(), QPushButton) and endItem.widget().text() == "End Loop"):
            for connector in endItem.connectors:
                if(connector.endItem() is endItem):
                    continue
                else:
                    connectedLoopWidget_name = self.getNextWidgetName(connector.endItem())
                    endItem_name = "End_" + connectedLoopWidget_name
                    return endItem_name


        if(isinstance(endItem.widget(), QPushButton) and endItem.widget().text() == "do"):
            return self.getDoWidgetName(endItem)

        endItem_Widget = self.getDefaultWidget(endItem)
        endItem_name = ""
        if(isinstance(endItem_Widget,Field)):
            endItem_name = endItem_Widget.table.cellWidget(0,1).text()

        elif(isinstance(endItem_Widget, Decision) or isinstance(endItem_Widget,While_Loop) or
             isinstance(endItem_Widget, For_Loop) or isinstance(endItem_Widget, CodeBlock)):
            endItem_name = endItem_Widget.getName()
        elif(isinstance(endItem_Widget, Variable)):
            # if(endItem_Widget.getName() == ""):
            #     self.variable_count += 1
            #     tempVariableName = "Variable"+str(self.variable_count)
            #     endItem_Widget.setName(tempVariableName)
            #     endItem_name = tempVariableName
            # else:
            #     endItem_name = endItem_Widget.getName()
            endItem_name = "Variable"+str(endItem_Widget.getVariableNumber())

        return endItem_name

    def getDoWidgetName(self, doProxyWidget):

        # Checks if connected to a while already
        for connector in doProxyWidget.connectors:
            if(connector.endItem() is doProxyWidget and 
                (isinstance(self.getDefaultWidget(connector.startItem()), While_Loop))):
                whileWidget = self.getDefaultWidget(connector.startItem())
                connectedWhileWidget_name = whileWidget.getName()

                doWidget_name = "do_" + connectedWhileWidget_name
                return doWidget_name

        # Gives default name
        doWidget_name = "do_" + str(self.while_count)
        return doWidget_name

    def clearCanvass(self):
        for item in self.proxyWidgetList:
            item.removeConnectors()
            self.removeItem(item)
        self.proxyWidgetList.clear()
        self.proxyDefinedFieldList.clear()
        self.variableList.clear()
        self.countFields = 0
        self.decision_count = 0
        self.while_count = 0 
        self.forloop_count = 0
        self.codeBlock_count = 0
        self.variable_count = 0

