import os
from colorama import Fore
import csv
from halo import Halo
from datetime import datetime, timezone

def visual_inspections(client, colour):
    print(f"{colour("(Optional) back --> return to home menu", Fore.YELLOW)}")
    file_path = input("CSV directory: ")

    if file_path == "back":
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    if file_path == "":
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{colour("••• ERROR: Empty CSV directory, try again •••", Fore.LIGHTRED_EX)}")
        return
    
    component_type = input("\nComponent type: \n\tA--> Bare Module\n\tB--> PCB Flex\n\tC --> Back to Menu\n\n\tChoice: ").strip().upper()

    if component_type == "C":
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
                if component_type == "A":
                    if component['componentType']['code'] != "BARE_MODULE":
                        print("The component do not correspond to bare module, please try again.")
                        break
                    if len(row) < 4:
                        print(f"The rows for {row[0]} component are incomplete, skipping...")
                        skipped_list.append(row[0])
                        continue  
                    if component['currentStage']['code'] != "BAREMODULERECEPTION":
                        spinner = Halo(text=f"{component['code']} needs a stage change, commencing now >>>", spinner='earth')
                        spinner.start()
                        new_stage = client.post('setComponentStage',
                                                json={"component": component['code'],
                                                      "stage": "BAREMODULERECEPTION"})
                        spinner.succeed(f"Stage for {row[0]} changed succesfully!")
                    else:
                        print("Correct stage for VI upload")
                    # Now to upload the VI test run
                    test_json = {
                          "component": row[0],
                          "testType": "VISUAL_INSPECTION",
                          "institution": "LIV",
                          "runNumber": "1",
                          "date": iso_time,
                          "passed": True,
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
                    test_upload = client.post('uploadTestRunResults', json=test_json)
                    print(f"Visual inspection for {row[0]} has been succesfully uploaded")
                else:
                    if component['componentType']['code'] != "PCB":
                        print("The component does not correspond to PCB, please try again")
                        break
                    if len(row) < 15:
                        print(f"The rows for {row[0]} component are incomplete, skipping...")
                        skipped_list.append(row[0])
                        continue  
                    if component['currentStage']['code'] != "PCB_RECEPTION_MODULE_SITE":
                        spinner = Halo(text=f"{component['code']} needs a stage change, commencing now >>>", spinner='earth')
                        spinner.start()
                        new_stage = client.post('setComponentStage',
                                                json={"component": component['code'],
                                                      "stage": "PCB_RECEPTION_MODULE_SITE"})
                        spinner.succeed(f"Stage for {row[0]} changed succesfully!")
                    else:
                        print("Correct stage for VI upload")

                    test_json = {
                      "component": row[0],
                      "testType": "VISUAL_INSPECTION",
                      "institution": "LIV",
                      "runNumber": "1",
                      "date": iso_time,
                      "passed": True,
                      "problems": False,
                      "properties": {
                        "OPERATOR": "Andy Bukowski",
                        "INSTRUMENT": "Epson V850",
                        "ANALYSIS_VERSION": None
                      },
                      "results": {
                        "WIREBOND_PADS_CONTAMINATION_GRADE": row[1],
                        "PARTICULATE_CONTAMINATION_GRADE": row[2],
                        "WATERMARKS_GRADE": row[3],
                        "SCRATCHES_GRADE": row[4],
                        "TRACES_GRADE": row[5],
                        "SOLDERMASK_IRREGULARITIES_GRADE": row[6],
                        "HV_LV_CONNECTOR_ASSEMBLY_GRADE": row[7],
                        "DATA_CONNECTOR_ASSEMBLY_GRADE": row[8],
                        "SOLDER_SPILLS_GRADE": row[9],
                        "COMPONENT_MISALIGNMENT_GRADE": row[10],
                        "SHORTS_OR_CLOSE_PROXIMITY_GRADE": row[11],
                        "OPENS_TOMBSTONING_GRADE": row[12],
                        "OVERALL_GRADE": row[13],
                        "OBSERVATION": row[14]
                      }
                    }
                    test_upload = client.post('uploadTestRunResults', json=test_json)
                    print(f"Visual inspection for {row[0]} has been succesfully uploaded")
            except Exception as e:
                print(e)
    finished = input(f"{colour("PRESS ENTER TO RETURN TO MENU", Fore.YELLOW)}")
    if finished == "":
        os.system('cls' if os.name == 'nt' else 'clear')