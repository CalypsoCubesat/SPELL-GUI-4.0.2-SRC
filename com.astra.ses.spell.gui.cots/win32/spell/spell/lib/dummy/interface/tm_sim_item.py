###############################################################################
"""
Date: 01/07/2008

Project: UGCS/USL

Description
===========

TM item for simulations in standalone driver.

Authoring
=========

@organization: SES Astra / SES Engineering

@copyright: This software is the copyrighted work of SES Engineering S.A. 
            All rights reserved.
            
@license: License information
    
@author: Rafael Chinchilla Camara (GMV Aerospace & Defence S.A.)
@author: Fabien Bouleau (SES Engineering S.A.)

@version: 1.0
@requires: Python 2.5.x"""

################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.utils.log import *
from spell.lib.exception import *
from spell.lib.adapter.tm_item import TmItemClass

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************
from math import *

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['TmItemSimClass']

#*******************************************************************************
# Module globals
#*******************************************************************************

################################################################################
class TmItemSimClass(TmItemClass):
    
    model = None
    rawExpression = None
    engExpression = None
    period = None
    timerCount = 0
    currentPosition = 0
    
    #==========================================================================    
    def __init__(self, model, name, description, rawExpression, engExpression, period = 0):
        TmItemClass.__init__(self,model.tmClass,name,description)
        self._status = True
        self.model = model
        self.rawExpression = rawExpression
        self.engExpression = engExpression
        self.rawValue = None
        self.engValue = None
        self.period = period
        self.timerCount = 0
        self.currentPosition = -1
        LOG("NAME: " + repr(name) + ", DESC:" + repr(description))
        self._recalculate()

    #==========================================================================    
    def refreshSimulatedValue(self):    
        if self.period == 0: return
        self.timerCount = self.timerCount + 1
        if self.timerCount == self.period:
            self.timerCount = 0
            self._recalculate()

    #==========================================================================    
    def change(self, changeDef):
        raw,eng = self._evaluate()
        
        # Changes for shitfting values of a list
        if type(changeDef) == str and changeDef.startswith('+'):
            # For lists, the amount must be integer
            amount = eval(changeDef[1:])
            if type(raw)==list or type(eng)==list:
                # Shift the position as requested
                max = len(raw)
                self.currentPosition = self.currentPosition + int(amount)
                if self.currentPosition>=max: self.currentPosition = 0
                # Update values
                if type(raw)==list:
                    self._setRaw(raw[self.currentPosition])
                if type(eng)==list:
                    self._setEng(eng[self.currentPosition])
            else:
                # For non-lists, just add the amount
                self._setRaw(self._rawValue + amount)
                if eng is not None:
                    self._setEng(self._engValue + amount)
        elif type(changeDef) == str and changeDef.startswith('-'):
            amount = eval(changeDef[1:])
            if type(raw)==list or type(eng)==list:
                max = len(raw)
                self.currentPosition = self.currentPosition - int(amount)
                if self.currentPosition<0: self.currentPosition = max-1
                if type(raw)==list:
                    self._setRaw(raw[self.currentPosition])
                if type(eng)==list:
                    self._setEng(eng[self.currentPosition])
            else:
                self._setRaw(self._rawValue - amount)
                if eng is not None:
                    self._setEng(self._engValue - amount)
        # Changes for setting values
        else:
            if type(raw)==list or type(eng)==list:
                if changeDef in eng:
                    idx = eng.index(changeDef)
                    self._setEng(eng[idx])
                    self._setRaw(raw[idx])
                elif changeDef in raw:
                    idx = raw.index(changeDef)
                    self._setRaw(raw[idx])
                    if eng is not None:
                        self._setEng(eng[idx])
                elif str(changeDef) in map(str,raw):
                    idx = map(str,raw).index(str(changeDef))
                    self._setRaw(raw[idx])
                    if eng is not None:
                        self._setEng(eng[idx])
                elif str(changeDef) in map(str,eng):
                    idx = map(str,eng).index(str(changeDef))
                    self._setEng(eng[idx])
                    self._setRaw(raw[idx])
            else:
                try:
                    self._setRaw(eval(str(changeDef)))
                except:
                    self._setRaw(eval("'" + str(changeDef) + "'"))
                if eng is not None:
                    try:
                        self._setEng(eval(str(changeDef)))
                    except:
                        self._setRaw(eval("'" + str(changeDef) + "'"))
        if eng is None:
            self._setEng(self._rawValue)
    
    #==========================================================================    
    def _recalculate(self):
        # First change the wildcards in the expressions
        raw,eng = self._evaluate()

        if type(raw)==list or type(eng)==list:
            max = len(raw)
            self.currentPosition = self.currentPosition +1
            if self.currentPosition==max: self.currentPosition = 0
            if raw is not None:
                self._setRaw(raw[self.currentPosition])
            if eng is not None:
                self._setEng(eng[self.currentPosition])
        else:
            self._setRaw(raw)
            if eng is not None:
                self._setEng(eng)
        if eng is None:
            self._setEng(self._rawValue)            

    #==========================================================================    
    def _evaluate(self):
        try:
            rawExpression = self._changeWildcards(self.rawExpression)
            raw = eval(rawExpression)
            engExpression = self._changeWildcards(self.engExpression)
            eng = eval(engExpression)
        except BaseException,ex:
            raise DriverException("Malformed simulation expression (" + repr(ex) + ")")
        if type(raw)==list and type(eng)==list:
            if len(raw)!=len(eng):
                raise DriverException("Malformed simulation expression")
        return [raw,eng]
                
    #==========================================================================    
    def _changeWildcards(self, expression):
        if expression.find('$TIME$')!=-1:
            ctime = str(self.model.getCurrentTime())
            expression = expression.replace('$TIME$',ctime)
        return expression

    #==========================================================================    
    def _setLimit(self, limitName, limitValue ):
        LOG("Limit " + limitName + " value set to " + str(limitValue))

################################################################################
