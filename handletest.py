import pyads
from ctypes import sizeof


def mycallback(notification, data):
    data_type = tags[data]
    handle, timestamp, value = plc.parse_notification(notification, data_type)
    print(timestamp, value)


tags = {"MAIN.afbAxes[1].stAxisStruct.stStatus.bMoving": pyads.PLCTYPE_BOOL}
plc = pyads.Connection('192.168.0.25.1.1', 852)

plc.open()

attr = pyads.NotificationAttrib(sizeof(pyads.PLCTYPE_BOOL))
# add_device_notification returns a tuple of notification_handle and
# user_handle which we just store in handles
handles = plc.add_device_notification('MAIN.afbAxes[1].stAxisStruct.stStatus.bMoving', attr, mycallback)


while True:
    try:
        pass
    except KeyboardInterrupt:
        plc.close()
