import ctypes

mylib = ctypes.cdll.LoadLibrary("/home/sample/libhello_world.so")
mylib.do_hello.restype = ctypes.c_int

result = mylib.do_hello()
print (result)