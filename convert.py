
import re
import subprocess
import sys
import os
import time
import chardet
import fitz
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt  # 添加Qt模块
from ebooklib import epub
from bs4 import BeautifulSoup
import zipfile

class FileConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Converter')
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon("./res/icon/logo50.png"))  # 设置窗口图标
        self.label = QLabel('可将文件转换为epub文件，支持的文件格式如下:\n.txt, .csv, .py, .md,.docx,.doc,.xls,.xlsx,.pdf,.htm,.html,.mobi,.azw,.azw3',self)
        self.button = QPushButton('Convert', self)
        self.button.clicked.connect(self.convertFiles)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def convertFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Select files', os.getcwd())
        if not files:
            return

        output_file, _ = QFileDialog.getSaveFileName(self, 'Save EPUB file', os.getcwd(), 'EPUB Files (*.epub)')
        if not output_file:
            return

        self.create_epub(files, output_file)


    def return_text(self, filepath):
        file_extension = os.path.splitext(filepath)[1].lower()
        text = None
        start_reading_time = time.time()
        try:
            if file_extension in [".txt", ".csv", ".py", ".md",".docx",".doc"]:
                with open(filepath, 'rb') as file:
                    rawdata = file.read()
                    encoding = chardet.detect(rawdata)['encoding']
                    if encoding==None:
                        encoding='utf-8'
                with open(filepath, 'r', encoding=encoding, errors='ignore') as file:
                    text = file.read()
            elif file_extension in [".xls", ".xlsx"]:
                df = pd.read_excel(filepath)
                df = df.fillna('')
                text = df.to_string(index=False)
                text = re.sub(r'Unnamed: \d+', '', text)
            elif file_extension == ".pdf":
                with fitz.open(filepath) as doc:
                    text = ''
                    contains_text = False
                    for page in doc:
                        page_text = page.get_text()
                        if page_text.strip():
                            contains_text = True
                            text += page_text
                    if contains_text==False:
                        text = self.extract_text_from_image_pdf(filepath)
            elif file_extension in [".htm", ".html"]:
                with open(filepath, 'rb') as file:
                    rawdata = file.read()
                    encoding = chardet.detect(rawdata)['encoding']
                if encoding is None:
                    encoding = 'utf-8'
                with open(filepath, 'r', encoding=encoding, errors='ignore') as file:
                    html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
            elif file_extension in [".mobi", ".azw", ".azw3"]:
                file_base_name = os.path.splitext(os.path.basename(filepath))[0]
                txt_filepath = os.path.join(filepath, f'{file_base_name}.txt')
                subprocess.run(['ebook-convert', filepath, txt_filepath], check=True)
                with open(txt_filepath, 'r', encoding='utf-8', errors='ignore') as file:
                   text = file.read()
        except Exception as e:
            return None
        if text is not None:
            return text
        else:
            return None



    def create_epub(self, files, output_file):
        book = epub.EpubBook()
        for file_path in files:
            content=self.return_text(file_path)

        # Add content to epub book
        chapter = epub.EpubHtml(title=os.path.basename(file_path), file_name=os.path.basename(file_path) + '.xhtml', lang='en')
        chapter.content = '<html><body><pre>{}</pre></body></html>'.format(content)  # Wrap content in <pre> tag to preserve whitespace
        book.add_item(chapter)
        book.toc.append((chapter, os.path.basename(file_path)))

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        book.spine = ['nav'] + [item for item in book.toc]
        book.title = os.path.splitext(os.path.basename(output_file))[0]

        try:
            epub.write_epub(output_file, book, {})

            # Now, let's make sure the generated EPUB file is a valid zip archive
            with zipfile.ZipFile(output_file, 'r') as epub_zip:
                # Validate the contents
                epub_zip.testzip()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error occurred: {str(e)}", QMessageBox.Ok)
            return False

        return True

def convert_and_run():
    # 设置Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    converter = FileConverter()
    converter.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    convert_and_run()
