"""
Panflute filter to allow file includes

Each include statement has its own line and has the syntax:

    !include ../somefolder/somefile

Or

    $include ../somefolder/somefile

Each include statement must be in its own paragraph. That is, in its own line
and separated by blank lines.

If no extension was given, ".md" is assumed.
"""

import os
import panflute as pf


def is_include_line(elem):
    # Debug
    #with open('test.out', 'w') as f:
    #    f.write(str(elem.content))

    if len(elem.content) < 3:
        return False
    elif not all (isinstance(x, (pf.Str, pf.Space)) for x in elem.content):
        return False
    elif elem.content[0].text != '!include' and elem.content[0].text != '$include':
        return False
    elif type(elem.content[1]) != pf.Space:
        return False
    else:
        return True


def get_filename(elem):
    fn = pf.stringify(elem, newlines=False).split(maxsplit=1)[1]
    if not os.path.splitext(fn)[1]:
        fn += '.md'
    return fn

# Record whether the entry has been entered
entryEnter = False

def action(elem, doc):
    global entryEnter

    if isinstance(elem, pf.Para) and is_include_line(elem):
        # The entry file's directory
        entry = doc.get_metadata('include-entry')
        if not entryEnter and entry:
            os.chdir(entry)
            entryEnter = True

        fn = get_filename(elem)

        if not os.path.isfile(fn):
            raise ValueError('Included file not found: ' + fn + ' ' + entry + ' ' + os.getcwd())
        
        with open(fn, encoding="utf-8") as f:
            raw = f.read()

        # Save current path
        cur_path = os.getcwd()

        # Change to included file's path so that sub-include's path is correct
        target = os.path.dirname(fn)
        # Empty means relative to current dir
        if not target:
            target = '.'

        os.chdir(target)

        # Add recursive include support
        new_elems = pf.convert_text(raw, extra_args=['--filter=pandoc-include'])

        # Restore to current path
        os.chdir(cur_path)
        
        # Alternative A:
        return new_elems
        # Alternative B:
        # div = pf.Div(*new_elems, attributes={'source': fn})
        # return div


def main(doc=None):
    return pf.run_filter(action, doc=doc) 


if __name__ == '__main__':
    main()

