import pyads
import time
from datetime import datetime
SLEEP_TIME = 5
# connect to plc and open connection
plc = pyads.Connection('192.168.0.25.1.1', 852)
with plc:
    while True:
        for i in range(1, 10):
            # read int value by name
            plc.write_by_name("MAIN.afbAxes[1].stAxisStruct.stControl.fVelocity", i)
            print(f"Sent {i} velocity to PLC at {datetime.now()}")
            time.sleep(SLEEP_TIME)
