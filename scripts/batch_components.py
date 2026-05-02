import os
from colorama import Fore
import csv

def batch_components(client, colour):
    print(f"{colour("(Optional) back --> return to home menu", Fore.YELLOW)}")
    id_input = input("Batch identifier (mongoDB ID):  ")
    if id_input == "back":
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    elif id_input == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: Empty input for mongoDB, please try again •••", Fore.RED)}")
        return

    try:
        batch = client.get(
            'getBatch',
            json = {
                "id": id_input
            }
        )
        with open("batch_components.csv", 'w', newline = "") as file:
            writer = csv.writer(file)
            data = []
            for elements in batch['components']:
                data.append(elements['serialNumber'])
            for item in data:
                writer.writerow([item])
            print("The number of components in the batch: ", len(data))
    except Exception as e:
        print(e)
    finished = input(f"{colour("PRESS ENTER TO RETURN TO MENU", Fore.YELLOW)}")
    if finished == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        return