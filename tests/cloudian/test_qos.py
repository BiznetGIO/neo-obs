import pytest
from obs.libs.cloudian import qos

class TestQos:
    def test_get(self):
        list_params = {
            "groupId": "testing",
            "userId": "user_483_20973_stage_wjv-1",
        }
        list_qos = qos.get(data=list_params)
        test_data = {'groupId': 'testing', 'userId': 'user_483_20973_stage_wjv-1', 'labelId': 'qos.userQosOverrides.title', 'qosLimitList': [{'type': 'STORAGE_QUOTA_KBYTES', 'value': 20971520}, {'type': 'REQUEST_RATE_LW', 'value': 10}, {'type': 'REQUEST_RATE_LH', 'value': 20}, {'type': 'DATAKBYTES_IN_LW', 'value': -1}, {'type': 'DATAKBYTES_IN_LH', 'value': -1}, {'type': 'DATAKBYTES_OUT_LW', 'value': -1}, {'type': 'DATAKBYTES_OUT_LH', 'value': -1}, {'type': 'STORAGE_QUOTA_COUNT', 'value': -1}]}
        assert list_qos == test_data

    def test_get_fail(self):
        list_params = {
            "groupId": "testing",
            "userId": "user_483_20973_stage_wjv-12",
        }
        list_qos = qos.get(data=list_params)
        assert None == list_qos

    def test_update(self):
        update_params = {
            'userId': 'user_483_20973_stage_wjv-1',
            'groupId': 'testing',
            'storageQuotaKBytes': 20*1024*1024,
            'storageQuotaCount': -1,
            'wlRequestRate': 10,
            'hlRequestRate': 20,
            'wlDataKBytesIn': -1,
            'hlDataKBytesIn': -1,
            'wlDataKBytesOut': -1,
            'hlDataKBytesOut': -1
        }
        update_qos = qos.update(data=update_params)
        assert {} == update_qos

    def test_update_fail(self):
        update_params = {
            'userId': 'user_483_20973_stage_wjv-12',
            'groupId': 'testing',
            'storageQuotaKBytes': 20*1024*1024,
            'storageQuotaCount': -1,
            'wlRequestRate': 10,
            'hlRequestRate': 20,
            'wlDataKBytesIn': -1,
            'hlDataKBytesIn': -1,
            'wlDataKBytesOut': -1,
            'hlDataKBytesOut': -1
        }
        update_qos = qos.update(data=update_params)
        assert None == update_qos

    def test_delete(self):
        update_params = {
            'userId': 'neoobs5',
            'groupId': 'testing',
            'storageQuotaKBytes': 20*1024*1024,
            'storageQuotaCount': -1,
            'wlRequestRate': 10,
            'hlRequestRate': 20,
            'wlDataKBytesIn': -1,
            'hlDataKBytesIn': -1,
            'wlDataKBytesOut': -1,
            'hlDataKBytesOut': -1
        }
        qos.update(data=update_params)
        delete_params = {
            'userId': 'neoobs5',
            'groupId': 'testing'
        }
        delete_qos = qos.delete(data=delete_params)
        assert {} == delete_qos

    def test_delete_fail(self):
        delete_params = {
            'userId': 'neoobs55',
            'groupId': 'testing'
        }
        delete_qos = qos.delete(data=delete_params)
        assert None == delete_qos