# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Any

import os
import pkg_resources

from bag.util.cache import Param
from bag.design.module import Module
from bag.design.database import ModuleDB


# noinspection PyPep8Naming
class bag_testbenches_ec__mos_tb_sp(Module):
    """Module for library bag_testbenches_ec cell mos_tb_sp.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'mos_tb_sp.yaml'))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        return dict(
            dut_lib="Transistor DUT library name.",
            dut_cell='Transistor DUT cell name.',
            vbias_dict='Additional bias voltage dictionary.',
            ibias_dict='Additional bias current dictionary.',
            dut_conns='Transistor DUT connection dictionary.',
        )

    @classmethod
    def get_default_param_values(cls) -> Dict[str, Any]:
        return dict(
            vbias_dict=None,
            ibias_dict=None,
            dut_conns=None,
        )

    def design(self, dut_lib: str, dut_cell: str, vbias_dict: Optional[Dict[str, List[str]]],
               ibias_dict: Optional[Dict[str, List[str]]],
               dut_conns: Optional[Dict[str, str]]) -> None:
        """Design this testbench.
        """
        if vbias_dict is None:
            vbias_dict = {}
        if ibias_dict is None:
            ibias_dict = {}
        if dut_conns is None:
            dut_conns = {}

        # setup bias sources
        self.design_dc_bias_sources(vbias_dict, ibias_dict, 'VBIAS', 'IBIAS', define_vdd=False)

        # setup DUT
        self.replace_instance_master('XDUT', dut_lib, dut_cell, static=True)
        for term_name, net_name in dut_conns.items():
            self.reconnect_instance_terminal('XDUT', term_name, net_name)
