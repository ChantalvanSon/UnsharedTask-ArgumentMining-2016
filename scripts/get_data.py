import csv
import os
from lxml import etree
import itertools
from KafNafParserPy import *


variant_C = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantC"
variant_D = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantD"
#filename_discussion = "/Users/Chantal/Documents/argmin2016-unshared-task-master/data/variantD/devel/Dd001.txt"



def get_comments_from_discussion(infilename):
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


    # For each comment, get the post id (unique within discussion), username, previous post id (if it is a reaction to another comment), and the text of the comment
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
            text = "\n\n".join(lines[1:])

            comment_data = [os.path.basename(infilename),debate_title, debate_description, article_title, post_id, username, previous_post_id, text]
            discussion_data.append(comment_data)
            
        except:
            continue

    return discussion_data
        
def write_stripped_file(outfilename, article_title, content_article):
    outdir = os.path.dirname(outfilename)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not article_title.endswith("." or "?" or "!"):
        article_title = article_title + "."
    outfile = open(outfilename, "w")
    outfile.write(article_title + "\n\n")
    outfile.write(content_article)
    outfile.close()


###############################################################################
# Functions for getting information about propositions from CAT and NAF files #
###############################################################################

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

def get_paragraph(sent_id, filename_article_naf):
    '''
    Reads a NAF file and returns the full text of a paragraph given a sentence id of this paragraph
    '''
    naf = KafNafParser(filename_article_naf)
    paragraph = ""
    for token in naf.get_tokens():
        if sent_id == str(int(token.get_sent()) - 1):
            para_id = token.get_para()
    for token in naf.get_tokens():
        if token.get_para() == para_id:
            paragraph = paragraph + " " + token.get_text()
    return paragraph, para_id

def get_propositions(filename_article_cat, filename_article_naf):
    '''
    Returns a list of all annotated propositions in a CAT file, with for each proposition the texts of the event, argument(s), sentence, and paragraph
    '''

    propositions = []
    #paragraphs = {}
    
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
        sent_id = get_sent_id(event_id, list_events, list_tokens)                
        sentence = get_full_sentence(sent_id, list_tokens)
        paragraph, para_id = get_paragraph(sent_id, filename_article_naf)
        propositions.append([event_text, arguments_texts, sentence, paragraph])

        #if para_id not in paragraphs:
            #paragraphs[para_id] = {"text":paragraph, "propositions":[[event_text, "ARGUMENTS", sentence]]}
        #else:
            #paragraphs[para_id]["propositions"].append([event_text, "ARGUMENTS", sentence])
            

    infile.close()
    
    return propositions#, paragraphs
    

#################
# Main function #
#################

def main(variant_C, variant_D):
    originals_D = os.path.join(variant_D, "original")
    for subdir, dirs, files in os.walk(originals_D):
        for subset in dirs:

            # Get all data for each comment in datasets variant D (for development set, crowdsourcing set, test set)
            all_data = [["debate id", "debate title", "debate description", "article title", "post id", "username", "previous post id", "text comment", "text article", "text event", "arguments", "sentence", "paragraph"]]
            for filename in os.listdir(os.path.join(subdir,subset)):
                if filename.endswith(".txt"):
                    print "Processing:", filename
                    
                    # Get text from corresponding article in dataset variant C
                    filename_article = os.path.join(variant_C,"original",subset,filename.replace("D", "C"))
                    infile = open(filename_article)
                    content_article = infile.read().split("\n\n")[3:] # remove first 3 lines (debate title, description and article title)
                    content_article = "\n\n".join([x.replace('\n', ' ') for x in content_article]) # remove single newlines and join paragraphs

                    # Get data from each comment in dataset variant D
                    filename_discussion = os.path.join(subdir,subset,filename)
                    discussion_data = get_comments_from_discussion(filename_discussion)

                        
                    # Write stripped text to new folder for variant C (excluding debate description and title)
                    article_title = discussion_data[0][3]
                    outfilename = filename_article.replace("original", "stripped")
                    if not os.path.exists(os.path.dirname(outfilename)):
                        os.makedirs(os.path.dirname(outfilename))
                    write_stripped_file(outfilename, article_title, content_article)

                    # Get propositions from CAT file
                    if subset == "devel": # comment after experimenting
                        filename_article_cat = filename_article.replace("original", "CAT-annotated") + ".xml"
                        filename_article_naf = filename_article.replace("original", "NAF-tokenized")
                        propositions = get_propositions(filename_article_cat, filename_article_naf)
                    else:
                        continue


                    # Collect all data and turn into one list (for writing the csv) ######################### EDIT HERE!
                    for comment_data in discussion_data:
                        comment_data.append(content_article)


                        # CREATE SEPARATE DATA ENTRIES (LINES) FOR EACH PROPOSITION
                        for proposition in propositions:
                            text_event = proposition[0]
                            arguments = proposition[1] ## list; how to process this?
                            sentence = proposition[2]
                            paragraph = proposition[3]
                            all_data.append(comment_data + proposition)

                        # CREATE SEPARATE DATA ENTRIES (LINES) FOR EACH PARAGRAPH (NOT FINISHED YET -- PROBABLY WON'T USE)
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
            outputfile = os.path.join(outdir_csv, subset + ".csv")
            #outputfile = os.path.join(subdir, subset, "comments_data.csv")
            with open(outputfile, "wb") as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerows(all_data)

    print "Done"
                    

main(variant_C, variant_D)

       

