import csv
import os
from lxml import etree
import itertools
from KafNafParserPy import *
from naf_information import *
from cat_information import *


variant_C = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantC"
variant_D = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantD"


##############################################################################
# Function for getting information from about the comments in the discussion #
##############################################################################

def get_comments_from_discussion(infilename):
    """
    Reads the discussion files (VariantD) from the data provided for the ACL Unshared Task on Argument Mining and
    returns a list with information about each comment in the discussion [[info_comment1], [info_comment2]], that is:
    - corresponding filename
    - debate title
    - debate description
    - article title
    - post id
    - username
    - previous post id (if it is a reaction to another comment) or NA
    - text of comment
    """

    discussion_data = []
    infile = open(infilename, "r")
    content = infile.read()
    comments = content.split("\n\n\n")
    # Get debate title, debate description, and article title
    lines = comments[0].split("\n\n")
    debate_title = lines[0].replace("Debate title: ", "").replace("\n", "")
    debate_description = lines[1].replace("Debate description: ", "").replace("\n", "")
    article_title = lines[2].replace("Article title: ", "").replace("\n", "")
    comments[0] = "#" + comments[0].split("#")[1] # remove debate title etc. from first comment

    # Get all information for each comment
    for comment in comments:
        lines = comment.split("\n\n")
        try:
            post_id = lines[0].split()[0]
            username = lines[0].split()[1]

            if len(lines[0].split()) > 2:
                previous_post_id = lines[0].split()[3]
            else:
                previous_post_id = "NA"

            lines = [line.replace('\n', ' ') for line in lines]
            #text = "\n\n".join(lines[1:])
            text = " <br/>".join(lines[1:])

            comment_data = [os.path.basename(infilename),debate_title, debate_description, article_title, post_id, username, previous_post_id, text]
            discussion_data.append(comment_data)

        except:
            continue

    return discussion_data


###############################################################################
# Functions for getting information about propositions from CAT and NAF files #
###############################################################################


def get_commented_sentences(filename_article_cat):
    """Finds all sentences that contain a COMMENTED_UPON markable in a CAT file and returns a list of sentences"""
    relevant_sentences = []
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
            relevant_sentences.append(sentence)
    infile.close()
    #print(relevant_sentences)
    return relevant_sentences


def get_relevant_sentences(inputdir_annotations):
    relevant_sentences = {}
    annotators = [name for name in os.listdir(inputdir_annotations) if os.path.isdir(os.path.join(inputdir_annotations, name))]

    # Get annotated sentences in one file from one annotator
    first_annotator = os.path.join(inputdir_annotations, annotators[0])
    for filename_cat in os.listdir(first_annotator):
        if filename_cat.endswith(".xml"):
            filename_cat = os.path.join(first_annotator, filename_cat)
            annotated_sentences = [get_relevant_sentences(filename_cat)]

            # Get annotated sentences in corresponding file from other annotators
            for annotator in annotators:
                filename_cat = filename_cat.replace(annotators[0], annotator)
                annotated_sentences.append(get_relevant_sentences(filename_cat))

            # Compare annotations and count number of annotations for each sentence
            all_annotated_sentences = list(set([item for sublist in annotated_sentences for item in sublist]))
            relevant_sentences_file = {}
            for sentence in all_annotated_sentences:
                for set_sentences in annotated_sentences:
                    if sentence in set_sentences:
                        if sentence not in relevant_sentences_file:
                            relevant_sentences_file[sentence] = 1
                        else:
                            relevant_sentences_file[sentence] += 1

            # Create dictionary with key = filename and value = dictionary of sentences with counts
            relevant_sentences[os.path.basename(filename_cat)] = relevant_sentences_file

    return relevant_sentences


def get_propositions(filename_article_cat, filename_article_naf):
    '''
    Returns a list of all annotated propositions in a CAT file, with for each proposition:
     - the event (string)
     - argument(s) (list) -> should be adapted
     - sentence (string)
     - paragraph (string)
    '''

    propositions = []

    # Get basic information from CAT file (XML objects of tokens, markables and relations)
    infile = open(filename_article_cat, "r")
    raw = infile.read()
    root = etree.XML(raw)
    list_tokens = root.findall("token")
    list_propositions = (root.find("Relations")).findall("PROPOSITION")
    list_events = (root.find("Markables")).findall("EVENT")
    list_arguments = (root.find("Markables")).findall("ARGUMENT")

    # For each proposition (= CAT relation), get the texts of the event, argument(s), sentence, and paragraph
    for prop in list_propositions:
        event_id = prop.find("source").get("m_id")
        event_text = get_text_markable(event_id, list_events, list_tokens)
        list_target_arg = prop.findall("target")
        arguments_texts = []
        for argument in list_target_arg:
            arg_id = argument.get("m_id")
            argument_text = get_text_markable(arg_id, list_arguments, list_tokens)
            arguments_texts.append(argument_text)
        sent_ids = get_sent_ids(event_id, list_events, list_tokens)
        for sent_id in sent_ids:
            sent_id_naf = str(int(sent_id) + 1) # sent id CAT different than NAF
            sentence = get_full_sentence(sent_id, list_tokens)
            paragraph, para_id = get_paragraph(sent_id_naf, filename_article_naf)
            propositions.append([event_text, arguments_texts, sentence, paragraph])

    infile.close()

    return propositions


#################
# Main function #
#################

def main(variant_C, variant_D, option):
    originals_D = os.path.join(variant_D, "original")
    for subdir, dirs, files in os.walk(originals_D):
        for subset in dirs:

            # Get annotations on relevant sentences (NOT FINISHED YET!)
            #annotations_dir = os.path.join(variant_C, "CAT-with-comments-annotated", subset)
            #if subset == "devel":
                #annotated_sentences = get_relevant_sentences(annotations_dir)

            # Get all data for each comment in datasets variant D (for development set, crowdsourcing set, test set)
            #all_data = [["debate id", "debate title", "debate description", "article title", "post id", "username", "previous post id", "text comment", "text article", "text event", "arguments", "sentence", "paragraph"]]
            #all_data = [["debate id", "debate title", "debate description", "article title", "post id", "username", "previous post id", "text comment", "text article", "sentence article", "paragraph article"]]
            all_data = [["debate id", "debate title", "debate description", "article title", "post id", "username", "previous post id", "text comment", "text article", "paragraph id article", "sentence1", "sentence2", "sentence3", "sentence4", "sentence5", "sentence6", "sentence7"]]
            for filename in os.listdir(os.path.join(subdir,subset)):
                if filename.endswith(".txt"):
                    print("Processing:", filename)

                    # Get text from corresponding article in dataset variant C
                    filename_article = os.path.join(variant_C,"original",subset,filename.replace("D", "C"))
                    infile = open(filename_article)
                    content_article = infile.read().split("\n\n")[3:] # remove first 3 lines (debate title, description and article title)
                    content_article = "\n\n".join([x.replace('\n', ' ') for x in content_article]) # remove single newlines and join paragraphs

                    # Get data from each comment in dataset variant D
                    filename_discussion = os.path.join(subdir,subset,filename)
                    discussion_data = get_comments_from_discussion(filename_discussion)
                    # debate_title = discussion_data[0][1]
                    # debate_description = discussion_data[0][2]
                    # article_title = discussion_data[0][3]

                    # Get propositions from CAT file
                    if subset == "devel": # comment after experimenting
                        filename_article_cat = filename_article.replace("original", "CAT-annotated") + ".xml"
                        filename_article_naf = filename_article.replace("original", "NAF-tokenized")
                        propositions = get_propositions(filename_article_cat, filename_article_naf)
                        sentences = get_sentences_naf(filename_article_naf)
                    else:
                        continue


                    # Collect all data and turn into one list (for writing the csv)
                    for comment_data in discussion_data:
                        comment_data.append(content_article)

                        # CREATE SEPARATE DATA ENTRIES (LINES) FOR EACH PARAGRAPH (WITH SEPARATE SENTENCES)
                        if option == "1":
                            paragraphs = get_paragraphs_sentences_naf(filename_article_naf)
                            for par_id in paragraphs:
                                sentences = paragraphs[par_id]
                                to_add = comment_data + [par_id] + sentences
                                all_data.append(to_add)

                        # CREATE SEPARATE DATA ENTRIES (LINES) FOR EACH SENTENCE IN ARTICLE
                        if option == "2":
                            for sent_id in sentences:
                                sentence = sentences[sent_id]
                                paragraph, para_id = get_paragraph(sent_id, filename_article_naf)
                                to_add = comment_data + [sentence, paragraph]
                                all_data.append(to_add)

                        # CREATE SEPARATE DATA ENTRIES (LINES) FOR EACH PROPOSITION
                        if option == "3":
                            for proposition in propositions:
                                text_event = proposition[0]
                                arguments = proposition[1] ## list; how to process this?
                                sentence = proposition[2]
                                paragraph = proposition[3]
                                all_data.append(comment_data + proposition)

                        # CREATE SEPARATE DATA ENTRIES (LINES) FOR EACH RELEVANT SENTENCE
                        #if option == "4":


                        # CREATE SEPARATE DATA ENTRIES (LINES) FOR EACH PARAGRAPH (NOT FINISHED YET -- PROBABLY WON'T USE)
                        #if option == "X":
                            #for para_id in paragraphs:
                                #paragraph = paragraphs[para_id]["text"]
                                #propositions = paragraphs[para_id]["propositions"]
                                #if len(propositions) == 3:
                                    #list_propositions = list(itertools.chain(*propositions))
                                    #to_add = comment_data.append(paragraph) #+ list_propositions
                                    #print to_add + list_propositions
                                    #all_data.append(to_add)
                                #else:
                                    #print len(propositions)

            # Write the data to csv file in directory
            outdir_csv = os.path.join(variant_D, "csv")
            if not os.path.exists(outdir_csv):
                os.makedirs(outdir_csv)
            outputfile = os.path.join(outdir_csv, subset + option + ".csv")
            print(outputfile)
            # outputfile = os.path.join(subdir, subset, "comments_data.csv")
            with open(outputfile, "w") as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerows(all_data)

    print("Done")

main(variant_C, variant_D, "1")
