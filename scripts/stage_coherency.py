import os
from colorama import Fore
from collections import Counter

def stage_coherency(client, colour):
    serial_n = input("Serial number: ")
    if serial_n == "":
        print(colour("••• Empty serial number input, try again •••",Fore.RED))
    elif len(serial_n) > 14:
        print(colour("••• Invalid serial number, try again •••",Fore.RED))

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
        {"\n\t".join(combiner)}
            """)
        
        for x,y in combined_list:
            new_stage = next(iter(repeated_ys))
            if y != new_stage:
                choice = input(f"{colour("Would you like to force stage coherency? (Y/N): ",Fore.LIGHTBLUE_EX)}").strip().upper()
                if choice == "Y":
                    try:
                        stage_change = client.post("setComponentStage",
                                                json={
                                                    "component": str(x),
                                                    "stage": str(new_stage)
                                                })
                        print(colour(f"••• Stage change for {x} succesfully changed to {new_stage}",Fore.LIGHTCYAN_EX))
                    except Exception as e:
                        print(e)

        input(f"{colour("••• PRESS ENTER TO RETURN TO MAIN MENU •••",Fore.YELLOW)}")
        os.system("clear") 
    except Exception as e:
        print(e)