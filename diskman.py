import os
from disk_management import list_disks, list_and_select_disk, create_partition
from volume_management import format_volume_quick, list_volumes, resize_volume, format_volume
import diskmanhelp

def print_version_info():
  """Prints the version information, copyright notice, and computer name."""
  computer_name = os.environ.get('COMPUTERNAME', 'Unknown')
  print(" DiskMan Version 1.0.0")
  print("Copyright (C) ZMSTECH.")
  print(f"On computer: {computer_name}")

def main():
  """Main program loop with basic text-based UI (TUI)"""
  selected_disk = None

  while True:
    print("\n**  DiskMan **")  # Enhanced banner
    print("1. List Disks")
    print("2. Select Disk")
    print("3. Create and Delete Partition (on Selected Disk)")
    print("4. Format Volume (Quick) - Selected Disk")
    print("5. Format Volume (Custom) - Selected Disk")
    print("6. Resize Volume - Selected Disk")
    print("7. List Volumes (All Disks or Selected Disk)")
    print("8. Exit DiskPart")
    print("9. Help")
    print("10. Exit")
    choice = input("Enter your choice (1-10): ")

    if choice == "1":
      list_disks()
    elif choice == "2":
      selected_disk = list_and_select_disk()
    elif choice == "3":
        if selected_disk:
            try:
                size = int(input("Enter size for the primary partition (in MB): "))
                if size <= 0:
                    print("Partition size must be greater than zero.")
                else:
                    if create_partition(selected_disk, size):
                        print("Partition created successfully.")
                    else:
                        print("Partition creation failed.")
            except ValueError:
                print("Invalid input. Please enter a valid integer value for partition size.")
        else:
            print("No disk selected. Please select a disk first.")



    elif choice == "4":
      if selected_disk:
        format_volume_quick(selected_disk)
      else:
        print("No disk selected. Please select a disk first.")
    elif choice == "5":
        if selected_disk:
            supported_file_systems = ['NTFS', 'FAT32', 'exFAT']  # Update with actual supported file systems
            print("Supported file systems:", supported_file_systems)
            fs = input("Enter file system (e.g., NTFS, FAT32, exFAT): ").upper()
            if fs not in supported_file_systems:
                print("Invalid file system.")
                continue
            size = input("Enter allocation unit size: ")
            label = input("Enter volume label: ")
            format_volume(selected_disk, fs, size, label)
        else:
            print("No disk selected. Please select a disk first.")

    elif choice == "6":
        if selected_disk:
            print("\n** Resize Volume **")
            extend_size = input("Enter size to extend volume (in MB, leave empty for no extension): ").strip()
            shrink_desired_size = input("Enter desired size to shrink (in MB, leave empty for no shrink): ").strip()
            shrink_min_size = input("Enter minimum size to shrink (in MB, leave empty for no shrink): ").strip()
            
            if extend_size or shrink_desired_size or shrink_min_size:
                volumes = selected_disk.associators("Win32_DiskDriveToDiskPartition")[0].associators("Win32_LogicalDisk")
                resize_volume(volumes, extend_size, shrink_desired_size, shrink_min_size)
            else:
                print("No resizing options provided. Operation canceled.")
        else:
            print("No disk selected. Please select a disk first.")

    elif choice == "7":
      if selected_disk:
        print("\nVolume Information for Selected Disk:")
        list_volumes(selected_disk)
      else:
        print("\nVolume Information for All Disks:")
        list_volumes()
    elif choice == "8":
      print("Exiting DiskPart")
      break
    elif choice == "9":
        diskmanhelp.display_help()  
    elif choice == "10":
      print("Exiting...")
      break
    else:
      print("Invalid choice. Please enter a number between 1 and 10.")



if __name__ == "__main__":
  print_version_info()
  main()
