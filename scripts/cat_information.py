"""
General functions for getting information from CAT XML files
"""


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
    Reads a CAT file and returns the id of the sentence of a predicate given the predicate id
    '''
    for markable in list_markables:
        if (markable.get("id") or markable.get("m_id")) == markable_id:
            first_word = markable.findall("token_anchor")[0]
    for token in list_tokens:
        if token.get("t_id") == first_word.get("t_id"):
            sent_id = token.get("sentence")
            break
    return sent_id


def get_full_sentence(sent_id, list_tokens):
    '''
    Reads a CAT file and returns the full text of a sentence given its id
    '''
    sentence = ""
    for token in list_tokens:
        if token.get("sentence") == sent_id:
            word = token.text + " "
            sentence = sentence + word
    return sentence