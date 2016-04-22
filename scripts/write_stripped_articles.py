"""
Reads the original data files (variant C) provided for the Unshared Task on Argumentation Mining 2016 (ACL) and writes
them in to a new format in a specified outputdir (remove meaningless newlines, debate title and debate description)
"""

import os

inputdir = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantC/original"
outputdir = "/Users/Chantal/Documents/UnsharedTask-ACL-2016/data/variantC/stripped"


def main(inputdir, outputdir):
    for subdir, dirs, files in os.walk(inputdir):
        for subset in dirs:
            outdir = os.path.join(outputdir, subset)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            for filename in os.listdir(os.path.join(subdir, subset)):
                if filename.endswith(".txt"):
                    print("Processing:", filename)

                    # Read files in dataset variant C
                    filename_article = os.path.join(inputdir, subdir, subset, filename)
                    infile = open(filename_article)
                    content_article = infile.read().split("\n\n")

                    # Get debate title
                    # debate_title = content_article[0].replace("\n", "").replace("Debate title: ", "")
                    # if not debate_title.endswith("." or "?" or "!"):
                        # debate_title = debate_title + "."

                    # Get debate description
                    # debate_description = content_article[1].replace("\n", "").replace("Debate description: ", "")
                    # if not debate_description.endswith("." or "?" or "!"):
                        # debate_description = debate_description + "."

                    # Get article title
                    article_title = content_article[2].replace("\n", "").replace("Article title: ", "")
                    if not article_title.endswith("." or "?" or "!"):
                        article_title = article_title + "."

                    # Get article text remove first 3 lines (debate title, description and article title),
                    # remove single newlines and join paragraphs
                    text_article = "\n\n".join([x.replace('\n', ' ') for x in content_article[3:]])

                    # Write to outputfile
                    outfilename = os.path.join(outdir, filename)
                    outfile = open(outfilename, "w")
                    outfile.write(article_title + "\n\n")
                    outfile.write(text_article)
                    outfile.close()

main(inputdir, outputdir)
