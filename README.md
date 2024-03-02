# Veeam_Task
# Folder Synchronization Utility

This Python script synchronizes the contents of two folders, ensuring that the replica folder matches the source folder's contents. It offers periodic synchronization and logs file operations.

## Usage

Run the script from the command line with the following syntax:

```bash
python sync_folders.py path_to_source_folder path_to_replica_folder --interval interval_seconds --log log_file
```
## Example:

```bash
python sync_folders.py "C:\Users\costa\Downloads\Veeam_Task\source" "C:\Users\costa\Downloads\Veeam_Task\replica" --interval 20 --log sync.log
```

