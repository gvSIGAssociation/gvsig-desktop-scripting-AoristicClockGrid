# encoding: utf-8

import gvsig
from gvsig import geom
import sys
import datetime
from org.gvsig.symbology.fmap.mapcontext.rendering.legend.styling import LabelingFactory
from org.gvsig.symbology.fmap.mapcontext.rendering.legend.impl import SingleSymbolLegend
from java.awt import Color
from org.gvsig.symbology.swing import SymbologySwingLocator
from org.gvsig.fmap.mapcontext import MapContextLocator
from org.gvsig.tools import ToolsLocator
from java.util import Date
from java.util import Calendar
from java.text import SimpleDateFormat
from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR
from org.gvsig.fmap.dal import DALLocator
from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from org.gvsig.fmap.dal.feature import FeatureStore

def main(*args):
  proportionX = 1
  proportionY = 1
  nameFieldHour = "CDATE"
  nameFieldDay = "CMPLNT_FR_"
  nameFieldHour = "CMPLNT_FR_"
  dm = DALLocator.getDataManager()
  evaluator = dm.createExpresion("")
  exp = ExpressionEvaluatorLocator.getManager().createExpression()
  exp.setPhrase('')
  print evaluator
  expression = exp
  xi = 0
  yi = 0
  store = gvsig.currentLayer().getFeatureStore()
  aoristicClockGrid(store,
                      proportionX,
                      proportionY,
                      nameFieldHour,
                      nameFieldDay,
                      expression,
                      0,
                      0)
  
def aoristicClockGrid(store,
                      proportionX,
                      proportionY,
                      nameFieldHour,
                      nameFieldDay,
                      expression,
                      xi=0,
                      yi=0,
                      selfStatus=None):

  
  
  # Setting coordinates to aoristic clock
  
  #layer = gvsig.currentLayer()
    
  # New points layer
  schema = gvsig.createFeatureType(store.getDefaultFeatureType()) # DefaultFeatureType
  newPoints = gvsig.createShape(schema)
  
  ##
  ## TRANSFROM TO DATE COORDINATES FOR GRID
  ##
  #if store.getSelection().getSize()==0:
  #  fs = store.getFeatureSet(fq)
  #else:
  #  fs = store.getSelection()
    ###
  ### GET VALUES
  ###
  if store.getSelection().getSize()!=0:
    fset = store.getSelection()
  elif expression.getPhrase() != '':
    evaluator = DALLocator.getDataManager().createExpresion(expression)
    #evaluator = expressionEvaluatorManager.createEvaluator(expression)
    fq = store.createFeatureQuery()
    fq.addFilter(evaluator)
    fq.retrievesAllAttributes()
    fset = store.getFeatureSet(fq)
  else:
    fset = store.getFeatureSet()
    
  newStore = newPoints.getFeatureStore()
  newStore.edit(FeatureStore.MODE_APPEND)
  size = fset.getSize()
  if selfStatus!=None: selfStatus.setRangeOfValues(0,size)
  n = 0
  i18nManager = ToolsLocator.getI18nManager()
  processText = i18nManager.getTranslation("_Processing")
  for f in fset:
    n+=1
    if selfStatus!=None: 
      selfStatus.next()
      selfStatus.setProgressText(processText + ": " + str(n)+" / "+str(int(size)))
      if selfStatus.isCanceled() == True:
        newPoints.finishEditing()
        return True
    dateFieldHour = f.get(nameFieldHour) #getFieldAsDate(f.get(nameFieldHour), patternHour)
    dateFieldDay = f.get(nameFieldDay) #getFieldAsDate(f.get(nameFieldDay), patternDay)
    newDateGeom = getGeometryFromDayHour(dateFieldDay, dateFieldHour,proportionX, proportionY)
    nf = newStore.createNewFeature(f)
    nf.setDefaultGeometry(newDateGeom)
    newStore.insert(nf)
    
  newStore.commit()
  gvsig.currentView().addLayer(newPoints)

  baseLines = createBaseLayers(proportionX, proportionY)

  ###
  ### LEGEND AND LABELS
  ###
  mp = MapContextLocator.getMapContextManager()
  try:
    leg = mp.createLegend("HeatmapLegend")
    leg.setROI(baseLines.getFullEnvelope().getGeometry())
    #leg.setUseFixedViz(False)
    #leg.setCorrectionFixedViz(100)
    leg.setDistance(30)
    try:
      colorTables = SymbologySwingLocator.getSwingManager().createColorTables()
      colorTable = colorTables.get(0)
      leg.setColorTable(colorTable.getColors())
    except:
      leg.setColorTable(100, Color(0, 0, 255, 0), Color(255, 0, 0, 255))
    newPoints.setLegend(leg)
  except:
    ex = sys.exc_info()[1]
    error = "Error" + str(ex.__class__.__name__)+ str(ex)
    logger(error, LOGGER_ERROR)
  newPoints.setName("Ao-Data")
  
  
def createBaseLayers( proportionX = 1, proportionY = 1):

  schema = gvsig.createFeatureType() # DefaultFeatureType
  schema.append("GEOMETRY", "GEOMETRY")
  schema.get("GEOMETRY").setGeometryType(geom.LINE, geom.D2)
  baseLines = gvsig.createShape(schema)

  schema = gvsig.createFeatureType() # DefaultFeatureType
  schema.append("LABEL", "STRING", 20)
  schema.append("GEOMETRY", "GEOMETRY")
  schema.get("GEOMETRY").setGeometryType(geom.POINT, geom.D2)
  basePoints = gvsig.createShape(schema)
  i18nManager = ToolsLocator.getI18nManager()
  days = {0:i18nManager.getTranslation("_Monday"),
          1:i18nManager.getTranslation("_Tuesday"),
          2:i18nManager.getTranslation("_Wednesday"),
          3:i18nManager.getTranslation("_Thursday"),
          4:i18nManager.getTranslation("_Friday"),
          5:i18nManager.getTranslation("_Saturday"),
          6:i18nManager.getTranslation("_Sunday")
          }

  # Y axis: Days
  
  numberDays = 7
  numberHours = 24
  
  for k in range(0, numberHours+1):
    line = geom.createGeometry(geom.LINE)
    for i in range(0,numberDays):
      x = proportionX * k
      y = proportionY * i
      point = geom.createPoint(geom.D2,x, y)
      line.addVertex(point)
      if i==numberDays-1:
        x = x
        y = y+0.2
        point = geom.createPoint(geom.D2,x, y)
        basePoints.append({"LABEL":k,"GEOMETRY":point})
      
    baseLines.append({"GEOMETRY": line})
  
  # X axis: Days
  numberDays = 7
  numberHours = 24
  
  for i in range(0, numberDays):
    line = geom.createGeometry(geom.LINE)
    x = 0
    y = proportionY * i
    point = geom.createPoint(geom.D2,x, y)
    line.addVertex(point)
    
    x = proportionX * numberHours
    point = geom.createPoint(geom.D2,x, y)
    line.addVertex(point)
      
    baseLines.append({"GEOMETRY": line})

    x = -2.5
    y = y - 0.2
    point = geom.createPoint(geom.D2,x, y)
    basePoints.append({"LABEL":days[i],"GEOMETRY":point})

  # Commits
  basePoints.commit()
  basePoints.setName("Ao-Label")
  baseLines.commit()
  baseLines.setName("Ao-Grid")
  
  # Labels and legends
  ds = LabelingFactory().createDefaultStrategy(basePoints)
  
  ds.setTextField("LABEL")
  ds.setFixedSize(20)
  basePoints.setLabelingStrategy(ds)
  basePoints.setIsLabeled(True)

  leg = SingleSymbolLegend()
  leg.setShapeType(geom.POINT)
  manager = leg.getSymbolManager()
  pointSymbol = manager.createSymbol(geom.POINT)
  pointSymbol.setColor(Color.black)
  pointSymbol.setSize(0)
  leg.setDefaultSymbol(pointSymbol)
  basePoints.setLegend(leg)


  leg = SingleSymbolLegend()
  leg.setShapeType(geom.LINE)
  manager = leg.getSymbolManager()
  newline = manager.createSymbol(geom.LINE)
  newline.setColor(Color.black)
  leg.setDefaultSymbol(newline)
  baseLines.setLegend(leg)
  
  gvsig.currentView().addLayer(basePoints)
  gvsig.currentView().addLayer(baseLines)
  return baseLines
  
def getGeometryFromDayHour(dayField, hourField, proportionX, proportionY):
    cal = Calendar.getInstance()
    cal.setTime(dayField)
    y = cal.get(Calendar.DAY_OF_WEEK)
    interChangeToOrderRange = {Calendar.MONDAY:0,
          Calendar.TUESDAY:1,
          Calendar.WEDNESDAY:2,
          Calendar.THURSDAY:3,
          Calendar.FRIDAY:4,
          Calendar.SATURDAY:5,
          Calendar.SUNDAY:6
          }
    yf = interChangeToOrderRange[y] * proportionY
    
    
    cal = Calendar.getInstance()
    cal.setTime(hourField)
    h = cal.get(Calendar.HOUR_OF_DAY)
    m = cal.get(Calendar.MINUTE)
    s = cal.get(Calendar.SECOND)
    totalSecs = float(m*60 + s)/3600
    x = float(h) + float(totalSecs)
    xf = x * proportionX
    
    newGeom = geom.createPoint(geom.D2, xf, yf)
    return newGeom
    
def getFieldAsDate(field, pattern):
    if isinstance(field, unicode):
      formatter = SimpleDateFormat(pattern)
      newDate = formatter.parse(field)
      return newDate
    elif isinstance(field, Date):
      return field
    else:
      return None