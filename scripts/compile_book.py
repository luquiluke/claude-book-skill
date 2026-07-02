"""
/book — Book DOCX Compiler
==========================
Builds a complete book .docx from one master content file.

Two modes:
  default  — self-contained: generates a clean book template (Georgia, real heading
             styles, page-number footer, US Letter, 1" margins). No dependencies.
  --sample — clones formatting (styles, fonts, theme, footers) from a .docx the
             author provides, rift-style: copy the file, replace the body, keep the
             sample's section properties so its page setup survives.

Usage:
    python compile_book.py <content.txt> <output.docx>
        [--title "T"] [--subtitle "S"] [--author "A"] [--sample template.docx]
    python compile_book.py --selftest

Content markup (one paragraph per line):
    # Chapter title        -> Heading 1 (automatically starts a new page)
    ## Section             -> Heading 2
    ### Subsection         -> Heading 3
    ~tagline~              -> italic body line
    > quoted/aside text    -> Quote style (italic, indented)
    **whole line bold**    -> bold body line (closing beats)
    - item                 -> bulleted body line
    [PAGEBREAK]            -> manual page break
    [TOC]                  -> table-of-contents field (Word: right-click > Update Field)
    (blank line)           -> spacer paragraph
    anything else          -> body paragraph (**bold** / _italic_ inline markup works)
"""

import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from xml.dom import minidom
from xml.sax.saxutils import escape


# ---------------------------------------------------------------- text -> runs

def escape_xml(text):
    return escape(text, {'"': '&quot;', "'": '&apos;'})


def parse_runs(text):
    """Split inline **bold** / _italic_ markup into (text, bold, italic) tuples."""
    pattern = r'\*\*(.+?)\*\*|_(.+?)_|([^*_]+)'
    runs = []
    for m in re.finditer(pattern, text, re.DOTALL):
        if m.group(1) is not None:
            runs.append((m.group(1), True, False))
        elif m.group(2) is not None:
            runs.append((m.group(2), False, True))
        else:
            runs.append((m.group(3), False, False))
    return runs


def runs_to_xml(runs, force_italic=False, force_bold=False):
    xml = ''
    for text, bold, italic in runs:
        if not text:
            continue
        rpr = ''
        if bold or force_bold:
            rpr += '<w:b/><w:bCs/>'
        if italic or force_italic:
            rpr += '<w:i/><w:iCs/>'
        rpr_block = f'<w:rPr>{rpr}</w:rPr>' if rpr else ''
        space = ' xml:space="preserve"' if text != text.strip() or '  ' in text else ''
        xml += f'<w:r>{rpr_block}<w:t{space}>{escape_xml(text)}</w:t></w:r>'
    return xml


def para(style, runs_xml):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs_xml}</w:p>\n'


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n'


def toc_field():
    return (
        '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:t>Right-click here and choose "Update Field" to build the table of contents.</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>\n'
    )


# ---------------------------------------------------------- content -> body xml

def content_to_xml(lines, title=None, subtitle=None, author=None):
    body = ''
    if title:
        body += para('BookTitle', runs_to_xml([(title, False, False)]))
        if subtitle:
            body += para('BookSubtitle', runs_to_xml([(subtitle, False, False)]))
        if author:
            body += para('BookAuthor', runs_to_xml([(author, False, False)]))
        body += page_break()

    last_was_break = bool(title)
    first_para = True          # nothing emitted yet at all
    prev_was_heading = False   # next body para gets FirstParagraph (no indent)

    for line in lines:
        line = line.rstrip('\n')
        stripped = line.strip()

        if stripped == '':
            if not prev_was_heading:
                body += '<w:p><w:pPr><w:pStyle w:val="BodyText"/></w:pPr></w:p>\n'
            continue

        if stripped == '[PAGEBREAK]':
            body += page_break()
            last_was_break = True
            prev_was_heading = False
            continue

        if stripped == '[TOC]':
            body += toc_field()
            last_was_break = False
            first_para = False
            prev_was_heading = False
            continue

        if line.startswith('# '):
            if not first_para and not last_was_break:
                body += page_break()   # every chapter starts on a fresh page
            body += para('Heading1', runs_to_xml([(line[2:], False, False)]))
            prev_was_heading = True
        elif line.startswith('## '):
            body += para('Heading2', runs_to_xml([(line[3:], False, False)]))
            prev_was_heading = True
        elif line.startswith('### '):
            body += para('Heading3', runs_to_xml([(line[4:], False, False)]))
            prev_was_heading = True
        elif line.startswith('~') and line.endswith('~') and len(line) > 1:
            body += para('BodyText', runs_to_xml(parse_runs(line[1:-1]), force_italic=True))
            prev_was_heading = False
        elif line.startswith('> '):
            body += para('BookQuote', runs_to_xml(parse_runs(line[2:])))
            prev_was_heading = False
        elif line.startswith('- '):
            body += para('BulletItem', runs_to_xml(parse_runs('•  ' + line[2:])))
            prev_was_heading = False
        elif line.startswith('**') and line.endswith('**') and not line[2:-2].count('**'):
            body += para('BodyText', runs_to_xml(parse_runs(line[2:-2]), force_bold=True))
            prev_was_heading = False
        else:
            style = 'FirstParagraph' if prev_was_heading else 'BodyText'
            body += para(style, runs_to_xml(parse_runs(line)))
            prev_was_heading = False

        last_was_break = False
        first_para = False

    return body


# ------------------------------------------------------------- default template

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
</Relationships>"""

FOOTER = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr {W}>
<w:p><w:pPr><w:jc w:val="center"/></w:pPr>
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>
</w:ftr>"""


def _style(sid, name, based, ppr, rpr, heading_lvl=None):
    outline = f'<w:outlineLvl w:val="{heading_lvl}"/>' if heading_lvl is not None else ''
    keep = '<w:keepNext/>' if heading_lvl is not None else ''
    based_x = f'<w:basedOn w:val="{based}"/>' if based else ''
    return (f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{name}"/>{based_x}'
            f'<w:pPr>{keep}{ppr}{outline}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>')


STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {W}>
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Georgia" w:hAnsi="Georgia" w:eastAsia="Georgia" w:cs="Georgia"/>
<w:sz w:val="24"/><w:szCs w:val="24"/>
</w:rPr></w:rPrDefault><w:pPrDefault/></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
{_style('BookTitle', 'Book Title', None,
        '<w:jc w:val="center"/><w:spacing w:before="3600" w:after="240"/>',
        '<w:b/><w:sz w:val="56"/><w:szCs w:val="56"/>')}
{_style('BookSubtitle', 'Book Subtitle', None,
        '<w:jc w:val="center"/><w:spacing w:after="240"/>',
        '<w:i/><w:color w:val="595959"/><w:sz w:val="32"/><w:szCs w:val="32"/>')}
{_style('BookAuthor', 'Book Author', None,
        '<w:jc w:val="center"/><w:spacing w:before="720"/>',
        '<w:sz w:val="28"/><w:szCs w:val="28"/>')}
{_style('Heading1', 'heading 1', None,
        '<w:spacing w:before="480" w:after="360"/>',
        '<w:b/><w:sz w:val="36"/><w:szCs w:val="36"/>', heading_lvl=0)}
{_style('Heading2', 'heading 2', None,
        '<w:spacing w:before="360" w:after="180"/>',
        '<w:b/><w:sz w:val="28"/><w:szCs w:val="28"/>', heading_lvl=1)}
{_style('Heading3', 'heading 3', None,
        '<w:spacing w:before="280" w:after="140"/>',
        '<w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/>', heading_lvl=2)}
{_style('BodyText', 'Body Text', None,
        '<w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:ind w:firstLine="360"/>', '')}
{_style('FirstParagraph', 'First Paragraph', 'BodyText',
        '<w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:ind w:firstLine="0"/>', '')}
{_style('BookQuote', 'Book Quote', 'BodyText',
        '<w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:ind w:left="720" w:firstLine="0"/>',
        '<w:i/>')}
{_style('BulletItem', 'Bullet Item', 'BodyText',
        '<w:spacing w:after="60" w:line="276" w:lineRule="auto"/><w:ind w:left="425" w:firstLine="0"/>', '')}
</w:styles>"""

DEFAULT_SECTPR = ('<w:sectPr><w:footerReference w:type="default" r:id="rId2"/>'
                  '<w:pgSz w:w="12240" w:h="15840"/>'
                  '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                  'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')


def build_document_xml(body, sectpr):
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<w:document {W} {R} '
            'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="">'
            f'<w:body>\n{body}{sectpr}</w:body></w:document>')


# --------------------------------------------------------------------- builders

def create_default(body, output_path):
    doc = build_document_xml(body, DEFAULT_SECTPR)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', ROOT_RELS)
        z.writestr('word/_rels/document.xml.rels', DOC_RELS)
        z.writestr('word/styles.xml', STYLES)
        z.writestr('word/footer1.xml', FOOTER)
        z.writestr('word/document.xml', doc)


def create_from_sample(body, output_path, sample_path):
    """Clone the sample docx wholesale, replace the body, keep its page setup.
    The sample must define the style names used by the markup (Heading1..3, BodyText);
    missing styles fall back to Word defaults — cosmetic, not fatal."""
    shutil.copy2(sample_path, output_path)
    with zipfile.ZipFile(output_path, 'r') as zin:
        files = {n: zin.read(n) for n in zin.namelist()}

    old_doc = files['word/document.xml'].decode('utf-8')
    sects = re.findall(r'<w:sectPr(?:\s[^>]*)?(?:/>|>.*?</w:sectPr>)', old_doc, re.DOTALL)
    sectpr = sects[-1] if sects else '<w:sectPr/>'

    files['word/document.xml'] = build_document_xml(body, sectpr).encode('utf-8')
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)


def compile_book(content_file, output_path, title=None, subtitle=None, author=None,
                 sample=None):
    with open(content_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    body = content_to_xml(lines, title=title, subtitle=subtitle, author=author)
    if sample:
        create_from_sample(body, output_path, sample)
    else:
        create_default(body, output_path)
    print(f'Created: {output_path}')


# --------------------------------------------------------------------- selftest

def selftest():
    content = (
        "[TOC]\n\n# Chapter one\n~A tagline in italics~\n\nFirst paragraph after the "
        "heading with **bold** and _italic_ inline.\nSecond paragraph, plain.\n\n"
        "## A section\n> A quoted aside.\n- first bullet\n- second bullet\n"
        "**A bold closing beat**\n[PAGEBREAK]\nText after a manual break.\n"
        "# Chapter two\nBody of chapter two.\n"
    )
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, 'content.txt')
        with open(src, 'w', encoding='utf-8') as f:
            f.write(content)

        out1 = os.path.join(td, 'default.docx')
        compile_book(src, out1, title='Test Book', subtitle='A Subtitle', author='An Author')
        with zipfile.ZipFile(out1) as z:
            assert z.testzip() is None
            doc = z.read('word/document.xml').decode('utf-8')
            minidom.parseString(doc)
            minidom.parseString(z.read('word/styles.xml').decode('utf-8'))
            minidom.parseString(z.read('word/footer1.xml').decode('utf-8'))
        assert 'TOC \\o' in doc, 'TOC field missing'
        assert doc.count('<w:br w:type="page"/>') >= 3, 'title/chapter/manual breaks missing'
        assert 'Heading1' in doc and 'BookQuote' in doc and 'BulletItem' in doc
        assert '•' in doc, 'bullet glyph missing'

        out2 = os.path.join(td, 'cloned.docx')
        compile_book(src, out2, sample=out1)   # clone the default build as its own sample
        with zipfile.ZipFile(out2) as z:
            assert z.testzip() is None
            doc2 = z.read('word/document.xml').decode('utf-8')
            minidom.parseString(doc2)
            assert 'word/styles.xml' in z.namelist(), 'cloned styles lost'
        assert '<w:footerReference' in doc2, "sample's sectPr (page numbers) not preserved"
    print('selftest OK')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Compile a book content file into .docx')
    ap.add_argument('content', nargs='?', help='master content .txt (markup in docstring)')
    ap.add_argument('output', nargs='?', help='output .docx path')
    ap.add_argument('--title')
    ap.add_argument('--subtitle')
    ap.add_argument('--author')
    ap.add_argument('--sample', help='docx to clone formatting from')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()

    if args.selftest:
        selftest()
        sys.exit(0)
    if not args.content or not args.output:
        ap.error('content and output are required (or use --selftest)')
    compile_book(args.content, args.output, title=args.title, subtitle=args.subtitle,
                 author=args.author, sample=args.sample)
