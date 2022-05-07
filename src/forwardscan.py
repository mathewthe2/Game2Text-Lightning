# words = {'もっと': '(some) more; even more; longer; further',
#          'も': 'too; also; in addition; as well; (not) either (in a negative sentence)'
#          }

from dictionary.jedict import jedict

def get_matches(s):
    results = []
    for i in range(len(s), 0, -1):
        if s[0:i] in jedict:
            results.append(jedict[s[0:i]])
    return results


def get_longest_match(s):
    for i in range(len(s), 0, -1):
        if s[0:i] in jedict:
            meanings = jedict[s[0:i]]
            first_meaning = meanings[0]
            has_kanji = len(first_meaning[0]) > 0
            s = ''
            if has_kanji:
                s = '{}({}): {}'.format(first_meaning[0], first_meaning[1], first_meaning[2])
            else:
                s = '{}: {}'.format(first_meaning[1], first_meaning[2])
            return s[:80]
    return None

# print(get_longest_match('もっと'))
