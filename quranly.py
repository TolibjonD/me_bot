import requests
# print(res_sura['chapter'][0]['text'])

def get_one_surah(sura,tafsir= 'uzb-muhammadsodikmu',oyat=None):
    url_sura=f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{tafsir}/{sura}.json"
    r_sura = requests.get(url_sura)
    res_sura = r_sura.json()
    text = []
    for verse in res_sura['chapter']:
        text.append(f"{verse['verse']}) {verse['text']}\n")
    return text

# me = get_one_surah(sura=1)
# print(me)

def get_surah_info():
    url_info = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/info.json"
    r_info = requests.get(url_info)
    res_info = r_info.json()
    chapters = res_info['chapters']
    count_surah = len(chapters)
    first_sura = chapters[0]['name']
    surah_names = []
    for chapter in chapters:
        surah_names.append({ f"{chapter['name']}":chapter['englishname']})
    return {
        "count": count_surah,
        "first": first_sura,
        "names": surah_names
    }

# me2 = get_surah_info()
# print(me2['names'][0])


def get_audio_of_sura(sura_id):
    url = f"https://api.alquran.cloud/v1/surah/{sura_id}/ar.alafasy"
    r = requests.get(url)
    res = r.json()
    audio_url = res['data']['ayahs']
    audios = []
    for audio in audio_url:
        audios.append({"audio": audio['audio'], "text": audio['text'] })
    return audios
