import pyads
import time

# connect to plc and open connection
plc = pyads.Connection('5.73.93.67.1.1', 851)
with plc:
    i = plc.read_by_name("GVL_APP.nAXIS_NUM")
    print(f"axes num is: {i}")
    p = plc.read_by_name("GVL.astAxes[1].stStatus.fActPosition")
    print(f"position is {p}")

