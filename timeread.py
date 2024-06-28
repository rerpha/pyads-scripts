import pyads
import time

plc = pyads.Connection('192.168.0.25.1.1', 852)
with plc:
    tot = 0
    n = 0
    for _ in range(1000):
        start = time.time()
        plc.read_by_name(f"GVL.astAxes[{26}].stStatus.bMoving")
        plc.read_by_name(f"GVL.astAxes[{26}].stStatus.bMoving")
        end = time.time()
        tot += (end-start)*1000
        n += 1

    print(tot/n)
