import os
import shutil
import time
import schedule
import threading
import sys

def input_thread():
    input("Press enter to quit!\n")

def sync_folders(source, replica, log_file_path):

    log_file = open(log_file_path, 'a')

    # Check if both source and replica folders exist
    if not os.path.isdir(source):
        print(f"Error: {source} is not a directory.")
        return
    if not os.path.isdir(replica):
        print(f"Error: {replica} is not a directory.")
        return

    # Loop through all files and subdirectories in the source folder
    for item in os.listdir(source):
        src_item_path = os.path.join(source, item)
        repl_item_path = os.path.join(replica, item)

        # If item is a file, copy or update it in the replica folder
        if os.path.isfile(src_item_path):
            if os.path.exists(repl_item_path):
                if os.path.getmtime(src_item_path) != os.path.getmtime(repl_item_path):
                    shutil.copy2(src_item_path, repl_item_path)
                    log_file.write(f"Updated file {item} from {source_path} to {replica_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    print(f"Updated file {item} from {source_path} to {replica_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                shutil.copy2(src_item_path, repl_item_path)
                log_file.write(f"Copied file {item} from {source_path} to {replica_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print(f"Copied file {item} from {source_path} to {replica_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # If item is a subdirectory, create or update it in the replica folder
        elif os.path.isdir(src_item_path):
            if os.path.exists(repl_item_path):
                sync_folders(src_item_path, repl_item_path, log_file_path)
            else:
                shutil.copytree(src_item_path, repl_item_path)
                log_file.write(f"Created folder {item} in {replica_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print(f"Created folder {item} in {replica_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # If item is neither a file nor a subdirectory, ignore it
        else:
            log_file.write(f"Ignored folder {item} in {replica_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"Ignored folder {item} in {replica_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Loop through all files and subdirectories in the replica folder
    for item in os.listdir(replica):
        src_item_path = os.path.join(source, item)
        repl_item_path = os.path.join(replica, item)

        # If item does not exist in source folder, delete it from replica folder
        if not os.path.exists(src_item_path):
            if os.path.isfile(repl_item_path):
                os.remove(repl_item_path)
                log_file.write(f"Deleted file {item} from {replica} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print(f"Deleted file {item} from {replica} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            elif os.path.isdir(repl_item_path):
                shutil.rmtree(repl_item_path)
                log_file.write(f"Deleted folder {item} from {replica} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print(f"Deleted folder {item} from {replica} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

if len(sys.argv) != 5:
    print("Usage: python veeam.py <source_folder> <replica_folder> <interval_time_sec> <log_file> ")
    sys.exit()

source_path = sys.argv[1]
replica_path = sys.argv[2]
interval_time_sec = int(sys.argv[3])
log_file_path = sys.argv[4]

t = threading.Thread(target=input_thread)
t.start()

sync_folders(source_path, replica_path, log_file_path)
schedule.every(interval_time_sec).seconds.do(sync_folders, source_path, replica_path, log_file_path)

while True:
    schedule.run_pending()
    time.sleep(1)
    if not t.is_alive():
        break
