import zipfile
import xml.sax.saxutils as saxutils
import os

def escape(text):
    return saxutils.escape(str(text))

class DocxBuilder:
    def __init__(self, filename):
        self.filename = filename
        self.body_elements = []

    def add_title(self, text):
        xml = f"""
        <w:p>
            <w:pPr>
                <w:pStyle w:val="Title"/>
                <w:jc w:val="center"/>
                <w:spacing w:before="240" w:after="120"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:b/>
                    <w:sz w:val="48"/>
                    <w:color w:val="1F4E79"/>
                </w:rPr>
                <w:t>{escape(text)}</w:t>
            </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_subtitle(self, text):
        xml = f"""
        <w:p>
            <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:before="0" w:after="240"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:i/>
                    <w:sz w:val="24"/>
                    <w:color w:val="595959"/>
                </w:rPr>
                <w:t>{escape(text)}</w:t>
            </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_heading_1(self, text):
        xml = f"""
        <w:p>
            <w:pPr>
                <w:pStyle w:val="Heading1"/>
                <w:spacing w:before="360" w:after="120"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:b/>
                    <w:sz w:val="32"/>
                    <w:color w:val="2E75B6"/>
                </w:rPr>
                <w:t>{escape(text)}</w:t>
            </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_heading_2(self, text):
        xml = f"""
        <w:p>
            <w:pPr>
                <w:pStyle w:val="Heading2"/>
                <w:spacing w:before="240" w:after="80"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:b/>
                    <w:sz w:val="26"/>
                    <w:color w:val="1F4E79"/>
                </w:rPr>
                <w:t>{escape(text)}</w:t>
            </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_heading_3(self, text):
        xml = f"""
        <w:p>
            <w:pPr>
                <w:pStyle w:val="Heading3"/>
                <w:spacing w:before="180" w:after="60"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:b/>
                    <w:sz w:val="22"/>
                    <w:color w:val="333333"/>
                </w:rPr>
                <w:t>{escape(text)}</w:t>
            </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_paragraph(self, text, bold=False, italic=False):
        xml = f"""
        <w:p>
            <w:pPr>
                <w:spacing w:before="0" w:after="120" w:line="276" w:lineRule="auto"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:sz w:val="22"/>
                    {"<w:b/>" if bold else ""}
                    {"<w:i/>" if italic else ""}
                </w:rPr>
                <w:t>{escape(text)}</w:t>
            </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_bullet(self, bold_prefix, text):
        xml = f"""
        <w:p>
            <w:pPr>
                <w:ind w:left="480" w:hanging="240"/>
                <w:spacing w:before="40" w:after="80"/>
            </w:pPr>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/>
                    <w:sz w:val="22"/>
                </w:rPr>
                <w:t>• </w:t>
            </w:r>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:b/>
                    <w:sz w:val="22"/>
                </w:rPr>
                <w:t>{escape(bold_prefix)} </w:t>
            </w:r>
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:sz w:val="22"/>
                </w:rPr>
                <w:t>{escape(text)}</w:t>
            </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_code_block(self, code_text):
        lines = code_text.strip().split("\n")
        runs = []
        for i, line in enumerate(lines):
            runs.append(f"""
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                    <w:sz w:val="19"/>
                    <w:color w:val="2B2B2B"/>
                </w:rPr>
                <w:t xml:space="preserve">{escape(line)}</w:t>
            </w:r>
            """)
            if i < len(lines) - 1:
                runs.append("<w:r><w:br/></w:r>")

        xml = f"""
        <w:p>
            <w:pPr>
                <w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>
                <w:ind w:left="360" w:right="360"/>
                <w:spacing w:before="120" w:after="160"/>
            </w:pPr>
            {"".join(runs)}
        </w:p>
        """
        self.body_elements.append(xml)

    def add_table(self, headers, rows):
        header_cells = "".join([
            f"""
            <w:tc>
                <w:tcPr>
                    <w:shd w:val="clear" w:color="auto" w:fill="2E75B6"/>
                    <w:tcMar>
                        <w:top w:w="120" w:type="dxa"/>
                        <w:left w:w="160" w:type="dxa"/>
                        <w:bottom w:w="120" w:type="dxa"/>
                        <w:right w:w="160" w:type="dxa"/>
                    </w:tcMar>
                </w:tcPr>
                <w:p>
                    <w:pPr><w:jc w:val="left"/></w:pPr>
                    <w:r>
                        <w:rPr>
                            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                            <w:b/>
                            <w:color w:val="FFFFFF"/>
                            <w:sz w:val="20"/>
                        </w:rPr>
                        <w:t>{escape(h)}</w:t>
                    </w:r>
                </w:p>
            </w:tc>
            """ for h in headers
        ])

        rows_xml = []
        for r_idx, row in enumerate(rows):
            fill = "F9FBFD" if r_idx % 2 == 1 else "FFFFFF"
            cells = "".join([
                f"""
                <w:tc>
                    <w:tcPr>
                        <w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>
                        <w:tcMar>
                            <w:top w:w="100" w:type="dxa"/>
                            <w:left w:w="160" w:type="dxa"/>
                            <w:bottom w:w="100" w:type="dxa"/>
                            <w:right w:w="160" w:type="dxa"/>
                        </w:tcMar>
                    </w:tcPr>
                    <w:p>
                        <w:r>
                            <w:rPr>
                                <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                                <w:sz w:val="20"/>
                            </w:rPr>
                            <w:t>{escape(cell)}</w:t>
                        </w:r>
                    </w:p>
                </w:tc>
                """ for cell in row
            ])
            rows_xml.append(f"<w:tr>{cells}</w:tr>")

        xml = f"""
        <w:tbl>
            <w:tblPr>
                <w:tblW w:w="5000" w:type="pct"/>
                <w:tblBorders>
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="D9D9D9"/>
                    <w:left w:val="none"/>
                    <w:bottom w:val="single" w:sz="8" w:space="0" w:color="2E75B6"/>
                    <w:right w:val="none"/>
                    <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E6E6E6"/>
                    <w:insideV w:val="none"/>
                </w:tblBorders>
            </w:tblPr>
            <w:tr>{header_cells}</w:tr>
            {"".join(rows_xml)}
        </w:tbl>
        <w:p><w:pPr><w:spacing w:after="160"/></w:pPr></w:p>
        """
        self.body_elements.append(xml)

    def save(self):
        doc_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
            <w:body>
                {"".join(self.body_elements)}
                <w:sectPr>
                    <w:pgSz w:w="12240" w:h="15840"/>
                    <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
                </w:sectPr>
            </w:body>
        </w:document>
        """

        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
            <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
            <Default Extension="xml" ContentType="application/xml"/>
            <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
        </Types>
        """

        rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
            <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
        </Relationships>
        """

        with zipfile.ZipFile(self.filename, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml', content_types)
            z.writestr('_rels/.rels', rels)
            z.writestr('word/document.xml', doc_xml)
        print(f"Document saved successfully: {self.filename}")

print("DocxBuilder class ready")
