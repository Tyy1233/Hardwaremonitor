import psutil
import subprocess
import time
import datetime



def monitor_cpu():
    # Get CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)

    # Check if there has been a sudden spike in usage
    threshold = 15  # Change this value to adjust the sensitivity
    if abs(cpu_percent - monitor_cpu.last_cpu_percent) > threshold:
        # Get the current time and format it as a string
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Write a message to the text file
        with open("spikes.txt", "a") as f:
            f.write(f"[{time_stamp}] CPU usage spiked from {monitor_cpu.last_cpu_percent}% to {cpu_percent}%\n")

    # Store the current usage for the next iteration
    monitor_cpu.last_cpu_percent = cpu_percent

# Initialize the last_cpu_percent variable
monitor_cpu.last_cpu_percent = 0





def monitor_gpu(last_utilization):
    # Run the nvidia-smi command
    output = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    # Parse the output
    lines = output.split("\n")
    header, *values = lines
    utilization = [int(line.split(",")[0].strip(" %")) for line in values]

    # Check if there has been a sudden spike in usage
    threshold = 30  # Change this value to adjust the sensitivity
    for i, u in enumerate(utilization):
        if abs(u - last_utilization[i]) > threshold:
            # Get the current time and format it as a string
            time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Write a message to the text file
            with open("spikes.txt", "a") as f:
                f.write(f"[{time_stamp}] GPU {i} usage spiked from {last_utilization[i]}% to {u}%\n")

    # Store the current utilization for the next iteration
    return utilization

# Initialize the last_utilization variable
last_utilization = [0]

while True:
    last_utilization = monitor_gpu(last_utilization)






def monitor_hard_drives():
    # Get hard drive usage
    drives = psutil.disk_partitions()
    for drive in drives:
        if drive.device not in monitor_hard_drives.last_usage:
            monitor_hard_drives.last_usage[drive.device] = 0
        usage = psutil.disk_usage(drive.mountpoint)

        # Check if there has been a sudden spike in usage
        threshold = 20  # Change this value to adjust the sensitivity
        if abs(usage.percent - monitor_hard_drives.last_usage[drive.device]) > threshold:
            # Get the current time and format it as a string
            time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Write a message to the text file
            with open("spikes.txt", "a") as f:
                f.write(f"[{time_stamp}] Hard drive {drive.device} usage spiked from {monitor_hard_drives.last_usage[drive.device]}% to {usage.percent}%\n")

        # Store the current usage for the next iteration
        monitor_hard_drives.last_usage[drive.device] = usage.percent

# Initialize the last_usage dictionary
monitor_hard_drives.last_usage = {}




def monitor_memory():
    # Get memory usage
    memory_percent = psutil.virtual_memory().percent

    # Check if there has been a sudden spike in usage
    threshold = 2  # Change this value to adjust the sensitivity
    if abs(memory_percent - monitor_memory.last_memory_percent) > threshold:
        # Get the current time and format it as a string
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Write a message to the text file
        with open("spikes.txt", "a") as f:
            f.write(f"[{time_stamp}] Memory usage spiked from {monitor_memory.last_memory_percent}% to {memory_percent}%\n")

    # Store the current usage for the next iteration
    monitor_memory.last_memory_percent = memory_percent

# Initialize the last_memory_percent variable
monitor_memory.last_memory_percent = 0








def main():
    while True:
        monitor_cpu()
        monitor_gpu()
        monitor_hard_drives()
        monitor_memory()
        
        time.sleep(1)

main()