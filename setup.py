from cx_Freeze import setup, Executable

setup(
    name="PDF to DOCX Converter",
    version="1.0",
    description="Convert PDF files to DOCX files",
    executables=[Executable("pdf_to_docx.py")],
)
