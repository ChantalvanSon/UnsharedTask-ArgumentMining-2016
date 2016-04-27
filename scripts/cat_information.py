"""
General functions for getting information from CAT XML files
"""

from lxml import etree

def get_all_sentences(filename):
    '''
    Reads a CAT file and returns a dictionary with the sentence ids (int) and full texts (str) of all sentences
    '''
    infile = open(filename, "r")
    raw = infile.read()
    root = etree.XML(raw)
    list_tokens = root.findall("token")
    sentences = {}
    sent_id = "0"
    sentence = ""
    for token in list_tokens:
        if token.get("sentence") == sent_id:
            sentence = sentence + " " + token.text
        else:
            sentences[int(sent_id)] = sentence
            sent_id = token.get("sentence")
            sentence = token.text
    if sent_id not in sentences:
        sentences[int(sent_id)] = sentence
    return sentences


def get_text_markable(markable_id, list_markables, list_tokens):
    '''
    Reads a CAT file and returns the full text of a markable given its id
    '''
    markable_text = ""
    for markable in list_markables:
        if markable.get("m_id") == markable_id:
            markable_tokens = markable.findall("token_anchor")
            for markable_token in markable_tokens:
                for token in list_tokens:
                    if token.get("t_id") == markable_token.get("t_id"):
                        word = token.text + " "
                        markable_text = markable_text + word
    return markable_text


def get_sent_id(markable_id, list_markables, list_tokens):
    '''
    Reads a CAT file and returns the id of the sentence of a markable given the markable id
    '''
    # Assumes markables do not cross sentences
    for markable in list_markables:
        if (markable.get("id") or markable.get("m_id")) == markable_id:
            first_word = markable.findall("token_anchor")[0]
    for token in list_tokens:
        if token.get("t_id") == first_word.get("t_id"):
            sent_id = token.get("sentence")
            break
    return sent_id

def get_sent_ids(markable_id, list_markables, list_tokens):
    '''
    Reads a CAT file and returns a list of the ids of the sentences of a markable given the markable id
    '''
    # Allows for markables to cross sentences
    sent_ids = []
    tokens_markable = []
    for markable in list_markables:
        if (markable.get("id") or markable.get("m_id")) == markable_id:
            for token_markable in markable.findall("token_anchor"):
                tokens_markable.append(token_markable.get("t_id"))
    for token in list_tokens:
        if token.get("t_id") in tokens_markable:
            sent_ids.append(token.get("sentence"))
    return sent_ids

def get_full_sentence(sent_id, list_tokens):
    '''
    Reads a CAT file and returns the full text of a sentence given its id
    '''
    sentence = ""
    for token in list_tokens:
        if token.get("sentence") == sent_id:
            if sentence == "":
                sentence = token.text
            else:
                sentence = sentence + " " + token.text
    return sentence