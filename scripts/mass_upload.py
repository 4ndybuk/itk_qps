import os
from colorama import Fore
import csv
from halo import Halo
from datetime import datetime, timezone

def mass_upload(client, colour):
    print(f"{colour("(Optional) back --> return to home menu", Fore.YELLOW)}")
    print(f"{colour("(Optional) show --> show example .csv file", Fore.LIGHTBLUE_EX)}")
    file_path = input("CSV directory: ")
    
    if file_path == "show":
        print(f"""
                    .CSV file for mass upload
        ╔═════════════════════════════════════════════════════════════╗
        ║                                                             ║
        ║                     20UPGBXXXXXXXX,1242.2 <-- MASS IN MG    ║
        ║   SERIAL NUMBER --> 20UPGBXXXXXXXX,3253.2                   ║
        ║                     20UPGBXXXXXXXX,1834.3                   ║
        ║                     ...,...                                 ║
        ╚═════════════════════════════════════════════════════════════╝
              
        {colour("* Only one type of component per .csv file, do not mix types!", Fore.LIGHTRED_EX)}
            """)
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

    component_type = input(f"\nComponent type:\n\tA --> PCB Flex\n\tB --> Bare Module\n\tC --> Assembled Module\n\tD --> Back to Menu\n\t\n\tChoice: ").strip().upper()
    print("")

    if component_type == "back":
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    if component_type == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: Empty component type input, please try again •••", Fore.LIGHTRED_EX)}")
        return
    
    failed_list = []
    spinner = Halo(text="••• Pushing test runs to the database •••", spinner='earth')
    spinner.start()
    with open(file_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            # print(row)
            try:
                now_utc = datetime.now(timezone.utc)
                iso_time = now_utc.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
                if component_type == "A":
                    test_json = {
                        "component": row[0],
                        "testType": "MASS",
                        "institution": "LIV",
                        "runNumber": "1",
                        "date": iso_time,
                        "passed": True,
                        "problems": False,
                        "properties": {
                            "OPERATOR": "Andy Bukowski",
                            "INSTRUMENT": "Ohaus Pioneer",
                            "ANALYSIS_VERSION": None
                        },
                        "results": {
                            "MASS": row[1]
                        }
                        }
                elif component_type == "B":
                    test_json = {
                        "component": row[0],
                        "testType": "MASS_MEASUREMENT",
                        "institution": "LIV",
                        "runNumber": "1",
                        "date": iso_time,
                        "passed": True,
                        "problems": False,
                        "properties": {
                            "SCALE_ACCURACY": 0.1,
                            "ANALYSIS_VERSION": None,
                            "MEASUREMENT_DATE": iso_time,
                            "OPERATOR_IDENTITY": "Andy Bukowski"
                        },
                        "results": {
                            "MASS": row[1]
                        }
                        }
                elif component_type == "C":
                    test_json = {
                      "component": row[0],
                      "testType": "MASS_MEASUREMENT",
                      "institution": "LIV",
                      "runNumber": "1",
                      "date": iso_time,
                      "passed": True,
                      "problems": False,
                      "properties": {
                        "SCALE_ACCURACY": 0.1,
                        "ANALYSIS_VERSION": None,
                        "MEASUREMENT_DATE": iso_time,
                        "OPERATOR_IDENTITY": "Andy Bukowski"
                      },
                      "results": {
                        "MASS": row[1]
                      }
                    }
                else:
                    return
                test_upload = client.post('uploadTestRunResults',json=test_json)
            except Exception as e:
                print(e)
                failed_list.append(row[0])
                
        if len(failed_list) < 1:
            print("\n\nAll components masses succesfully uploaded")
        else:
            print("These components have failed the upload test", failed_list)
    spinner.succeed("••• RETURN PROMPT •••")
    finished = input(f"{colour("PRESS ENTER TO RETURN TO MENU", Fore.YELLOW)}")
    if finished == "":
        os.system('cls' if os.name == 'nt' else 'clear')