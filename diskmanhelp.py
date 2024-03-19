def display_help():
  """Provides detailed help information on zms DiskMan features."""
  print("\n** zms DiskMan Help **")
  print("This section provides detailed instructions on using zms DiskMan features:")

  print("\n1. List Disks:")
  print("Displays information about all connected disks, including size and status.")

  print("\n2. Select Disk:")
  print("Allows you to choose a specific disk for further operations. Subsequent actions like")
  print("formatting, partitioning, and resizing will be performed on the selected disk unless")
  print("otherwise specified.")

  print("\n3. Create and Delete Partition (on Selected Disk):")
  print("Creates a new primary partition on the selected disk. You will be prompted to enter the")
  print("desired size of the partition in megabytes (MB).")
  print("**Note:** This feature is currently under development and may not be fully functional.")

  print("\n4. Format Volume (Quick) - Selected Disk:")
  print("Performs a quick format on a suitable volume of the selected disk. Quick format removes")
  print("the existing file system and prepares the volume for use. You will be prompted to confirm")
  print("the formatting operation.")

  print("\n5. Format Volume (Custom) - Selected Disk:")
  print("Offers more control over formatting compared to the quick format option. You will need to")
  print("specify the desired file system (e.g., NTFS, exFAT), allocation unit size, and volume label.")
  print("**Note:** Formatting a volume erases all data on it. Ensure you have a backup of important data")
  print("before proceeding.")

  print("\n6. Resize Volume - Selected Disk:")
  print("Allows you to extend or shrink the selected volume. You can provide the size to extend in MB,")
  print("the desired size to shrink to in MB, and the minimum allowed size for shrinking in MB.")
  print("**Note:** Resizing operations may not be possible on all volumes or may have limitations depending")
  print("on the disk configuration. Ensure you have sufficient free space on the disk for extending.")

  print("\n7. List Volumes (All Disks or Selected Disk):")
  print("Displays detailed information about volumes, including label, file system, size, status,")
  print("creation date, cluster size, and drive type. If a disk is selected, the list will be specific")
  print("to volumes on that disk. Otherwise, it will show volumes on all connected disks.")

  print("\n8. Exit DiskPart:")
  print("Terminates the zms DiskMan program.")

  print("\n10. Exit:")
  print("Also exits the zms DiskMan program.")

  input("Press Enter to continue...")
