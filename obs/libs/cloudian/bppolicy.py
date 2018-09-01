from obs.libs.cloudian import requestors


base_url = 'bppolicy'
def list(data=None, json=None, method='GET'):
    list_policy = requestors.request(
                    url=base_url + '/listpolicy',
                    data=data,
                    json=json,
                    method=method)
    return list_policy

def get(data=None, json=None, method='GET'):
    detail_policy = requestors.request(
                    url=base_url,
                    data=data,
                    json=json,
                    method=method)
    return detail_policy

def buckets(data=None, json=None, method='GET'):
    bucket_policy = requestors.request(
                    url=base_url + '/bucketsperpolicy',
                    data=data,
                    json=json,
                    method=method)
    return bucket_policy
