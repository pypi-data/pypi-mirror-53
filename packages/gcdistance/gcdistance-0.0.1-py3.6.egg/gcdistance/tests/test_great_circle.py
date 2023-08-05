# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:30:50 2019

@author: lealp
"""

from unittest import TestCase

from gcdistance.gcdistance import great_circle_distance

class Testgcdistance(TestCase):
    def test_distance(self):
        
        P1 = (1,2)
        
        P2 = (2,3)
        
        s = great_circle_distance(P1, P2)
        
        self.assertTrue(isinstance(s, float))