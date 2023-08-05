# pyxmatters
The pyxmatters package provides a rest api interface with xMatters. There are also file reading capabilities to assist with synchronizing data.

## Install pyxmatters
Navigate to the cmd and enter:
* `pip3 install pyxmatters`

## For Upgrades of pyxmatters
Navigate to the cmd and enter:
* `sudo pip3 install --upgrade --force-reinstall pyxmatters`

Reference:
* https://stackoverflow.com/questions/47071256/how-to-update-upgrade-a-package-using-pip

## Overview of the pyxmatters package

### pyxmatters/rest
This directory provides user, device, group, and site rest api capabilities.

### pyxmatters/file
This directory provides a mechanism to organize user, device, group, and site information for synchronization.

### pyxmatters/util
This directory contains misc. utilities that provide benefits to users executing ETL processes with pyxmatters.

## Working Projects
For implementation in a working project see: https://github.com/matthewhenry1/integrator-py

## Notes on managing the package

### Uploading
Procedure:
1. Update the version in the setup.py. Increment by 1 and keep existing structure
2. `python3 setup.py sdist bdist_wheel`
3. `twine upload dist/*`

References:
* https://pypi.org/project/twine/
* https://stackoverflow.com/questions/52016336/how-to-upload-new-versions-of-project-to-pypi-with-twine

### Testing locally
To test locally uninstall the package by:
* `sudo pip3 uninstall pyxmatters`
* add `pyxmatters` to the local directory in which you want to test and then import `pyxmatters` as you normally would
* begin testing
