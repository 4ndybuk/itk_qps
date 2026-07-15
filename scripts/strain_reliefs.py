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
            if "20UPGM" not in row and len(row) != 14:
                print(colour(f"Incorrect serial number for {row}, skipping •••", Fore.RED))
                failed_list.append(row)
            # Set relief to true for the modules
            relief_response = client.post("setComponentProperty",json={
                "component": "20UPGM24810187",
                "code": "OEC_SR",
                "value": True
                })
    spinner.succeed("••• RETURN PROMPT •••")
    finished = input(f"{colour("PRESS ENTER TO RETURN TO MENU", Fore.YELLOW)}")
    if finished == "":
        os.system('cls' if os.name == 'nt' else 'clear')
    
