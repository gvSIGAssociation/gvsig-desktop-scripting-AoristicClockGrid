# encoding: utf-8
import gvsig
from gvsig import getResource
from java.io import File
from org.gvsig.tools import ToolsLocator
from addons.AoristicClockGrid.aoristicClockGridGeoprocess import AoristicClockGridGeoprocess

def i18nRegister():
    i18nManager = ToolsLocator.getI18nManager()
    i18nManager.addResourceFamily("text",File(getResource(__file__,"i18n")))
  
def main(*args):
  i18nRegister()
  process = AoristicClockGridGeoprocess()
  process.selfregister("Scripting")
  process.updateToolbox()
