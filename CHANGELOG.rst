Unreleased
==========

0.3.6 (2024-07-19)
==================
- Upgrade library in api requirements


0.3.5 (2024-07-18)
==================
- Update create credential request to return new credential info in response


0.3.4 (2021-10-29)
==================
- Update turn off verify ssl when bucket name have dot


0.3.3 (2021-08-31)
==================
- Update Use raise instead return for response with error
- Update list bucket function to show grantee info
- Add debug function in storage
- Add debug function in admin


0.3.2 (2021-06-03)
==================
- Add add function to give permission for grantee
- Update add grantee function to spesific user
- Add add suspend/unsuspend user function in CLI
- Update add sanitize function in neo obs CLI
- Add list download function in libs
- Update add bulk download in CLI
- Update bulk download in APIh
- Add Add multipart upload function to CLI
- Add abort & complete multipart upload function
- Update fix respond when download empty object
- Add granted access to user in cli
- Update change default value to empty string 

0.3.1 (2020-07-14)
==================
- Add create bucket function with boto3
- Add use_neo env to switch create bucket function
- Add random_name argument to create bucket function in API
- Update create bucket test

0.3.0 (2020-06-15)
==================
- Add list multipart uploads function
- Add list part function
- Add abort multipart uploads function
- Add complete multipart uploads function
- Update docs

0.2.8 (2020-05-28)
==================
- Fix: Pypi doesn't support raw html tag
- Add: hook upload to Pypi in travis

0.2.7 (2020-05-27)
==================
- Add file_uploadobj in libs and use it in obs api
- Add threads in gunicorn config

0.2.6 (2020-05-12)
==================
- Fix api cannot access cloudian with secure url
- Refactor upload file to use tempdir
- Change acl message when success

0.2.5 (2020-04-29)
==================
- Add directory download function
- Add bucket download function
- Refactor default value in config

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
