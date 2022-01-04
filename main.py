import pyads
import time
from datetime import datetime

# connect to plc and open connection
plc = pyads.Connection('192.168.0.25.1.1', 852)
with plc:
    while True:
        # read int value by name
        i = plc.read_by_name("MAIN.afbAxes[1].stAxisStruct.stStatus.bMoving")
        print(f"from PLC, moving is: {i} at {datetime.now()}")
        time.sleep(0.01)
