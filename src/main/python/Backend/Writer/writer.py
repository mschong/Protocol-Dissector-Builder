try:
    a = open("PCAPServices.py")
except:
    testMe = open("PCAPServices.py","w+")
    testMe.write(
'''
import PCAP
import sys
global PCAPFile
try:
    while(1):
        print("loop")
        currCommand = input().split(" ")
        if currCommand[0] == "create":
            PCAPFile = PCAP.PCap(currCommand[1])
            PCAPFile.convertPCAP()
        elif currCommand[0] =="print":
            print("Printing")
            PCAPFile.printPackets()
            print("Success!")
            sys.exit()
        elif currCommand[0] == "save":
            PCAPFile.savePackets()
            print("saved")
        elif currCommand[0] == "dissect":
            PCAPFile.dissectPCAP(currCommand[1],currCommand[2])
            PCAPFile.colorFilter(currCommand[1],currCommand[2])
            PCAPFile.savePackets()
            print("dissected")
            sys.exit()
        elif currCommand[0] == "colorcode":
            #PCAPFile.colorFilter()
            print("colored")
        elif currCommand[0] == "debug":
            print(currCommand)
        else:
            pass
        currCommand = ""
except Exception as e:
    writeMe = open("errorFile","w+")
    writeMe.write(str(e))
'''
    )

    testMe.close()
try:
    a = open("PCAP.py")
except:
    testMe = open ("PCAP.py","w+")

    testMe.write(
    '''
from subprocess import call
import pyshark
import os
import py
import json
import platform
class PCap:
    def __init__(self,PCAPLocation):
        self.fileLocation = PCAPLocation
        self.pcapFile =""
        self.pcapDissectedFile=""
        # self.colorFlag = False
        self.yellowFlag = False
        self.colorList = {}
    def convertPCAP(self):
        print("Opening file with PyShark")

        self.pcapFile = pyshark.FileCapture(self.fileLocation)
        print("Done")
        return "Done"

    def dissectPCAP(self,workspace,project):
        paramPath = '{}/Lua/{}.lua'.format(workspace,project)
        print("Loading lua script from {}".format(paramPath))
        param = {"-X": 'lua_script:'  + paramPath}

        self.pcapFile = pyshark.FileCapture(input_file=self.fileLocation,custom_parameters=param)
        return "SUCCESSFUL"

    def savePackets(self):
        packets = {}
        protocols = {}
        fields = {}
        output = []
        try:
            os.remove("{}/{}.log".format(os.getcwd(), "dictColor"))
            os.remove("{}/{}.log".format(os.getcwd(), "dict"))
        except:
            pass

        for pkt in self.pcapFile:
            number = pkt.frame_info.get_field_value("number")
            protocols = {}
            for protocol in (pkt.frame_info.protocols).split(":"):
                fields = {}
                try:
                    for val in pkt[protocol].field_names:
                        fields[val] = pkt[protocol].get_field_value(val)
                except:
                    pass
                protocols[protocol] = fields
            packets[number] = protocols

        if self.colorList:
            # if platform.system() == 'Linux' or platform.system() == 'Windows':
            #     writeFile = open("../UI/MainPane/dictColor.log","w")
            # if platform.system() == 'Darwin':
            writeFile = open("{}/{}.log".format(os.getcwd(), "dictColor"), "w+")
            # writeFile = open(os.getcwd() + "/src/main/python/UI/MainPane/dictColor.log","w+")
            output = [packets,protocols,self.colorList]
        else:
            # if platform.system() == 'Linux' or platform.system() == 'Windows':
            #     writeFile = open("../UI/MainPane/dict.log","w")
            # if platform.system() == 'Darwin':
            # writeFile = open(os.getcwd() + "/src/main/python/UI/MainPane/dict.log","w+")
            writeFile = open("{}/{}.log".format(os.getcwd(), "dict"), "w+")

            output = [packets,protocols]
        json.dump(output,writeFile)
        writeFile.close()

    def printPackets(self):
        i=0
        for pkt in self.pcapFile:
            print("Packet #: " + str(i))
            print(pkt.pretty_print())
            i = i+1

    def colorFilter(self,workspace,project):
        tw = py.io.TerminalWriter()
        i = 0
        j = 0
        path = '{}/{}.pdbproj'.format(workspace,project)
        print("CURR PATH {}".format(path))
        with open(path) as f:
            data = json.load(f)
        if os.listdir(workspace) == []:
            self.yellowFlag = True
            for x in self.pcapFile:
                self.colorList[j] = "Yellow"
                j+=1
        for pkt in self.pcapFile:
            self.colorList[i] = ""
            theProtocols =pkt.frame_info.protocols.split(":")
            for prot in theProtocols:
                expectedVal=""
                try:
                    expectedVal = list(data.keys())[list(data.values()).index(prot)]
                except Exception as e:
                    pass
                if prot in data.values():
                    if prot==data['name']:
                        self.colorList[i] = "Green"
                        break
                    else:
                        if prot.casefold()==str(pkt.transport_layer).casefold():
                            try:
                                diff = ""
                                diff = (set(pkt[prot].field_names) ^ set(data.keys()))
                            except Exception as e:
                                print(str(e))
                                pass
                            if  len(diff)-len(data.keys()) > 0:
                                self.colorList[i] = "Yellow"
                if self.colorList[i] == "":
                            self.colorList[i] = "Red"
            if (self.yellowFlag == True) or (self.colorList[i] == "Yellow"):
                tw.write("%s : %s" %( str(i+1), pkt), yellow=True, bold=True)
            elif self.colorList[i] == "Red":
                tw.write("%s : %s" %( str(i+1), pkt), red=True, bold=True)
            else:
                tw.write("%s : %s" %( str(i+1), pkt), green=True, bold=True)
            i+=1
        print("COMPLETE")

'''
    )
    testMe.close()
try:
    a = open("demo.py")
except:
    testMe = open("demo.py","w+")
    testMe.write('''
#!/usr/bin/python

"""
The MIT License (MIT)

Copyright (c) 2016 Luca Weiss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor

from waitingspinnerwidget import QtWaitingSpinner


class Demo(QWidget):


    spinner = None

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        groupbox1 = QGroupBox()
        groupbox1_layout = QHBoxLayout()
        self.setLayout(grid)
        self.setWindowTitle("LOADING")
        self.setMinimumSize(200,200)
        self.setWindowFlags(Qt.Dialog)

        # SPINNER
        self.spinner = QtWaitingSpinner(self)
        self.spinner.setLineWidth(15)
        self.spinner.setLineLength(30)
        self.spinner.setColor(QColor(0,0,139))


        # Layout adds
        groupbox1_layout.addWidget(self.spinner)
        groupbox1.setLayout(groupbox1_layout)


        grid.addWidget(groupbox1, *(1, 1))
        self.spinner.start()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Demo()
    sys.exit(app.exec())
    ''')
    testMe.close()
try:
    a = open("waitingspinnerwidget.py")
except:
    tryMe = open("waitingspinnerwidget.py","w+")
    tryMe.write('''
"""
The MIT License (MIT)

Copyright (c) 2012-2014 Alexander Turkin
Copyright (c) 2014 William Hallatt
Copyright (c) 2015 Jacob Dawid
Copyright (c) 2016 Luca Weiss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QtWaitingSpinner(QWidget):
    def __init__(self, parent, centerOnParent=True, disableParentWhenSpinning=False, modality=Qt.NonModal):
        super().__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        # WAS IN initialize()
        self._color = QColor(Qt.black)
        self._roundness = 100.0
        self._minimumTrailOpacity = 3.14159265358979323846
        self._trailFadePercentage = 80.0
        self._revolutionsPerSecond = 1.57079632679489661923
        self._numberOfLines = 20
        self._lineLength = 10
        self._lineWidth = 2
        self._innerRadius = 10
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()
        # END initialize()

        self.setWindowModality(modality)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, QPaintEvent):
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(Qt.NoPen)
        for i in range(0, self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength, self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(i, self._currentCounter, self._numberOfLines)
            color = self.currentLineColor(distance, self._numberOfLines, self._trailFadePercentage,
                                          self._minimumTrailOpacity, self._color)
            painter.setBrush(color)
            painter.drawRoundedRect(QRect(0, -self._lineWidth / 2, self._lineLength, self._lineWidth), self._roundness,
                                    self._roundness, Qt.RelativeSize)
            painter.restore()

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.updateSize()

    def color(self):
        return self._color

    def roundness(self):
        return self._roundness

    def minimumTrailOpacity(self):
        return self._minimumTrailOpacity

    def trailFadePercentage(self):
        return self._trailFadePercentage

    def revolutionsPersSecond(self):
        return self._revolutionsPerSecond

    def numberOfLines(self):
        return self._numberOfLines

    def lineLength(self):
        return self._lineLength

    def lineWidth(self):
        return self._lineWidth

    def innerRadius(self):
        return self._innerRadius

    def isSpinning(self):
        return self._isSpinning

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color=Qt.black):
        self._color = QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize(self):
        size = (self._innerRadius + self._lineLength) * 2
        self.setFixedSize(size, size)

    def updateTimer(self):
        self._timer.setInterval(1000 / (self._numberOfLines * self._revolutionsPerSecond))

    def updatePosition(self):
        if self.parentWidget() and self._centerOnParent:
            self.move(self.parentWidget().width() / 2 - self.width() / 2,
                      self.parentWidget().height() / 2 - self.height() / 2)

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, colorinput):
        color = QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color
    ''')
    tryMe.close()
