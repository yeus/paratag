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

## ubuntu 16.04

    pip3 install --user pypdf2
    pip3 install --user xlwt
    pip3 install --user xattr  #for setting extended attributes
    sudo apt install python3-pandas  #using databases

