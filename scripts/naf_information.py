"""
General functions for getting information from NAF files
"""

from KafNafParserPy import *


def get_paragraph(sent_id, filename_article_naf):
    """Reads a NAF file and returns the full text of a paragraph given a sentence id of this paragraph"""
    naf = KafNafParser(filename_article_naf)
    paragraph = ""
    for token in naf.get_tokens():
        if sent_id == token.get_sent():
        #if sent_id == str(int(token.get_sent()) - 1): # sent id CAT different than NAF
            para_id = token.get_para()
    for token in naf.get_tokens():
        if token.get_para() == para_id:
            paragraph = paragraph + " " + token.get_text()
    return paragraph, para_id


def get_paragraphs_sentences_naf(filename_article_naf):
    """Reads a NAF file and returns a dictionary with all sentences for each paragraph {para id: [sentences]}"""
    naf = KafNafParser(filename_article_naf)
    sentences = {}
    sent_id = "1"
    para_id = "1"
    sentence = ""
    for token in naf.get_tokens():
        if sent_id == token.get_sent():
            sentence = sentence + " " + token.get_text()
        else:
            if not para_id in sentences:
                sentences[para_id] = [sentence]
            else:
                sentences[para_id].append(sentence)
            sent_id = token.get_sent()
            para_id = token.get_para()
            sentence = token.get_text()
    # Add last sentence
    if not sentence in sentences[para_id]:
        sentences[para_id].append(sentence)
    return sentences


def get_sentences_naf(filename_article_naf):
    """Reads a NAF file and returns a dictionary with all sentences {sent id: string}"""
    naf = KafNafParser(filename_article_naf)
    sentences = {}
    sent_id = "1"
    sentence = ""
    for token in naf.get_tokens():
        if sent_id == token.get_sent():
            sentence = sentence + " " + token.get_text()
        else:
            sentences[sent_id] = sentence
            sent_id = token.get_sent()
            sentence = token.get_text()
    # LAST SENTENCE MISSING?
    #if not sentence in sentences[sent_id]:
        #sentences[sent_id].append(sentence)
    return sentences