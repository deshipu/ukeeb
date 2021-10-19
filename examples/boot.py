import board
import digitalio
import storage
import usb_cdc
import usb_hid

row = digitalio.DigitalInOut(board.RX)
col = digitalio.DigitalInOut(board.D14)
col.switch_to_output(value=1)
row.switch_to_input(pull=digitalio.Pull.DOWN)

if not row.value:
    storage.disable_usb_drive()
    usb_cdc.disable()

usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.CONSUMER_CONTROL))

row.deinit()
col.deinit()
