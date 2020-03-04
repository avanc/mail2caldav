import logging
logger = logging.getLogger(__name__)

from icalendar import Calendar
import icalendar
import copy

from .error import MergeFailedError

def parse(ics):
  cal=Calendar.from_ical(ics)
  return cal

def merge(cal1, cal2):
  if not cal2.has_key("METHOD"):
    raise MergeFailedError("No 'METHOD' found", cal2.to_ical())
  
  if len(cal2.walk("VEVENT")) != 1:
    raise MergeFailedError("Calendar with only one VEVENT expected", cal2.to_ical())
  
  
  cal3=None;
  
  if cal2["METHOD"]=="REQUEST":
    cal3 = Calendar()

    if cal1 is None:
      cal1 = Calendar()

    for key in cal2.keys():
      if key != "METHOD":
        cal3.add(key, cal2[key])
        
    for component in cal2.subcomponents:
      if component.name in ["VTIMEZONE"]:
        cal3.add_component(copy.deepcopy(component))
      elif component.name == "VEVENT":
        merged=False
        uid=component["UID"]
        rid=None
        if component.has_key("RECURRENCE-ID"):
          rid = component["RECURRENCE-ID"]
          
        for vevent in cal1.walk("VEVENT"):
          if isSame(vevent, uid, rid):
            cal3.add_component(copy.deepcopy(component))
            merged=True
          else:
            cal3.add_component(copy.deepcopy(vevent))
            
        if not merged:
          cal3.add_component(copy.deepcopy(component))
          
      else:
        MergeFailedError("Unknown component {component}".format(component=component.name), cal2.to_ical())
  
  elif cal2["METHOD"]=="CANCEL":
    vevent=cal2.walk("VEVENT")[0]
    if vevent.has_key("RECURRENCE-ID"):
      uid=vevent["UID"]
      rid=vevent["RECURRENCE-ID"]
      
      cal3 = Calendar()

      if cal1 is None:
        cal1 = Calendar()

      for key in cal2.keys():
        if key != "METHOD":
          cal3.add(key, cal2[key])
          
      for component in cal2.subcomponents:
        if component.name in ["VTIMEZONE"]:
          cal3.add_component(copy.deepcopy(component))
        elif component.name == "VEVENT":
            
          for vevent in cal1.walk("VEVENT"):
            if isSame(vevent, uid, rid):
              pass
            elif isSame(vevent, uid):
              newcomponent=copy.deepcopy(vevent)
              if newcomponent.has_key("EXDATE"):
                exdates=newcomponent["EXDATE"]
                
                if areEqual(component["RECURRENCE-ID"], exdates):
                  logger.info("EXDATE for {date} already exists".format(date=component["RECURRENCE-ID"].dt))
                else:
                  newcomponent.add("EXDATE", component["RECURRENCE-ID"])
              else:
                newcomponent.add("EXDATE", component["RECURRENCE-ID"])

              cal3.add_component(newcomponent)
            else:
              cal3.add_component(copy.deepcopy(vevent))
            
        else:
          MergeFailedError("Unknown component {component}".format(component=component.name), cal2.to_ical())
      
  
  else:
    raise MergeFailedError("Unknown method {method} found".format(method=cal2["METHOD"]), cal2.to_ical())
  
  return cal3




def isSame(vevent, uid, recurrence_id=None):
  result=False;
  if vevent["UID"] == uid:
    rid=None
    if vevent.has_key("RECURRENCE-ID"):
      rid = vevent["RECURRENCE-ID"]   
    if areEqual(rid, recurrence_id):
      result=True

  return result



def findEventByUID(cal, uid, recurrence_id=None):
  result=None;
  for vevent in cal1.walk("VEVENT"):
    if vevent["UID"] == uid:
      rid=None
      if vevent.has_key("RECURRENCE-ID"):
        rid = vevent["RECURRENCE-ID"]     
      if areEqual(rid, recurrence_id):
        if result is not None:
          raise MergeFailedError("Calendar has several VEVENTS with same UID:RECCURENEC-ID combination", cal.to_ics())
          
        result=vevent

  return result

def areEqual(obj1, obj2):
  import icalendar
  result=False
  
  if type(obj1) == icalendar.prop.vDDDTypes:
    if type(obj2) == icalendar.prop.vDDDTypes:
      if obj1.dt == obj2.dt:
        if obj1.params==obj2.params:
          result=True
    elif type(obj2) == icalendar.prop.vDDDLists:
      if obj1.params == obj2.params:
        for dt in obj2.dts:
          if obj1.dt==dt.dt:
            result=True
  else:
    result= (obj1 == obj2)
    
  return result
