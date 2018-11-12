# encoding: utf-8
from gvsig.uselib import use_plugin
use_plugin("org.gvsig.toolbox")
use_plugin("org.gvsig.geoprocess.app.mainplugin")

import gvsig
import pdb
from gvsig import geom
from gvsig import commonsdialog
from gvsig.libs.toolbox import ToolboxProcess, NUMERICAL_VALUE_DOUBLE,SHAPE_TYPE_POLYGON,NUMERICAL_VALUE_INTEGER,SHAPE_TYPE_POLYGON, SHAPE_TYPE_POINT, SHAPE_TYPE_MIXED
from es.unex.sextante.gui import core
from es.unex.sextante.gui.core import NameAndIcon
from es.unex.sextante.additionalInfo import AdditionalInfoVectorLayer
from es.unex.sextante.gui.core import SextanteGUI
from org.gvsig.geoprocess.lib.api import GeoProcessLocator
from addons.AoristicClockGrid.aoristicClockGrid import aoristicClockGrid
from org.gvsig.tools import ToolsLocator
from org.gvsig.andami import PluginsLocator
import os
from java.io import File

class AoristicClockGridGeoprocess(ToolboxProcess):
  def getHelpFile(self):
    name = "aoristicclockgrid"
    extension = ".xml"
    locale = PluginsLocator.getLocaleManager().getCurrentLocale()
    tag = locale.getLanguage()
    #extension = ".properties"

    helpPath = gvsig.getResource(__file__, "help", name + "_" + tag + extension)
    if os.path.exists(helpPath):
        return File(helpPath)
    #Alternatives
    alternatives = PluginsLocator.getLocaleManager().getLocaleAlternatives(locale)
    for alt in alternatives:
        helpPath = gvsig.getResource(__file__, "help", name + "_" + alt.toLanguageTag() + extension )
        if os.path.exists(helpPath):
            return File(helpPath)
    # More Alternatives
    helpPath = gvsig.getResource(__file__, "help", name + extension)
    if os.path.exists(helpPath):
        return File(helpPath)
    return None
  def defineCharacteristics(self):
    i18nManager = ToolsLocator.getI18nManager()
    self.setName(i18nManager.getTranslation("_Aoristic_clock_grid_name"))
    self.setGroup(i18nManager.getTranslation("_Criminology_group"))

    self.setUserCanDefineAnalysisExtent(False)
    params = self.getParameters()
    params.addInputVectorLayer("LAYER",i18nManager.getTranslation("_Input_layer"), AdditionalInfoVectorLayer.SHAPE_TYPE_ANY, True)
    params.addNumericalValue("PROPORTIONX", i18nManager.getTranslation("_Proportion_X"),0, NUMERICAL_VALUE_DOUBLE)
    params.addNumericalValue("PROPORTIONY", i18nManager.getTranslation("_Proportion_Y"),0, NUMERICAL_VALUE_DOUBLE)
    params.addTableField("FIELDHOUR", i18nManager.getTranslation("_Field_hour"), "LAYER", True)
    params.addString("PATTERNHOUR", i18nManager.getTranslation("_Pattern_hour"))
    
    params.addTableField("FIELDDAY", i18nManager.getTranslation("_Field_day"), "LAYER", True)
    params.addString("PATTERNDAY", i18nManager.getTranslation("_Pattern_day"))
    params.addString("FILTEREXPRESSION",i18nManager.getTranslation("_Filter_expression"))
    
  def processAlgorithm(self):
        features=None
        params = self.getParameters()
        sextantelayer = params.getParameterValueAsVectorLayer("LAYER")
        proportionX = params.getParameterValueAsDouble("PROPORTIONX")
        proportionY = params.getParameterValueAsDouble("PROPORTIONY")
        
        nameFieldHour = params.getParameterValueAsInt("FIELDHOUR")
        nameFieldDay =  params.getParameterValueAsInt("FIELDDAY")
        
        patternHour = params.getParameterValueAsString("PATTERNHOUR")
        patternDay =  params.getParameterValueAsString("PATTERNDAY")
        expression = params.getParameterValueAsString("FILTEREXPRESSION")
        store = sextantelayer.getFeatureStore()

        aoristicClockGrid(store,
                      proportionX,
                      proportionY,
                      nameFieldHour,
                      nameFieldDay,
                      patternHour,
                      patternDay,
                      expression,
                      0,
                      0,
                      self)
        print "Proceso terminado %s" % self.getCommandLineName()
        return True
        
def main(*args):
        process = AoristicClockGridGeoprocess()
        process.selfregister("Scripting")
        process.updateToolbox()