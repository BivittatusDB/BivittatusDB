import os
import platform
import time

def pause_and_clean(duration):
    time.sleep(duration)
    
    # Check the operating system using platform.system()
    system_name = platform.system()
    
    if system_name == 'Windows':
        os.system('cls')
    elif system_name in ['Linux', 'Darwin']:  # Darwin' is for macOS
        os.system('clear')
    else:
        raise NotImplementedError(f"The operating system '{system_name}' is not supported for clearing the screen.")

# Example
#pause_and_clean(2)  
# Pause for 2 seconds and then wipe the screen.
