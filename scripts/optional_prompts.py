from colorama import Fore

def defects_list(colour):
    defetcts = print(f"""
        
        {colour("List of defects for bare and assembled module VI", Fore.LIGHTYELLOW_EX)}
        
        0 - no defect
        1 - Sensor systematic rough edge or dicing effect
        2 - Sensor tooling marks
        3 - Sensor scratch (random)
        4 - Sensor dot-like contamination
        5 - Sensor chipped corner
        6 - FE chip chipped outer corner
        7 - FE chip bond pad contamination
        8 - FE chip irregular dicing
        9 - FE chip scratch on back side
        10 - FE chip scratch on top side (pad side)
        11 - FE chip chipper inner corner
        12 - FE chip excess material (not diced near FE border)
        13 - Other defect

               """)
    
    return defetcts

def example_csv(colour):
    examples = print(f"""
                .CSV file for visual inspections
                                     
                {colour("BARE MODULES", Fore.LIGHTBLUE_EX)}
        A - Defects - They go from 0 to 13 and they are often stacked together
            e.g 0,1 and 8 would be 018
        B - Sensor condition (1 -> Good, 2 -> Issues, 3 -> Bad)
        C - Front-end (FE) chips condition (1 -> Good, 2 -> Issues, 3 -> Bad)

        ╔══════════════════════════════════════════════════════════╗
        ║                                                          ║
        ║     Row 1 -->  20UPGBXXXXXXXX,Pass,A,B,C                 ║
        ║                20UPGBXXXXXXXX,Fail,A,B,C  <-- Row 2      ║
        ║                20UPGBXXXXXXXX,Pass,A,B,C                 ║
        ║                ...                                       ║
        ║                                                          ║
        ╚══════════════════════════════════════════════════════════╝

        {colour("* Only one type of component per .csv file, do not mix types!", Fore.LIGHTRED_EX)}


                {colour("HYBRID PCB FLEXES", Fore.LIGHTGREEN_EX)}
        {colour("All criteria are graded 1-3 (1 -> Good, 2 -> Issues, 3 -> Bad) except the comments", Fore.LIGHTMAGENTA_EX)}
        A - Wirebond pads clear of contamination, discolouring, spills, deposits, particles, 
            etc that can cause issues with wirebonding
        B - Particulate contamination on the PCB including pick-up points
        C - Watermarks on the PCB
        D - Scratches on the wirebonding pads and the PCD that can cause issues
            with wirebonding and/or electrical functionality of the PCB
        E - Issues seen on traces like spurious copper, spur, mousebit, pin hole,
            short, breakout etc. that reduce/cut the copper traces width
        F - Soldermask irregularity/cracks grade
        G - HV LV connector assembly issue
        H - Data connector assembly issue
        I - Solder spills as part of assembly process on wirebonding pads
        J - Component misalignment
        K - Shorts/close proximity of components due to misalignment
        L - Opens or tombstoning, where one end of the component lifts 
            from a pad of the PCB during the soldering process
        M - Overall grade (scale 1-3)
        N - Observations (comment)

        ╔══════════════════════════════════════════════════════════════════════╗
        ║                                                                      ║
        ║  Row 1 ->  20UPGPQXXXXXXX,Pass,A,B,C,D,E,F,G,H,I,J,K,L,M,N           ║
        ║            20UPGPQXXXXXXX,Fail,A,B,C,D,E,F,G,H,I,J,K,L,M,N           ║
        ║            20UPGPQXXXXXXX,Pass,A,B,C,D,E,F,G,H,I,J,K,L,M,N <- Row 3  ║
        ║            ...                                                       ║
        ║                                                                      ║
        ╚══════════════════════════════════════════════════════════════════════╝

                {colour("ASSEMBLED MODULES", Fore.LIGHTGREEN_EX)}
        A - Defects - They go from 0 to 13 and they are often stacked together
            e.g 0,1 and 8 would be 018
        
        Grading criteria: (1 -> Good, 2 -> Issues, 3 -> Bad)
        B - SMD components condition
        C - Sensor condition 
        D - Front-end (FE) chips condition 
        E - Glue distribution 
        F - Observations (comment)

        ╔══════════════════════════════════════════════════════════╗
        ║                                                          ║
        ║  Row 1 ->  20UPGMXXXXXXXX,Pass,A,B,C,D,E,F               ║
        ║            20UPGMXXXXXXXX,Fail,A,B,C,D,E,F               ║
        ║            20UPGMXXXXXXXX,Pass,A,B,C,D,E,F  <- Row 3     ║
        ║            ...                                           ║
        ║                                                          ║
        ╚══════════════════════════════════════════════════════════╝

               """)
    
    return examples

# Stage dictionaries
assembled_list = [
    "MODULE/INIT",
    "MODULE/ASSEMBLY",
    "MODULE/WIREBONDING",
    "MODULE/INITIAL_WARM",
    "MODULE/INITIAL_COLD",
    "MODULE/PARYLENE_MASKING",
    "MODULE/PARYLENE_COATING",
    "MODULE/PARYLENE_UNMASKING",
    "MODULE/POST_PARYLENE_WARM",
    "MODULE/POST_PARYLENE_COLD"
]

bare_list = [
    "BAREMODULEASSEMBLY",
    "BAREMODULERECEPTION",
    "MODULE/ASSEMBLY",
    "MODULE/WIREBONDING",
    "MODULE/INITIAL_WARM",
    "MODULE/INITIAL_COLD",
    "MODULE/PARYLENE_UNMASKING",
    "MODULE/POST_PARYLENE_WARM",
    "MODULE/POST_PARYLENE_COLD"
]

flex_list = [
    "PCB_INIT",
    "PCB_RECEPTION",
    "PCB_BEING_POPULATED",
    "PCB_POPULATION",
    "PCB_QC",
    "PCB_POPULATION",
    "PCB_READY_FOR_MODULE",
    "PCB_RECEPTION_MODULE_SITE",
    "COMPLETE",
    "MODULE/ASSEMBLY",
    "MODULE/WIREBONDING",
    "MODULE/INITIAL_WARM",
    "MODULE/INITIAL_COLD",
    "MODULE/PARYLENE_UNMASKING",
    "MODULE/POST_PARYLENE_WARM",
    "MODULE/POST_PARYLENE_COLD",
]