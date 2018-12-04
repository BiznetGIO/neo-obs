import pytest

from obs.libs.cloudian import user


class TestUser:
    def test_list(self):
        list_user_params = {
            'groupId': 'testing',
            'userType': 'all',
            'userStatus': 'active'
        }
        userlist = user.get_list(data=list_user_params)
        
        assert userlist

    def test_list_fail(self):
        list_user_params = {
            'groupId': 'testing',
            'userType': 'all'
        }
        userlist = user.get_list(data=list_user_params)
        
        assert None == userlist

    def test_get(self):
        detail_user_param = {
            'userId': 'buatdarilib1',
            "groupId": 'testing'
        }
        res = user.detail(data=detail_user_param)
        test_data = {'userId': 'buatdarilib1', 'userType': 'User', 'fullName': 'edit dari lib', 'emailAddr': '', 'address1': '', 'address2': '', 'city': '', 'state': '', 'zip': '', 'country': '', 'phone': '', 'groupId': 'testing', 'website': '', 'active': 'true', 'canonicalUserId': '6df8c1f68af292367e778a47e11182c8', 'ldapEnabled': False}
        assert test_data == res

    def test_get_fail(self):
        detail_user_param = {
            'userId': 'buatdarilib1s',
            "groupId": 'testing'
        }
        res = user.detail(data=detail_user_param)
        assert None == res

    def test_create(self):
        delete_user_param = {
            'userId': 'neoobs2',
            'groupId': 'testing'
        }
        remove = user.delete(data=delete_user_param)
        create_user_param = {
            "address1": "456 Shakedown St.",
            "city": "Portsmouth",
            "zip": "03803",
            "phone": "132-132-1312",
            "website": "",
            "active": "true",
            "userType": "User",
            "emailAddr": "jgarc@geemail.com",
            "fullName": "Jerry Garcia",
            "groupId": "testing",
            "userId": "neoobs2",
            "state": "NH",
            "country": "USA"
        }
        res = user.create(data=None, json=create_user_param, method='PUT')
        assert res

    def test_create_fail(self):
        create_user_param = {
            "address1": "456 Shakedown St.",
            "city": "Portsmouth",
            "zip": "03803",
            "phone": "132-132-1312",
            "website": "",
            "active": "true",
            "userType": "User",
            "emailAddr": "jgarc@geemail.com",
            "fullName": "Jerry Garcia",
            "groupId": "testing",
            "userId": "neoobs1",
            "state": "NH",
            "country": "USA"
        }
        res = user.create(data=None, json=create_user_param, method='PUT')
        assert None == res

    def test_update(self):
        update_user_param = {
            "address1": "456 Shakedown St.",
            "city": "update 3",
            "zip": "03803",
            "phone": "132-132-1312",
            "website": "",
            "active": "true",
            "userType": "User",
            "emailAddr": "jgarc@geemail.com",
            "fullName": "Jerry Garcia",
            "groupId": "testing",
            "userId": "neoobs3",
            "state": "NH",
            "country": "USA"
        }
        res = user.update(data=None, json=update_user_param)
        assert {} == res

    def test_update_fail(self):
        update_user_param = {
            "address1": "456 Shakedown St.",
            "city": "update 3",
            "zip": "03803",
            "phone": "132-132-1312",
            "website": "",
            "active": "true",
            "userType": "User",
            "emailAddr": "jgarc@geemail.com",
            "fullName": "Jerry Garcia",
            "groupId": "testing",
            "userId": "neoobs22",
            "state": "NH",
            "country": "USA"
        }
        res = user.update(data=None, json=update_user_param)
        assert None == res

    def test_delete(self):
        create_user_param = {
            "address1": "456 Shakedown St.",
            "city": "Portsmouth",
            "zip": "03803",
            "phone": "132-132-1312",
            "website": "",
            "active": "true",
            "userType": "User",
            "emailAddr": "jgarc@geemail.com",
            "fullName": "Jerry Garcia",
            "groupId": "testing",
            "userId": "testdelete1",
            "state": "NH",
            "country": "USA"
        }
        create = user.create(data=None, json=create_user_param)
        delete_user_param = {
            'userId': 'testdelete1',
            'groupId': 'testing'
        }
        res = user.delete(data=delete_user_param)
        assert {} == res

    def test_delete_fail(self):
        delete_user_param = {
            'userId': 'testdelete1nouser',
            'groupId': 'testing'
        }
        res = user.delete(data=delete_user_param)
        assert None == res
