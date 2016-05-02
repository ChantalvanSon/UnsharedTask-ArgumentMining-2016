"""
Gets all sentences annotated with a COMMENTED_UPON markable and counts how many annotators have
annotated the same sentence. Writes output to TSV outputfile.
"""

import os
import csv
from cat_information import *
import collections

outfilename = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/Task1-annotations/distribution_annotations_round1.csv"
inputdir = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/Task1-annotations/CAT-Round-1/devel"


def get_annotated_sentences(filename_article_cat):
    """Get all sentences from a CAT file that contain a COMMENTED_UPON markable"""
    annotated_sentences = []
    infile = open(filename_article_cat, "r")
    raw = infile.read()
    root = etree.XML(raw)
    list_tokens = root.findall("token")
    list_commented = (root.find("Markables")).findall("COMMENTED_UPON")
    for commented in list_commented:
        commented_id = commented.get("m_id")
        sent_ids = get_sent_ids(commented_id, list_commented, list_tokens)
        for sent_id in sent_ids:
            sentence = get_full_sentence(sent_id, list_tokens)
            annotated_sentences.append(sentence)
    infile.close()
    #print(annotated_sentences)
    return annotated_sentences


def main(inputdir, outfilename):
    # Get names of annotators and create first row of csv file
    annotators = [name for name in os.listdir(inputdir) if os.path.isdir(os.path.join(inputdir, name))]
    first_row = ["discussion_id", "comment_id", "sentence", "comment"]
    for annotator in annotators:
        first_row.append(annotator)
    first_row.append("total")
    to_write = [first_row]

    # Get annotated sentences in one file from one annotator
    first_annotator = os.path.join(inputdir, annotators[0])
    for filename_cat in os.listdir(first_annotator):
        if filename_cat.endswith(".xml"):
            filename_cat = os.path.join(first_annotator, filename_cat)

            # Get all sentences (and make sorted list of dictionary)
            all_sentences = get_all_sentences(filename_cat)
            all_sentences = collections.OrderedDict(sorted(all_sentences.items()))
            comment = all_sentences[0].replace("COMMENT: ", "")
            del all_sentences[0]  # remove first sentence, this is the comment in these files
            all_sentences = list(all_sentences.values())

            # Get all annotated sentences from first annotator
            annotated_sentences = {}
            annotations = get_annotated_sentences(filename_cat)
            annotated_sentences[annotators[0]] = annotations
            #all_annotated_sentences = [annotations]

            # Get annotated sentences in corresponding file from other annotators
            for annotator in annotators[1:]:
                #filename = filename_cat.replace(annotators[0], annotator)
                #filename = os.path.join(os.path.dirname(filename_cat), annotator)
                filename = os.path.join(inputdir, annotator, os.path.basename(filename_cat))
                annotations = get_annotated_sentences(filename)
                annotated_sentences[annotator] = annotations
                #all_annotated_sentences.append(annotations)

            annotated_sentences = collections.OrderedDict(sorted(annotated_sentences.items()))
            #print(all_sentences)
            #print(annotated_sentences)

            # Make list of all needed data and write to output file
            discussion_id = os.path.basename(filename_cat).split("#")[0]
            comment_id = "#" + os.path.basename(filename_cat).split("#")[1].split(".")[0]
            for sentence in all_sentences:
                data = [discussion_id, comment_id, sentence, comment]
                for annotator in annotated_sentences:
                    if sentence in annotated_sentences[annotator]:
                        data.append(1)
                    else:
                        data.append(0)
                data.append(sum(data[4:]))
                to_write.append(data)

    with open(outfilename, "w") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(to_write)


main(inputdir, outfilename)
