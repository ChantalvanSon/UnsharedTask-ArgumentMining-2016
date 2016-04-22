"""
Reads the original data files (variant C) provided for the Unshared Task on Argumentation Mining 2016 (ACL) and writes
them in to a new format in a specified outputdir (remove meaningless newlines, debate title and debate description)
"""

import os

inputdir_CAT = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantC/CAT-tokenized"
inputdir_discussion = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantD/original"
outputdir = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantC/CAT-with-comments"


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



def main(inputdir_CAT, inputdir_discussion, outputdir):
    for subdir, dirs, files in os.walk(inputdir_CAT):
        for subset in dirs:
            outdir = os.path.join(outputdir, subset)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            for filename in os.listdir(os.path.join(subdir, subset)):
                if filename.endswith(".txt"):
                    print("Processing:", filename)

                    # Get text from article in CAT tokenized format
                    filename_article = os.path.join(inputdir_CAT, subdir, subset, filename)
                    infile = open(filename_article, "r")
                    text_article = infile.read()
                    infile.close()

                    # Get corresponding discussion data
                    filename_discussion = os.path.join(inputdir_discussion, subset, filename.replace("C", "D"))
                    discussion_data = get_comments_from_discussion(filename_discussion)
                    for comment in discussion_data:
                        text_comment = "COMMENT: " + comment[-1].replace("<br/>", "").replace("  ", " ")
                        post_id = comment[0].replace(".txt", "") + comment[4] + ".txt"
                        outfilename = os.path.join(outdir, post_id)
                        to_write = text_comment.replace(" ", "\n") + "\n<EOS>\n" + text_article
                        outfile = open(outfilename, "w")
                        outfile.write(to_write)
                        outfile.close()




main(inputdir_CAT, inputdir_discussion, outputdir)
