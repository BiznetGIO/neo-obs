""" Packaging Setting. """


from setuptools import setup, find_packages


base_url = 'https://github.com/BiznetGIO/neo-obs'
version_tag = '1.0.0'


setup(
    name='cloudian-s3',
    version=version_tag,
    description='Neo Cloudian S3 Library',
    author='BiznetGio',
    author_email='support@biznetgio.com',
    license='MIT',
    url=base_url,
    download_url=base_url + '/archive/' + version_tag + '.tar.gz',
    packages=find_packages(),
    keywords=['cloudian', 'S3', 'api-client'],
    platforms=['Any']
)
