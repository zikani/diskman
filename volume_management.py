# volume_management.py
import wmi



def format_volume(logical_disk, file_system, size, label):
    """Formats the selected volume with the specified file system."""
    try:
        logical_disk.FileSystem = file_system
        logical_disk.Format(size=size, label=label, quick_format=True)
        print("Formatting completed successfully.")
    except Exception as e:
        print(f"Error during custom format: {e}")



def resize_volume(volumes, extend_size=None, shrink_desired_size=None, shrink_min_size=None, shrink_unallocated=False):
    """Extends or shrinks the selected volume.

    Args:
        volumes (list): List of WMI objects representing logical disks (volumes).
        extend_size (int, optional): Size (in MB) to extend the volume by. Defaults to None.
        shrink_desired_size (int, optional): Desired size (in MB) to shrink the volume to. Defaults to None.
        shrink_min_size (int, optional): Minimum allowed size (in MB) for shrinking. Defaults to None.
        shrink_unallocated (bool, optional): Flag to shrink only unallocated space (future implementation). Defaults to False.

    Returns:
        bool: True on success, False on error.
    """

    try:
        if not volumes:
            print("No volumes found.")
            return False

        # Display available volumes for selection with sizes and free space
        print("Available Volumes:")
        print("Volume   Size     Free Space")
        print("-------  -------  ----------")
        for i, volume in enumerate(volumes, start=1):
            size_mb = volume.Size / (1024**2)
            free_space_mb = volume.FreeSpace / (1024**2)
            print(f"{i}. {volume.DeviceID}   {size_mb:.2f} MB   {free_space_mb:.2f} MB")

        # Prompt user to select a volume
        while True:
            try:
                volume_number = int(input("Enter the number of the volume to resize (0 to cancel): "))
                if volume_number == 0:
                    print("Resize canceled.")
                    return False
                elif 1 <= volume_number <= len(volumes):
                    selected_volume = volumes[volume_number - 1]
                    print(f"Selected volume: {selected_volume.DeviceID}")
                    break
                else:
                    print("Invalid volume number. Please enter a number within the range.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Get current volume size
        current_size = int(selected_volume.Size // (1024**2))
        free_space = int(selected_volume.FreeSpace // (1024**2))  # Current free space on the volume

        # Print available space
        print(f"Available space on volume {selected_volume.DeviceID}: {free_space} MB")

        # User confirmation for resize operations
        if extend_size is not None:
            confirmation = input(f"Are you sure you want to extend volume {selected_volume.DeviceID} by {extend_size} MB? (y/n): ")
        elif shrink_desired_size is not None:
            confirmation = input(f"Are you sure you want to shrink volume {selected_volume.DeviceID} to {shrink_desired_size} MB? (y/n): ")
        else:
            confirmation = input(f"Are you sure you want to shrink volume {selected_volume.DeviceID} to a minimum size of {shrink_min_size} MB? (y/n): ")

        if confirmation.lower() != 'y':
            print("Resize canceled.")
            return False

        # Handle extend operation
        if extend_size is not None:
            # Check if there's enough free space on the volume
            if free_space < extend_size:
                print(f"Insufficient free space on volume {selected_volume.DeviceID}. Required: {extend_size} MB, Available: {free_space} MB.")
                return False
            selected_volume.Extend(Size=extend_size)
            print("Volume extended successfully.")
            return True

        # Handle shrink operation
        elif shrink_desired_size is not None:
            # Ensure shrink size is within valid range (current size to minimum size)
            if shrink_desired_size < shrink_min_size or shrink_desired_size > current_size:
                print(f"Invalid shrink size. Desired size ({shrink_desired_size} MB) must be between current size ({current_size} MB) and minimum size ({shrink_min_size} MB).")
                return False
            selected_volume.Shrink(DesiredNewSize=shrink_desired_size, MinimumSize=shrink_min_size)
            print("Volume shrunk successfully.")
            return True

    except Exception as e:
        print(f"Error during volume resize: {e}")
        return False




def mount_volume(logical_disk):
    """Mounts the selected volume."""
    try:
        logical_disk.Mount()
        print("Volume mounted successfully.")
    except Exception as e:
        print(f"Error during volume mounting: {e}")


def dismount_volume(logical_disk):
    """Dismounts the selected volume."""
    try:
        logical_disk.Dismount()
        print("Volume dismounted successfully.")
    except Exception as e:
        print(f"Error during volume dismounting: {e}")



def format_volume_quick(selected_disk):
    """Performs a quick format on the selected volume."""
    try:
        partitions = selected_disk.associators("Win32_DiskDriveToDiskPartition")

        if not partitions:
            print("No partitions found on the selected disk.")
            return

        found_partition = None
        for partition in partitions:
            try:
                logical_disk = partition.associators("Win32_LogicalDisk")[0]
                if logical_disk.DriveType == 3:  # Check for DriveType 3 (Fixed disk)
                    found_partition = logical_disk
                    break
            except IndexError:
                continue

        if found_partition:
            # Ask for confirmation
            confirm = input(f"Are you sure you want to format volume {found_partition.DeviceID}? (yes/no): ").lower()
            if confirm == 'yes':
                print(f"Formatting volume: {found_partition.DeviceID} (Quick Format)")
                try:
                    # Use quick format method from Win32_LogicalDisk class
                    found_partition.QuickFormat()
                    print("Formatting completed successfully.")
                except Exception as e:
                    print(f"Error during quick format: {e}")
            else:
                print("Format operation cancelled.")
        else:
            print("No suitable volume found for quick format on the selected disk.")
    except Exception as e:
        print(f"An error occurred: {e}")


def format_volume_custom(selected_disk):
    """Formats the selected volume with custom options."""
    try:
        partitions = selected_disk.associators("Win32_DiskDriveToDiskPartition")

        if not partitions:
            print("No partitions found on the selected disk.")
            return

        found_partition = None
        for partition in partitions:
            try:
                logical_disk = partition.associators("Win32_LogicalDisk")[0]
                if logical_disk.DriveType == 3:  # Check for DriveType 3 (Fixed disk)
                    found_partition = logical_disk
                    break
            except IndexError:
                continue

        if found_partition:
            # Ask for confirmation
            confirm = input(f"Are you sure you want to format volume {found_partition.DeviceID}? (yes/no): ").lower()
            if confirm == 'yes':
                file_system = input("Enter file system (e.g., NTFS, exFAT): ")
                print(f"Formatting volume: {found_partition.DeviceID} with file system {file_system}")

                try:
                    # Use custom format method from Win32_LogicalDisk class
                    found_partition.FileSystem = file_system
                    found_partition.Format()
                    print("Formatting completed successfully.")
                except Exception as e:
                    print(f"Error during custom format: {e}")
            else:
                print("Format operation cancelled.")
        else:
            print("No suitable volume found for formatting on the selected disk.")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_volumes(disk=None):
    """Lists volumes on the selected disk or all disks if none is selected."""
    c = wmi.WMI()

    if disk:
        # List volumes on the selected disk
        print("\nVolume ###  Ltr  Label        Fs     Type        Size     Status     Info")
        print("----------  ---  -----------  -----  ----------  -------  ---------  --------")
        for i, partition in enumerate(disk.associators("Win32_DiskDriveToDiskPartition"), start=1):
            try:
                # Retrieve volume letter
                volume_letter = ""
                for logical_disk in partition.associators("Win32_LogicalDisk"):
                    volume_letter = logical_disk.DeviceID
                    break
                if not volume_letter:
                    volume_letter = " "

                label = partition.VolumeName if hasattr(partition, 'VolumeName') else " "
                file_system = partition.FileSystem if hasattr(partition, 'FileSystem') else " "
                size = int(partition.Size) / (1024**3) if hasattr(partition, 'Size') else "Unknown"  # Convert bytes to GB
                size_str = f"{size:.2f} GB" if isinstance(size, float) else size
                
                # Retrieve volume status
                status = "Unknown"
                for volume in partition.associators("Win32_LogicalDisk"):
                    if hasattr(volume, "HealthState"):
                        status = volume.HealthState
                    elif hasattr(volume, "OperationalStatus"):
                        status = volume.OperationalStatus
                    break
                
                # Retrieve additional information from Win32_DiskPartition class
                additional_info = ""
                for disk_partition in partition.associators("Win32_DiskPartition"):
                    creation_date = disk_partition.CreationDate if hasattr(disk_partition, "CreationDate") else "Unknown"
                    cluster_size = disk_partition.BlockSize if hasattr(disk_partition, "BlockSize") else "Unknown"
                    disk_type = disk_partition.DriveType if hasattr(disk_partition, "DriveType") else "Unknown"
                    additional_info += f"Creation Date: {creation_date}, Cluster Size: {cluster_size}, Drive Type: {disk_type}"
                
                print(f"Volume {i:<5}    {volume_letter:<3} {label[:11]:<11}  {file_system[:5]:<5}  Partition  {size_str:<8}  {status:<9}  {additional_info}")
            except AttributeError as e:
                print(f"AttributeError: {e}. Skipping volume.")
    else:
        # List volumes on all disks
        print("\nAll Volumes:")
        for disk in c.Win32_DiskDrive():
            print(f"\n  Volumes on Disk {disk.Caption}:")
            for i, partition in enumerate(disk.associators("Win32_DiskDriveToDiskPartition"), start=1):
                try:
                    # Retrieve volume letter
                    volume_letter = ""
                    for logical_disk in partition.associators("Win32_LogicalDisk"):
                        volume_letter = logical_disk.DeviceID
                        break
                    if not volume_letter:
                        volume_letter = " "

                    label = partition.VolumeName if hasattr(partition, 'VolumeName') else " "
                    file_system = partition.FileSystem if hasattr(partition, 'FileSystem') else " "
                    size = int(partition.Size) / (1024**3) if hasattr(partition, 'Size') else "Unknown"  # Convert bytes to GB
                    size_str = f"{size:.2f} GB" if isinstance(size, float) else size
                    
                    # Retrieve volume status
                    status = "Unknown"
                    for volume in partition.associators("Win32_LogicalDisk"):
                        if hasattr(volume, "HealthState"):
                            status = volume.HealthState
                        elif hasattr(volume, "OperationalStatus"):
                            status = volume.OperationalStatus
                        break
                    
                    # Retrieve additional information from Win32_DiskPartition class
                    additional_info = ""
                    for disk_partition in partition.associators("Win32_DiskPartition"):
                        creation_date = disk_partition.CreationDate if hasattr(disk_partition, "CreationDate") else "Unknown"
                        cluster_size = disk_partition.BlockSize if hasattr(disk_partition, "BlockSize") else "Unknown"
                        disk_type = disk_partition.DriveType if hasattr(disk_partition, "DriveType") else "Unknown"
                        additional_info += f"Creation Date: {creation_date}, Cluster Size: {cluster_size}, Drive Type: {disk_type}"
                    
                    print(f"    Volume {i:<5}    {volume_letter:<3} {label[:11]:<11}  {file_system[:5]:<5}  Partition  {size_str:<8}  {status:<9}  {additional_info}")
                except AttributeError as e:
                    print(f"AttributeError: {e}. Skipping volume.")

