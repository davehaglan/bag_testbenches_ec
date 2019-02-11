# -*- coding: utf-8 -*-

from typing import Dict, Any

import os
import pkg_resources

from bag.util.cache import Param
from bag.design.module import Module
from bag.design.database import ModuleDB


# noinspection PyPep8Naming
class bag_testbenches_ec__bias_sources(Module):
    """Module for library bag_testbenches_ec cell bias_sources.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'bias_sources.yaml'))

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
            voltage_dict='voltage bias dictionary.',
            current_dict='current bias dictionary.',
        )

    def design(self, voltage_dict=None, current_dict=None):
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
        if voltage_dict is None:
            voltage_dict = {}
        if current_dict is None:
            current_dict = {}

        voltage_names = sorted(voltage_dict.keys())
        current_names = sorted(current_dict.keys())

        if 'ibias' not in current_dict and 'ibias' not in voltage_dict:
            self.remove_pin('ibias')

        if 'vbias' not in current_dict and 'vbias' not in voltage_dict:
            self.remove_pin('vbias')

        for prefix, info_dict, name_list, prop_name in (('V', voltage_dict, voltage_names, 'vdc'),
                                                        ('I', current_dict, current_names, 'idc')):
            inst_names, term_list, val_list = [], [], []
            for name in name_list:
                pname, nname, val = info_dict[name]
                inst_names.append(prefix + name)
                term_list.append(dict(PLUS=pname, MINUS=nname))
                val_list.append(val)
                if name != 'ibias' and name != 'vbias':
                    self.add_pin(name, 'inputOutput')

            master_name = prefix + '0'
            self.array_instance(master_name, inst_names, term_list=term_list)
            for inst_name, val in zip(inst_names, val_list):
                self.instances[inst_name].set_param(prop_name, val)
