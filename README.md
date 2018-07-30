# paratag

automated tagging of files based on certain critera.

paratag := parametric taggig

paratag analyzes files according to some rules which can be configured by the user
and automatically writes the information into extended attributes of
the files and directories. These criteria can then be picked up by search engines such as baloo or recoll.

right now only pdf files are supported.
    
# installation

## ubuntu 16.04

    pip3 install --user pypdf2
    pip3 install --user xlwt
    pip3 install --user xattr  #for setting extended attributes
    sudo apt install python3-pandas  #using databases



# notes
## interesting commandline applications:

Print all meta information in an image, including duplicate and unknown tags, sorted by group (for family 1).

    exiftool -a -u -g1
