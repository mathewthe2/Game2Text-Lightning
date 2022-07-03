import yaml
from japanese.pitch import Pitch

class AnkiSettings():
    def __init__(self, appctxt):
        self.anki_models_path = appctxt.get_resource('anki/user_models.yaml')
        self.anki_defaults_path = appctxt.get_resource('anki/user_defaults.yaml')
        self.active_model = None
        self.active_field_value_map = None
        self.pitch = Pitch(appctxt.get_resource('rikaisama/pitch_accents.sqlite'))

    def get_default_deck_model(self):
        with open(self.anki_defaults_path, 'r') as stream:
            try:
                result = yaml.safe_load(stream)
                if result:
                    deck = result['deck_name'] if 'deck_name' in result else None
                    model = result['model_name'] if 'model_name' in result else None
                    return deck, model
                else:
                    return None, None
            except yaml.YAMLError as exc:
                print(exc)
        return result

    def update_default_deck(self, deck):
        old_deck, model = self.get_default_deck_model()
        self.save_default_deck_model(deck, model)

    def update_default_model(self, model):
        deck, old_model = self.get_default_deck_model()
        self.save_default_deck_model(deck, model)

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

        # clear field value cache
        if model_name == self.active_model:
            self.active_model = None
            self.active_field_value_map = None

    def save_default_deck_model(self, deck, model):
        result = {
            'deck_name': deck,
            'model_name': model
        }
        with open(self.anki_defaults_path, 'w') as outfile:
            yaml.dump(result, outfile, sort_keys=False, default_flow_style=False)
            return outfile.name

    def save_user_models(self, anki_models):
        with open(self.anki_models_path, 'w') as outfile:
            yaml.dump(anki_models, outfile, sort_keys=False, default_flow_style=False)
            return outfile.name

    def get_field_value_map(self, model_name):
        # use cache
        if model_name == self.active_model:
            return self.active_field_value_map
        # fetch
        models = self.get_user_models()
        field_value_map = {}
        if models:
            field_value_map = next((model['field_value_map'] for model in models if model['model_name'] == model_name), {})
        # cache results
        self.active_model = model_name
        self.active_field_value_map = field_value_map
        # return result
        return field_value_map

# if __name__  == '__main__':
#     from fbs_runtime.application_context.PyQt5 import ApplicationContext
#     appctxt = ApplicationContext()
#     settings = AnkiSettings(appctxt)
#     settings.update_default_deck('Default')
#     settings.update_default_model('Mining')