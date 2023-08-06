# pvview
display one or more EPICS PVs in a PyDM GUI window as a table


INSTALL:

    pip install pvview

EXAMPLE:

    pvview.py {sky,xxx}:{iso8601,:UPTIME} xxx:alldone adsky:cam1:Acquire &

![pvview image](screen.jpg)

The `pvview` code was migrated from the 
[BcdaQWidgets](https://github.com/BCDA-APS/bcdaqwidgets) project 
(PyQt4-aware widgets for Python2)
to use the [PyDM](https://github.com/slaclab/pydm) project.
