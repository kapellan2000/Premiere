# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2020 Richard Premiere
#
# Licensed under GNU GPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import platform
import shutil

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

if platform.system() == "Windows":
    if sys.version[0] == "3":
        import winreg as _winreg
    else:
        import _winreg

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_Premiere_Integration(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.examplePath, self.afVersion = self.getPremierePath()
    @err_catcher(name=__name__)
    def getPremierePath(self, single=True):
        try:
            psPaths = []
            if platform.system() == "Windows":
                psPaths = ["C:\Program Files (x86)\Common Files\Adobe\CEP\extensions\\"]
                afVersion = 0
            elif platform.system() == "Darwin":
                for foldercont in os.walk("/Applications"):
                    for folder in reversed(sorted(foldercont[1])):
                        if folder.startswith("Adobe Premiere Pro"):
                            psPaths.append(os.path.join(foldercont[0], folder))
                            if single:
                                break
                    break
        
            if single:
                return psPaths[-1],afVersion if psPaths else None
            else:
                return psPaths if psPaths else []
        except:
            return None

    def addIntegration(self, installPath):
        try:
            if not os.path.exists(installPath):
                QMessageBox.warning(
                    self.core.messageParent,
                    "Prism Integration",
                    "Invalid Premiere path: %s.\nThe path doesn't exist."
                    % installPath,
                    QMessageBox.Ok,
                )
                return False

            #if int(str(installPath)[-4:])< 2019:
            #    QMessageBox.warning(self.core.messageParent, "Prism Integration", "Unsupported version. Use Premiere 2019 or higher")
            #    return ""
                
            integrationBase = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "Integration"
            )

            if platform.system() == "Windows":
                osName = "Windows"
            elif platform.system() == "Darwin":
                osName = "Mac"


            origLFile = os.path.join(integrationBase,"Windows", "CEP.ppro")
            scriptdir = os.path.join(installPath)
            pkgdir = os.path.join(scriptdir,"CEP.ppro")
            mainServer = os.path.join(installPath,"CEP.ppro","js","main.js")
            
            if os.path.exists(pkgdir):
                #os.remove(scriptdir)
                shutil.rmtree(pkgdir)

            #shutil.copy2(origLFile, scriptdir)
            shutil.copytree(origLFile, pkgdir)
            with open(mainServer, "r") as init:
                initStr = init.read()

            with open(mainServer, "w") as init:
                initStr = initStr.replace(
                    "PRISMROOT",  self.core.prismRoot.replace("/", "\\\\")
                )
                init.write(initStr)


            #confFile = "Adobe After Effects " + str(self.afVersion) + " Prefs.txt"
            #config = os.path.join(os.environ["appdata"],"Adobe", "After Effects", str(self.afVersion), confFile)

            #with open(config, "r") as initConf:
            #    initStrConf = initConf.read()

            #with open(config, "w") as initConf:
            #    initStrConf = initStrConf.replace(
            #        '"Pref_SCRIPTING_FILE_NETWORK_SECURITY" = "0', '"Pref_SCRIPTING_FILE_NETWORK_SECURITY" = "1'
            #    )
            #    initConf.write(initStrConf)





            #if result is True:
            return True
            #else:
            #    raise Exception(result)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msgStr = (
                "Errors occurred during the installation of the Premiere integration.\nThe installation is possibly incomplete.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )
            msgStr += "\n\nRunning this application as administrator could solve this problem eventually."

            self.core.popup(msgStr, title="Prism Integration")
            return False

    def removeIntegration(self, installPath):
        try:
            for i in [
                "Prism.jsx",
            ]:
                fPath = os.path.join(installPath, "Support Files", "Scripts", "ScriptUI Panels", i)
                if os.path.exists(fPath):
                    os.remove(fPath)

            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()

            msgStr = (
                "Errors occurred during the removal of the Premiere integration.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )
            msgStr += "\n\nRunning this application as administrator could solve this problem eventually."

            self.core.popup(msgStr, title="Prism Integration")
            return False

    def updateInstallerUI(self, userFolders, pItem):
    
        try:
        
            psItem = QTreeWidgetItem(["Premiere"])
            psItem.setCheckState(0, Qt.Checked)
            pItem.addChild(psItem)

            psPaths = self.getPremierePath(single=False) or []
            
            psCustomItem = QTreeWidgetItem(["Custom"])
            psCustomItem.setToolTip(0, 'e.g. "%s"' % self.examplePath)
            psCustomItem.setToolTip(1, 'e.g. "%s"' % self.examplePath)
            psCustomItem.setText(1, "< doubleclick to browse path >")
            psCustomItem.setCheckState(0, Qt.Unchecked)
            psItem.addChild(psCustomItem)
            psItem.setExpanded(True)

            activeVersion = False
            for i in reversed(psPaths):
                psVItem = QTreeWidgetItem([i[-4:]])
                psItem.addChild(psVItem)

                if os.path.exists(i):
                    psVItem.setCheckState(0, Qt.Checked)
                    psVItem.setText(1, i)
                    psVItem.setToolTip(0, i)
                    psVItem.setText(1, i)
                    activeVersion = True
                else:
                    psVItem.setCheckState(0, Qt.Unchecked)
                    psVItem.setFlags(~Qt.ItemIsEnabled)

            if not activeVersion:
                psItem.setCheckState(0, Qt.Unchecked)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = QMessageBox.warning(
                self.core.messageParent,
                "Prism Installation",
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno),
            )
            return False

    def installerExecute(self, PremiereItem, result):
        try:
            psPaths = []
            installLocs = []

            if PremiereItem.checkState(0) != Qt.Checked:
                return installLocs

            for i in range(PremiereItem.childCount()):
                item = PremiereItem.child(i)
                if item.checkState(0) == Qt.Checked and os.path.exists(item.text(1)):
                    psPaths.append(item.text(1))

            for i in psPaths:
                result["Premiere integration"] = self.core.integration.addIntegration(self.plugin.pluginName, path=i, quiet=True)
                if result["Premiere integration"]:
                    installLocs.append(i)

            return installLocs
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = QMessageBox.warning(
                self.core.messageParent,
                "Prism Installation",
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno),
            )
            return False
