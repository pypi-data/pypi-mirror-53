# LibSAN

Python library to manage Storage Area Network devices

## Dependencies:
* Python 2 >=2.7 or Python 3 >=3.4
* Make sure to have setuptools, wheel updated.

#### Fedora
    dnf install python3-netifaces augeas-libs
#### RHEL-7
    yum install augeas-libs
#### RHEL-6
* Install python3 from EPEL repos or other sources.
```
yum install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
yum install python34 --enablerepo=epel
```
## How to install the module:
    git clone; cd python-libsan
    pip install .
    # or
    python setup.py install
    python setup.py install --prefix=  # Fedora
    # use 'python3', 'pip3' where available

### PyPI pre-build package
    pip install libsan

## How to uninstall the module
    pip uninstall libsan
    # or
    python setup.py install --force --record files.txt
    cat files.txt | xargs rm -rf

## How to create a tar file
    python setup.py sdist

## How to create an rpm package
    python setup.py bdist --format=rpm

## Usage:
    Before using the modules it is better to copy sample_san_top.conf
    to /etc/san_top.conf (this is the default path to read the config) and
    edit it according to your SAN environment.
