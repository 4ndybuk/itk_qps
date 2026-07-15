import os
import csv
from colorama import Fore
from halo import Halo

def strain_reliefs(client, colour):
    print(f"{colour("(Optional) back --> return to home menu", Fore.YELLOW)}")
    print(f"{colour("Hint: One serial number per row needed, no commas", Fore.LIGHTBLUE_EX)}")
    file_path = input("CSV directory: ")

    if file_path == "back":
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    if file_path == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: Empty CSV directory, try again •••", Fore.LIGHTRED_EX)}")
        return
    
    if ".csv" not in file_path:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: File name must end with .csv, try again •••", Fore.LIGHTRED_EX)}")
        return
    
    spinner = Halo(text="••• Pushing test runs to the database •••", spinner='earth')
    spinner.start()
    failed_list = []
    with open(file_path, 'r', newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            # Check whether the serial number is correct
            if "20UPGM" not in str(row) and len(row) != 14:
                print(colour(f"\nIncorrect serial number for {row}, skipping •••", Fore.RED))
                failed_list.append(row)
            # Set relief to true for the modules
            try:
                relief_response = client.post("setComponentProperty",json={
                    "component": row[0],
                    "code": "OEC_SR",
                    "value": True
                    })
            except Exception:
                print(colour(f"\nError setting property for {row}, skipping •••", Fore.RED))
                failed_list.append(row)
    print(colour(f"\nFailed modules:\n{failed_list}", Fore.RED))
    spinner.succeed("••• RETURN PROMPT •••")
    finished = input(f"{colour("PRESS ENTER TO RETURN TO MENU", Fore.YELLOW)}")
    if finished == "":
        os.system('cls' if os.name == 'nt' else 'clear')
    
