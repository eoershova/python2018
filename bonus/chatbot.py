import os
import re
import collections
import random
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
books = ['1.txt', '2.txt']
all_forms = collections.defaultdict(list)
case_prepositions = collections.defaultdict(list)


# classifies words according to their grammar tag prepositions
# are stored separately
# for their grammar tag can be determined by the following noun
def word_finder():
    for book in books:
        with open(book, 'r', encoding='utf-8') as file:
            text = file.read()
            clean_text = re.sub(r'[^А-ЯЁа-яё\d-]', ' ', text)
            words = clean_text.split()
            prepositions = []
            for word in words:
                original_word = word
                word = morph.parse(word)[0]
                if word.tag.POS == "PREP":
                    prepositions.append(original_word)
                    continue
                else:
                    all_forms[word.tag].append(original_word)
            prepositions = set(prepositions)
            preps_case = []
            for preposition in prepositions:
                prep = preposition.lower()
                clean_text = clean_text.lower()
                fw = re.compile(r'\s' + prep + r'\s[А-ЯЁёа-я]+')
                following_words = re.findall(fw, clean_text)
                case_count = collections.Counter()
                if len(following_words) > 1:
                    for option in following_words:
                        following_word = option.split()[1]
                        for_pos = morph.parse(following_word)[0]
                        if for_pos.tag.POS == 'NOUN':
                            case_count[for_pos.tag.case] += 1
                case = case_count.most_common(1)
                if case == []:
                    continue
                case = (case[0][0])
                prep_case = preposition, case
                preps_case.append(prep_case)
            for preposition, case in preps_case:
                case_prepositions[case].append(preposition)


def user_listener(user_answer):
    sentence = collections.OrderedDict()
    user_answer = re.sub(r'[^А-ЯЁа-яё\d]', ' ', user_answer)
    n = 0
    for word in user_answer.split():
        n += 1
        sentence.update({n: word})
    return sentence


def answer_maker(sentence):
    answer = ''
    for word in sentence:
        index = int(word)
        original_word = sentence[word]
        word = morph.parse(original_word)[0]
        gram_tag = word.tag
        if word.tag.POS == 'PREP':
            next_word_index = index + 1
            next_word = sentence[next_word_index]
            next_word = morph.parse(next_word)[0]
            case = next_word.tag.case
            try:
                substitute = random.choice(case_prepositions[case])
                if substitute.lower() == original_word.lower():
                    if len(case_prepositions[case]) > 1:
                        substitute = random.choice(case_prepositions[case])
                    if len(case_prepositions[case]) == 1:
                        substitute = 'Чебаркуль'
                if index == 1:
                    substitute = substitute.capitalize()
                answer = answer + ' ' + substitute
            except KeyError:
                substitute = 'Чебаркуль'
                answer = answer + ' ' + substitute
        else:
            try:
                substitute = random.choice(all_forms[gram_tag])
                if substitute.lower() == original_word.lower():
                    if len(all_forms[gram_tag]) > 1:
                        substitute = random.choice(all_forms[gram_tag])
                    if len(all_forms[gram_tag]) == 1:
                        substitute = 'Чебаркуль'
                if index == 1:
                    substitute = substitute.capitalize()
                answer = answer + ' ' + substitute
            except KeyError:
                substitute = 'Чебаркуль'
                answer = answer + ' ' + substitute

    return answer


def main():
    word_finder()
    punct, sentence = user_listener()
    answer_maker(punct, sentence)


if __name__ == '__main__':
    main()
