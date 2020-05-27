Unreleased
==========

0.2.7 (2020-05-27)
==================
- add file_uploadobj in libs and use it in obs api
- add threads in gunicorn config

0.2.6 (2020-05-12)
==================
- fix api cannot access cloudian with secure url
- refactor upload file to use tempdir
- change acl message when success

0.2.5 (2020-04-29)
==================
- Add directory download function
- Add bucket download function
- refactor default value in config

0.2.3 (2020-03-11)
==================
- Add log function
- Fix bug: input bool value
- Fix bug: no content when user id not found
- Add testing for API
- Update docs to add API documentation

0.2.2 (2020-02-12)
==================
- Added API to neo-obs
    - Added list bucket in storage function
    - Added list object in storage function
    - Added create bucket in storage function
    - Added delete bucket in storage function
    - Added bucket info in storage function
    - Added delete object in storage function
    - Added object info in storage function
    - Added upload object in storage function
    - Added download object in storage function
    - Added copy object in storage function
    - Added move object in storage function
    - Added object usage in storage function
    - Added bucket usage in storage function
    - Added set object ACL in storage function
    - Added set bucket ACL in storage function
    - Added get object url in storage function
    - Added make directory in storage function
    - Added list gmt_policy in storage function
    - Added create user in admin function 
    - Added delete user in admin function 
    - Added suspend & unsuspend user in admin function 
    - Added list user in admin function 
    - Added user info in admin function 
    - Added set qos user limit in admin function 
    - Added delete qos user limit in admin function 
    - Added qos user info in admin function
    - Added create new credibility for user in admin function
    - Added change status credibility for user in admin function
    - Added delete credibility for user in admin function
    - Added list credibility user in admin function

0.1.1 (2020-01-13)
==================

- Add directory experience. Treat object ends with a backslash as a directory.
- Modify the use of `prefix`. Now we use `s3://bucket/a/b/` instead of `-p a/b/`
- Fix download error for the object that contains forward-slash (#26)
- Add a choice of using HTTPS or HTTP to access buckets
 
0.1.0 (2019-10-01)
==================

Initial release.
