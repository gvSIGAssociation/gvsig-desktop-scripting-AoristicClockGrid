# encoding: utf-8

import gvsig
import pdb
from gvsig import geom
from gvsig import commonsdialog
from gvsig.libs.toolbox import ToolboxProcess, NUMERICAL_VALUE_DOUBLE,SHAPE_TYPE_POLYGON,NUMERICAL_VALUE_INTEGER,SHAPE_TYPE_POLYGON, SHAPE_TYPE_POINT
from es.unex.sextante.gui import core
from es.unex.sextante.gui.core import NameAndIcon

from es.unex.sextante.gui.core import SextanteGUI
from org.gvsig.geoprocess.lib.api import GeoProcessLocator

from addons.PointDensityGrid import pointDensityGrid
reload(pointDensityGrid)

from addons.PointDensityGrid.pdglib.hexa_grid import pointDensityGrid_hexa
from addons.PointDensityGrid.pdglib.square_grid import pointDensityGrid_square
from addons.PointDensityGrid.pointDensityGrid import pointDensityGridCreation
from addons.PointDensityGrid.pointDensityGrid import GRID_HEXAGON_HORIZONTAL,GRID_HEXAGON_VERTICAL,GRID_SQUARE

class AoristicClockGridGeoprocess(ToolboxProcess):
  def defineCharacteristics(self):
      self.setName("_Point_density_grid_geoprocess_name")
      self.setGroup("_Criminology_group")
      self.setUserCanDefineAnalysisExtent(False)
      params = self.getParameters()
      params.addInputVectorLayer("LAYER","_Input_layer", SHAPE_TYPE_POINT, True)
      params.addNumericalValue("DISTANCEGRID", "_Grid_distance",0, NUMERICAL_VALUE_DOUBLE)
      params.addSelection("GRIDTYPE", "_Grid_type", 
                          [GRID_HEXAGON_HORIZONTAL, 
                           GRID_HEXAGON_VERTICAL,
                           GRID_SQUARE]);
      params.addBoolean("ADDEMPTYGRID", "_Add_empty_grids", True)
      params.addString("EXPRESSION", "_Value_expression")
      self.addOutputVectorLayer("RESULT_POLYGON", "DensityGrid", SHAPE_TYPE_POLYGON)
      
  def processAlgorithm(self):
        features=None
        params = self.getParameters()
        sextantelayer = params.getParameterValueAsVectorLayer("LAYER")
        distancegrid = params.getParameterValueAsDouble("DISTANCEGRID")
        gridType = params.getParameterValueAsString("GRIDTYPE")
        addEmptyGrids = params.getParameterValueAsBoolean("ADDEMPTYGRID")
        valueExpression = params.getParameterValueAsString("EXPRESSION")

        store = sextantelayer.getFeatureStore()
        projection = sextantelayer.getCRS()

        pointDensityGridCreation(self, store, gridType, distancegrid, addEmptyGrids, projection)
        print "Proceso terminado %s" % self.getCommandLineName()
        return True
        
def main(*args):
        process = PointDensityGridGeoprocess()
        process.selfregister("Scripting")
        process.updateToolbox()