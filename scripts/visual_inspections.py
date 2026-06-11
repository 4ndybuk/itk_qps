import os
from colorama import Fore
from scripts.optional_prompts import defects_list, example_csv, assembled_list, bare_list, flex_list
from datetime import datetime, timezone
from halo import Halo
import csv

def stage_check(row, client, colour, stage, stage_list, component, test_json):
    # Stage check for either stage change or retroactive upload
    current = component['currentStage']['code']
    if stage_list.index(current) < stage_list.index(stage):
        if os.name != 'nt':
            spinner = Halo(text=f"{component['code']} needs a stage change, commencing now >>>", spinner='earth')
            spinner.start()
            new_stage = client.post('setComponentStage',
                                json={"component": component['code'],
                                      "stage": stage})
            spinner.succeed(f"Stage for {row[0]} changed succesfully!")    
        else:
            print(colour(f"{component['code']} needs a stage change, commencing now >>>", Fore.YELLOW))
            new_stage = client.post('setComponentStage',
                                json={"component": component['code'],
                                        "stage": stage})
            print(colour(f"Stage for {row[0]} changed succesfully!", Fore.GREEN))
    else:
        print(colour(f"{component['code']} needs a retroactive upload, commencing now >>>"))
        test_json["stage"] = stage
        test_json["isRetroactive"] = True

def visual_inspections(client, colour):
    # Retrieve logged user's name
    user = client.get('getUser', json={'userIdentity': client.user.identity})
    operator = f"{user['firstName']} {user['lastName']}"

    while True:
        print(f"""
        {colour("(Optional) back --> return to home menu", Fore.YELLOW)}
        {colour("(Optional) show --> show example .csv file", Fore.LIGHTBLUE_EX)}
        {colour("(Optional) defects --> show list of defects for VI upload", Fore.LIGHTBLUE_EX)}
        """)
        file_path = input("CSV directory: ")

        if file_path == "defects":
            os.system("cls" if os.name == 'nt' else "clear")
            defects = defects_list(colour)
            continue

        if file_path == "show":
            os.system("cls" if os.name == 'nt' else "clear")
            examples = example_csv(colour)
            continue

        if file_path == "back":
            os.system('cls' if os.name == 'nt' else 'clear')
            return

        if file_path == "":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{colour("••• ERROR: Empty CSV directory, try again •••", Fore.LIGHTRED_EX)}")
            return
        
        if ".csv" in file_path:
            break
    
    component_type = input(f"""
        Component type:
        {colour("A --> PCB Flex", Fore.CYAN)}
        {colour("B --> Bare Module", Fore.LIGHTGREEN_EX)}
        {colour("C --> Assembled Module", Fore.LIGHTYELLOW_EX)}
        {colour("back --> Back to Menu", Fore.YELLOW)}
        
        Choice: """).strip().upper()
    
    if component_type == "BACK":
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    if component_type == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: Empty component type input, try again •••", Fore.LIGHTRED_EX)}")
        return

    skipped_list = []
    with open(file_path, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:    
            try:
                now_utc = datetime.now(timezone.utc)
                iso_time = now_utc.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
                component = client.get('getComponent',json={"component": row[0],"alternativeIdentifier": False})

                # Pass/Fail criteria
                if row[1] == "Pass":
                    row[1] = True
                elif row[1] == "Fail":
                    row[1] = False
                else:
                    os.system("cls" if os.name == 'nt' else "clear")
                    print(colour("••• ERROR: Incorrect Pass/Fail input in the .CSV file, please check!"))
                    return

                if component_type == "B":
                    if component['componentType']['code'] != "BARE_MODULE":
                        print("The component do not correspond to bare module, please try again.")
                        break

                    if len(row) < 4:
                        print(f"The rows for {row[0]} component are incomplete, skipping...")
                        skipped_list.append(row[0])
                        continue

                    # Verify input values
                    if int(row[3]) not in [1,2,3] or int(row[4]) not in [1,2,3]:
                        print(colour("Incorrect input type (integers between 1 and 3 only), skipping...", Fore.RED))
                        skipped_list.append(row[0])
                        continue

                    # Now to upload the VI test run
                    test_json = {
                          "component": row[0],
                          "testType": "VISUAL_INSPECTION",
                          "institution": "LIV",
                          "runNumber": "1",
                          "date": iso_time,
                          "passed": row[1],
                          "problems": False,
                          "properties": {
                            "ANALYSIS_VERSION": None,
                            "MEASUREMENT_DATE": iso_time
                          },
                          "results": {
                            "DEFECTS": row[2],
                            "SMD_COMPONENTS_PASSED_QC": None,
                            "SENSOR_CONDITION_PASSED_QC": row[3],
                            "FE_CHIP_CONDITION_PASSED_QC": row[4],
                            "GLUE_DISTRIBUTION_PASSED_QC": None,
                            "WIREBONDING_PASSED_QC": None,
                            "PARYLENE_COATING_PASSED_QC": None,
                            "OBWBP_ASSEMBLY_PASSED_QC": None,
                            "STRAIN_RELIEF_PASSED_QC": None
                          }
                        }
                    
                    # Stage check
                    stage = "BAREMODULERECEPTION"
                    if component['currentStage']['code'] != stage:
                        stage_check(row, client, colour, stage, bare_list, component, test_json)
                    else:
                        print("Correct stage for VI upload")
                    test_upload = client.post('uploadTestRunResults', json=test_json)
                    print(f"Visual inspection for {row[0]} has been succesfully uploaded")
                    
                elif component_type == "A":
                    if component['componentType']['code'] != "PCB":
                        print("The component does not correspond to PCB, please try again")
                        break

                    if len(row) < 15:
                        print(f"The rows for {row[0]} component are incomplete, skipping...")
                        skipped_list.append(row[0])
                        continue
                    
                    if not all(int(x) in [1, 2, 3] for x in row[2:14]):
                        print(colour("Incorrect input type (integers between 1 and 3 only), skipping...", Fore.RED))
                        skipped_list.append(row[0])
                        continue

                    test_json = {
                      "component": row[0],
                      "testType": "VISUAL_INSPECTION",
                      "institution": "LIV",
                      "runNumber": "1",
                      "date": iso_time,
                      "passed": row[1],
                      "problems": False,
                      "properties": {
                        "OPERATOR": operator,
                        "INSTRUMENT": "Epson V850",
                        "ANALYSIS_VERSION": None
                      },
                      "results": {
                        "WIREBOND_PADS_CONTAMINATION_GRADE": row[2],
                        "PARTICULATE_CONTAMINATION_GRADE": row[3],
                        "WATERMARKS_GRADE": row[4],
                        "SCRATCHES_GRADE": row[5],
                        "TRACES_GRADE": row[6],
                        "SOLDERMASK_IRREGULARITIES_GRADE": row[7],
                        "HV_LV_CONNECTOR_ASSEMBLY_GRADE": row[8],
                        "DATA_CONNECTOR_ASSEMBLY_GRADE": row[9],
                        "SOLDER_SPILLS_GRADE": row[10],
                        "COMPONENT_MISALIGNMENT_GRADE": row[11],
                        "SHORTS_OR_CLOSE_PROXIMITY_GRADE": row[12],
                        "OPENS_TOMBSTONING_GRADE": row[13],
                        "OVERALL_GRADE": row[14],
                        "OBSERVATION": row[15]
                      }
                    }

                    # Stage check
                    stage = "PCB_RECEPTION_MODULE_SITE"
                    if component['currentStage']['code'] != stage:
                        stage_check(row, client, colour, stage, flex_list, component, test_json)
                    else:
                        print("Correct stage for VI upload")
                    test_upload = client.post('uploadTestRunResults', json=test_json)
                    print(f"Visual inspection for {row[0]} has been succesfully uploaded")

                elif component_type == "C":
                    if component['componentType']['code'] != "MODULE":
                        print("The component does not correspond to assembled module, please try again")
                        break

                    if len(row) < 8:
                        print(f"The rows for {row[0]} component are incomplete, skipping...")
                        skipped_list.append(row[0])
                        continue
                    
                    if not all(int(x) in [1, 2, 3] for x in row[3:6]):
                        print(colour("Incorrect input type (integers between 1 and 3 only), skipping...", Fore.RED))
                        skipped_list.append(row[0])
                        continue

                    test_json = {
                        "component": row[0],
                        "testType": "VISUAL_INSPECTION",
                        "institution": "LIV",
                        "runNumber": "1",
                        "date": iso_time,
                        "passed": row[1],
                        "problems": False,
                        "properties": {
                            "ANALYSIS_VERSION": None,
                            "MEASUREMENT_DATE": iso_time,
                            "MEASUREMENT_DURATION": None
                        },
                        "results": {
                            "DEFECTS": row[2],
                            "SMD_COMPONENTS_PASSED_QC": row[3],
                            "SENSOR_CONDITION_PASSED_QC": row[4],
                            "FE_CHIP_CONDITION_PASSED_QC": row[5],
                            "GLUE_DISTRIBUTION_PASSED_QC": row[6],
                            "WIREBONDING_PASSED_QC": None,
                            "PARYLENE_COATING_PASSED_QC": None,
                            "OBWBP_ASSEMBLY_PASSED_QC": None,
                            "STREIN_RELIEF_PASSED_QC": None,
                            "OBSERVATION": row[7]
                        }
                        }
                    
                    stage = "MODULE/ASSEMBLY"
                    if component['currentStage']['code'] != stage:
                        stage_check(row, client, colour, stage, assembled_list, component, test_json)
                    else:
                        print("Correct stage for VI upload")
                    test_upload = client.post('uploadTestRunResults', json=test_json)
                    print(f"Visual inspection for {row[0]} has been succesfully uploaded")
            except Exception as e:
                print(e)
    print(colour(f"Skipped components\n\t{skipped_list}", Fore.RED))
    finished = input(f"{colour("PRESS ENTER TO RETURN TO MENU", Fore.YELLOW)}")
    if finished == "":
        os.system('cls' if os.name == 'nt' else 'clear')