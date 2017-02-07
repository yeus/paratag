# paratag

automated tagging of files based on users critera.

paratag := parametric taggig
paratag := 

paratag analyzes files according to some rules which can be configured by the user
and automatically writes the information into extended attributes of
the files and directories.

right now only pdf files are supported.

# interesting commandline applications:

Print all meta information in an image, including duplicate and unknown tags, sorted by group (for family 1).

    exiftool -a -u -g1

    
# installation

    pip install --user pypdf2
    pip install --user xlwt
    pip install --user xattr  #for setting extended attributes
