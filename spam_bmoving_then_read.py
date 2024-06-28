import pyads
import time

plc = pyads.Connection('192.168.0.25.1.1', 852)
with plc:
    init_vel = plc.read_by_name(f"GVL.astAxes[{29}].stControl.fVelocity")

    for _ in range(10000):
        # start = time.time()
        plc.read_by_name(f"GVL.astAxes[{29}].stStatus.bMoving")
        # plc.read_by_name(f"GVL.astAxes[{29}].stStatus.bMoving")
        # end = time.time()
        # tot += (end-start)*1000
        # n += 1

    plc.write_by_name(f"GVL.astAxes[{29}].stControl.fVelocity", init_vel+1)
    time.sleep(1)
    res = plc.read_by_name(f"GVL.astAxes[{29}].stControl.fVelocity")

    print(init_vel+1)
    print(res)
