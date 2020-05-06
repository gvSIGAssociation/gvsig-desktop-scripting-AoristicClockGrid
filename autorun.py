# encoding: utf-8
import gvsig
from gvsig import getResource
from java.io import File
from org.gvsig.tools import ToolsLocator


try:
  from addons.AoristicClockGrid.aoristicClockGridGeoprocess import AoristicClockGridGeoprocess
except:
  import sys
  ex = sys.exc_info()[1]
  gvsig.logger("Can't load module 'AoristicClockGridGeoprocess'. " + str(ex), gvsig.LOGGER_WARN)#, ex)
  AoristicClockGridGeoprocess = None


def i18nRegister():
    i18nManager = ToolsLocator.getI18nManager()
    i18nManager.addResourceFamily("text",File(getResource(__file__,"i18n")))
  
def main(*args):
  if AoristicClockGridGeoprocess == None:
    return
  i18nRegister()
  process = AoristicClockGridGeoprocess()
  process.selfregister("Scripting")
  process.updateToolbox()
