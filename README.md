# NTFS Mount Fixer

NTFS Mount Fixer is a simple GUI tool that helps users fix NTFS partition errors on Linux systems. The tool uses `ntfsfix` to clear the "dirty" flag on NTFS partitions, allowing the system to mount them correctly. This application provides an intuitive graphical interface for selecting partitions and running the necessary fix commands.

## Features

- **List Partitions**: Displays all partitions with relevant information, such as partition name, filesystem type, and size.
- **Select Partition**: Users can click on a partition to automatically populate the partition path in the input field.
- **Run ntfsfix**: Runs `ntfsfix --clear-dirty` on the selected partition to resolve NTFS mounting issues.
- **Root Password Prompt**: After confirming the fix, the app asks for the root password to execute the `ntfsfix` command with elevated privileges.

## Installation

1. **Install Dependencies**:
   - Make sure you have Python installed on your system.
   - You need the `tkinter` library for the GUI, and `ntfsfix` for fixing NTFS partitions.
   
   On a Debian-based distribution (Ubuntu, etc.), you can install the required dependencies with:

   ```bash
   sudo apt update
   sudo apt install python3-tk ntfs-3g
   ```

2. **Clone the repository**:
   
   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/ntfs-mount-fixer.git
   cd ntfs-mount-fixer
   ```

3. **Run the script**:

   After installing the dependencies and cloning the repo, simply run the application with Python:

   ```bash
   python3 main.py
   ```

## Usage

1. **Select Partition**:  
   From the main window, you will see a list of available partitions on your system, including their filesystem type and size. Click on the partition that you want to fix.

2. **Enter Partition Name (Optional)**:  
   If the listbox is not sufficient, you can manually enter the partition path (e.g., `/dev/sdb1`) into the input field.

3. **Run `ntfsfix`**:  
   After selecting the partition, click the "Run ntfsfix" button to attempt to fix the selected NTFS partition. You will be prompted to enter the root password to run the fix command with elevated privileges.

4. **Success or Failure**:  
   Once the process completes, the result is shown in the output area. If the partition is processed successfully, only the success message will be displayed. If there is an error, the full output of the command will be shown for debugging purposes.

## How it Works

The tool runs the `ntfsfix` command with the `--clear-dirty` option on the selected partition. This helps clear the "dirty" flag that may prevent NTFS partitions from being mounted correctly. Here's the basic command it uses:

```bash
sudo ntfsfix --clear-dirty /dev/sdb1
```

The program retrieves all available partitions using the `lsblk` command and allows the user to select the one they want to fix. Upon confirmation, it asks for the root password to execute the command with elevated privileges.

## Troubleshooting

- **"sudo: ntfsfix: command not found"**:  
  Ensure that `ntfs-3g` is installed on your system. On Ubuntu/Debian, use:

  ```bash
  sudo apt install ntfs-3g
  ```

- **Permissions issues**:  
  Make sure the script has the necessary permissions to run `sudo` and access the partitions.

## Contributing

If you would like to contribute to the project, feel free to fork the repository and submit pull requests. If you encounter any bugs or have feature suggestions, please open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Notes

- **Security Warning**: Since this app requires root privileges, always ensure that you trust the source of the script before running it.
- This tool is designed for Linux-based systems. For Windows or macOS, different methods or tools would be required to fix NTFS partition issues.

---
