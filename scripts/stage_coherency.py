import os
from colorama import Fore
from collections import Counter
import json

def stage_coherency(client, colour):
    def stage_change(component, stage):
        try:
            stage_change = client.post("setComponentStage",
                                    json={
                                        "component": component,
                                        "stage": stage
                                    })
            print(colour(f"••• Stage change for {component} succesfully advanced to {stage}",Fore.LIGHTGREEN_EX))
        except Exception as e:
            print(e)

    while True:
        print(colour("(Optional) back --> Return to main menu", Fore.YELLOW))
        serial_n = input("Serial number: ")
        if serial_n == "":
            print(colour("••• Empty serial number input, try again •••",Fore.RED))
        elif len(serial_n) > 14:
            print(colour("••• Invalid serial number, try again •••",Fore.RED))
        elif serial_n == "back":
            os.system('clear')
            return

        try:
            response = client.get(
                "getComponent",
                json = {
                    "component": serial_n
                }
            )
            children_sn = [item['component']['serialNumber'] for item in response['children']]
            children_stage = [item['component']['currentStage']['code'] for item in response['children']]
            combined_list = list(zip(children_sn, children_stage))
            y_counts = Counter(y for x,y in combined_list)
            repeated_ys = {y for y,count in y_counts.items() if count >= 3}
            colour_coded = [(x, colour(y, Fore.GREEN) if y in repeated_ys else colour(y, Fore.RED)) for x, y in combined_list]
            combiner = [f"{x}               {y}" for x,y in colour_coded]
            print(f"""
            {colour(f"••• STAGE COHERENCY CHECK FOR {serial_n} •••", Fore.YELLOW)}

            {colour("CHILD SERIAL NUMBER",Fore.LIGHTCYAN_EX)}       │  {colour("CURRENT STAGE",Fore.LIGHTCYAN_EX)}
            ──────────────────────────│─────────────────────
            {"\n\t    ".join(combiner)}
                """)
            
            choice = input(f"{colour("Would you like to force stage coherency? (Y/N): ",Fore.LIGHTBLUE_EX)}").strip().upper()
            if choice == "Y":
                new_stage = "BAREMODULERECEPTION"
                if all(y == new_stage for x,y in combined_list):
                    print(colour("All components are at the right stage!", Fore.GREEN))
                    continue
                for x,y in combined_list:
                    if y != new_stage:
                        if "20UPGS" in x:
                            ordered_stages = ["sensor_manufacturer",
                                            "WAFER_PROCESSING",
                                            "BAREMODULEASSEMBLY",
                                            "BAREMODULERECEPTION",
                                            "MODULE/ASSEMBLY",
                                            "MODULE/WIREBONDING"]
                        elif "20UPGF" in x:
                            ordered_stages = ["TESTONWAFER",
                                            "BAREMODULEASSEMBLY",
                                            "BAREMODULERECEPTION",
                                            "MODULE/ASSEMBLY",
                                            "MODULE/WIREBONDING"]
                            
                        current_index = ordered_stages.index(y)
                        target_index = ordered_stages.index(new_stage)
                        if current_index > target_index:
                            stage_change(str(x), new_stage)
                        else:
                            for stage in ordered_stages[current_index + 1 : target_index + 1]:
                                stage_change(str(x), stage)
            else:
                input(f"{colour("••• PRESS ENTER TO RETURN TO MAIN MENU •••",Fore.YELLOW)}")
                os.system("clear")
                break

            yes_no = input(f"{colour("••• Would you like to stage check another component? (Y/N): ",Fore.YELLOW)}").strip().upper()
            if yes_no == "Y":
                continue
            else:
                input(f"{colour("••• PRESS ENTER TO RETURN TO MAIN MENU •••",Fore.YELLOW)}")
                os.system("clear")
                return
        except Exception as e:
            print(e)