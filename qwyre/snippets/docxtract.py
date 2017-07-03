from pydocx import PyDocX #Docx2Html
#import sys
from bs4 import BeautifulSoup

def fix_tags(html):
    valid_simplify = ['em', 'i', 'b', 'strong']
    for v in valid_simplify:
        rem, rem_ = u'</{0}><{0}>'.format(v), u'</{0}> <{0}>'.format(v)
        html = html.replace(rem_, " ")
        html = html.replace(rem, "")
    #print html.encode(sys.stdout.encoding, errors='replace')
    return html
    
def docxtract(docxfile="C:/Users/Turukawa/OneDrive/Novels/Tartarus Falls/sample.docx"):
    valid_unwrap = ['div', 'span']
    valid_del = ['hr']
    header = [u'h1', u'h2', u'h3', u'h4']
    right_align = {'class': u"pydocx-right", 'style': u"text-align:right"}
    result = fix_tags(PyDocX.to_html(docxfile))
    html = BeautifulSoup(result, 'html.parser').body
    # clear up the mess
    # http://stackoverflow.com/q/1765848
    for v in valid_unwrap:
        for match in html.find_all(v):
            if match['class'] == [right_align['class']]:
                if match.parent.name == u'p':
                    match.parent['style'] = right_align['style']
            match.unwrap()
    for v in valid_del:
        for match in html.find_all(v):
            match.decompose()
    # Get the tree
    p = False
    tree = []
    for child in html.find_all(True):
        if child.name in header:
            if p:
                tree.append([ptext, p])
                p = False
            tree.append(["<b>%s</b>" % child.get_text(), unicode(child)])
        elif child.name == u'p': # Ensure only paragraphs, not elements within paragraphs
            if child.get_text().strip():
                if p:
                    p = ''.join([p, unicode(child)])
                else:
                    p = unicode(child)
                    ptext = "%s..." % child.get_text()[:80]
    if p:
        tree.append([ptext, p])
    return tree