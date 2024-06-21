import os
import re
import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from pdfminer.high_level import extract_text
from docx import Document

def clean_text_for_xml(text):
    # NULL 바이트 및 제어 문자를 제거하는 정규 표현식
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    return text

def extract_text_from_pdf(pdf_path):
    # pdfminer를 사용하여 PDF에서 텍스트 추출
    text = extract_text(pdf_path)
    text = text.replace("\n\n", "\n")
    return clean_text_for_xml(text)

def save_text_to_docx(text, docx_path):
    # DOCX 파일로 저장
    doc = Document()
    doc.add_paragraph(text)
    doc.save(docx_path)

def handle_dropped_files(event):
    pdf_path = event.data
    if (pdf_path.startswith('{') and pdf_path.endswith('}')):
        pdf_path = pdf_path[1:-1]
    print(f"PDF file dropped: {pdf_path}")
    if pdf_path.endswith('.pdf'):
        text = extract_text_from_pdf(pdf_path)
        docx_path = os.path.splitext(pdf_path)[0] + '.docx'
        save_text_to_docx(text, docx_path)
        result_label.config(text=f"Converted to DOCX and saved as {docx_path}")
    else:
        result_label.config(text="Please drop a PDF file.")

def open_file_dialog():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        text = extract_text_from_pdf(pdf_path)
        # text = translate_text(text)
        docx_path = os.path.splitext(pdf_path)[0] + '.docx'
        save_text_to_docx(text, docx_path)
        result_label.config(text=f"Converted to DOCX and saved as {docx_path}")

if __name__ == "__main__":
    # Tkinter GUI 설정
    root = TkinterDnD.Tk()
    root.title("PDF to DOCX Converter")

    # 파일 드래그 앤 드랍 영역
    drop_label = tk.Label(root, text="Drag and drop a PDF file here or click to select a file", width=50, height=10, bg="lightgray")
    drop_label.pack(pady=20)

    # 결과 표시 라벨
    result_label = tk.Label(root, text="", wraplength=400)
    result_label.pack(pady=10)

    # 파일 선택 버튼
    open_button = tk.Button(root, text="Select PDF file", command=open_file_dialog)
    open_button.pack(pady=20)

    # 드래그 앤 드랍 이벤트 바인딩
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind('<<Drop>>', handle_dropped_files)

    # Tkinter 이벤트 루프 시작
    root.mainloop()

