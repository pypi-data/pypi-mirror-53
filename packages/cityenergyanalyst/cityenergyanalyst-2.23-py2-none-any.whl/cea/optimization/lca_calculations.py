# -*- coding: utf-8 -*-
"""
This file imports the price details from the cost database as a class. This helps in preventing multiple importing
of the corresponding values in individual files.
"""
from __future__ import division

import numpy as np
import pandas as pd

from cea.optimization.constants import *
from cea.constants import HOURS_IN_YEAR
import warnings
warnings.filterwarnings("ignore")

__author__ = "Sreepathi Bhargava Krishna"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Sreepathi Bhargava Krishna"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


class LcaCalculations(object):
    def __init__(self, locator, detailed_electricity_pricing):
        # heating_lca = pd.read_excel(locator.get_life_cycle_inventory_supply_systems(), sheet_name="HEATING")
        # cooling_lca = pd.read_excel(locator.get_life_cycle_inventory_supply_systems(), sheet_name="COOLING")
        electricity_costs = pd.read_excel(locator.get_electricity_costs(), sheet_name="ELECTRICITY")
        # dhw_lca = pd.read_excel(locator.get_life_cycle_inventory_supply_systems(), sheet_name="DHW")
        resources_lca = pd.read_excel(locator.get_life_cycle_inventory_supply_systems(),
                                      sheet_name="RESOURCES")

        self.ETA_FINAL_TO_USEFUL = 0.9  # assume 90% system efficiency in terms of CO2 emissions and overhead emissions (\
        self.CC_SIGMA = 4 / 5
        self.CC_EL_TO_TOTAL = 4 / 9

        self.NG_BACKUPBOILER_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Natural Gas'].iloc[0][
            'CO2']  # kg_CO2 / MJ_useful
        self.NG_BACKUPBOILER_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Natural Gas'].iloc[0][
            'PEN']  # MJ_oil / MJ_useful

        # Boiler
        self.NG_BOILER_TO_CO2_STD = (resources_lca[resources_lca['Description'] == 'Natural Gas'].iloc[0][
                    'CO2'] / self.ETA_FINAL_TO_USEFUL)  # kg_CO2 / MJ_useful
        self.NG_BOILER_TO_OIL_STD = (
                resources_lca[resources_lca['Description'] == 'Natural Gas'].iloc[0][
                    'PEN'] / self.ETA_FINAL_TO_USEFUL)  # MJ_oil / MJ_useful

        self.SOLARCOLLECTORS_TO_CO2 = resources_lca[resources_lca['Description'] == 'Solar'].iloc[0][
            'CO2']  # kg_CO2 / MJ_useful
        self.SOLARCOLLECTORS_TO_OIL = resources_lca[resources_lca['Description'] == 'Solar'].iloc[0][
            'PEN']  # MJ_oil / MJ_useful

        if pd.read_excel(locator.get_archetypes_system_controls())['has-heating-season'].item():
            # HEATING
            self.BG_BACKUPBOILER_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                'CO2']  # kg_CO2 / MJ_useful
            self.SMALL_GHP_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                'CO2']  # kg_CO2 / MJ_useful

            self.BG_BACKUPBOILER_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                'PEN']  # MJ_oil / MJ_useful
            self.SMALL_GHP_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                'PEN']  # MJ_oil / MJ_useful

            ######### Biogas to Agric. Bio Gas emissions
            self.NORMAL_BG_TO_AGRICULTURE_CO2 = resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                'CO2']  # Values from Electricity used for comparison
            self.NORMAL_BG_TO_AGRICULTURE_EPRIM = resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                'PEN']  # Values from Electricity used for comparison

            # Furnace
            self.FURNACE_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Wood'].iloc[0][
                                          'CO2'] / self.ETA_FINAL_TO_USEFUL * (
                                              1 + self.CC_SIGMA)  # kg_CO2 / MJ_useful
            self.FURNACE_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Wood'].iloc[0][
                                          'PEN'] / self.ETA_FINAL_TO_USEFUL * (
                                              1 + self.CC_SIGMA)  # MJ_oil / MJ_useful

            if BIOGAS_FROM_AGRICULTURE_FLAG:
                self.BG_BOILER_TO_CO2_STD = 0.339 * 0.87 * self.NORMAL_BG_TO_AGRICULTURE_CO2 / (
                        1 + DH_NETWORK_LOSS) / self.ETA_FINAL_TO_USEFUL  # kg_CO2 / MJ_useful
                self.BG_BOILER_TO_OIL_STD = 0.04 * 0.87 * self.NORMAL_BG_TO_AGRICULTURE_EPRIM / (
                        1 + DH_NETWORK_LOSS) / self.ETA_FINAL_TO_USEFUL  # MJ_oil / MJ_useful

            else:
                self.BG_BOILER_TO_CO2_STD = self.NG_BOILER_TO_CO2_STD * 0.04 / 0.0691  # kg_CO2 / MJ_useful
                self.BG_BOILER_TO_OIL_STD = self.NG_BOILER_TO_OIL_STD * 0.339 / 1.16  # MJ_oil / MJ_useful

            # HP Lake
            self.LAKEHP_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
                                         'CO2'] / self.ETA_FINAL_TO_USEFUL  # kg_CO2 / MJ_useful
            self.LAKEHP_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
                                         'PEN'] / self.ETA_FINAL_TO_USEFUL   # MJ_oil / MJ_useful

            #server
            self.SERVERHP_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
                                         'CO2'] / self.ETA_FINAL_TO_USEFUL  # kg_CO2 / MJ_useful
            self.SERVERHP_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
                                         'PEN'] / self.ETA_FINAL_TO_USEFUL   # MJ_oil / MJ_useful

            # HP Sewage
            self.SEWAGEHP_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Solid Waste'].iloc[0][
                                           'CO2'] / self.ETA_FINAL_TO_USEFUL  # kg_CO2 / MJ_useful
            self.SEWAGEHP_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Solid Waste'].iloc[0][
                                           'PEN'] / self.ETA_FINAL_TO_USEFUL  # MJ_oil / MJ_useful

            # GHP
            self.GHP_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
                                      'CO2'] / self.ETA_FINAL_TO_USEFUL  # kg_CO2 / MJ_useful
            self.GHP_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
                                      'PEN'] / self.ETA_FINAL_TO_USEFUL  # MJ_oil / MJ_useful

            if BIOGAS_FROM_AGRICULTURE_FLAG:
                self.BG_CC_TO_CO2_STD = (
                        resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                            'CO2'] / self.ETA_FINAL_TO_USEFUL * (1 + self.CC_SIGMA))  # kg_CO2 / MJ_useful
                self.BG_CC_TO_OIL_STD = (
                        resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                            'PEN'] / self.ETA_FINAL_TO_USEFUL * (1 + self.CC_SIGMA))  # MJ_oil / MJ_useful

            else:
                self.BG_CC_TO_CO2_STD = (
                        resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                            'CO2'] / self.ETA_FINAL_TO_USEFUL * (1 + self.CC_SIGMA))  # kg_CO2 / MJ_useful
                self.BG_CC_TO_OIL_STD = (
                        resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                            'PEN'] / self.ETA_FINAL_TO_USEFUL * (1 + self.CC_SIGMA))  # kg_CO2 / MJ_useful

            if BIOGAS_FROM_AGRICULTURE_FLAG:  # Use Biogas from Agriculture
                self.EL_BGCC_TO_OIL_EQ_STD = (
                        resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                            'PEN'] * self.CC_EL_TO_TOTAL)  # kg_CO2 / MJ_final
                self.EL_BGCC_TO_CO2_STD = (
                        resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                            'CO2'] * self.CC_EL_TO_TOTAL)  # kg_CO2 / MJ_final
            else:
                self.EL_BGCC_TO_OIL_EQ_STD = resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                                                 'PEN'] * self.CC_EL_TO_TOTAL  # kg_CO2 / MJ_final
                self.EL_BGCC_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Bio Gas'].iloc[0][
                                              'CO2'] * self.CC_EL_TO_TOTAL  # kg_CO2 / MJ_final

        ######### ELECTRICITY
        self.EL_PV_TO_OIL_EQ = resources_lca[resources_lca['Description'] == 'Solar'].iloc[0][
            'PEN']  # MJ_oil / MJ_final
        self.EL_PV_TO_CO2 = resources_lca[resources_lca['Description'] == 'Solar'].iloc[0]['CO2']  # kg_CO2 / MJ_final

        if detailed_electricity_pricing:
            self.ELEC_PRICE = electricity_costs['cost_kWh'].values/1000 # in USD_2015 per Wh
            self.ELEC_PRICE_EXPORT = electricity_costs['cost_sell_kWh'].values/1000 # in USD_2015 per Wh
        else:
            average_electricity_price = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
                                            'costs_kWh'] / 1000

            average_electricity_selling_price = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
                                            'costs_kWh'] / 1000
            self.ELEC_PRICE = np.ones(HOURS_IN_YEAR) * average_electricity_price # in USD_2015 per Wh
            self.ELEC_PRICE_EXPORT = np.ones(HOURS_IN_YEAR) * average_electricity_selling_price # in USD_2015 per Wh

        self.EL_TO_OIL_EQ = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
            'PEN']  # MJ_oil / MJ_final
        self.EL_TO_CO2 = resources_lca[resources_lca['Description'] == 'Electricity'].iloc[0][
            'CO2']  # kg_CO2 / MJ_final - CH Verbrauchermix nach EcoBau

        self.EL_NGCC_TO_OIL_EQ_STD = resources_lca[resources_lca['Description'] == 'Natural Gas'].iloc[0][
                                         'PEN'] * self.CC_EL_TO_TOTAL  # MJ_oil / MJ_final
        self.EL_NGCC_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Natural Gas'].iloc[0][
                                      'CO2'] * self.CC_EL_TO_TOTAL  # kg_CO2 / MJ_final

        self.NG_CC_TO_CO2_STD = resources_lca[resources_lca['Description'] == 'Natural Gas'].iloc[0][
                                    'CO2'] / self.ETA_FINAL_TO_USEFUL * (1 + self.CC_SIGMA)  # kg_CO2 / MJ_useful
        self.NG_CC_TO_OIL_STD = resources_lca[resources_lca['Description'] == 'Natural Gas'].iloc[0][
                                    'PEN'] / self.ETA_FINAL_TO_USEFUL * (1 + self.CC_SIGMA)  # MJ_oil / MJ_useful
