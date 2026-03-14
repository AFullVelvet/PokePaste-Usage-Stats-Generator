from pokemon_formats import PokePaste
from pokemon_formats import Showdown
from collections import Counter
import pandas as pd
import numpy as np
import mega_dict


with open('Pastes.txt', 'r') as file:
    pastes = file.read().splitlines()


species_list = []
number_of_teams = 0
mode = 'mons'
#print(pokepaste_json[1]['species'])

#things to grab:


#species, item, ability, moves

#INITIAL ROLLOUT:

# grab each pokemon from a team


if mode == 'mons':
    for link in pastes:
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
elif mode == 'items':
    for link in pastes:
        pokepaste_json = PokePaste.retrieve_pokepaste(link)
        number_of_teams +=1
        for pokemon in pokepaste_json:
            species_list.append(pokemon['item'].strip())


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