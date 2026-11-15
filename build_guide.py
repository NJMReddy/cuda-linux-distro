"""Generate the current verification guide without machine-specific paths."""
from pathlib import Path
from generate_guide_docx import DocxBuilder

def main():
    root=Path(__file__).resolve().parent
    doc=DocxBuilder(str(root/'HOW_TO_VERIFY_AND_TEST_GUIDE.docx'))
    doc.add_title('CUDA Linux — Verification and Demo Guide')
    doc.add_subtitle('NOT READY: build, boot, GPU and comparison evidence remains required')
    for name in ['README.md','docs/demo.md','docs/measurement-protocol.md','docs/final-audit-report.md']:
        doc.add_heading_1(name)
        file=root/name
        if not file.is_file():
            raise FileNotFoundError(file)
        for paragraph in file.read_text(encoding='utf-8').split('\n\n'):
            doc.add_paragraph(paragraph)
    doc.save()

if __name__=='__main__': main()
