import json
import urllib.request
import time

# from .word_audio import get_jpod_audio_base64
# ANKI_MODELS_FILENAME = 'ankimodels.yaml'

def request(action, params):
    return {'action': action, 'params': params, 'version': 6}

class AnkiConnect():
    def __init__(self, model='Basic'):
        self.port = 8765
        self.model = model

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

    def fetch_anki_fields(self, model_name):
        field_names = self.invoke('modelFieldNames', modelName=model_name)
        return field_names
        # result = {}
        # for model_name in model_names:
        #     field_names = self.invoke('modelFieldNames', {'modelName': model_name})
        #     result[model_name] = field_names
        # return result

    def fetch_anki_decks(self):
        result = self.invoke('deckNames')
        return result

    def fetch_models(self):
        result = self.invoke('modelNamesAndIds')
        return result

    def store_file(self):
        now = str(time.time())
        filename = '_{}.jpg'.format(now)
        print(filename)
        data = "SGVsbG8sIHdvcmxkIQ=="
        result = self.invoke('storeMediaFile', filename=filename, data=data)
        return result

    def store_picture(self, data):
        filename = '_{}.jpg'.format(time.time())
        result = self.invoke('storeMediaFile', filename=filename, data=data)
        return result

    def create_anki_note(self, note_data=None):
        expression = note_data['expression']
        definition = note_data['definition']
        reading = note_data['reading']
        sentence = note_data['sentence']
        # if 'screenshot' in note_data:
        #     # TODO: start new thread to save image
        #     result = self.store_picture(note_data['screenshot'])
        #     print('screenshot saved')
        # screenshot = note_data['screenshot'] if 'screenshot' in note_data else ''
        # print('screenshot', screenshot)

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


# def get_anki_models():
#     filename = None # str(Path(bundle_dir, 'anki', ANKI_MODELS_FILENAME))
#     ankiModels = []
#     with open(filename, 'r') as stream:
#         try:
#             ankiModels = yaml.safe_load(stream)
#             return ankiModels
#         except yaml.YAMLError as exc:
#             print(exc)

#     return ankiModels


if __name__  == '__main__':
    ac = AnkiConnect('Mining')

    from PIL import Image
    import base64
    from io import BytesIO
    image = Image.open(r'C:\Users\user\Documents\Game2Text-Lightning\src\main\persona.jpg')
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    data = base64.b64encode(img_byte).decode()
    note_data = {}
    note_data['screenshot'] = data
    note_data['expression'] = 'exp'
    note_data['reading'] = 'read'
    note_data['sentence'] = 'sent'
    note_data['definition'] = 'def'
    print(ac.create_anki_note(note_data))

    # print(ac.fetch_anki_decks())
    # print(ac.fetch_models())
    # print(ac.fetch_anki_fields('Basic'))
    # print(ac.create_anki_note())