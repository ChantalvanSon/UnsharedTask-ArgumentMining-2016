"""
This script uses data provided for the Unshared Task on Argumentation Mining 2016 (ACL).

Input:
- a directory with editorial articles (stripped, tokenized and converted to CAT format)
- a directory with discussions (original format) about these articles

Output:
- a directory with files in CAT format; each file contains in the first line a comment from the discussion,
and in the remaining lines the different sentences of the editorial article. The names of the files indicate the
discussion id (e.g. Dd001) and the comment id (e.g. #3).
"""

import os
import sys


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
            #text = "\n\n".join(lines[1:])
            text = " <br/>".join(lines[1:])

            comment_data = [os.path.basename(infilename),debate_title, debate_description, article_title, post_id, username, previous_post_id, text]
            discussion_data.append(comment_data)

        except:
            continue

    return discussion_data

def write_cat_files(inputdir_CAT, inputdir_discussion, outputdir):
    # Create output directory
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    # Go through each editorial article
    for filename in os.listdir(inputdir_CAT):
        if filename.endswith(".txt"):
            print("Processing:", filename)

            # Get text from article in CAT tokenized format
            filename_article = os.path.join(inputdir_CAT, filename)
            infile = open(filename_article, "r")
            text_article = infile.read()
            infile.close()

            # Get corresponding discussion data
            filename_discussion = os.path.join(inputdir_discussion, filename.replace("C", "D"))
            discussion_data = get_comments_from_discussion(filename_discussion)
            for comment in discussion_data:
                text_comment = "COMMENT: " + comment[-1].replace("<br/>", "").replace("  ", " ")
                post_id = comment[0].replace(".txt", "") + comment[4] + ".txt"
                outfilename = os.path.join(outputdir, post_id)
                to_write = text_comment.replace(" ", "\n") + "\n<EOS>\n" + text_article
                outfile = open(outfilename, "w")
                outfile.write(to_write)
                outfile.close()
    return


def main(argv=None):
    if argv is None:
        argv = sys.argv
        if len(argv) < 4:
            print("Error. Usage: python write_cat_files.py inputdir_articles inputdir_discussions outputdir")
        else:
            write_cat_files(argv[1], argv[2], argv[3])


if __name__ == '__main__':
    main()



#inputdir_CAT = "/Users/Chantal/Documents/Github/UnsharedTask-ArgumentMining-2016/data/editorial_articles/4-CAT-tokenized"
#inputdir_discussion = "/Users/Chantal/Documents/Github/UnsharedTask-ArgumentMining-2016/data/discussions/original"
#outputdir = "/Users/Chantal/Documents/Github/UnsharedTask-ArgumentMining-2016/test"
#write_cat_files(inputdir_CAT, inputdir_discussion, outputdir)