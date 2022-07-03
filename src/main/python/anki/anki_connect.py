import json
import logging
import urllib.request
import time
from threading import Thread 
from .anki_model import AnkiModel
from util.word_audio import get_jpod_audio_base64

def request(action, params):
    return {'action': action, 'params': params, 'version': 6}

class AnkiConnect():
    def __init__(self, deck=None, model=None, anki_settings=None):
        self.port = 8765
        self.model = model
        self.deck = deck
        self.anki_settings = anki_settings

    def invoke(self, action, **params):
        try:
            requestJson = json.dumps(request(action, params)).encode('utf-8')
            response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:{}'.format(self.port), requestJson)))
            if len(response) != 2:
                return 'Error: Response has an unexpected number of fields'
            if 'error' not in response:
                return 'Error: Response has an unexpected number of fields'
            if 'result' not in response:
                return 'Error: Response is missing required result field'
            if response['error'] is not None:
                return 'Error:' + response['error']
            return response['result']
        except:
            return 'Error: Failed to connect to Anki.'

    def _fetch_fields_for_model(self, model_name, result, index):
        try:
            field_names = self.invoke('modelFieldNames', modelName=model_name)
            result[index] = field_names
        except:
            logging.error('Failed to fetch fields')
        return True

    def fetch_anki_models(self):
        models = self.fetch_models()
        if not models:
            return[]
        model_names = list(models.keys())
        field_lists = [{} for x in model_names]
        threads = []
        for index, model_name in enumerate(model_names):
            process = Thread(target=self._fetch_fields_for_model, args=[model_name, field_lists, index])
            process.start()
            threads.append(process)
        for process in threads:
            process.join()
        result = []
        if len(model_names) == len(field_lists):
            result = [AnkiModel(
                id=models[model_name], 
                model_name=model_name,
                fields=field_lists[i])
                for i, model_name in enumerate(model_names)]
        return result

    def fetch_anki_decks(self):
        result = self.invoke('deckNames')
        if type(result) == list:
            return result
        else:
            if type(result) == str:
                logging.error(result)
            return []

    def fetch_models(self):
        result = self.invoke('modelNamesAndIds')
        if type(result) == dict:
            return result
        else:
            if type(result) == str:
                logging.error(result)
            return []

    def set_model(self, model_name):
        self.model = model_name

    def set_deck(self, deck_name):
        self.deck = deck_name

    # def store_file(self):
    #     now = str(time.time())
    #     filename = '_{}.jpg'.format(now)
    #     print(filename)
    #     data = "SGVsbG8sIHdvcmxkIQ=="
    #     result = self.invoke('storeMediaFile', filename=filename, data=data)
    #     return result

    # def store_picture(self, data):
    #     filename = '_{}.jpg'.format(time.time())
    #     result = self.invoke('storeMediaFile', filename=filename, data=data)
    #     return result

    def create_anki_note(self, note_data):
        if not self.anki_settings:
            logging.error("Anki settings not configured")
            return
        field_value_map = self.anki_settings.get_field_value_map(self.model)
        if not field_value_map:
            logging.error("Anki field value map not configured")
            return

        fields = {}
        screenshot_field = None
        word_audio_field = None
        for field, value in field_value_map.items():
            if value.lower() == 'screenshot':
                if 'screenshot' in note_data:
                    screenshot_field = field
            elif value.lower() == 'word_audio':
                if 'expression' in note_data and 'reading' in note_data:
                    note_data['word_audio'] = get_jpod_audio_base64(note_data['expression'], note_data['reading'])
                    word_audio_field = field
            elif value.lower() == 'pitch':
                if 'expression' in note_data and 'reading' in note_data:
                    if self.anki_settings.pitch:
                        fields[field] = self.anki_settings.pitch.get_pitch(note_data['expression'], note_data['reading'])
            else:
                fields[field] = note_data[value.lower()]
                
        note = {
            "deckName": self.deck,
            "modelName": self.model,
            "fields": fields,
            "tags": [
                "game2text"
            ],
        }
        if screenshot_field:
            note["picture"] =  [{
                "data": note_data['screenshot'],
                "filename": '_{}.jpg'.format(time.time()),
                "fields": [
                   screenshot_field
                ]
            }]
        if word_audio_field:
            note['audio'] = [{
                "data": note_data['word_audio'],
                "filename": '_{}.mp3'.format(time.time()),
                 "fields": [
                   word_audio_field
                ]
            }]
        result = self.invoke('addNote', note=note)
        return result

if __name__  == '__main__':
    from fbs_runtime.application_context.PyQt5 import ApplicationContext
    appctxt = ApplicationContext()
    ac = AnkiConnect('Mining', appctxt.get_resource('anki/user_models.yaml'))

    # from __init__ import Anki_Values
    # am = { 'model_name': 'Basic',
    #         'field_value_map': {
    #             'front': Anki_Values.EXPRESSION.name,
    #             'back': Anki_Values.DEFINITION.name
    #         }}
    # print(ac.save_user_models([am]))
    # print(ac.get_user_models())

    # from PIL import Image
    # import base64
    # from io import BytesIO

    # image = Image.open(r'C:\Users\user\Documents\Game2Text-Lightning\src\main\persona.jpg')
    # buffered = BytesIO()
    # image.save(buffered, format="JPEG")
    # img_byte = buffered.getvalue()
    # data = base64.b64encode(img_byte).decode()
    # note_data = {}
    # note_data['screenshot'] = data
    # note_data['expression'] = 'exp'
    # note_data['reading'] = 'read'
    # note_data['sentence'] = 'sent'
    # note_data['definition'] = 'def'
    # print(ac.create_anki_note(note_data))