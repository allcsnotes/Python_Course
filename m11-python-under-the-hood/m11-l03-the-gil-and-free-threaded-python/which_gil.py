import sys
import sysconfig

print("GIL on:", sys._is_gil_enabled())
print("built without GIL:",
      bool(sysconfig.get_config_var("Py_GIL_DISABLED")))
print("switch interval:", sys.getswitchinterval())
