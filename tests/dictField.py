#!/usr/bin/env python

# 
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import os
import unittest
import lsst.utils.tests as utilsTests
import lsst.pex.config as pexConf

class Config1(pexConf.Config):
    d1 = pexConf.DictField("d1", keytype=str, itemtype=int, default={"hi":4}, itemCheck=lambda x: x > 0)
    d2 = pexConf.DictField("d2", keytype=str, itemtype=str, default=None)
    d3 = pexConf.DictField("d1", keytype=float, itemtype=float, optional = True, itemCheck=lambda x: x > 0)

class DictFieldTest(unittest.TestCase):
    def testConstructor(self):
        try:
            class BadKeytype(pexConf.Config):
                d = pexConf.DictField("...", keytype=list, itemtype=int)
        except:
            pass
        else:
            raise SyntaxError("Unsupported keyptype DictFields should not be allowed")

        try:
            class BadItemtype(pexConf.Config):
                d = pexConf.DictField("...", keytype=int, itemtype=dict)
        except:
            pass
        else:
            raise SyntaxError("Unsupported itemtype DictFields should not be allowed")
       
        try:
            class BadItemCheck(pexConf.Config):
                d = pexConf.DictField("...", keytype=int, itemtype=int, itemCheck=4)
        except:
            pass
        else:
            raise SyntaxError("Non-callable itemCheck DictFields should not be allowed")
        
        try:
            class BadDictCheck(pexConf.Config):
                d = pexConf.DictField("...", keytype=int, itemtype=int, dictCheck=4)
        except:
            pass
        else:
            raise SyntaxError("Non-callable dictCheck DictFields should not be allowed")

    def testAssignment(self):
        c = Config1()
        self.assertRaises(pexConf.FieldValidationError, setattr, c, "d1", {3:3})
        self.assertRaises(pexConf.FieldValidationError, setattr, c, "d1", {"a":0})
        self.assertRaises(pexConf.FieldValidationError, setattr, c, "d1", [1.2, 3, 4])
        c.d1 = None; c.d1 = {"a":1, "b":2}
       
        self.assertRaises(pexConf.FieldValidationError, setattr, c, "d3", {"hi", True})
        c.d3={4:5}
        self.assertEqual(c.d3, {4.:5.})
       
    def testValidate(self):
        c = Config1()
        self.assertRaises(pexConf.FieldValidationError, Config1.validate, c)

        c.d2 = {"a":"b"}
        c.validate()

    def testInPlaceModification(self):
        c= Config1()
        self.assertRaises(pexConf.FieldValidationError, c.d1.__setitem__, 2, 0)
        self.assertRaises(pexConf.FieldValidationError, c.d1.__setitem__, "hi", 0)
        c.d1["hi"]=10
        self.assertEqual(c.d1, {"hi":10})

        c.d3={}
        c.d3[4]=5
        self.assertEqual(c.d3, {4.:5.})

def  suite():
    utilsTests.init()
    suites = []
    suites += unittest.makeSuite(DictFieldTest)
    suites += unittest.makeSuite(utilsTests.MemoryTestCase)
    return unittest.TestSuite(suites)

def run(exit=False):
    utilsTests.run(suite(), exit)

if __name__=='__main__':
    run(True)