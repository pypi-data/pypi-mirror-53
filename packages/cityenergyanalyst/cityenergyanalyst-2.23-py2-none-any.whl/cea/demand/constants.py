# -*- coding: utf-8 -*-
"""
This file contains the constants used in the building energy demand calculations
"""
__author__ = "Gabriel Happle"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


# all values are refactored from legacy Globalvars unless stated otherwise

# DEFAULT BUILDING GEOMETRY
H_F = 3.0  # average height per floor in m
D = 20.0  # in mm the diameter of the pipe to calculate losses

# SOLAR
RSE = 0.04  # thermal resistance of external surfaces according to ISO 6946

# HVAC SYSTEMS & VENTILATION
ETA_REC = 0.75  # constant efficiency of Heat recovery
DELTA_P_DIM = 5.0  # (Pa) dimensioning differential pressure for multi-storey building shielded from wind,
                 # according to DIN 1946-6
SHIELDING_CLASS = 2  # according to ISO 16798-7, 0 = open terrain, 1 = partly shielded from wind,
        #  2 = fully shielded from wind
P_FAN = 0.55  # specific fan consumption in W/m3/h
MIN_VENTILATION_RATE = 0.6  # l/s/m2 [https://escholarship.org/content/qt7k1796zv/qt7k1796zv.pdf]

# pumps ?
# TODO: Document
DELTA_P_1 = 0.1  # delta of pressure
F_SR = 0.3  # factor for pressure calculation
HOURS_OP = 5  # assuming around 2000 hours of operation per year. It is charged to the electrical system from 11 am to 4 pm
GR = 9.81  # m/s2 gravity
EFFI = 0.6  # efficiency of pumps

# WATER
FLOWTAP = 0.036  # in m3 == 12 l/min during 3 min every tap opening
TWW_SETPOINT = 60  # dhw tank set point temperature in C

# PHYSICAL
H_WE = 2466e3  # (J/kg) Latent heat of vaporization of water [section 6.3.6 in ISO 52016-1:2007]
C_A = 1006  # (J/(kg*K)) Specific heat of air at constant pressure [section 6.3.6 in ISO 52016-1:2007]

# RC-MODEL
B_F = 0.7  # it calculates the coefficient of reduction in transmittance for surfaces in contact with the ground according to values of SIA 380/1
H_IS = 3.45  # heat transfer coefficient between air and the surfacein W/(m2K)
H_MS = 9.1  # heat transfer coefficient between nodes m and s in W/m2K
LAMBDA_AT = 4.5 # dimensionless ratio between the internal surfaces area and the floor area from ISO 13790 Eq. 9

# RC-MODEL TEMPERATURE BOUNDS
T_WARNING_LOW = -30.0
T_WARNING_HIGH = 50.0

# SUPPLY AND RETURN TEMPERATURES OF REFRIGERATION SYSTEM
T_C_REF_SUP_0 = 1  # (°C) refactored from refrigeration loads, without original source
T_C_REF_RE_0 = 5  # (°C) refactored from refrigeration loads, without original source

# SUPPLY AND RETURN TEMPERATURES OF DATA CENTER COOLING SYSTEM
T_C_DATA_RE_0 = 15  # (°C) refactored from data center loads, without original source
T_C_DATA_SUP_0 = 7  # (°C) refactored from data center loads, without original source
