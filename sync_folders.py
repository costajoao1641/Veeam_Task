import os
import shutil
import time
import argparse
import logging
import filecmp
def sync_folders(source, replica, log_file,interval):
    """
    Synchronizes files and directories from the source folder to the replica folder.

    Args:
        source (str): Path to the source folder.
        replica (str): Path to the replica folder.
        log_file (str): Path to the log file.
        interval (int): Synchronization interval in seconds.
    """
    # Configure logging settings
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        try:
            # Iterate through each directory and file in the source folder
            for root, dirs, files in os.walk(source):
                # Create directories in replica if they don't already exist
                for dir in dirs:
                    source_path_dir=os.path.join(root, dir)
                    replica_path_dir = os.path.join(replica, os.path.relpath(source_path_dir, source))
                    if not os.path.exists(replica_path_dir):
                        os.makedirs(replica_path_dir)
                        logging.info(f"Created folder: {replica_path_dir} in replica_folder")
                # Copy files from source to replica folder if they don't exist or if they differ
                for file in files:
                    source_path_file = os.path.join(root, file)
                    replica_path_file = os.path.join(replica, os.path.relpath(source_path_file, source))
                    if not os.path.exists(replica_path_file) or not filecmp.cmp(replica_path_file, source_path_file, shallow=False): #or os.path.getmtime(source_path_file) > os.path.getmtime(replica_path_file) 
                        shutil.copy2(source_path_file, replica_path_file)
                        logging.info(f"Copied {source_path_file} to {replica_path_file}")

            # Clean up files and directories in replica folder that don't exist in source folder
            for root, dirs, files in os.walk(replica):
                for dir in dirs:
                    replica_path_dir=os.path.join(root, dir)
                    source_path_dir = os.path.join(source, os.path.relpath(replica_path_dir, replica))
                    if not os.path.exists(source_path_dir):
                        shutil.rmtree(replica_path_dir)
                        logging.warning(f"Removed folder: {replica_path_dir} from replica folder")
                for file in files:
                    replica_path_file = os.path.join(root, file)
                    source_path_file = os.path.join(source, os.path.relpath(replica_path_file, replica))
                    if not os.path.exists(source_path_file):
                        os.remove(replica_path_file)
                        logging.warning(f"Removed file: {replica_path_file} from replica folder")

            # Wait for the specified interval before next synchronization
            time.sleep(interval)

        except Exception as e:
            logging.error(f"Error occurred: {e}")

def main():
    """
    Main function to parse command-line arguments and start synchronization.
    """
    parser = argparse.ArgumentParser(description='Folder Synchronization')
    parser.add_argument('source', type=str, help='Source folder path')
    parser.add_argument('replica', type=str, help='Replica folder path')
    parser.add_argument('--interval', type=int, default=60, help='Interval in seconds for synchronization (default: 60)')
    parser.add_argument('--log', type=str, help='Path to log file (default: sync.log)')
    args = parser.parse_args()

    source = args.source
    replica = args.replica
    interval = args.interval
    log_file = args.log

    # Check if the source folder exists
    if not os.path.exists(source):
        logging.error("Source folder does not exist. Please create the source folder and rerun the program.") 
        return
    
    # Create replica folder if it doesn't exist
    if not os.path.exists(replica):
        logging.warning("Replica folder does not exist. A folder will be created in the directory.")
        os.makedirs(replica)
        logging.info(f"Created replica folder: {replica}")

    # Create an empty log file if it doesn't exist
    if not os.path.exists(log_file):
        open(log_file, 'a').close()
        

    # Start synchronization process
    sync_folders(source, replica, log_file,interval)

if __name__ == "__main__":
    
    main()