import os
import itkdb
import getpass
from colorama import Fore, Style

# Import scripts
from scripts.alternative_ids import alternative_ids
from scripts.batch_components import batch_components
from scripts.mass_upload import mass_upload
from scripts.filter_jigs import filter_jigs
from scripts.visual_inspections import visual_inspections
from scripts.eos_imager import eos_imager
from scripts.stage_coherency import stage_coherency

DEBUG = False

def colour(text, c):
    # Text colouring function
    return f"{c}{text}{Style.RESET_ALL}"

if DEBUG == False:
    while True:
        print(f"{colour("••• ATLAS ITk PRODUCTION DATABASE LOGIN •••", Fore.LIGHTBLUE_EX)}")
        try:
            code1 = getpass.getpass("Enter passcode 1: ")
            code2 = getpass.getpass("Enter passcode 2: ")
            u = itkdb.core.User(access_code1=code1, access_code2=code2)
            client = itkdb.Client(user=u)
            client.user.authenticate()
            user = client.get('getUser', json={'userIdentity': client.user.identity})
            operator = f"{user['firstName']} {user['lastName']}"
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        except KeyboardInterrupt:
            print(f"{colour("••• Quitting the program •••", Fore.RED)}")
            exit()
        except Exception:
            print(f"{colour("••• ERROR: Invalid login credentials, please try again •••", Fore.RED)}")
            continue

def welcome():
    # Welcome Page
    content = f"••• CURRENT USER: {operator}"
    width = 42
    padded = content.ljust(width)

    print(f"""
          
            ╔{"═" * (width + 2)}╗
            ║ {colour(padded, Fore.LIGHTGREEN_EX)} ║
            ╚{"═" * (width + 2)}╝
            ╭──────────────────────────────────────────────────────────────╮
            │      ◈◈◈◈ {colour("Welcome to ITk Quick Production Services", Fore.CYAN):<25} ◈◈◈◈      │
            │                                                              │
            │ {colour("Choose your service:", Fore.CYAN):<60}          │
            │                                                              │
            │ •A → Set alternative IDs for the components (.csv required)  │
            │ •B → Fetch and output specific batch components              │
            │ •C → Upload component masses in a batch (.csv required)      │
            │ •D → Search pixel module components by tool IDs              │
            │ •E → Upload component VI in a batch (.csv required)          │
            │ •F → Search component stored images status                   │
            │ •G → Stage coherency (Only for bare modules)                 │  
            │                                                              │
            │ {colour("exit", Fore.LIGHTRED_EX)} → Quit the program{"":<34}    │
            │                                                              │
            ╰──────────────────────────────────────────────────────────────╯
            """)
    choose_input = input("•Choice: ")
    if choose_input != "exit":
        return choose_input.strip().upper()
    else:
        return choose_input.strip()

def main():
    while True:
        service_input = welcome()
        match service_input:
            case "A":
                alternative_ids(client, colour)
            case "B":
                batch_components(client, colour)
            case "C":
                mass_upload(client, colour)
            case "D":
                filter_jigs(client, colour)
            case "E":
                visual_inspections(client, colour)
            case "F":
                eos_imager(client, colour)
            case "G":
                stage_coherency(client, colour)
            case "exit":
                break
            case "EXIT":
                break
            case "":
                os.system("clear")
                continue

if __name__ == "__main__":
    main()
