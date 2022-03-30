import os
import time
import datetime as dt
modpacks_folder = "_Modpacks_"


## Actions ##

# Save Modpack
def save_modpack(user_input) :
    
    if user_input :
        print("\n  Currently Enabled Mods:\n")

    enabled_mods = []
    for mod in mod_list :

        mod_name = mod[0]
        disabled = mod[1]
        
        if disabled == False :

            enabled_mods.append(mod_name)
            if user_input :
                print(mod_name)
    
    name = ""
    if user_input :
        name = input("\n  Modpack Name: ")
    if not name :
        name = "Backups/"+str(dt.datetime.now()).split(".")[0].replace(":","-")

    with open(f"{modpacks_folder}/{name}.txt", "w") as f:
        
        for mod_name in enabled_mods :
            f.write(f"{mod_name}\n")

# Load Modpack
def load_modpack(user_input) :

    if user_input :

        name = input("\n  Modpack Name: ")
        keep_enabled = False
        if input("  Disable Currently Enabled Mods? (y/n) ") == "n" :
            keep_enabled = True
    
        with open(f"{modpacks_folder}/{name}.txt", "r") as f:
        
            modpack = f.read().split("\n")     
    else :
        modpack = []
        keep_enabled = False
    
    # Generate backup before loading modpack
    save_modpack(False)

    for mod in mod_list :
        
        mod_name = mod[0]
        disabled = mod[1]

        if mod_name in modpack and disabled :
            os.remove(f"mods/{mod_name}/disable.it")

        elif not mod_name in modpack and not disabled and not keep_enabled :
            try :
                with open(f"mods/{mod_name}/disable.it","a") as f:
                    pass
            except :
                pass

# Edit Mods
def edit_mods() :

    for mod in mod_list :
        
        mod_name = mod[0]
        disabled = mod[1]
        id = mod[2]

        status = "Enabled"
        if disabled :
            status = "Disabled"

        print(f"{id} - {mod_name} - {status}")
    
    while True :

        id = input("\n  Mod Editing Id: ")

        if id == "" :
            break
        else :
            id = int(id)
        
        mod_name = mod_list[id][0]
        disabled = mod_list[id][1]

        new_status = "Disable"
        if disabled :
            new_status = "Enable"
        
        if not input(f"  {new_status} {mod_name}? (y/n) ") == "n" :

            mod_list[id][1] = not disabled
            
            if disabled :
                os.remove(f"mods/{mod_name}/disable.it")
            else :
                with open(f"mods/{mod_name}/disable.it","a") as f:
                    pass
            
            print(f"\n{new_status}d {mod_name}")






print("\n  Thank you for using Isaac Modpack Saver by RoarkCats!")


# Generate folders
print("\n  Generating folders...")

try :
    os.makedirs(f"{modpacks_folder}/Backups/")
except :
    pass

while True :

    # Index files
    print("  Indexing files...\n")

    if not os.path.isdir("mods") :
        print("  Error: Unable to find \"mods\" folder!\n")
        print("Exiting...")
        time.sleep(3)
        exit()

    mod_list = []
    id = 0
    for folder in os.listdir("mods") :

        if os.path.isdir(f"mods/{folder}") :

            is_mod = False
            disabled = False
            for file in os.listdir(f"mods/{folder}") :

                if file == "metadata.xml" :
                    is_mod = True

                if file == "disable.it" :
                    disabled = True

            if is_mod :
                mod_list.append([folder,disabled,id])
                id += 1

    modpack_list = []
    for file in os.listdir(f"{modpacks_folder}") :

        if file.lower().endswith(".txt") :

            modpack_list += file
            print(file.split(".txt")[0])


    # Ask what action the user would like to take
    action = input("\n  ▪ Choose Action: - Save Modpack (s) - Load Modpack (l) - Disable All Mods (d) - Edit Mods Enabled (e) - Exit (x)  ").lower()

    # Do action
    match action :
        case "s" :
            save_modpack(True)
        case "l" :
            load_modpack(True)
        case "d" :
            load_modpack(False)
        case "e" :
            print()
            edit_mods()
        case "x" :
            print("\nExiting...")
            time.sleep(0.75)
            exit()
        case _ :
            action = "no done"

    if not action == "no done" :
        print("\nDone!\n")
    else :
        print()