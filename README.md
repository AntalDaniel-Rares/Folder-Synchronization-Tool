# Folder-Synchronization-Tool
This script allows you to synchronize two folders by copying any new or modified files from the source folder to the replica folder, and deleting any files or folders from the replica folder that no longer exist in the source folder. The synchronization can be scheduled to run at a specific interval of time.

# Usage
To use this script, run the following command:<br>
`python folder_sync.py <source_folder> <replica_folder> <interval_time_sec> <log_file_path>`

Where:

`<source_folder>` is the path to the folder you want to synchronize from.<br>
`<replica_folder>` is the path to the folder you want to synchronize to.<br>
`<interval_time_sec>` is the interval time in seconds between each synchronization.<br>
`<log_file_path>` is the path to the log file where the synchronization activity will be recorded.<br>

# Example
For example, to synchronize the folder ~/Documents to the folder ~/Backup, with a synchronization interval of 3600 seconds (1 hour), and the log file saved at ~/log.txt, run the following command:<br>

`python folder_sync.py ~/Documents ~/Backup 3600 ~/log.txt`

# Requirements
 - Python 3.x
 - schedule module (pip install schedule)

# Logging
The tool also logs all changes made during the sync process to the specified log file. The log file will contain a record of all new and modified files that were copied from the source folder to the replica folder, as well as all files and subfolders that were deleted from the replica folder.

# Limitations
 - The script only synchronizes files and subdirectories, it does not handle other types of items such as links or device files.
 - The script does not handle file or folder renames, it treats renamed files or folders as new files or folders and copies them to the replica folder.
