#Import httpx to use API's for random word and dictionary
import httpx


def random_word(length: int=5) -> str:
    #URL for random word API
    url_random_word_api = f"https://random-word-api.herokuapp.com/word?length={length}"

    #empty list for returning all the lines in the word definition
    lines = []

    #loop while word not found
    while True:
        #Get random word from API
        with httpx.Client() as client:
            response = client.get(url_random_word_api)
            try:
                results = response.json() #set word in a list with the len of 1.
                    
            except Exception:
                results[0] = 'XXXXX'

        #Restart loop to try and get another word if exception.
        if results[0] == 'XXXXX':
            continue 
        
        #Url for dictionary API
        url_dictionary_api = f"https://api.dictionaryapi.dev/api/v2/entries/en/{results[0]}"

        #Get dictionary page for random word from dictionary API
        with httpx.Client() as client:
            response = client.get(url_dictionary_api)
            try:
                word_def = response.json()
                    
            except Exception:
                word_def = 'XXXXX'
        
        #If is a dict (or exception) then word not in dictionary (or failed), so restart loop to try again
        if word_def == 'XXXXX' or isinstance(word_def, dict):
            continue
        #if list, a result has been retrieved from dictionary API
        elif isinstance(word_def, list):
            #add results from dictionary to lines to generate the definition as a list
            for result in word_def:
                lines.append("-----------------------------------------------------------")
                lines.append(f"[b]{result['word']}[/b]")
                lines.append("-----------------------------------------------------------")
                for meaning in result.get("meanings", []):
                    lines.append(f"[i]{meaning['partOfSpeech']}[/i]")
                    lines.append("")
                    for definition in meaning.get("definitions", []):
                        lines.append(f" ~ {definition['definition']}")
        
        #turn definition list (lines) into a string then break the loop
        long_def = "\n".join(lines)
        break
     
    #return the random word and the definition
    return results[0].upper(), long_def 