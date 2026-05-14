#!/usr/bin/env python3
"""
Script untuk membuat file SINOPSIS_TESIS_S2.docx
Format bahasa manusia 100% akademis
"""
import zipfile
import os

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>
    <w:rPr><w:sz w:val="24"/><w:szCs w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr>
  </w:style>
</w:styles>'''


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def para(text, style=None, bold=False, center=False):
    ppr = ''
    if style or center:
        inner = ''
        if style:
            inner += f'<w:pStyle w:val="{style}"/>'
        if center:
            inner += '<w:jc w:val="center"/>'
        ppr = f'<w:pPr>{inner}</w:pPr>'
    rpr = '<w:rPr><w:b/></w:rPr>' if bold else ''
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'


def empty():
    return '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>'


def make_table(rows):
    num_cols = len(rows[0])
    col_width = 9000 // num_cols
    tbl = '<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/><w:tblBorders>'
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        tbl += f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
    tbl += '</w:tblBorders></w:tblPr><w:tblGrid>'
    for _ in range(num_cols):
        tbl += f'<w:gridCol w:w="{col_width}"/>'
    tbl += '</w:tblGrid>'
    for i, row in enumerate(rows):
        tbl += '<w:tr>'
        for cell in row:
            brpr = '<w:rPr><w:b/></w:rPr>' if i == 0 else ''
            tbl += f'<w:tc><w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/></w:tcPr>'
            tbl += f'<w:p><w:r>{brpr}<w:t xml:space="preserve">{esc(cell)}</w:t></w:r></w:p></w:tc>'
        tbl += '</w:tr>'
    tbl += '</w:tbl>'
    return tbl


def build_content():
    """Isi dokumen ditulis terpisah di fungsi content_*"""
    from content_parts import get_all_paragraphs
    return get_all_paragraphs()


def create_docx(output_path, body_xml):
    doc = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', doc)
        zf.writestr('word/styles.xml', STYLES)
    print(f"File berhasil dibuat: {output_path}")
    print(f"Ukuran: {os.path.getsize(output_path)} bytes")


if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/projects/sandbox/Discuss')
    from content_parts import get_all_paragraphs
    body = get_all_paragraphs()
    create_docx('/projects/sandbox/Discuss/SINOPSIS_TESIS_S2.docx', body)
