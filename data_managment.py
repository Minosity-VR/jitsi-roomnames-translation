####################################################################################################
####################################################################################################

from os import listdir, mkdir
from os.path import isfile, join

import json


####################################################################################################
####################################################################################################

def extract_data_lists_from_json(data_folder):
    """Extract Json lists from data files, and return it in Python list

    Args:
        data_folder (string):   Folder containing Json lists of words, stored in files
                                named <type>.en.json

    Returns:
        dict: {
            '<type1>': String[],
            '<type2>': String[],
            '<type3>': String[],
            ...
        }   
    """
    data_files = [f for f in listdir(data_folder) if isfile(join(data_folder, f))]

    words = {}

    for data_file in data_files:
        with open(f"{data_folder}/{data_file}", "r") as data:
            words[data_file.split(".")[0]] = json.load(data)
    
    return words


####################################################################################################
####################################################################################################

def write_fo_file(output_folder, language_OSI_code, type_name, type_data):
    """Write a Python object (in our case a list) to a JSON file

    Args:
        output_folder (string): Destination folder path
        language_OSI_code (string): OSI code for language (en, fr, es...)
        type_name (string): Type of words writed (adjectives, versb...)
        type_data (list): List of words to write to JSOn
    """
    # Create output folder (usually data_<language_OSI_code>)
    try:
        mkdir(output_folder)
    except FileExistsError:
        pass

    # Write python list to file as JSON list
    with open(f"{output_folder}/{type_name}.{language_OSI_code}.json", "w") as outfile:
        outfile.write(json.dumps(type_data, indent=4))


####################################################################################################
####################################################################################################

if __name__ == "__main__":
    test_number = -1

    ##################################################
    if test_number == 0:
        data_folder = './data_fr'
        jitsi_words = extract_data_lists_from_json(data_folder)
        fruits = jitsi_words["fruits"]
        for i in range(len(fruits)):
            fruits[i] = fruits[i].capitalize()

        fruits = sorted(list(dict.fromkeys(fruits)))

        write_fo_file('./data_fr', 'fr', 'animal', fruits)
    
    ##################################################
    if test_number == 1:
        words = []
        with open('./backup/pluralnouns.fr.json.bak', 'r') as data:
            words = json.load(data)
    
        words = sorted(list(dict.fromkeys(words)))

        with open('./backup/pluralnouns.fr.json', 'w') as outfile:
            outfile.write(json.dumps(words, indent=4))
