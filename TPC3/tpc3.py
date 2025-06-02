### TPC3 - TRADUTOR MD->HTML #######################################################
# ler o ficheiro markdown e fazer uma tradução básica para html
# executar: python3 tpc3.py < source.md
####################################################################################

import re, sys, os

src = sys.stdin.read()

####################################################################################
####################################################################################

pattern = r"""
( 
    (?P<header>
        (?: ^[ ]*\#{3}[ ]+(?P<header3>.*)$ )
    |   (?: ^[ ]*\#{2}[ ]+(?P<header2>.*)$ )
    |   (?: ^[ ]*\#{1}[ ]+(?P<header1>.*)$ )
    ) 
|   (?P<enumlist> 
        ^\d+\.[ ]+.*$ (?:\n\d+\.[ ]+.*$)*
    )
|   (?P<fontformat>
        ((?:\*\*\*)(?!\s) (?P<bolditalic>(?:\\\*|[^\n\r])+?)(?!\s) (?:\*\*\*))
    |   ((?:\*\*)(?!\s)   (?P<bold>      (?:\\\*|[^\n\r])+?)(?!\s) (?:\*\*))
    |   ((?:\*)(?!\s)     (?P<italic>    (?:\\\*|[^\n\r])+?)(?!\s) (?:\*))
    )
|   (?P<img>
        \!\[ (?P<imgdesc> [^\n]+?) \] \( (?P<imgpath> [\w]+?:\/{2}?[\w\d]+?\.[\w\d]+?\.[\w\d]+?.*?) \)
    )
|   (?P<href>
        \[ (?P<hrefdesc> [^\n]+?) \] \( (?P<hrefpath> [\w]+?:\/{2}?[\w\d]+?\.[\w\d]+?\.[\w\d]+?.*?) \)
    )
)

"""

####################################################################################
####################################################################################

def header_to_html(match):
    if match.group("header1"):
        return f"<h1>{match.group('header1')}</h1>"
    elif match.group("header2"):
        return f"<h2>{match.group('header2')}</h2>"
    elif match.group("header3"):
        return f"<h3>{match.group('header3')}</h3>"

def enumlist_to_html(match):
    items = re.findall(r'^\d+\.[ ]+(.*)$', match.group("enumlist"), re.MULTILINE)
    html = "<ol>\n"
    for item in items: html += f"  <li>{item}</li>\n"
    html += "</ol>"
    return html

def fontformat_to_html(match):
    if match.group("bolditalic"):
        return f"<strong><em>{match.group('bolditalic')}</em></strong>"
    elif match.group("bold"):
        return f"<strong>{match.group('bold')}</strong>"
    elif match.group("italic"):
        return f"<em>{match.group('italic')}</em>"
    
def img_to_html(match):
    return f'<img src="{match.group("imgpath")}" alt="{match.group("imgdesc")}">'

def href_to_html(match):
    return f'<a href="{match.group("hrefpath")}">{match.group("hrefdesc")}</a>'

def match_to_html(match):
    if match.group("header"):       return header_to_html(match)
    elif match.group("enumlist"):   return enumlist_to_html(match)
    elif match.group("fontformat"): return fontformat_to_html(match)
    elif match.group("img"):        return img_to_html(match)
    elif match.group("href"):       return href_to_html(match)
    else:                           return match.group(0)
    
####################################################################################
####################################################################################

html = r'<!-- PL 2024/25 TPC3 -->'
html += re.sub(
    pattern,
    lambda match: match_to_html(match),
    src,
    flags=re.MULTILINE | re.VERBOSE
)

if os.path.exists("out.html"):
    os.remove("out.html")
with open("out.html", "w") as file:
    file.write(html)