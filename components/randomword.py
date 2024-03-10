import httpx
#from textual.widgets import Static
#from textual.widget import Widget
#from textual.app import RenderResult

#from components.renderstring import RenderString

def random_word():
    url = "https://random-word-api.herokuapp.com/word?length=5"

    lines = []

    while True:
        with httpx.Client() as client:
            response = client.get(url)
            try:
                results = response.json()
                    
            except Exception:
                results[0] = 'XXXXX'
    
        if results[0] == 'XXXXX':
            continue

        url2 = f"https://api.dictionaryapi.dev/api/v2/entries/en/{results[0]}"

        with httpx.Client() as client:
            response = client.get(url2)
            try:
                word_def = response.json()
                    
            except Exception:
                word_def = 'XXXXX'
        
        if word_def == 'XXXXX' or isinstance(word_def, dict):
            continue
        elif isinstance(word_def, list):
            for result in word_def:
                    lines.append("-----------------------------------------------------------")
                    lines.append(f"[b]{result['word']}[/b]")
                    lines.append("-----------------------------------------------------------")
                    for meaning in result.get("meanings", []):
                        lines.append(f"[i]{meaning['partOfSpeech']}[/i]")
                        lines.append("")
                        for definition in meaning.get("definitions", []):
                            lines.append(f" ~ {definition['definition']}")
                        lines.append("-----------------------------------------------------------")
        

        long_def = "\n".join(lines)
        long_def += '\n\n Press [b]Ctrl+R[/b] to play again.'
        break
     
    return results[0].upper(), long_def 