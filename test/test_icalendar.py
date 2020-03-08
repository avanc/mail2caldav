#! /usr/bin/env python

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("m2c").setLevel(logging.DEBUG)

logger = logging.getLogger()

import unittest

from m2c import ical_tools
from m2c import error
import icalendar

def loadCal(filename):
    f=open(filename)
    ics=f.read()
    f.close()
    return ical_tools.parse(ics)
  

class TestMergeSingleEvent(unittest.TestCase):
  
  def test_new_event(self):
    ical=loadCal("test_data/01-01_NewSingleEvent.ics")
    ical_result=ical_tools.merge(None, ical);
    del ical["METHOD"]
    self.maxDiff=None
    self.assertEqual(ical.to_ical().decode("utf-8"), ical_result.to_ical().decode("utf-8"))
    
  def test_update_event(self):
    ical1=loadCal("test_data/01-01_NewSingleEvent.ics")
    del ical1["METHOD"]
    ical2=loadCal("test_data/01-02_SingleEventUpdateTime.ics")
    
    ical_result=ical_tools.merge(ical1, ical2);
    del ical2["METHOD"]
    self.assertEqual(ical2.to_ical(), ical_result.to_ical())
    
    ical3=loadCal("test_data/01-03_SingleEventUpdateLocation.ics")
    ical_result=ical_tools.merge(ical2, ical3);
    del ical3["METHOD"]
    self.assertEqual(ical3.to_ical(), ical_result.to_ical())
    

  def test_cancel_event(self):
    ical1=loadCal("test_data/01-03_SingleEventUpdateLocation.ics")
    del ical1["METHOD"]
    ical2=loadCal("test_data/01-04_SingleEventCancel.ics")
    
    ical_result=ical_tools.merge(ical1, ical2);
    self.assertEqual(None, ical_result)

    
  def test_merge_without_method(self):
    ical=loadCal("test_data/01-01_NewSingleEvent.ics")
    del ical["METHOD"]
    self.assertRaises(error.MergeFailedError, ical_tools.merge, ical, ical)


class TestMergeRepeatingEvent(unittest.TestCase):
  
  def test_new_event(self):
    cal_init=None
    cal_update=loadCal("test_data/02-01-NewRepeatingEvent.ics")
    cal_expected=loadCal("test_data/02-01-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))

    
  def test_update_single_event(self):
    cal_init=loadCal("test_data/02-01-Result.ics")
    cal_update=loadCal("test_data/02-02-RepeatingEventUpdateSingleTime.ics")
    cal_expected=loadCal("test_data/02-02-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))

  def test_cancel_single_event(self):
    cal_init=loadCal("test_data/02-02-Result.ics")
    cal_update=loadCal("test_data/02-03-RepeatingEventCancelSingle.ics")
    cal_expected=loadCal("test_data/02-03-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))

  def test_update_location_single_event(self):
    cal_init=loadCal("test_data/02-03-Result.ics")
    cal_update=loadCal("test_data/02-04-RepeatingEventUpdateSingleLocation.ics")
    cal_expected=loadCal("test_data/02-04-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))


  def test_update_summary_single_event(self):
    cal_init=loadCal("test_data/02-04-Result.ics")
    cal_update=loadCal("test_data/02-05-RepeatingEventUpdateSingleSummary.ics")
    cal_expected=loadCal("test_data/02-05-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))


  def test_update_summary_all_event(self):
    cal_init=loadCal("test_data/02-05-Result.ics")
    cal_update=loadCal("test_data/02-06-RepeatingEventUpdateAllSummary.ics")
    cal_expected=loadCal("test_data/02-06-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))


  def test_update_summary_single_event2(self):
    cal_init=loadCal("test_data/02-06-Result.ics")
    cal_update=loadCal("test_data/02-07-RepeatingEventUpdateSingleSummary.ics")
    cal_expected=loadCal("test_data/02-07-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))

  def test_cancel_single_event2(self):
    cal_init=loadCal("test_data/02-07-Result.ics")
    cal_update=loadCal("test_data/02-08-RepeatingEventCancel.ics")
    cal_expected=loadCal("test_data/02-08-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))

  def test_cancel_single_event3(self):
    cal_init=loadCal("test_data/02-08-Result.ics")
    cal_update=loadCal("test_data/02-09-RepeatingEventCancel.ics")
    cal_expected=loadCal("test_data/02-09-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))

  def test_cancel_whole_event(self):
    cal_init=loadCal("test_data/02-09-Result.ics")
    cal_update=loadCal("test_data/02-10-RepeatingEventCancel.ics")
    cal_expected=loadCal("test_data/02-10-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update);
    self.maxDiff=None
    self.assertIsNone(cal_result)



class TestRandomSequence(unittest.TestCase):
  
  def test_sequence_changed(self):
    cal_init=loadCal("test_data/02-03-Result.ics")
    cal_update1=loadCal("test_data/02-05-RepeatingEventUpdateSingleSummary.ics")
    cal_update2=loadCal("test_data/02-04-RepeatingEventUpdateSingleLocation.ics")
    cal_expected=loadCal("test_data/02-05-Result.ics")
    
    cal_result=ical_tools.merge(cal_init, cal_update1);
    cal_result=ical_tools.merge(cal_result, cal_update2);
    
    self.maxDiff=None
    self.assertEqual(cal_expected.to_ical().decode("utf-8"), cal_result.to_ical().decode("utf-8"))


class TestHelpers(unittest.TestCase):
  
  def test_getUid(self):
    cal_init=loadCal("test_data/02-03-Result.ics")
    
    uid=ical_tools.getUid(cal_init);
    self.assertEqual(uid, icalendar.prop.vText("040000008200E00074C5B7101A82E0080000000090C7403159F1D501000000000000000010000000C1DA4CA703FC8F4386A31D013E0E7274"))



if __name__ == '__main__':
  unittest.main()
