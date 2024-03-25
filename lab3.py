import os
import hashlib
from datetime import datetime

class Git:
    def __init__(self):
        self.root_directory = self.initialize_root_directory()
        solution_directory = os.path.dirname(self.root_directory)
        self.snapshot_file_path = os.path.join(solution_directory, "snapshot.txt")

    def initialize_root_directory(self):
        root_directory = os.path.dirname(os.path.abspath(__file__))
        while not any(file.endswith(".csproj") for file in os.listdir(root_directory)):
            root_directory = os.path.dirname(root_directory)
        root_directory = os.path.join(root_directory, "test")
        return root_directory

    def display_menu(self):
        print("Menu:")
        print("1. Commit")
        print("2. Info <filename>")
        print("3. Status")

    def handle_menu(self):
        self.display_menu()
        choice = input("Enter your choice (1/2/3): ")
        if choice == "1":
            self.commit()
        elif choice == "2":
            file_name = input("Enter filename: ")
            self.info(file_name)
        elif choice == "3":
            self.status()
        else:
            print("Invalid choice!")

    def info(self, file_name):
        full_path = os.path.join(self.root_directory, file_name)

        if os.path.exists(full_path):
            crtime = datetime.fromtimestamp(os.path.getctime(full_path))
            uptime = datetime.fromtimestamp(os.path.getmtime(full_path))

            print(f"Name: {file_name}")
            print(f"Created on: {crtime}")
            print(f"Updated on: {uptime}")
        else:
            print(f"File {file_name} does not exist")
            return

        ext = file_name.split(".")
        if ext[1] == "txt":
            with open(full_path, 'r') as file:
                lines = file.readlines()
                lcount = len(lines)
                print(f"Lines: {lcount}")

                all_text = ''.join(lines)
                words = all_text.split()
                wcount = len(words)
                print(f"Words: {wcount}")

                ccount = len(all_text)
                print(f"Characters: {ccount}")

        if ext[1] in ["jpg", "jpeg", "png", "svg"]:
            with open(full_path, 'rb') as file:
                bitmap = file.read()
                width, height = self.get_image_size(bitmap)
                print(f"Image size: {width}x{height}")

        if ext[1] in ["cs", "java", "py"]:
            with open(full_path, 'r') as file:
                lines = file.readlines()
                lcount = len(lines)
                print(f"Lines: {lcount}")

                text = ''.join(lines)
                clcount = text.count("class")
                print(f"Classes in code: {clcount}")

    def commit(self):
        print(f"[SNAPSHOT CREATED AT {datetime.now()}]")

        current_snapshot = {}
        previous_snapshot = self.load_previous_snapshot()

        for root, _, files in os.walk(self.root_directory):
            for file in files:
                file_path = os.path.join(root, file)
                current_hash = self.calculate_file_hash(file_path)
                current_snapshot[file_path] = current_hash
                print(os.path.basename(file_path))

        self.save_snapshot(current_snapshot)

    def load_previous_snapshot(self):
        previous_snapshot = {}

        if os.path.exists(self.snapshot_file_path):
            with open(self.snapshot_file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if len(parts) == 2:
                        previous_snapshot[parts[0]] = parts[1]

        return previous_snapshot

    def save_snapshot(self, current_snapshot):
        with open(self.snapshot_file_path, 'w') as file:
            for file_path, file_hash in current_snapshot.items():
                file.write(f"{file_path}|{file_hash}\n")

    def calculate_file_hash(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def status(self):
        previous_snapshot = self.load_previous_snapshot()

        current_snapshot = {}
        for root, _, files in os.walk(self.root_directory):
            for file in files:
                file_path = os.path.join(root, file)
                current_hash = self.calculate_file_hash(file_path)
                current_snapshot[file_path] = current_hash

        print("State of files since last snapshot:")
        for file_path, current_hash in current_snapshot.items():
            file_name = os.path.basename(file_path)
            previous_hash = previous_snapshot.get(file_path, None)
            if previous_hash and current_hash != previous_hash:
                print(f"{file_name} - Edited")
            else:
                print(f"{file_name} - No changes")

    def get_image_size(self, data):
        width = int.from_bytes(data[0x12:0x16], byteorder='little', signed=False)
        height = int.from_bytes(data[0x16:0x1A], byteorder='little', signed=False)
        return width, height

if __name__ == "__main__":
    git_instance = Git()
    git_instance.handle_menu()
