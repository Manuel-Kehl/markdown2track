#!/usr/bin/env python

import sys
import re
import StringIO

lheader = re.compile('\A\s*(?P<hashes>\#+)')
rheader = re.compile('(?P<hashes>\#+)\s*\Z')
setex_header_1 = re.compile('(.+\n)(=+)')
setex_header_2 = re.compile('(.+\n)(-+)')
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
    
    # Search for image tag and extract image information
    image_match = re.search('(\!\[\]\()(.*)(\))', line);
    if image_match:
      url = image_match.group(2)
      tag_original = image_match.group(0)
      tag_new = '[[Image(' + url + ')]]'
      # Replace the tag
      line = line.replace(tag_original, tag_new)
    
    # Return with any trailing newline removed
    return line.rstrip()

def main():
    if len(sys.argv) != 2:
        print "Usage: python markdown2trac <filename>"
        return
      
    # The file that has been passed to the script
    input_file = file(sys.argv[1])
    content = input_file.read()
    
    # Substitute Setex-headers (Level 1 and 2)
    for idx, header in enumerate([setex_header_1, setex_header_2]):
      header_match = header.findall(content);
      if header_match:
	# Run through all headers that were found
	for item in header_match:
	  header_title = item[0]
	  header_underline = item[1]
	  header_original = header_title + header_underline
	  # Determine header type via idx
	  header_new = "=" * idx + "= " + header_title    
	  # Replace headers
	  content = content.replace(header_original, header_new)
	
    # Treat content like file so it can be iterated line by line
    temp_file = StringIO.StringIO(content)
    
    delim = '{{{'
    for line in temp_file:
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

