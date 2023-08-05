#!/usr/bin/env python
# Copyright (c) 2019 Radware LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# @author: Leon Meguira, Radware


from radware.sdk.common import RadwareParametersStruct
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.GslbNewEnhDnsResVipTable import *
from radware.sdk.exceptions import DeviceConfiguratorError
from typing import List, Optional


class ResponderEntry(RadwareParametersStruct):
    def __init__(self):
        self.ip_ver = None
        self.name = None
        self.ip4_address = None
        self.ip6_address = None
        self.return_to_src_mac = None


class DNSRespondersParameters(RadwareParametersStruct):
    def __init__(self):
        self.dns_responders = list()


ResponderEntry.__annotations__ = {
    'ip_ver': Optional[EnumGslbDnsResVipIPVer],
    'name': Optional[str],
    'ip4_address': Optional[str],
    'ip6_address': Optional[str],
    'return_to_src_mac': Optional[EnumGslbDnsResVipRtsrcmac],
}

DNSRespondersParameters.__annotations__ = {
    'dns_responders': Optional[List[ResponderEntry]],
}

bean_map = {
    GslbNewEnhDnsResVipTable: dict(
        struct=List[ResponderEntry],
        direct=True,
        attrs=dict(
            Name='name',
            IPVer='ip_ver',
            V4='ip4_address',
            V6='ip6_address',
            Rtsrcmac='return_to_src_mac'
        )
    )
}

dns_resp_indexes_range = 10
dns_resp_index_prefix = 'DnsResp'


class DNSRespondersConfigurator(AlteonConfigurator):
    def __init__(self, alteon_connection):
        super(DNSRespondersConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: DNSRespondersParameters) -> DNSRespondersParameters:
        responders = self._device_api.read_all(GslbNewEnhDnsResVipTable())
        if responders:
            for responder in responders:
                new_entry = ResponderEntry()
                self._update_param_struct_attrs_from_object(new_entry, bean_map[GslbNewEnhDnsResVipTable]['attrs'],
                                                            responder)

                if new_entry not in parameters.dns_responders:
                    parameters.dns_responders.append(new_entry)
            return parameters

    def _update(self, parameters: DNSRespondersParameters, dry_run: bool) -> str:

        def _parse_index(cfg_idx):
            try:
                idx = int(cfg_idx.replace(dns_resp_index_prefix, ''))
            except ValueError:
                raise DeviceConfiguratorError(self.__class__, 'index parse error - unexpected index prefix1 {0}'
                                              .format(cfg_idx))
            return idx

        def _find_available_indexes():
            indexes = list()
            for i in range(1, dns_resp_indexes_range + 1):
                indexes.append(i)
            if responders:
                for resp in responders:
                    indexes.remove(_parse_index(resp.Index1))
                    indexes.remove(_parse_index(resp.Index2))
            return indexes

        def _lookup_current_entry(new_entry):
            for entry in responders:
                if entry.V4 and new_entry.ip4_address == entry.V4 and entry.V4 != '0.0.0.0':
                    return entry
                if entry.V6 and new_entry.ip6_address == entry.V6 and entry.V6 != '0:0:0:0:0:0:0:0':
                    return entry

        def _get_next_index():
            if len(available_indexes) > 0:
                return available_indexes.pop(0)
            else:
                raise DeviceConfiguratorError(self.__class__, 'no available dns responder index')

        responders = self._device_api.read_all(GslbNewEnhDnsResVipTable())
        if parameters.dns_responders:
            available_indexes = _find_available_indexes()
            for new_responder in parameters.dns_responders:
                if new_responder.name == '':
                    new_responder.name = None
                result = _lookup_current_entry(new_responder)
                if result:
                    self._update_object_attrs_from_struct(new_responder, bean_map[GslbNewEnhDnsResVipTable]['attrs'],
                                                          result)
                    self._device_api.update(result, dry_run=dry_run)
                else:
                    new_cfg_responder = GslbNewEnhDnsResVipTable()
                    self._update_object_attrs_from_struct(new_responder, bean_map[GslbNewEnhDnsResVipTable]['attrs'],
                                                          new_cfg_responder)
                    new_cfg_responder.Index1 = dns_resp_index_prefix + str(_get_next_index())
                    new_cfg_responder.Index2 = dns_resp_index_prefix + str(_get_next_index())
                    self._device_api.update(new_cfg_responder, dry_run=dry_run)
            return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: DNSRespondersParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        responders = self._device_api.read_all(GslbNewEnhDnsResVipTable())
        if responders:
            for responder in responders:
                self._device_api.delete(responder, dry_run=dry_run)
        return 'dns responders' + MSG_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(None, parameters)


DNSRespondersConfigurator.__annotations__ = {
    'parameters_class': DNSRespondersParameters
}
