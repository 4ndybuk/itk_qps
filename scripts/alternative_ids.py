import os
from colorama import Fore
import csv
import re

def alternative_ids(client, colour):
    print(f"{colour("(Optional) back --> return to home menu", Fore.YELLOW)}")
    file_path = input("CSV directory: ")
    
    if file_path == "back":
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    elif file_path == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: Empty CSV directory, please try again •••", Fore.RED)}")
        return

    elif ".csv" not in file_path:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: File name must end with .csv, please try again •••", Fore.RED)}")
        return
    
    failed_list = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            # Verify alternative ID convention
            if not re.match(r'^[A-Z]{3}_\d{3}$', row[1]):
                print(colour(f"Incorrect alternative ID format for {row[0]}, skipping...",
                             Fore.RED))
                failed_list.append(row[0])
                continue

            try:
                client.post(
                    'setComponentProperty',
                    json={
                        'component':row[0],
                        'code':"ALTERNATIVE_IDENTIFIER",
                        'value':row[1],
                    },
                )
                print(colour(f"Successfully set alternative ID for {row[0]}", Fore.LIGHTGREEN_EX))
            except Exception as e:
                print(e)
                failed_list.append(row[0])

        print("Failed to process the following", failed_list)
    finished = input(f"{colour("PRESS ENTER TO RETURN TO MENU", Fore.YELLOW)}")
    if finished == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        return