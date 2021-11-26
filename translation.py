####################################################################################################
####################################################################################################

from google.cloud import translate_v2 as translate
from data_managment import extract_data_lists_from_json, write_fo_file

import six


####################################################################################################
####################################################################################################

def translate_data(CATEGORIE, language_OSI_code):
    """Translates into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages

    You need a JSON Google-cloud-translate API key to launch the requests.
    Get one in Google Cloud platform, then do the following command:
    export GOOGLE_APPLICATION_CREDENTIALS='/path/to/the/json/key'

    Args:
        CATEGORIE           (List)      : List of words to be translated
        language_OSI_code   (string)    : Language to translate to (en, fr, es...)

    Returns:
        List: List of translated words
    """
    translate_client = translate.Client()
    translated_words = []
        
    for word in CATEGORIE:
        if isinstance(word, six.binary_type):
            word = word.decode("utf-8")
        result = translate_client.translate(word, target_language=language_OSI_code)

        translated_words.append(result["translatedText"])
        
    return translated_words

####################################################################################################
####################################################################################################

def translate_and_write(output_folder, dest_language, type_name, type_data):
    """Translate the content of lists.
    Write the output in the given folder, in a created <type_name>.<dest_language>.json JSON file.

    Args:
        output_folder   (string)    : Folder path where to store translation
        dest_language   (string)    : Language to be translated to
        type_name       (string)    : Description of the list (verbs, adjectives, pluralnouns...)
        type_data       (list)      : List of words/sentences to be translated
    """
    translated_words = translate_data(type_data, dest_language)              # get translations
    translated_words = sorted(list(dict.fromkeys(translated_words)))    # Sort alphabetically
    write_fo_file(output_folder, dest_language, type_name, translated_words)


####################################################################################################
####################################################################################################

if __name__ == "__main__":

    import threading
    import time
    import argparse

    ##################################################

    parser = argparse.ArgumentParser(description='Translate the Jitsi roomname-generation words')
        
    parser.add_argument("-l", "--lang",
    help="Language to translate to. Use ISO 639-1 language code (en, fr, es...)",
    default="fr")
        
    parser.add_argument("-i", "--input_folder", 
    help="Folder storing words to be translated",
    default="data_en")
        
    parser.add_argument("-d", "--destination_folder", 
    help="Folder path where will be stored translations. '_<lang>' will be added at the end",
    default="data")

    parser.add_argument("-m", "--no_multithread",
    help="If added, this flag will prevent the script from usinguse multithreading",
    action="store_false")

    args = parser.parse_args()

    ##################################################
    
    # -1    : Default behaviour.
    # 0     : Tiny test if something doesn't work.
    # 1     : Test for time difference.
    # ...   : Your on tests :)
    test_number = -1

    ##################################################
    ##########      Default  Behaviour      ##########
    ##################################################
    if test_number == -1:

        dest_language= args.lang
        input_folder = args.input_folder
        output_folder = f"{args.destination_folder}_{dest_language}"
        no_multithreading = args.no_multithread

        # Extract words
        vocabulary = extract_data_lists_from_json(input_folder)

        # Use multithreading: one thread for each file inside input_folder
        # We could do much better by just launching all API requests as async, but I don't know if 
        # it is possible using Google Cloud API (it must be, but we do not have that much data so
        # no need to complicate the code too much)
        if not no_multithreading:
            for type_name in vocabulary.keys():
                threading.Thread(target=translate_and_write, args=(output_folder, dest_language, type_name, vocabulary[type_name])).start()
            print("Words succesfully translated")
        
        else:
            for type_name in vocabulary.keys():
                translate_and_write(output_folder, dest_language, type_name, vocabulary[type_name])
            print("Words succesfully translated")


    ##################################################
    if test_number == 0:
        test = ["Hello", "World", "This", "Is", "a", "Test"]
        dest_language= args.lang
        translated_words = translate_data(test, dest_language)
        print(translated_words)
    
    ##################################################
    if test_number == 1:
        dest_language= args.lang
        input_folder = args.input_folder
        output_folder = f"{args.destination_folder}_{dest_language}"

        # Check multithreading time
        start_time = time.clock()
        for type_name in vocabulary.keys():
            threading.Thread(target=translate_and_write, args=(output_folder, dest_language, type_name, vocabulary[type_name])).start()
        print(f"Total time using multi-threading: {time.clock()-start_time}")

        # Check singlethreading time
        start_time = time.clock()
        for type_name in vocabulary.keys():
            translate_and_write(output_folder, dest_language, type_name, vocabulary[type_name])
        print(f"Total time without multi-threading: {time.clock()-start_time}")
