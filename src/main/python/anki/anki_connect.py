import json
import logging
import urllib.request
import time
import yaml
from threading import Thread 
from .anki_model import AnkiModel
# from .word_audio import get_jpod_audio_base64'

def request(action, params):
    return {'action': action, 'params': params, 'version': 6}

class AnkiConnect():
    def __init__(self, model='Basic', anki_models_path=''):
        self.port = 8765
        self.model = model
        self.anki_models_path = anki_models_path

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
        if type(result) == list:
            return result
        else:
            if type(result) == str:
                logging.error(result)
            return []

    def get_user_models(self):
        anki_models = []
        with open(self.anki_models_path, 'r') as stream:
            try:
                ankiModels = yaml.safe_load(stream)
                return ankiModels
            except yaml.YAMLError as exc:
                print(exc)
        return anki_models

    def update_user_model(self, model_name, field_value_map):
        new_model = {
            'model_name': model_name,
            'field_value_map': field_value_map
        }
        user_models = self.get_user_models()
        result = []
        if user_models:
            result = [user_model for user_model in user_models if user_model['model_name'] != model_name]
        result.append(new_model)
        self.save_user_models(result)

    def save_user_models(self, anki_models):
        with open(self.anki_models_path, 'w') as outfile:
            yaml.dump(anki_models, outfile, sort_keys=False, default_flow_style=False)
            return outfile.name

    def get_field_value_map(self, model_name):
        models = self.get_user_models()
        field_value_map = {}
        if models:
            field_value_map = next((model['field_value_map'] for model in models if model['model_name'] == model_name), {})
        return field_value_map

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

    def create_anki_note(self, note_data=None):
        expression = note_data['expression']
        definition = note_data['definition']
        reading = note_data['reading']
        sentence = note_data['sentence']

        note = {
            "deckName": "Default",
            "modelName": self.model,
            "fields": {
                "Word": expression,
                "Definition": definition,
                "Reading": reading,
                "Sentence": sentence
            },
            "tags": [
                "game2text"
            ],
        }
        if 'screenshot' in note_data:
            note["picture"] =  [{
                "data": note_data['screenshot'],
                "filename": '_{}.jpg'.format(time.time()),
                "fields": [
                    "Screenshot"
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

    # print(ac.fetch_anki_fields())
    # print(ac.fetch_models())
    # print(ac.fetch_anki_fields('Basic'))
    # print(ac.create_anki_note())