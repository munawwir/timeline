file = "SOPs/met_cages/Metabolic_Cages_GF_setup_and_calibration.md"

new_tag = ["test","test2"]

def check_tags(file, tag):
    """Checks if tag is in the file
    file = read in string of file
    tag = string tag"""

    tags = [x.replace("%20"," ") for x in file.split("https://img.shields.io/badge/tags-")[1].split("-lightgrey?style=flat-square")[0].split("%20|%20")]

    if tag in tags:
        return(True)
    else:
        return(False)

def add_tags(file, new_tag):
    """Read in .md file, take a list of tags to add, and add in those tags.
    file = file name to edit
    new_tag = list of new tags (strings)"""

    # new_tag = [x.replace(" ","%20") for x in new_tag]

    new_tag = ["%20|%20" + x for x in [x.replace(" ","%20") for x in new_tag]]

    f = open(file,"r").read()

    # [x.replace("%20"," ") for x in f.split("https://img.shields.io/badge/tags-")[1].split("-lightgrey?style=flat-square")[0].split("%20|%20")]

    old = f.split("https://img.shields.io/badge/tags-")[1].split("-lightgrey?style=flat-square")[0]

    new = old + "".join(new_tag)

    new

    # open(file,"w").write(f.replace(old, new))

check_tags(f,"test")

f.split("https://img.shields.io/badge/tags-")[1].split("-lightgrey?style=flat-square")[0].split("%20|%20")
