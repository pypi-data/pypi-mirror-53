# pvview
display one or more EPICS PVs in a PyDM GUI window as a table


INSTALL:

    pip install pvview

Most Recent Tagged Build for conda installation

[![Anaconda-Server Badge](https://anaconda.org/BCDA-APS/pvview/badges/installer/conda.svg)](https://conda.anaconda.org/aps-anl-tag)
[![Anaconda-Server Badge](https://anaconda.org/BCDA-APS/pvview/badges/platforms.svg)](https://anaconda.org/aps-anl-tag/pvview)
[![Anaconda-Server Badge](https://anaconda.org/BCDA-APS/pvview/badges/version.svg)](https://anaconda.org/aps-anl-tag/pvview)
[![Anaconda-Server Badge](https://anaconda.org/BCDA-APS/pvview/badges/downloads.svg)](https://anaconda.org/aps-anl-tag/pvview)

    conda install -c aps-anl-tag -c pydm-tag -c conda-forge pvview

EXAMPLE:

    pvview.py {sky,xxx}:{iso8601,:UPTIME} xxx:alldone adsky:cam1:Acquire &

![pvview image](screen.jpg)

The `pvview` code was migrated from the 
[BcdaQWidgets](https://github.com/BCDA-APS/bcdaqwidgets) project 
(PyQt4-aware widgets for Python2)
to use the [PyDM](https://github.com/slaclab/pydm) project.
