from forwardscan import get_longest_match

class Result():
    def __init__(self, characters):
        self.characters = characters
    
    # is character in boxes
    def detect_character(self, point):
        characters = []
        if not self.characters:
            return None
        for index, character in enumerate(self.characters):
            if character.touches_point(point):
                characters.append(character)
                # return character
        return characters

    def sentence(self):
        return ''.join([c.text for c in self.characters])

    def get_definition(self, characters):
        # characters = self.detect_character(point)
        if characters:
            s = self.sentence()[characters[0].index:]
            match = get_longest_match(s)
            if match:
                return match
                # glossary, meaning = match
                # return '{}: {}'.format(glossary, meaning)
            else:
                return characters[0].text
        else:
            return None


# def closest_node(node, nodes):
#     nodes = np.asarray(nodes)
#     deltas = nodes - node
#     dist_2 = np.einsum('ij,ij->i', deltas, deltas)
#     return np.argmin(dist_2)
    