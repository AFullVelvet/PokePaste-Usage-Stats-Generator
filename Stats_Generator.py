from pokemon_formats import PokePaste
from pokemon_formats import Showdown
from collections import Counter
import pandas as pd
import numpy as np
import mega_dict
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import requests


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

with open(file_path, 'r') as file:
    pastes = file.read().splitlines()



species_list = []
number_of_teams = 0
mode = 'mons'
#print(pokepaste_json[1]['species'])

#things to grab:


#species, item, ability, moves

#INITIAL ROLLOUT:

# grab each pokemon from a team

try :
    if mode == 'mons':
        for link in pastes:

            if 'pokepast.es' in link:
                pokepaste_json = PokePaste.retrieve_pokepaste(link)
                number_of_teams +=1
                for pokemon in pokepaste_json:
                    #check if item is mega stone (ends in ite)
                    if "ite" in pokemon['item']:
                        #Rule out eviolite and white herb
                        if pokemon['item'].strip() == "Eviolite":
                            species_list.append(pokemon['species'].strip())
                        elif pokemon['item'].strip() == "White Herb":
                            species_list.append(pokemon['species'].strip())

                        #call mega_dict function to see if match
                        else:
                            checked_name = mega_dict.mega_matcher(pokemon['item'].strip(),pokemon['species'].strip())
                            if checked_name != False:
                                species_list.append(checked_name.strip())
                            else:
                                species_list.append(pokemon['species'].strip())
                            
                            
                    #if string is returned, append that


                    # add to a list (Or some other way of tracking them)
                    else:
                        species_list.append(pokemon['species'].strip())
            
            # Code to handle new cobblemon pastes
            elif len(link) < 20 or 'cobblemon.tools' in link:
                if len(link) < 20:
                    response = requests.get('https://cobblemon.tools/api/v1/teams/' + link, headers = {"Content-Type": "application/json"})
                else:
                    team_id = link.removeprefix('https://cobblemon.tools/teams/')
                    response = requests.get('https://cobblemon.tools/api/v1/teams/' + team_id, headers = {"Content-Type": "application/json"})
                cobblemon_paste = response.json()
                number_of_teams +=1
                for pokemon in cobblemon_paste['team']:
                    #check if item is mega stone (ends in ite)
                    
                    #hacky workaround since everyhing has 10 characters at the start which are worthless
                    if "ite" in pokemon['item'][10:]:
                        #Rule out eviolite and white herb
                        if pokemon['item'][10:].capitalize().strip() == "Eviolite":
                            species_list.append(pokemon['species'][10:].capitalize().strip())
                        elif pokemon['item'][10:].capitalize().strip() == "White Herb":
                            species_list.append(pokemon['species'][10:].capitalize().strip())

                        #call mega_dict function to see if match
                        else:
                            checked_name = mega_dict.mega_matcher(pokemon['item'][10:].capitalize().strip(),pokemon['species'][10:].capitalize().strip())
                            if checked_name != False:
                                species_list.append(checked_name.strip())
                            else:
                                species_list.append(pokemon['species'][10:].capitalize().strip())
                            
                            
                    #if string is returned, append that


                    # add to a list (Or some other way of tracking them)
                    else:
                        species_list.append(pokemon['species'][10:].capitalize().strip())

    #only works for normal pokepastes, cobblemon pastes will probably act up
    elif mode == 'items':
        for link in pastes:
            pokepaste_json = PokePaste.retrieve_pokepaste(link)
            number_of_teams +=1
            for pokemon in pokepaste_json:
                species_list.append(pokemon['item'].strip())
except:
    messagebox.showerror(title = "Error", message = "This paste is bad:\n" + link + "\nIts on line " + str(number_of_teams + 1))

# grab all unqiue values in list
# find counts of each unique value
full_count = len(species_list)
totals = Counter(species_list)




# math????
# convert into dataframe

df = pd.DataFrame.from_dict(totals, orient='index')
df = df.rename(columns={'index':'Pokemon', 0:'Count'})
df = df.reset_index()
df = df.rename(columns={'index':'Pokemon'})
df = df.sort_values(['Count', "Pokemon"],ascending=False)

# add a column which calcs the percentage amount of each item
df["Percentage"] = df['Count'] / number_of_teams

#print(df)

df.to_csv("Usage_stats.csv", index=False)


# export dataframe into csv or smth