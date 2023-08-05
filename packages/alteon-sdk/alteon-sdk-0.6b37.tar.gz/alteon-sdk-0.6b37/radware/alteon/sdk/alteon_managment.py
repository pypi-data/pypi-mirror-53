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


from radware.alteon.beans.Global \
    import Root, EnumAgApplyConfig, EnumAgSaveConfig, EnumAgRevert, EnumAgRevertApply, EnumAgReset, EnumAgDiffState, \
    EnumAgSyncStatus, EnumSlbOperConfigSync
from radware.alteon.beans.AgApplyTable import *
from radware.alteon.beans.AgSaveTable import *
from radware.alteon.beans.AgDiffTable import *
from radware.sdk.management import DeviceInfo, DeviceOper, DeviceConfig, MSG_REBOOT_STATEFUL, MSG_REBOOT, MSG_NOT_ACCESSIBLE
from radware.alteon.api import AlteonDevice
from radware.alteon.exceptions import AlteonRequestError
from radware.sdk.exceptions import DeviceFunctionError
from radware.sdk.api import BaseAPI
from radware.sdk.device import DeviceType
from abc import ABCMeta
import time
import logging


MSG_REVERT = 'unapplied changes reverted'
MSG_REVERT_APPLY = 'unsaved changes reverted'
MSG_DEVICE_TIMEOUT = 'device timeout'
DIFF_CHANGE = 'identical to new config'

log = logging.getLogger(__name__)


class AlteonMngBase(BaseAPI, AlteonDevice):
    __metaclass__ = ABCMeta

    def __init__(self, adc_connection):
        AlteonDevice.__init__(self, adc_connection)
        log.info(' {0} initialized, server: {1}'.format(self.__class__.__name__, adc_connection.id))


class AlteonMngInfo(AlteonMngBase, DeviceInfo):

    def __init__(self, adc_connection):
        AlteonMngBase.__init__(self, adc_connection)

    @property
    def device_name(self):
        return json.loads(self._rest.read_data_object('sysName'))['sysName']

    @property
    def software(self):
        return self._read_sys_info().agSoftwareVersion

    def is_accessible(self, timeout_second=5, retries=1):
        timeout_bck = self._rest.timeout
        self._rest._timeout = timeout_second
        try:
            self._read_sys_info(retries)
        except AlteonRequestError:
            log.debug(' {0} , server: {1} , {2}'.format(self.__class__.__name__, self.connection.id,
                                                        MSG_NOT_ACCESSIBLE))
            return False
        except Exception as e:
            raise e
        self._rest._timeout = timeout_bck
        return True

    @property
    def is_container(self):
        return self.form_factor.lower() == 'vx' or self.form_factor.lower() == 'standalone'

    @property
    def is_vx(self):
        return self.form_factor.lower() == 'vx'

    @property
    def is_standalone(self):
        return self.form_factor.lower() == 'standalone'

    @property
    def is_vadc(self):
        return self.form_factor.lower() == 'vadc'

    @property
    def is_master(self):
        return self.ha_state.lower() == 'master'

    @property
    def is_backup(self):
        return self.ha_state.lower() == 'backup'

    @property
    def ha_state(self):
        if not self.is_container:
            root = Root()
            root.vrrpInfoHAState = READ_PROP
            return self._rest.read(root).vrrpInfoHAState
        return None

    @property
    def mac_address(self):
        return self._read_sys_info().hwMACAddress

    @property
    def form_factor(self):
        return self._read_sys_info().agFormFactor

    @property
    def platform_id(self):
        return self._read_sys_info().agPlatformIdentifier

    @property
    def uptime(self):
        return self._read_sys_info().agSwitchUpTime

    def _read_sys_info(self, retries=3):
        root = Root()
        root.agSoftwareVersion = READ_PROP
        root.hwMACAddress = READ_PROP
        root.agSwitchLastBootTime = READ_PROP
        root.agSwitchLastApplyTime = READ_PROP
        root.agSwitchLastSaveTime = READ_PROP
        root.agMgmtCurCfgIpAddr = READ_PROP
        root.agSwitchUpTime = READ_PROP
        root.agFormFactor = READ_PROP
        root.agPlatformIdentifier = READ_PROP
        return self._rest.read(root, retries)


class AlteonMngConfig(AlteonMngBase, DeviceConfig):

    def __init__(self, adc_connection):
        AlteonMngBase.__init__(self, adc_connection)

    def commit(self):
        try:
            apply_result = self.apply()
        except DeviceFunctionError as e:
            self.revert()
            return dict(
                success=False,
                state=e.args
            )
        return dict(
            success=True,
            state=apply_result
        )

    def commit_save(self):
        commit_result = self.commit()
        if commit_result['success']:
            try:
                commit_result = self.save()
            except DeviceFunctionError as e:
                return dict(
                    success=False,
                    state=e.args
                )
        return commit_result

    def apply(self):
        log.debug(' {0}: APPLY, server: {1}'.format(self.__class__.__name__, self.connection.id))
        root = Root()
        root.agApplyConfig = EnumAgApplyConfig.idle
        self._rest.update(root)
        root.agApplyConfig = EnumAgApplyConfig.apply
        self._rest.update(root)
        apply_state = None
        for x in range(0, 20):
            time.sleep(3)
            apply_state = self._rest.read(root)
            if apply_state.agApplyConfig != EnumAgApplyConfig.inprogress:
                break

        if apply_state.agApplyConfig == EnumAgApplyConfig.complete:
            log.debug(' {0}: APPLY, server: {1}, State: {2}'.format(self.__class__.__name__, self.connection.id,
                                                                    apply_state.agApplyConfig.name))
            return apply_state.agApplyConfig.name
        apply_table = self._rest.read_all_no_translation(AgApplyTable())
        raise DeviceFunctionError(self.apply, DeviceType.Alteon, apply_table, apply_state.agApplyConfig)

    def save(self):
        log.debug(' {0}: SAVE, server: {1}'.format(self.__class__.__name__, self.connection.id))
        root = Root()
        root.agSaveConfig = EnumAgSaveConfig.idle
        self._rest.update(root)
        root.agSaveConfig = EnumAgSaveConfig.save
        self._rest.update(root)
        save_state = None
        for x in range(0, 5):
            time.sleep(1)
            save_state = self._rest.read(root)
            if save_state.agSaveConfig != EnumAgSaveConfig.inprogress:
                break

        if save_state.agSaveConfig == EnumAgSaveConfig.complete:
            log.debug(' {0}: SAVE, server: {1}, State: {2}'.format(self.__class__.__name__, self.connection.id,
                                                                   save_state.agSaveConfig.name))
            return save_state.agSaveConfig.name
        save_table = self._rest.read_all_no_translation(AgSaveTable())
        raise DeviceFunctionError(self.save, DeviceType.Alteon, save_table, save_state.agSaveConfig)

    def revert(self):
        log.debug(' {0}: REVERT, server: {1}'.format(self.__class__.__name__, self.connection.id))
        root = Root()
        root.agRevert = EnumAgRevert.revert
        self._rest.update(root)
        return MSG_REVERT

    def revert_apply(self):
        log.debug(' {0}: REVERT_APPLY, server: {1}'.format(self.__class__.__name__, self.connection.id))
        root = Root()
        root.agRevertApply = EnumAgRevertApply.revertApply
        self._rest.update(root)
        return MSG_REVERT_APPLY

    def sync(self):
        log.debug(' {0}: SYNC, server: {1}'.format(self.__class__.__name__, self.connection.id))
        root = Root()
        root.slbOperConfigSync = EnumSlbOperConfigSync.sync
        self._rest.update(root)

        root.slbOperConfigSync = None
        root.agSyncStatus = READ_PROP
        root.agLastSyncInfoTableToString = READ_PROP
        sync_state = None
        for x in range(0, 20):
            time.sleep(1)
            sync_state = self._rest.read(root)
            if sync_state.agSyncStatus != EnumAgSyncStatus.inprogress:
                break
        if sync_state.agSyncStatus == EnumAgSyncStatus.success:
            log.debug(' {0}: SYNC, server: {1}, State: {2}'.format(self.__class__.__name__, self.connection.id,
                                                                   sync_state.agSyncStatus.name))
            return sync_state.agSyncStatus.name

        raise DeviceFunctionError(self.sync, DeviceType.Alteon, sync_state.agLastSyncInfoTableToString,
                                  sync_state.agSyncStatus)

    def diff(self):
        log.debug(' {0}: DIFF, server: {1}'.format(self.__class__.__name__, self.connection.id))
        return self._get_diff(EnumAgDiffState.diff)

    def diff_flash(self):
        log.debug(' {0}: DIFF_FLASH, server: {1}'.format(self.__class__.__name__, self.connection.id))
        return self._get_diff(EnumAgDiffState.flashdiff)

    def _get_diff(self, diff_type):
        root = Root()
        root.agDiffState = EnumAgDiffState.idle
        self._rest.update(root)
        root.agDiffState = diff_type
        self._rest.update(root)
        diff_state = None
        for x in range(0, 5):
            time.sleep(1)
            diff_state = self._rest.read(root)
            if diff_state.agDiffState != EnumAgDiffState.inprogress:
                break

        if diff_state.agDiffState == EnumAgDiffState.complete:
            diff_items = list()
            for item in self._rest.read_all_no_translation(AgDiffTable()):
                diff_items.append(Decoders.hex_str_to_ascii(item['StringVal']))

            log.debug(' {0}: {2}, server: {1} Content: {3}'.format(self.__class__.__name__, self.connection.id,
                                                                   diff_type, diff_items))
            return diff_items

        raise DeviceFunctionError(self.diff, DeviceType.Alteon, None, diff_state.agDiffState)

    def pending_configuration_validation(self):
        diff = self.diff()
        diff_flash = self.diff_flash()
        if DIFF_CHANGE not in diff[0]:
            raise DeviceFunctionError(self.pending_configuration_validation, DeviceType.Alteon,
                                      "pending diff:\n{0}".format(diff))
        if DIFF_CHANGE not in diff_flash[0]:
            raise DeviceFunctionError(self.pending_configuration_validation, DeviceType.Alteon,
                                      "pending diff_flash:\n{0}".format(diff_flash))


class AlteonMngOper(AlteonMngBase, DeviceOper):
    REBOOT = 'reboot'
    REBOOT_STATEFUL = 'reboot_stateful'
    
    def __init__(self, adc_connection):
        AlteonMngBase.__init__(self, adc_connection)
        self._mng_info = AlteonMngInfo(adc_connection)

    def reboot(self):
        log.debug(' {0}: {1}, server: {2}'.format(self.__class__.__name__, self.REBOOT.upper(), self.connection.id))
        root = Root()
        root.agReset = EnumAgReset.reset
        self._rest.update(root)
        return MSG_REBOOT

    def reboot_stateful(self, timeout_seconds=600):
        self.reboot()
        while timeout_seconds > 0:
            time.sleep(10)
            if self._mng_info.is_accessible():
                log.debug(' {0}: {1}, server: {2}, State: {3}'.format(self.__class__.__name__,
                                                                      self.REBOOT_STATEFUL.upper(), self.connection.id,
                                                                      MSG_REBOOT_STATEFUL))
                return MSG_REBOOT_STATEFUL
            timeout_seconds -= 10
        raise DeviceFunctionError(self.reboot_stateful, DeviceType.Alteon, 'device timeout')


