import pyads


plc = pyads.Connection('192.168.0.25.1.1', 852)
with plc:
    while True:
        plc.read_by_name(f"GVL.astAxes[{29}].stStatus.bMoving")
        