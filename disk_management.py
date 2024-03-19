import wmi
import subprocess
import sys

def list_disks():
    """Lists all connected disks with basic information."""
    try:
        c = wmi.WMI()
        disk_counter = 1  # Counter for disk numbering

        print("Disk ### Status  Size")
        print("------- -------- --------")
        for disk in c.Win32_DiskDrive():
            # Extract relevant disk details (assuming size in GB)
            size = int(disk.Size) / (1024**3)  # Convert bytes to GB
            status = disk.Status

            # Format output similar to the sample
            print(f"Disk {disk_counter}  {status[:6]}  {size:.2f} GB")
            disk_counter += 1  # Increment disk counter
    except Exception as wmi_error:
        print(f"WMI error occurred: {wmi_error}")
        print("Falling back to subprocess to execute diskpart commands...")
        try:
            # Execute diskpart commands using subprocess
            diskpart_output = subprocess.run(["diskpart", "/c", "list disk"], capture_output=True, text=True)
            if diskpart_output.returncode == 0:
                print(diskpart_output.stdout)
            else:
                print("Error executing diskpart commands.")
        except Exception as subprocess_error:
            print(f"Error occurred while listing disks: {subprocess_error}")
            sys.exit(1)

def list_and_select_disk():
    """Lists disks and prompts the user to select one."""
    try:
        c = wmi.WMI()
        disks = c.Win32_DiskDrive()

        if not disks:
            print("No disks found on the system.")
            return None

        print("Available disks:")
        print("Disk ###  Status       Size")
        print("-------  --------  --------")
        for i, disk in enumerate(disks):
            status = disk.Status if hasattr(disk, 'Status') else "Unknown"
            size = f"{int(disk.Size) / (1024**3):.2f} GB" if hasattr(disk, 'Size') else "Unknown"
            print(f"{i + 1}.       {status:<10}  {size}")

        while True:
            try:
                disk_number = int(input("Enter the number of the disk to select (0 to cancel): "))
                if disk_number == 0:
                    print("Operation canceled.")
                    return None
                elif 1 <= disk_number <= len(disks):
                    selected_disk = disks[disk_number - 1]
                    print(f"Selected disk: {selected_disk.Caption}")
                    return selected_disk
                else:
                    print("Invalid disk number. Please enter a number within the range.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def create_partition(disk_number: int, partition_size_mb: int) -> bool:
    """
    Creates a new primary partition on the specified disk using WMI or subprocess.

    Args:
        disk_number (int): The disk number (0 for the first disk, 1 for the second, etc.).
        partition_size_mb (int): The desired size of the partition in Megabytes (MB).

    Returns:
        bool: True if the partition was successfully created, False otherwise.
        
    Raises:
        ValueError: If the disk number or partition size is invalid.
        OSError: If an error occurs during partition creation.
    """
    try:
        # Connect to WMI
        c = wmi.WMI()

        # Get logical disks
        logical_disks = c.Win32_LogicalDisk(DriveType=0)  # Restrict to fixed disks

        # Check if disk number is valid
        if not 0 <= disk_number < len(logical_disks):
            raise ValueError(f"Invalid disk number: {disk_number}")

        # Check if partition size is valid
        if partition_size_mb <= 0:
            raise ValueError("Partition size must be greater than zero.")

        # Get selected disk object
        selected_disk = logical_disks[disk_number]

        # Check if there's enough free space
        free_space_mb = int(selected_disk.FreeSpace // (1024**2))
        if free_space_mb < partition_size_mb:
            raise OSError(f"Insufficient free space on disk. Required: {partition_size_mb} MB, Available: {free_space_mb} MB.")

        # Create the new partition using WMI
        selected_disk.CreatePartition(Type='Basic', UseMaximumSize=False, MaximumSize=partition_size_mb * 1024 * 1024)
        return True
    except Exception as wmi_error:
        print(f"WMI error occurred: {wmi_error}")
        print("Attempting to create partition using subprocess...")
        try:
            # Attempt to create the partition using subprocess (requires administrative privileges)
            subprocess.run(["diskpart", "/s", "create_partition_script.txt"], check=True)
            return True
        except subprocess.CalledProcessError as subprocess_error:
            print(f"Subprocess error occurred: {subprocess_error}")
            raise OSError("Failed to create partition using both WMI and subprocess.")
        except Exception as subprocess_error:
            print(f"Unknown subprocess error occurred: {subprocess_error}")
            raise OSError("Failed to create partition using both WMI and subprocess.")

