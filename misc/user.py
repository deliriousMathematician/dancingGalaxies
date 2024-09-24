# UI related functions....
#
# To Do:
#   - Update with new function arguments (see renderers.py and writers.py)
#   - ...
#
#   --------------------------------------------------------------------------------------------------------------------

def get_user_inputs():
    # vmin (getting exponent which must be positive)
    while True:
        try:
            vmin_exp = int(input("\nEnter a positive exponent for the colormap minimum (vmin) (E.g., 5 for 10^5): "))
            if vmin_exp < 0:
                raise ValueError("vmin_exp must be a positive number")
            vmin = 10 ** vmin_exp
            break

        except ValueError as e:
            print(f"Invalid input for vmin: {e}. Please try again.")

    # vmax (getting exponent which must be greater than that of vmin)
    while True:
        try:
            vmax_exp = int(input("\nEnter the exponent for the colormap maximum (vmax) (E.g., 10 for 10^10): "))
            vmax = 10 ** vmax_exp
            if vmax <= vmin:
                raise ValueError("vmax must be greater than vmin")
            break

        except ValueError as e:
            print(f"Invalid input for vmax: {e}. Please try again.")

    # z_shift (set at a minimum limit of 0.001)
    while True:
        try:
            z_shift = float(input("\nEnter the distance along z to be shifted per frame (z_shift) (E.g., 0.01): "))
            if z_shift <= 0.001:
                raise ValueError("z_shift must be greater than 0.001")
            break

        except ValueError as e:
            print(f"Invalid input for z_shift: {e}. Please try again.")

    # z_max (must be positive)
    while True:
        try:
            z_max = float(input("\nEnter the maximum z-distance (z_max) to be covered in the animation (E.g., 0.25): "))
            if z_max <= 0:
                raise ValueError("z_max must be a positive number")
            break

        except ValueError as e:
            print(f"Invalid input for z_max: {e}. Please try again.")

    # interval (must be positive)
    while True:
        try:
            interval = int(input("\nEnter the time (in ms) between frames (i.e., the interval) (E.g., 250): "))
            if interval <= 0:
                raise ValueError("interval must be a positive number")
            break

        except ValueError as e:
            print(f"Invalid input for interval: {e}. Please try again.")

    # colorbar (adjusted so that it is not case or space sensitive)
    while True:

        colorbar_input = input("\nToggle the colorbar on/off (Enter True/False): ").strip().lower()

        if colorbar_input == 'true':
            colorbar = True
            break

        elif colorbar_input == 'false':
            colorbar = False
            break

        else:
            print("Invalid input for the colorbar. Must be either 'True' or 'False'. Please try again.")

    # z (set so it cannot be negative)
    while True:
        try:
            z = float(input("\nEnter the starting z-coordinate (E.g., 0): "))
            if z < 0:
                raise ValueError("z must be a non-negative number")
            break

        except ValueError as e:
            print(f"Invalid input for z: {e}. Please try again.")

    # Return the values if all inputs are valid.
    return vmin, vmax, z_shift, z_max, interval, colorbar, z


# Calling the function (not an efficient method of doing this, will fix later)
user_values = get_user_inputs()
vmin = user_values[0]  # Colormap minimum
vmax = user_values[1]  # Colormap maximum
z_shift = user_values[2]  # Distance (in kpc) to be shifted per frame [avoid values <= 0.001]
z_max = user_values[3]  # Maximum z-distance to cover in the animation (in kpc)
interval = user_values[4]  # Time (in ms) between frames
colorbar = user_values[5]  # To toggle colorbar on/off
z = user_values[6]  # Starting z value

# 'Confirming' the values.
if user_values:
    print(f"\nThe following are the received input values: \nvmin: {vmin}, \nvmax: {vmax},"
          f"\nz_shift: {z_shift}, \nz_max: {z_max}, \ninterval: {interval}, \ncolorbar: {colorbar}, \nz: {z}")

# Loading the Simulation
sim = input("\nEnter Simulation Path: ")  # User input

# Choosing ffmpeg.exe path
ffmpeg_path = input("\nEnter the ffmpeg file path: ") # User input