#!/usr/bin/env python

import sys
import re

lheader = re.compile('\A\s*(?P<hashes>\#+)')
rheader = re.compile('(?P<hashes>\#+)\s*\Z')
litalics = re.compile('_(?P<keep>[\W])')
ritalics = re.compile('(?P<keep>[\W])_')
numbered = re.compile('^1\.')

def translate_line(line):
    # Substitute # for = in the headers
    for header in [lheader, rheader]:
        if header.search(line):
            nhashes = len(header.search(line).group('hashes'))
            line = header.sub('=' * nhashes, line)

    # Change delimiters for bold
    line = line.replace('**', "'''")

    # Change delimiters for italics. This elaborate way of doing it ensures
    # that a variable or function name separated by underscores, such as
    # foo_bar, doesn't get italicized.
    line = litalics.sub(r"''\g<keep>", line)
    line = ritalics.sub(r"\g<keep>''", line)

    # Add a space before numbered lists
    line = numbered.sub(' 1.', line)
    
    #Search for image tag and extract image information
    image_match = re.search('(\!\[\]\()(.*)(\))', line);
    
    if image_match:
      url = image_match.group(2)
      tag_original = image_match.group(0)
      tag_new = '[[Image(' + url + ')]]'
      #replace the tag
      line = line.replace(tag_original, tag_new)
    
    # Return with any trailing newline removed
    return line.rstrip()

def main():
    if len(sys.argv) != 2:
        print "Usage: python markdown2trac <filename>"
        return
    
    delim = '{{{'
    for line in file(sys.argv[1]):
        line = translate_line(line)

        # Change code marking from `code` to {{{code}}}
        ix = line.find('`')
        while ix != -1:
            line = line[:ix] + delim + line[ix+1:]
            if delim == '{{{':
                delim = '}}}'
            else:
                delim = '{{{'
            ix = line.find('`', ix + 1)
        
        print line

if __name__ == "__main__":
    main()

