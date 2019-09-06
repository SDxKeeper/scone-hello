# scone-hello

This hello world project provides demonstrates how to run C++ applications capable to be run in iExec environment
Currently it's possible to run only python processes, that is why your app should be converted into form of shared library
and called from python via ctypes. All fork, spawn, exec methods do not work in iexechub/python-scone image from 8/5/2019