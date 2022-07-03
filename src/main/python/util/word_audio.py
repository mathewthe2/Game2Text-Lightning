import requests
import base64
import hashlib

def get_jpod_audio(url):
    try:
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(url, verify=False, timeout=5)
        return r
    except:
        return None

def validate_jpod_audio_url(url):
    jpod_audio = get_jpod_audio(url)
    if jpod_audio:
        return len(jpod_audio.content) != 52288 # invalid audio
    else:
        return False

def audioIsPlaceholder(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest() == '7e2c2f954ef6051373ba916f000168dc'

def get_jpod_audio_url(kanji, kana):
    url = 'https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji={}&kana={}'.format(kanji, kana)
    return url if (validate_jpod_audio_url(url)) else ''

def get_jpod_audio_base64(kanji, kana):
    jpod_url = get_jpod_audio_url(kanji, kana)
    if jpod_url:
        print('jpod', jpod_url)
        jpod_audio = get_jpod_audio(jpod_url)
        if jpod_audio:
            return 'data:audio/mp3;base64,' + str(base64.b64encode(jpod_audio.content))
        else:
            return ''
    return ''