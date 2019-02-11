# -*- coding: utf-8 -*-

from typing import Dict, Sequence, Tuple, Union, Optional, Any

import os
import pkg_resources

from bag.math import float_to_si_string
from bag.util.cache import Param
from bag.design.module import Module
from bag.design.database import ModuleDB


# noinspection PyPep8Naming
class bag_testbenches_ec__dut_wrapper_dm(Module):
    """Module for library bag_testbenches_ec cell dut_wrapper_dm.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'dut_wrapper_dm.yaml'))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        return dict(
            dut_lib='DUT library name.',
            dut_cell='DUT cell name.',
            balun_list='list of baluns to create.',
            pin_list='list of input/output pins.',
            dut_conns='DUT connection dictionary.',
            cap_list='list of load capacitances.',
            vcvs_list='list of voltage-controlled voltage sources.',
        )

    @classmethod
    def get_default_param_values(cls) -> Dict[str, Any]:
        return dict(
            cap_list=None,
            vcvs_list=None,
        )

    def design(self,  dut_lib: str, dut_cell: str,
               balun_list: Sequence[Tuple[str, str, str, str]],
               cap_list: Optional[Sequence[Tuple[str, str, Union[float, str]]]],
               pin_list: Sequence[Tuple[str, str]],
               dut_conns: Dict[str, str],
               vcvs_list: Sequence[Tuple[str, str, str, str, Dict[str, Any]]],
               ) -> None:
        """Design this wrapper schematic.

        This cell converts a variable number of differential pins to single-ended pins or
        vice-versa, by using ideal_baluns.  It can also create extra pins to be connected
        to the device.  You can also optionally instantiate capacitive loads or
        voltage-controlled voltage sources.

        VDD and VSS pins will always be there for primary supplies.  Additional supplies
        can be added as inputOutput pins using the pin_list parameters.  If you don't need
        supply pins, they will be left unconnected.

        NOTE: the schematic template contains pins 'inac', 'indc', 'outac', and 'outdc' by
        default.  However, if they are not specified in pin_list, they will be deleted.
        In this way designer has full control over how they want the inputs/outputs to be
        named.

        Parameters
        ----------
        dut_lib : str
            DUT library name.
        dut_cell : str
            DUT cell name.
        balun_list: Sequence[Tuple[str, str, str, str]]
            list of baluns to instantiate, represented as a list of
            (diff, comm, pos, neg) tuples.
        cap_list : Sequence[Tuple[str, str, Union[float, str]]]
            list of load capacitors to create.  Represented as a list of (pos, neg, cap_val) tuples.
            cap_val can be either capacitance value in Farads or a variable name/expression.
        pin_list : Sequence[Tuple[str, str]]
            list of pins of this schematic, represented as a list of (name, purpose) tuples.
            purpose can be 'input', 'output', or 'inputOutput'.
        dut_conns : Dict[str, str]
            a dictionary from DUT pin name to the net name.  All connections should
            be specified, including VDD and VSS.
        vcvs_list : Sequence[Tuple[str, str, str, str, Dict[str, Any]]]
            list of voltage-controlled voltage sources to create.  Represented as a list of
            (pos, neg, ctrl-pos, ctrl-neg, params) tuples.
        """
        # error checking
        if not balun_list:
            raise ValueError('balun_list cannot be None or empty.')
        if not pin_list:
            raise ValueError('pin_list cannot be None or empty.')
        if not dut_conns:
            raise ValueError('dut_conns cannot be None or empty.')

        # delete default input/output pins
        for pin_name in ('inac', 'indc', 'outac', 'outdc'):
            self.remove_pin(pin_name)

        # add pins
        for pin_name, pin_type in pin_list:
            self.add_pin(pin_name, pin_type)

        # replace DUT
        self.replace_instance_master('XDUT', dut_lib, dut_cell, static=True)

        # connect DUT
        for dut_pin, net_name in dut_conns.items():
            self.reconnect_instance_terminal('XDUT', dut_pin, net_name)

        # add baluns and connect them
        inst_name = 'XBAL'
        num_inst = len(balun_list)
        name_list = ['%s%d' % (inst_name, idx) for idx in range(num_inst)]
        self.array_instance(inst_name, name_list)
        for iname, (diff, comm, pos, neg) in zip(name_list, balun_list):
            self.reconnect_instance_terminal(iname, 'd', diff)
            self.reconnect_instance_terminal(iname, 'c', comm)
            self.reconnect_instance_terminal(iname, 'p', pos)
            self.reconnect_instance_terminal(iname, 'n', neg)

        # configure load capacitors
        inst_name = 'CLOAD'
        if cap_list:
            num_inst = len(cap_list)
            name_list = ['%s%d' % (inst_name, idx) for idx in range(num_inst)]
            self.array_instance(inst_name, name_list)
            for iname, (pos, neg, val) in zip(name_list, cap_list):
                self.reconnect_instance_terminal(iname, 'PLUS', pos)
                self.reconnect_instance_terminal(iname, 'MINUS', neg)
                if isinstance(val, str):
                    pass
                elif isinstance(val, float) or isinstance(val, int):
                    val = float_to_si_string(val)
                else:
                    raise ValueError('Unknown schematic instance parameter: %s' % val)
                self.instances[iname].set_param('c', val)
        else:
            self.delete_instance(inst_name)

        # configure vcvs
        inst_name = 'ECTRL'
        if vcvs_list:
            num_inst = len(vcvs_list)
            name_list = ['%s%d' % (inst_name, idx) for idx in range(num_inst)]
            self.array_instance(inst_name, name_list)
            for iname, (pos, neg, cpos, cneg, params) in zip(name_list, vcvs_list):
                self.reconnect_instance_terminal(iname, 'PLUS', pos)
                self.reconnect_instance_terminal(iname, 'MINUS', neg)
                self.reconnect_instance_terminal(iname, 'NC+', cpos)
                self.reconnect_instance_terminal(iname, 'NC-', cneg)
                for key, val in params.items():
                    if isinstance(val, str):
                        pass
                    elif isinstance(val, float) or isinstance(val, int):
                        val = float_to_si_string(val)
                    else:
                        raise ValueError('Unknown schematic instance parameter: %s' % val)
                    self.instances[iname].set_param(key, val)
        else:
            self.delete_instance(inst_name)
