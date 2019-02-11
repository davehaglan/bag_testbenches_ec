# -*- coding: utf-8 -*-

from typing import Dict, Any

import os
import pkg_resources

from bag.util.cache import Param
from bag.design.module import Module
from bag.design.database import ModuleDB


# noinspection PyPep8Naming
class bag_testbenches_ec__amp_tb_ac_tran(Module):
    """Module for library bag_testbenches_ec cell amp_tb_ac_tran.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'amp_tb_ac_tran.yaml'))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        """Returns a dictionary from parameter names to descriptions.

        Returns
        -------
        param_info : Optional[Dict[str, str]]
            dictionary from parameter names to descriptions.
        """
        return dict(
            dut_lib='DUT library name.',
            dut_cell='DUT cell name.',
            dut_conns='DUT connection dictionary.',
            vbias_dict='Voltage source dictionary.',
            ibias_dict='Current source dictionary.',
            tran_fname='Transient stimulus file name.',
            no_cload='True to disable output capacitor load.',
        )

    def design(self, dut_lib='', dut_cell='', dut_conns=None,
               vbias_dict=None, ibias_dict=None, tran_fname='', no_cload=False):
        """To be overridden by subclasses to design this module.

        This method should fill in values for all parameters in
        self.parameters.  To design instances of this module, you can
        call their design() method or any other ways you coded.

        To modify schematic structure, call:

        rename_pin()
        delete_instance()
        replace_instance_master()
        reconnect_instance_terminal()
        restore_instance()
        array_instance()
        """
        if vbias_dict is None:
            vbias_dict = {}
        if ibias_dict is None:
            ibias_dict = {}
        if dut_conns is None:
            dut_conns = {}

        # setup bias sources
        self.design_dc_bias_sources(vbias_dict, ibias_dict, 'VSUP', 'IBIAS', define_vdd=True)

        # setup pwl source
        self.instances['VIN'].set_param('fileName', tran_fname)

        # delete load cap if needed
        if no_cload:
            self.delete_instance('CLOAD')

        # setup DUT
        self.replace_instance_master('XDUT', dut_lib, dut_cell, static=True)
        for term_name, net_name in dut_conns.items():
            self.reconnect_instance_terminal('XDUT', term_name, net_name)
