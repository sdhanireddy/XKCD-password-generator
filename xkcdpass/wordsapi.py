import requests
from collections import defaultdict

def get(word, param):
  url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/{param}"

  headers = {
    "X-RapidAPI-Key": "d7c5dec7e4mshcd9e0cf561f94b5p14389fjsn0aae7b32d195",
    "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
  }
  print('making call for', word)

  return requests.request("GET", url, headers=headers)

def parts_of_speech(word):
  res = get(word, 'definitions')
  res.raise_for_status()
  parts = set()
  for d in res.json()['definitions']:
    parts.add(d['partOfSpeech'])
  return parts

def create_and_write(file, items):
  with open(f"static/{file}", 'a') as f:
    f.write("\n")
    f.write("\n".join(items))

def get_wordlist(filename):
  words = set()
  with open(f'static/{filename}', encoding='utf-8') as wlf:
    for line in wlf:
      thisword = line.strip()
      words.add(thisword)
  return sorted(list(words))

LAST_WORD = 'fame'
NUM_CALLS_EXTRA = 0

if __name__ == '__main__':
  all_words = get_wordlist('eff-long')
  index = all_words.index(LAST_WORD)
  total_calls = index + NUM_CALLS_EXTRA + 1 # +1 for zero-indexing
  words = all_words[index+1:]
  # words = set(all_words)
  # existing_parts_of_speech = ['adjective', 'adverb', 'None', 'noun', 'verb']
  # for file in existing_parts_of_speech:
  #   for word in get_wordlist(file):
  #     words.discard(word)
  # words = sorted(list(words))
  parts_dict = defaultdict(set)
  for word in words[:2500-total_calls]:
    try:
      parts = parts_of_speech(word)
    except:
      parts_dict['misses'].add(word)
      continue
    for part in parts:
      parts_dict[part].add(word)
  for part, words_set in parts_dict.items():
    create_and_write(part, sorted(list(words_set)))