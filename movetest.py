import pyads
import time

def move(plc, pos, axis, velocity):
    # does exactly what the motor record does for an absolute move
    plc.write_by_name(f"GVL.astAxes[{axis}].stControl.fVelocity", velocity)
    plc.write_by_name(f"GVL.astAxes[{axis}].stControl.fPosition", pos)

    plc.write_by_name(f"GVL.astAxes[{axis}].stControl.eCommand", 0, pyads.PLCTYPE_INT)
    plc.write_by_name(f"GVL.astAxes[{axis}].stControl.bExecute", 1)


# connect to plc and open connection

def poll_instead_of_sleeping(plc, axis, t):
    start = time.time()
    n = 0
    while time.time() < start + t:
        plc.read_by_name(f"GVL.astAxes[{axis}].stStatus.bMoving")
        n += 1

    print(f"spammed {n} bmobings")


PRE_DELAY = 0.5


def waitfor_move(plc, axis, post_delay):
    start = time.time()
    time.sleep(PRE_DELAY)
    while True:
        time.sleep(0.2)
        is_moving = plc.read_by_name(f"GVL.astAxes[{axis}].stStatus.bMoving")
        pos = plc.read_by_name(f"GVL.astAxes[{axis}].stStatus.fActPosition")
        sp = plc.read_by_name(f"GVL.astAxes[{axis}].stControl.fPosition")
        
        if is_moving != 1:
            break
    time.sleep(post_delay)

    end = time.time()
    print(f"waitfor_move time {end-start}, final pos {pos}, final sp {sp}")

    return (pos, sp)


def do_test(post_delay):

    plc = pyads.Connection('192.168.0.25.1.1', 852)
    with plc:
        axis = 26

        plc.write_by_name(f"GVL.astAxes[{axis}].stControl.bReset", 1)

        p = plc.read_by_name(f"GVL.astAxes[{axis}].stStatus.fActPosition")
        v = 2
        print(f"start position is {p}")

        #initial move 
        move(plc, 20, axis, v)

        # wait a bit
        #time.sleep(5)
        # poll_instead_of_sleeping(plc, axis, 5)
        (p, sp) = waitfor_move(plc, axis, post_delay)
        if sp != 20.0:
            print("IT DIDN'T TAKE THE STUPID SP")
        if p < 19.99 or p > 20.01:
            return False
        
        # final_pos = plc.read_by_name(f"GVL.astAxes[{axis}].stStatus.fActPosition")
        # if final_pos < 19.99 or final_pos > 20.01:
        #     return False

        # send three moves in succession
        move(plc, 18, axis, v)

        (p, sp) = waitfor_move(plc, axis, post_delay)
        if sp != 18.0:
            print("IT DIDN'T TAKE THE STUPID SP MK2")
        if p < 17.99 or p > 18.01:
            return False
        
        # for _ in range(100):
        #     plc.read_by_name(f"GVL.astAxes[{axis}].stStatus.bMoving")

        error_num =plc.read_by_name(f"GVL.astAxes[{axis}].stStatus.nErrorID")

        print(f"errors are {error_num}")

        move(plc, 16, axis, v)

        (p, sp) = waitfor_move(plc, axis, post_delay)


        final_pos = plc.read_by_name(f"GVL.astAxes[{axis}].stStatus.fActPosition")
        final_sp = plc.read_by_name(f"GVL.astAxes[{axis}].stControl.fPosition")


        print(f"final sp is {final_sp}, position is {final_pos}")

        return 15.99 < final_pos < 16.01

        
def do_full_test():
    m = {}
    for post_delay in range(0, 5000, 2):
        print(f"Testing post_delay {post_delay}")
        n = 0
        passed = 0
        for it in range(50):
            print(it)
            good = do_test(post_delay/1000.0)

            if good:
                passed += 1
            n += 1

            print(f"{100*(passed/n)}% good")
        
        m[post_delay] = 100*(passed/n)
        print(m)

do_full_test()