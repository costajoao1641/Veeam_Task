import os
import shutil
import time
import argparse
import logging

def sync_folders(source, replica, log_file,interval):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        try:
            for root, dirs, files in os.walk(source):
                # create similar directories in replica folder if not already created
                for dir in dirs:
                    source_path_dir=os.path.join(root, dir)
                    replica_path_dir = os.path.join(replica, os.path.relpath(source_path_dir, source))
                    if not os.path.exists(replica_path_dir):# or os.path.getmtime(source_path_dir) > os.path.getmtime(replica_path_dir):
                        os.makedirs(replica_path_dir)
                        logging.info(f"Created folder: {replica_path_dir} in replica_folder")
                #copy files from source to replica folder
                for file in files:
                    source_path_file = os.path.join(root, file)
                    replica_path_file = os.path.join(replica, os.path.relpath(source_path_file, source))
                    # only copies it if the file does not exist or if there is a last modification in the original file later than the last modification in the replica file
                    if not os.path.exists(replica_path_file) or os.path.getmtime(source_path_file) > os.path.getmtime(replica_path_file):
                        shutil.copy2(source_path_file, replica_path_file)
                        logging.info(f"Copied {source_path_file} to {replica_path_file}")

            #after copying the files and creating the directories it is necessary to eliminate directories or files that were eliminated form the source folder
            for root, dirs, files in os.walk(replica):
                for dir in dirs:
                    replica_path_dir=os.path.join(root, dir)
                    source_path_dir = os.path.join(source, os.path.relpath(replica_path_dir, replica))
                    #deletes directory if it doesn't exist in source folder
                    if not os.path.exists(source_path_dir):
                        shutil.rmtree(replica_path_dir)
                        logging.warning(f"Removed folder: {replica_path_dir} from replica folder")
                for file in files:
                    replica_path_file = os.path.join(root, file)
                    source_path_file = os.path.join(source, os.path.relpath(replica_path_file, replica))
                    #deletes file if it doesn't exist in source folder
                    if not os.path.exists(source_path_file):
                        os.remove(replica_path_file)
                        logging.warning(f"Removed file: {replica_path_file} from replica folder")
            time.sleep(interval)
        except Exception as e:
            logging.error(f"Error occurred: {e}")

def main():
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

    if not os.path.exists(source):
        logging.error("Source folder does not exist.") # A folder will be created in the directory.") --- Não sei se faz sentido criar a source folder
        #print("Source folder does not exist. A folder will be created in the directory.")
        #os.makedirs(source(source))
        #logging.info(f"Created source folder: {source}")
    if not os.path.exists(replica):
        logging.warning("Replica folder does not exist. A folder will be created in the directory.")
        #print("Replica folder does not exist. A folder will be created in the directory.")
        os.makedirs(replica)
        logging.info(f"Created replica folder: {replica}")

    sync_folders(source, replica, log_file,interval)

if __name__ == "__main__":
    
    main()