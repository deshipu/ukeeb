import board
import digitalio
import storage
import usb_cdc
import usb_hid
import matrix

row = digitalio.DigitalInOut(matrix.ROWS[0])
col = digitalio.DigitalInOut(matrix.COLS[0])
col.switch_to_output(value=1)
row.switch_to_input(pull=digitalio.Pull.DOWN)

bitmap_keyboard = usb_hid.Device(
    report_descriptor = (
        b'\x05\x01\t\x06\xa1\x01\x85\x04u\x01\x95\x08\x05\x07\x19\xe0)\xe7\x15'
        b'\x00%\x01\x81\x02\x95\x05u\x01\x05\x08\x19\x01)\x05\x91\x02\x95\x01u'
        b'\x03\x91\x03\x95xu\x01\x15\x00%\x01\x05\x07\x19\x00)w\x81\x02\xc0'
    ),
    usage_page = 0x1,
    usage = 0x6,
    in_report_lengths = (16,),
    out_report_lengths = (1,),
    report_ids=(4,),
)

if not row.value:
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_hid.enable((
        bitmap_keyboard,
        usb_hid.Device.CONSUMER_CONTROL
    ), boot_device=1)
else:
    usb_hid.enable((
        bitmap_keyboard,
        usb_hid.Device.CONSUMER_CONTROL
    ), boot_device=0)

row.deinit()
col.deinit()
