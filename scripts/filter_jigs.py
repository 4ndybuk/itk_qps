import os
from colorama import Fore
import csv
from halo import Halo

def filter_jigs(client, colour):
    print(f"{colour("(Optional) back --> return to home menu", Fore.YELLOW)}")
    file_path = input("CSV directory: ")
    if file_path == "back":
        os.system('cls' if os.name == 'nt' else 'clear')
        return
    
    if ".csv" not in file_path:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: File name must end with .csv, try again •••", Fore.LIGHTRED_EX)}")
        return
    
    if file_path == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: Empty CSV directory, try again •••", Fore.LIGHTRED_EX)}")
        return

    if os.name == 'nt':
        print(colour("Retrieving component assembly data", Fore.GREEN))
    else:
        spinner = Halo(text="Retrieving component assembly data", spinner='earth')
        spinner.start()
    tool_list = []
    with open(file_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                component = client.get('getComponent', 
                                       json={"component":row[0],
                                             "alternativeIdentifier":False})
                test_id = [item['id'] 
                           for element in component['tests'] 
                           for item in element['testRuns'][0:] 
                           if element['code'] == "GLUE_MODULE_FLEX_ATTACH"]
                
                test_run = client.get('getTestRun',
                                      json={"testRun": test_id[0]})
                tool_id = [element['value'] for element in test_run['properties'] if element['code'] == 'TOOL_ID']
                if len(tool_id) == 0:
                    tool_id == "N/A"
                combined = [row[0], tool_id[0]]
                tool_list.append(combined)
            except Exception as e:
                print(e)
                return

    if os.name != "nt":   
        spinner.succeed("Done!")
    print("\nTool ID extraction completed, please choose your filter by ID number (none --> list all)")
    while True:
        filter_id = input("Tool ID: ")
        if filter_id in ['65','67','15','66','27','14']: 
            filtered_list = [row for row in tool_list if row[1] == int(filter_id)]
            print(f"{colour("••••••••••••••••••••••••••••", Fore.CYAN)}")
            print(*filtered_list, sep="\n")
            print(f"{colour("Number of filtered components: ", Fore.LIGHTYELLOW_EX)}", len(filtered_list))
            print(f"{colour("••••••••••••••••••••••••••••", Fore.CYAN)}")
        elif filter_id == "none":
            print(f"{colour("••••••••••••••••••••••••••••", Fore.CYAN)}")
            print(*tool_list, sep="\n")
            print(f"{colour("Total length of unfiltered list: ", Fore.LIGHTYELLOW_EX)}", len(tool_list))
            print(f"{colour("••••••••••••••••••••••••••••", Fore.CYAN)}")
        else:
            print(f"{colour("••• Invalid Tool ID •••", Fore.LIGHTRED_EX)}")
        
        continue_q = input("Choose another ID? (YES/NO): ").strip().upper()

        if continue_q == "NO":
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        elif continue_q == "YES":
            continue
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print(f"{colour("••• Invalid YES/NO response, returning to the main menu •••", Fore.LIGHTRED_EX)}")
            return