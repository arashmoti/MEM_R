import serial
import threading
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# --- CONFIGURATION ---
SERIAL_PORT = 'COM3'  # <<< CHANGE THIS TO YOUR PICO'S COM PORT
BAUD_RATE = 115200
HISTORY_LEN = 100     # Number of data points to show on the plot

# --- DATA STORAGE ---
# Use a negative range so the graph has a valid X-axis before data arrives
time_data = deque(range(-HISTORY_LEN, 0), maxlen=HISTORY_LEN)
target_pwm_data = deque([0]*HISTORY_LEN, maxlen=HISTORY_LEN)
actual_pwm_data = deque([0]*HISTORY_LEN, maxlen=HISTORY_LEN)
current_data = deque([0]*HISTORY_LEN, maxlen=HISTORY_LEN)

# Thread-safe flag for shutting down
running = True

# --- CONNECT TO PICO ---
try:
    pico_serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Failed to connect to {SERIAL_PORT}: {e}")
    exit()

# --- INPUT THREAD ---
def read_terminal_input():
    global running
    time.sleep(1) # Wait a second for serial connection to stabilize
    print("\n" + "="*50)
    print("MOTOR CONTROL TERMINAL")
    print("Commands:")
    print("  [0-100] : Set Target PWM %")
    print("  's'     : Stop Motor (0 PWM)")
    print("  'cal'   : Calibrate Sensor (Make sure motor is off)")
    print("  'q'     : Quit Program")
    print("="*50 + "\n")
    
    while running:
        user_input = input("Enter Command: ")
        if user_input.lower() == 'q':
            running = False
            pico_serial.write(b's\n') # Safely stop motor before quitting
            break
        
        # Send command to Pico
        command = f"{user_input}\n"
        pico_serial.write(command.encode('utf-8'))

# Start the input thread
input_thread = threading.Thread(target=read_terminal_input, daemon=True)
input_thread.start()

# --- PLOT SETUP ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.canvas.manager.set_window_title("Real-Time Motor Telemetry")

line_target, = ax1.plot(time_data, target_pwm_data, 'r--', label='Target PWM %')
line_actual, = ax1.plot(time_data, actual_pwm_data, 'b-', label='Actual PWM %')
line_current, = ax2.plot(time_data, current_data, 'g-', label='Current (A)')

ax1.set_ylim(-5, 105)
ax1.set_ylabel("PWM Percentage")
ax1.legend(loc='upper left')
ax1.grid(True)

ax2.set_ylim(-1, 6) # Adjust based on your HARD_LIMIT_A
ax2.set_ylabel("Current (Amps)")
ax2.set_xlabel("Time (Ticks)")
ax2.legend(loc='upper left')
ax2.grid(True)

# --- ANIMATION LOOP ---
def update_plot(frame):
    global running
    if not running:
        plt.close(fig)
        return

    # Read all available lines from serial
    while pico_serial.in_waiting:
        try:
            line = pico_serial.readline().decode('utf-8').strip()
        except UnicodeDecodeError:
            continue # Skip garbage bytes
            
        if not line:
            continue

        # Handle telemetry data
        if line.startswith("DATA,"):
            parts = line.split(',')
            if len(parts) == 4:
                try:
                    t_pwm = float(parts[1])
                    a_pwm = float(parts[2])
                    amps = float(parts[3])
                    
                    # Update rolling queues
                    time_data.append(time_data[-1] + 1)
                    target_pwm_data.append(t_pwm)
                    actual_pwm_data.append(a_pwm)
                    current_data.append(amps)
                except ValueError:
                    pass 

        # Handle text messages from Pico
        elif line.startswith("MSG,"):
            print(f"\n[PICO]: {line[4:]}")
            # Re-print input prompt so it doesn't get lost
            print("Enter Command: ", end='', flush=True) 

    # Update plot lines (Both X and Y coordinates)
    line_target.set_data(time_data, target_pwm_data)
    line_actual.set_data(time_data, actual_pwm_data)
    line_current.set_data(time_data, current_data)
    
    # Auto-scale X axis to create scrolling effect safely
    if time_data[0] != time_data[-1]:
        ax1.set_xlim(time_data[0], time_data[-1])
        ax2.set_xlim(time_data[0], time_data[-1])

    return line_target, line_actual, line_current

# Run animation at roughly 50ms intervals
ani = animation.FuncAnimation(fig, update_plot, interval=50, blit=False, cache_frame_data=False)

plt.tight_layout()
plt.show()

# Clean up after plot window is closed
running = False
if 'pico_serial' in locals() and pico_serial.is_open:
    pico_serial.close()
print("Disconnected.")