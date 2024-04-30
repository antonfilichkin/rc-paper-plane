import esp
import gc
import wifi

esp.osdebug(None)
gc.collect()


wifi.enable_ap_if()
