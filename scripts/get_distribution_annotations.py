"""
Gets all sentences annotated with a COMMENTED_UPON markable and counts how many annotators have
annotated the same sentence. Writes output to TSV outputfile.
"""

from lxml import etree
import os
from cat_information import *

outfilename = "/Users/Chantal/Desktop/distribution_annotations.csv"
inputdir = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/VariantC/CAT-with-comments-annotated/devel"


def get_relevant_sentences(filename_article_cat):
    """Get all sentences from a CAT file that contain a COMMENTED_UPON markable"""
    relevant_sentences = []
    infile = open(filename_article_cat, "r")
    raw = infile.read()
    root = etree.XML(raw)
    list_tokens = root.findall("token")
    list_commented = (root.find("Markables")).findall("COMMENTED_UPON")
    for commented in list_commented:
        commented_id = commented.get("m_id")
        sent_id = get_sent_id(commented_id, list_commented, list_tokens)
        sentence = get_full_sentence(sent_id, list_tokens)
        relevant_sentences.append(sentence)
    infile.close()
    #print(relevant_sentences)
    return relevant_sentences


def main(inputdir, outfilename):
    outfile = open(outfilename, "w")
    subsets = [name for name in os.listdir(inputdir) if os.path.isdir(os.path.join(inputdir, name))]
    first_subset = os.path.join(inputdir, subsets[0])
    for filename_cat in os.listdir(first_subset):
        if filename_cat.endswith(".xml"):
            filename_cat = os.path.join(first_subset, filename_cat)
            annotated_sentences = [get_relevant_sentences(filename_cat)]

            # Get other annotated sentences
            for subset in subsets:
                filename_cat = filename_cat.replace(subsets[0], subset)
                annotated_sentences.append(get_relevant_sentences(filename_cat))

            all_annotated_sentences = list(set([item for sublist in annotated_sentences for item in sublist]))
            relevant_sentences = {}
            for sentence in all_annotated_sentences:
                for set_sentences in annotated_sentences:
                    if sentence in set_sentences:
                        if sentence not in relevant_sentences:
                            relevant_sentences[sentence] = 1
                        else:
                            relevant_sentences[sentence] += 1

            for sentence in relevant_sentences:
                s = os.path.basename(filename_cat) + "\t" + sentence + "\t" + str(relevant_sentences[sentence]) + "\n"
                outfile.write(s)

    outfile.close()


main(inputdir, outfilename)
