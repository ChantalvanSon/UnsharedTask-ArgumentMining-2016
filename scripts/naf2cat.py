"""
Converts all tokenized KAF/NAF files in directory to simple tokenized input format for CAT (one token per line and <EOS> between sentences).
"""


import sys
import os
from lxml import etree

def get_root(path):
    infile = open(path,"r")
    raw = infile.read()    
    root = etree.XML(raw)
    del raw
    return root

def kaf_to_cat(filename, outputfile):
    sent = 0
    content = ""
    try:
        root = get_root(filename)
        text_layer = root.find("text")
        for word in text_layer.findall("wf"):
            if sent != word.get("sent"):
                if content != "":
                    content += "<EOS>\n"
            content += word.text + "\n"
            sent = word.get("sent")
        content += "<EOS>\n"
        content = content.encode("utf8")
    except:
        print "ERROR: Could not extract text from " + filename + ". Continuing with other files."
        content = ""
    f = open(outputfile, "w")
    f.write(content)
    f.close()




def main(argv=None):
    if argv is None:
        argv = sys.argv
        if len(argv) < 3:
            print 'Error. Usage: python from_kaf_to_cat.py input_dir output_dir'
        else:
            if not os.path.exists(argv[2]):
                os.makedirs(argv[2])
            for filename in os.listdir(argv[1]):                
                infile = os.path.join(argv[1], filename)
                cat_filename = filename.replace(".naf", ".txt")
                outfile = os.path.join(argv[2], cat_filename)
                kaf_to_cat(infile, outfile)

if __name__ == '__main__':
    main()   
