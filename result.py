import numpy as np

class Result():
    def __init__(self, characters):
        self.characters = characters
    
    # is character in boxes
    def detect_character(self, point):
        characters = []
        if not self.characters:
            return None
        for character in self.characters:
            if character.touches_point(point):
                characters.append(character)
                # return character
        return characters

# def closest_node(node, nodes):
#     nodes = np.asarray(nodes)
#     deltas = nodes - node
#     dist_2 = np.einsum('ij,ij->i', deltas, deltas)
#     return np.argmin(dist_2)
    