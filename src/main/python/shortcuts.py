from pynput import keyboard

SHIFT_STATE = False
def on_press(key):
    global SHIFT_STATE
    if key == keyboard.Key.shift:
        SHIFT_STATE = True
        print("shift pressed")

def on_release(key):
    global SHIFT_STATE
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    elif key == keyboard.Key.shift:
        SHIFT_STATE = False
        print('shift released')

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()