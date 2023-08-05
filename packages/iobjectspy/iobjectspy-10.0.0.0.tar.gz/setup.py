from setuptools import setup

import sys
import platform

plat_bit = platform.architecture()[0]

major = sys.version_info.major
minor = sys.version_info.minor
micro = sys.version_info.micro

package_dir = {}

if major == 3 and minor == 5:
    if micro > 2:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py35_64/iobjectspy'}
    else:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py352_64/iobjectspy'}
elif major == 3 and minor == 6:
    if micro < 6:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py36_64/iobjectspy'}
    else:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py366_64/iobjectspy'}
elif major == 3 and minor == 7:
    package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py37_64/iobjectspy'}
else:
    raise RuntimeError('Unsupported python version : %d.%d ' % (major, minor))

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='iobjectspy',
    version='10.0.0',
    packages=['iobjectspy'],
    url='http://iobjectspy.supermap.io',
    license='SuperMap',
    description='SuperMap iObjects Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'py4j==0.10.7'
    ],
    package_data={
        'iobjectspy': [
            '*.*',
            'ml/*',
            'ml/analyst/*',
            'ml/toolkit/*',
            'ml/geoparsing/*',
            'ml/vision/*',
            'ml/vision/_dataprepare_collector/*',
            'ml/vision/_inference_collector/*',
            'ml/vision/_trainer_collector/*',
            'ml/vision/_sample/*',
            'ml/vision/_models/*',
            'ml/vision/_models/*/*',
            'ml/vision/_models/*/*/*',
            'ml/vision/_models/*/*/*/*',
            'ml/vision/_models/*/*/*/*/*',
            'ml/vision/_models/*/*/*/*/*/*',
            'ml/vision/_models/*/*/*/*/*/*/*',
            '_jsuperpy/*',
            '_jsuperpy/jars/*.jar',
            'rpc/*',
            'rpc/protos/*',
            '_jsuperpy/data/*']},
    package_dir=package_dir,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ]
)
