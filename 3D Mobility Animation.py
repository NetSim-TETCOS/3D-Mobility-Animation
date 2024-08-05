import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import tempfile
import os
import random
import matplotlib.colors as mcolors
from datetime import datetime

# Set Arial as the default font
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = '10'
random.seed(2)

temp_dir = tempfile.gettempdir()
netsim_dir = os.path.join(temp_dir,'NetSim')
latest_version=None
latest_mod_time=datetime.min

# Find the latest modified version folder
for subdir in os.listdir(netsim_dir):
    folder_path = os.path.join(netsim_dir, subdir, 'log')
    if os.path.isdir(folder_path):
        mod_time = datetime.fromtimestamp(os.path.getmtime(folder_path))
        if mod_time > latest_mod_time:
            latest_mod_time = mod_time
            latest_version = subdir

relative_path = f'NetSim\\{latest_version}\\log\\Mobility_log.csv'

file_path = os.path.join(temp_dir, relative_path)

if not os.path.exists(file_path):
    print("Mobility_log.csv file not found")

else:

    print("Reading Mobility File...")
    print("Please Wait...\n")
    # Load data from the file, skipping the first row containing column headers
    data = pd.read_csv(file_path)
    Device_names = data['Device Name'].unique()
    device_ids = data['Device Id'].unique()  # Unique device IDs

    min_x, max_x = data['Position X(m)'].min(), data['Position X(m)'].max()
    min_y, max_y = data['Position Y(m)'].min(), data['Position Y(m)'].max()
    min_z, max_z = data['Position Z(m)'].min(), data['Position Z(m)'].max()
    min_x,max_x = min_x-min_x,max_x+min_x
    min_y, max_y = min_y-min_y,max_y+min_y
    min_z, max_z = min_z-min_z,max_z+min_z
    # Create a 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Color map for devices
    #first_five_color = 'tab:blue'
    #second_five_color = 'tab:orange'
    def is_dark(color):
        r, g, b = mcolors.hex2color(mcolors.CSS4_COLORS[color])
        brightness = 0.299 * r + 0.587 * g + 0.114 * b
        return brightness < 0.5

    color_list = [color for color in mcolors.CSS4_COLORS if is_dark(color)]
    random.shuffle(color_list)
    device_colors = {device_id: color_list[i % len(color_list)] for i, device_id in enumerate(device_ids)}
    line_width = 1.5

    def update(frame):
        ax.clear()
        ax.set_xlabel('X Distance (m)', fontsize=12)
        ax.set_ylabel('Y Distance (m)', fontsize=12)
        ax.set_zlabel('Z Distance (m)', fontsize=12)

         # Set fixed limits for x and y axes
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_zlim(min_z,max_z)

        for i, device_id in enumerate(device_ids):
            device_data = data[data['Device Id'] == device_id]
            device_data = device_data[device_data['Time(ms)'] <= frame * 1000]  # Assuming time is in milliseconds
            x = device_data['Position X(m)']  # X coordinates
            y = device_data['Position Y(m)']  # Y coordinates
            z = device_data['Position Z(m)']  # Z coordinates

            device_name = Device_names[i]
            #color = first_five_color if i < 5 else second_five_color
            color=device_colors[device_id]
            # Modify marker style at specific time
            if frame * 1000 == 245000:
                marker = '-'
                markersize = 10  # Increase marker size for better visibility
                print(f"Frame: {frame}, Time: {frame * 1000}")
            else:
                marker = '-'  # Use line marker for regular points
                markersize = 10  # Line width
                print(f"Frame: {frame}, Time: {frame * 1000}")

            ax.plot(x, y, z, marker, markersize=markersize, linewidth=line_width, color=color, label=device_name)
            ax.plot(x, y, z, 'o', markersize=3, color=color) 

        ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1), fontsize=10, ncol=1)  # Move legend to the right outside the plot
        ax.grid(True, linestyle='--', alpha=0.7)  # Add grid lines with dashed style and transparency

        # Stop the animation if the last frame is reached
        if frame == num_frames - 1:
            ani.event_source.stop()

    def on_key(event):
        if event.key == 'q':  # Press 'q' to stop the animation
            ani.event_source.stop()

    max_time = data['Time(ms)'].max()
    num_frames = int(max_time / 1000) + 1  # Ensure we include the last second

    ani = FuncAnimation(fig, update, frames=num_frames, interval=100)  # Animate every second
    # Save the animation as a GIF
    #ani.save('multiple_animation.gif', writer='pillow', fps=10)
    # Connect the key press event to the handler
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Adjusting space between plot and borders
    plt.subplots_adjust(left=0.000, right=1.000, top=1.000, bottom=0.000)  # Adjust the left and right spaces as needed
    manager=plt.get_current_fig_manager()
    manager.window.state('zoomed')
    manager.set_window_title('Mobility Animation') 

    # Show the plot
    plt.show()
