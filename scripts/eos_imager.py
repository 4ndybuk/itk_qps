import os
from colorama import Fore
import csv

def eos_imager(client, colour):
    # Retrieve information about images per visual inspection
    def component_images(response: str, stage: str):
            tests = client.get(
                    "listTestRunsByComponent",
                    json={
                        "filterMap": {
                            "serialNumber": response,
                            "testType": ["VISUAL_INSPECTION"],
                            "stage": [stage],
                            "state": ["ready"]
                        }
                    }
                )
            try:
                id_ = tests.data[0]['id']
                test = client.get("getTestRun", json = {"testRun": id_})
                values = [element['title'] for element in test['attachments']]
                return values
            except AttributeError:
                return []

    def retrieve_image_info(response):
            
        def pull_data(boole):
            # Component pull from production database
            data = client.get("getComponent", json={"component": response,
                                                     "alternativeIdentifier": boole})
            return data
        
        if any(x in response for x in ["LIV", "OX", "GLA"]):
            component = pull_data(True)
        else:
            component = pull_data(False)

        def get_stage(serial):
            # Retrieve component current stage
            get_component = client.get("getComponent", json={"component": serial})
            component_stage = get_component['currentStage']['code']
            return component_stage
        
        def check_component(info, index):
            # Check component contents to output
            if len(info) >= 1:
                return info[index]
            else:
                return []
        
        if component['type']['code'] == "OUTER_SYSTEM_QUAD_MODULE":
            # Only for modules
            children_sn = [element['component']['serialNumber'] for element in component['children'] if element['component'] is not None]

            module_reception = component_images(component['serialNumber'], "MODULE/ASSEMBLY")
            module_wire = component_images(component['serialNumber'], "MODULE/WIREBONDING")
            module_masking = component_images(component['serialNumber'], "MODULE/PARYLENE_MASKING")
            module_unmasking = component_images(component['serialNumber'], "MODULE/PARYLENE_UNMASKING")

            # Extract subcomponent strings
            child_flex = [serial for serial in children_sn if '20UPGPQ' in serial][0]
            child_bare = [serial for serial in children_sn if '20UPGB' in serial][0]

            flex_reception = component_images(str(child_flex), "PCB_RECEPTION_MODULE_SITE")
            bare_reception = component_images(str(child_bare), "BAREMODULERECEPTION")

            print(f"""
            ---------------------------------------------------------
                  
            {colour("IMAGE UPLOAD STATUS FOR MODULE", Fore.CYAN)} {colour(component['serialNumber'], Fore.YELLOW)}:

                {colour("• MODULE VI", Fore.GREEN)} --> Total images: {colour(len(module_reception), Fore.WHITE)}
                    - Image: {colour(check_component(module_reception, 0) , Fore.LIGHTCYAN_EX)}
                    - Image: {colour(check_component(module_reception, 1) , Fore.LIGHTCYAN_EX)}

                {colour("• MODULE VI WIREBONDING", Fore.MAGENTA)} --> Total images: {colour(len(module_wire), Fore.WHITE)}
                    - Image: {colour(check_component(module_wire, 0), Fore.LIGHTCYAN_EX)}

                {colour("• MODULE VI MASKING", Fore.BLUE)} --> Total images: {colour(len(module_masking), Fore.WHITE)}
                    - Image: {colour(check_component(module_masking, 0), Fore.LIGHTCYAN_EX)}
                    - Image: {colour(check_component(module_masking, 1), Fore.LIGHTCYAN_EX)}

                {colour("• MODULE VI UNMASKING", Fore.RED)} --> Total images: {colour(len(module_unmasking), Fore.WHITE)}
                    - Image: {colour(check_component(module_unmasking, 0), Fore.LIGHTCYAN_EX)}
                    - Image: {colour(check_component(module_unmasking, 1), Fore.LIGHTCYAN_EX)}

                {colour("SUB-COMPONENTS:", Fore.CYAN)}

                {colour("• MODULE FLEX", Fore.GREEN)} -> {colour(child_flex, Fore.YELLOW)} - Total images: {colour(len(flex_reception), Fore.WHITE)}
                    - Image: {colour(check_component(flex_reception, 0), Fore.LIGHTCYAN_EX)}
                    - Image: {colour(check_component(flex_reception, 1), Fore.LIGHTCYAN_EX)}

                {colour("• BARE MODULE", Fore.GREEN)} -> {colour(child_bare, Fore.YELLOW)} - Total images: {colour(len(bare_reception), Fore.WHITE)}
                    - Image: {colour(check_component(bare_reception, 0), Fore.LIGHTCYAN_EX)}
                    - Image: {colour(check_component(bare_reception, 1), Fore.LIGHTCYAN_EX)}

            {colour("----------------------------------------------------------", Fore.LIGHTBLACK_EX)}
                """)
        else:
            if component['type']['code'] == "QUAD_PCB":
                component_reception = component_images(component['serialNumber'], "PCB_RECEPTION_MODULE_SITE")
            else:
                component_reception = component_images(component['serialNumber'], "BAREMODULERECEPTION")

            print(f"""
            {colour("---------------------------------------------------------", Fore.LIGHTBLACK_EX)}

            {colour("IMAGE UPLOAD STATUS FOR PIXEL COMPONENT", Fore.CYAN)} {colour(component['serialNumber'], Fore.YELLOW)}:

            {colour("• COMPONENT VI AT RECEPTION", Fore.GREEN)} --> Total images: {colour(len(component_reception), Fore.WHITE)}
            {colour("• IMAGES INFO:", Fore.CYAN)}
                - Image: {colour(check_component(component_reception, 0), Fore.LIGHTCYAN_EX)}
                - Image: {colour(check_component(component_reception, 1), Fore.LIGHTCYAN_EX)}

            {colour("---------------------------------------------------------", Fore.LIGHTBLACK_EX)}
                   """)
    # Run the function 
    while True:
        print(f"""
            Would you like to input a single entry or a list?
              
            Option A --> Single entry (single input)
            Option B --> List entry (.csv list)
            {colour("Option C --> Return to Home", Fore.YELLOW)}
              
              """)
        response = input("Choice: ").strip().upper()
        if response == "C":
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        
        if response == "":
            print(f"{colour("••• ERROR: Empty input, please try again •••", Fore.LIGHTRED_EX)}")
            continue

        if response == "A":
            serial_n = input("Component ID (Serial Number / Alternative ID): ")
            if serial_n == "":
                print(f"{colour("••• ERROR: Empty input, please try again •••", Fore.LIGHTRED_EX)}")
                continue

            if len(serial_n) > 15:
                print(f"{colour("••• ERROR: Invalid serial number, please try again •••", Fore.LIGHTRED_EX)}")
                continue
            try:
                retrieve_image_info(serial_n)
            except Exception as e:
                print(e)
                print(f"Could not check component {serial_n}, please check it in the database") 
        
        elif response == "B":
            file_name = input("File directory: ")
            if file_name == "":
                print(f"{colour("••• ERROR: Empty input, please try again •••", Fore.LIGHTRED_EX)}")
                continue
            elif ".csv" not in file_name:
                print(f"{colour("••• ERROR: File name must end with .csv, please try again •••", Fore.LIGHTRED_EX)}")
                continue

            with open(file_name, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                   try:
                    retrieve_image_info(row[0])
                   except Exception as e:
                     print(e)
                     print(f"Could not check component {row[0]}, please check it in the database first")
                     continue

        else:
            print(f"{colour("••• ERROR: Invalid chosen option, please try again •••", Fore.LIGHTRED_EX)}")
            continue

        choice = input("Try another one? (Y/N): ").strip().upper()
        if choice != "Y":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
