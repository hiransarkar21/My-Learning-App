import sys
import threading
import PyPDF2
import pyttsx3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from docx import Document
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

font = QFont("Ubuntu")
font.setWordSpacing(1.5)
font.setLetterSpacing(QFont.AbsoluteSpacing, 1)


def speaking_engine(*text):

    complete_text = "".join(text)
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    engine.say(complete_text)
    engine.runAndWait()


class Dialog_for_Creating_file(QDialog):

    def closeEvent(self, QCloseEvent):
        window.create_file_button_clicked()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__(parent=None)

        self.is_new_file_opened_for_saving = False
        self.is_existing_file_opened_for_saving = False
        self.mainwindow_height = 690
        self.mainwindow_width = 1000
        self.mainwindow_window_configuration()
        self.mainwindow_user_interface()

    def mainwindow_window_configuration(self):

        self.setGeometry(200, 35, self.mainwindow_width, self.mainwindow_height)
        self.setFixedHeight(self.mainwindow_height)
        self.setFixedWidth(self.mainwindow_width)
        self.setWindowTitle("My Learning App")
        self.setFont(font)

    def mainwindow_user_interface(self):

        default_header_style = QLabel(self)
        default_header_style.move(0, 0)
        default_header_style.resize(self.mainwindow_width, 40)
        default_header_style.setStyleSheet("border: 0px medium; background-color: auto;")

        new_file_button = QPushButton(self)
        new_file_button.resize(100, 32)
        new_file_button.move(20, 3)
        new_file_button.setText("New File")
        new_file_button.setFont(font)
        new_file_button.setStyleSheet("background-color: auto; border: 0px medium; font-size: 13px;")
        new_file_button.clicked.connect(self.new_file_button_clicked)

        open_file_button = QPushButton(self)
        open_file_button.resize(100, 32)
        open_file_button.setText("Open File")
        open_file_button.move(107, 3)
        open_file_button.setFont(font)
        open_file_button.setStyleSheet("background-color: auto; border: 0px medium; font-size: 13px;")
        open_file_button.clicked.connect(self.open_file_button_clicked)

        self.save_file_button = QPushButton(self)
        self.save_file_button.move(200, 3)
        self.save_file_button.resize(100, 32)
        self.save_file_button.setText("Save File")
        self.save_file_button.setFont(font)
        self.save_file_button.setStyleSheet("background-color: auto; border: 0px medium; font-size: 13px;")
        self.save_file_button.clicked.connect(self.save_file_button_clicked)

        todo_button = QPushButton(self)
        todo_button.move(self.mainwindow_width - 440, 3)
        todo_button.setText("Todo Window")
        todo_button.resize(110, 32)
        todo_button.setFont(font)
        todo_button.setStyleSheet("background-color: auto; border: 0px medium; font-size: 13px;")
        todo_button.clicked.connect(self.todo_window)

        pdf_to_audiobook = QPushButton(self)
        pdf_to_audiobook.move(self.mainwindow_width - 315, 3)
        pdf_to_audiobook.resize(130, 33)
        pdf_to_audiobook.setText("Pdf to Audiobook")
        pdf_to_audiobook.setFont(font)
        pdf_to_audiobook.setStyleSheet("background-color: auto; border: 0px medium; font-size: 13px;")
        pdf_to_audiobook.clicked.connect(self.convert_pdf_to_audiobook)

        summarize_button = QPushButton(self)
        summarize_button.resize(100, 32)
        summarize_button.setText("Summarize")
        summarize_button.setFont(font)
        summarize_button.move(int(self.mainwindow_width - 180), 3)
        summarize_button.setStyleSheet("background-color: auto; border: 0px medium; font-size: 13px;")
        summarize_button.clicked.connect(self.summarize)

        settings_button = QPushButton(self)
        settings_button.resize(90, 32)
        settings_button.setText("Settings")
        settings_button.setFont(font)
        settings_button.move(self.mainwindow_width - 90, 3)
        settings_button.setStyleSheet("background-color: auto; border: 0px medium; font-size: 13px;")
        settings_button.clicked.connect(self.settings_window)

        self.default_startup_note = QLabel(self)
        self.default_startup_note.move(255, 250)
        self.default_startup_note.setText("\t\t\tWelcome to My Learning App\n\n\t\tPlease open or create a new file"
                                          " to work on")
        self.default_startup_note.setStyleSheet("color: black;  font-size: 13px;")

        self.default_startup_new_file_button = QPushButton(self)
        self.default_startup_new_file_button.move(360, 340)
        self.default_startup_new_file_button.setText("New File")
        self.default_startup_new_file_button.resize(120, 35)

        self.default_startup_new_file_button.setStyleSheet("background-color: #ccccca; color: black;\
         border:0px medium; border-radius: 4px; font-size: 13px;")
        self.default_startup_new_file_button.clicked.connect(self.new_file_button_clicked)

        self.default_startup_open_file_button = QPushButton(self)
        self.default_startup_open_file_button.move(500, 340)
        self.default_startup_open_file_button.setText("Open File")
        self.default_startup_open_file_button.resize(120, 35)
        self.default_startup_open_file_button.setStyleSheet("background-color: #ccccca; color: black; ;\
        border: 0px medium; border-radius: 4px; font-size: 13px;")
        self.default_startup_open_file_button.clicked.connect(self.open_file_button_clicked)

    def new_file_button_clicked(self):

        # closing existing widgets

        self.default_startup_note.close()
        # self.default_startup_screen.close()
        self.default_startup_new_file_button.close()
        self.default_startup_open_file_button.close()

        # showing default screen before loading the file

        self.new_writing_area = QTextEdit(self)
        self.new_writing_area.move(6, 40)
        self.new_writing_area.resize(985, 620)
        self.new_writing_area.setFont(font)
        self.new_writing_area.setAcceptRichText(True)
        self.new_writing_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.new_writing_area.setStyleSheet("background-color: #dbdbd3; color: black; \
                padding-right: 15px; padding-left: 15px; padding-top: 15px; padding-bottom: 15px;\
                border: 0px medium; border-radius: 2px; font-size: 13px;")
        self.new_writing_area.show()

        self.dialog_for_creating_new_file = Dialog_for_Creating_file(self)
        self.dialog_for_creating_new_file.setFixedWidth(450)
        self.dialog_for_creating_new_file.setFixedHeight(350)
        self.dialog_for_creating_new_file.setFont(font)
        self.dialog_for_creating_new_file.setWindowTitle("Create a File")

        window_label = QLabel("Create New File", self.dialog_for_creating_new_file)
        window_label.move(170, 30)
        window.setStyleSheet("font-size: 13px;")

        name_label = QLabel("Name ", self.dialog_for_creating_new_file)
        name_label.move(50, 100)
        name_label.setStyleSheet("font-size: 13px;")

        self.get_file_name = QLineEdit(self.dialog_for_creating_new_file)
        self.get_file_name.move(100, 95)
        self.get_file_name.resize(220, 30)
        self.get_file_name.setPlaceholderText("my_file.txt | my_file.docx".center(0))
        self.get_file_name.setStyleSheet("font-size: 13px; background-color: #dbdbd3; border: 0px medium;\
                border-radius: 3px; padding-right: 15px; padding-left: 15px;")

        location_label = QLabel(self.dialog_for_creating_new_file)
        location_label.move(50, 150)
        location_label.setText("Path")
        location_label.setStyleSheet("font-size: 12px;")

        self.get_file_path_initial = QLineEdit(self.dialog_for_creating_new_file)
        self.get_file_path_initial.move(100, 145)
        self.get_file_path_initial.resize(220, 30)
        self.get_file_path_initial.setReadOnly(True)
        self.get_file_path_initial.setPlaceholderText("Location".center(30))
        self.get_file_path_initial.setStyleSheet("font-size: 13px; background-color: #dbdbd3; border: 0px medium;\
                border-radius: 3px; padding-right: 10px; padding-left: 10px;")

        get_file_path_dialog_button = QPushButton(self.dialog_for_creating_new_file)
        get_file_path_dialog_button.resize(30, 30)
        get_file_path_dialog_button.move(330, 145)
        get_file_path_dialog_button.setText("...")
        get_file_path_dialog_button.setStyleSheet("border: 0px medium; border-radius: 3px; background-color: #dbdbd3;\
        font-size: 15px;")
        get_file_path_dialog_button.clicked.connect(self.get_actual_path_by_QFileDialog)

        self.create_file_button = QPushButton(self.dialog_for_creating_new_file)
        self.create_file_button.move(170, 250)
        self.create_file_button.resize(120, 35)
        self.create_file_button.setText("Create")
        self.create_file_button.setStyleSheet("font-size: 13px; background-color: black; border: 0px medium;\
                border-radius: 3px; padding-right: 10px; padding-left: 10px; color: white;")
        self.create_file_button.clicked.connect(self.create_file_button_clicked)

        footer_note = QLabel(self.dialog_for_creating_new_file)
        footer_note.move(110, 320)
        footer_note.setText(" *Please do not use pdf as an extension")
        footer_note.setStyleSheet("font-size: 11px;")

        self.dialog_for_creating_new_file.exec_()

    def get_actual_path_by_QFileDialog(self):

        initial_path = QFileDialog.getExistingDirectory(self, "Choose Folder", "")
        self.get_file_path_initial.setText(initial_path[0:10000])
        self.get_actual_path_of_new_file = initial_path[0:10000] + "/" + self.get_file_name.text()

    def create_file_button_clicked(self):

        if len(self.get_file_name.text()) > 1 and len(self.get_file_path_initial.text()) > 2:
            self.is_new_file_opened_for_saving = True
            self.dialog_for_creating_new_file.close()

        else:

            self.dialog_for_creating_new_file.close()
            self.new_writing_area.close()
            self.default_startup_note.show()
            self.default_startup_open_file_button.show()
            self.default_startup_new_file_button.show()

    def open_file_button_clicked(self):

        self.new_opening_and_editing_area = QTextEdit(self)
        self.new_opening_and_editing_area.resize(985, 620)
        self.new_opening_and_editing_area.move(6, 40)
        self.new_opening_and_editing_area.setAcceptRichText(True)
        self.new_opening_and_editing_area.setFont(font)
        self.new_opening_and_editing_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.new_opening_and_editing_area.setStyleSheet("background-color: #dbdbd3; color: black; \
                                   padding-right: 15px; padding-left: 15px; padding-top: 15px; padding-bottom: 15px;\
                                   border: 0px medium; border-radius: 2px; font-size: 13px;")
        self.new_opening_and_editing_area.show()

        choose_file = QFileDialog.getOpenFileName(self, "Open a file", "", "Text Documents (*.txt);;\
        Word document(*.docx);;PDF (*.pdf)")
        self.location_of_the_file_to_be_opened = choose_file[0]

        try:
            if len(self.location_of_the_file_to_be_opened) >= 2:
                if self.location_of_the_file_to_be_opened.endswith(".txt"):

                    with open(self.location_of_the_file_to_be_opened, "rt") as alpha_file:
                        data = alpha_file.read()
                        alpha_file.close()

                    self.new_opening_and_editing_area.setText(data)
                    self.is_existing_file_opened_for_saving = True

                elif self.location_of_the_file_to_be_opened.endswith(".docx"):

                    loading_file = Document(self.location_of_the_file_to_be_opened)
                    data = []
                    for paras in loading_file.paragraphs:
                        data.append(paras.text)

                    cleaned_data = "\n".join(data)
                    self.new_opening_and_editing_area.setText(str(cleaned_data))
                    self.is_existing_file_opened_for_saving = True

                elif self.location_of_the_file_to_be_opened.endswith(".pdf"):

                    file = open(self.location_of_the_file_to_be_opened, "rb")
                    data = ""
                    pdf_reader = PyPDF2.PdfFileReader(file)
                    for page in range(int(pdf_reader.getNumPages())):
                        page_object = pdf_reader.getPage(page)
                        data += page_object.extractText()

                    file.close()
                    self.new_opening_and_editing_area.setText(data)
                    self.new_opening_and_editing_area.setReadOnly(True)
            else:
                self.new_opening_and_editing_area.close()
                self.default_startup_open_file_button.show()
                self.default_startup_new_file_button.show()
                self.default_startup_note.show()

        except:
            if __name__ == "__main__":
                thread = threading.Thread(target=speaking_engine, args="Error loading file")
                thread.start()

            self.new_opening_and_editing_area.close()
            self.default_startup_open_file_button.show()
            self.default_startup_new_file_button.show()
            self.default_startup_note.show()

        else:
            pass

    def save_file_button_clicked(self):

        if self.is_new_file_opened_for_saving == False and self.is_existing_file_opened_for_saving == False:
            if __name__ == "__main__":
                thread = threading.Thread(target=speaking_engine, args="Please select a file")
                thread.start()

        elif self.is_new_file_opened_for_saving:

            data = self.new_writing_area.toPlainText()
            alpha_file = open(self.get_actual_path_of_new_file, "w")
            alpha_file.write(data)
            alpha_file.close()

        elif self.is_existing_file_opened_for_saving:

            data = self.new_opening_and_editing_area.toPlainText()
            alpha_file = open(self.location_of_the_file_to_be_opened, "w")
            alpha_file.write(data)
            alpha_file.close()

        else:
            pass

    def todo_window(self):

        class TodoWindow(QWidget):

            def __init__(self):
                super().__init__()

                self.todo_window_height = 570
                self.todo_window_width = 650

                self.todo_window_configuration()
                self.todo_window_user_interface()

            def todo_window_configuration(self):

                self.setGeometry(350, 70, self.todo_window_width, self.todo_window_height)
                self.setFixedHeight(self.todo_window_height)
                self.setFixedWidth(self.todo_window_width)
                self.setWindowTitle("Manage Todos")
                self.setFont(font)

            def todo_window_user_interface(self):

                window_label = QLabel(self)
                window_label.setText("Task Handler")
                window_label.move(260, 40)
                window_label.setStyleSheet("font-size: 13px;")

                self.text_for_todo_window_functions = QLineEdit(self)
                self.text_for_todo_window_functions.move(140, 110)
                self.text_for_todo_window_functions.resize(300, 35)
                self.text_for_todo_window_functions.setPlaceholderText("Items or Text".center(45))
                self.text_for_todo_window_functions.setStyleSheet("border: 0px medium; border-radius: 3px; \
                font-size: 12px; padding-left: 10px; padding-right: 10px;\
                background-color: #dbdbd3;")

                self.todo_section = QListWidget(self)
                self.todo_section.move(30, 170)
                self.todo_section.resize(460, 250)
                self.todo_section.setUpdatesEnabled(True)
                self.todo_section.setStyleSheet("border: 0px medium; background-color: #e0e0de; border: 0px medium; \
                border-radius: 3px; padding-top: 15px; padding-bottom: 15px; font-size: 13px;")

                self.add_task_to_todo_section = QPushButton(self)
                self.add_task_to_todo_section.resize(120, 35)
                self.add_task_to_todo_section.setText("Add Task")
                self.add_task_to_todo_section.move(510, 195)
                self.add_task_to_todo_section.setStyleSheet("border: 0px medium; background-color: #dbdbd3;\
                border-radius: 3px; font-size: 13px;")
                self.add_task_to_todo_section.clicked.connect(self.add_task_to_todo_section_button_clicked)

                self.delete_task_from_todo_section = QPushButton(self)
                self.delete_task_from_todo_section.setText("Delete Task")
                self.delete_task_from_todo_section.resize(120, 35)
                self.delete_task_from_todo_section.move(510, 245)
                self.delete_task_from_todo_section.setStyleSheet("border: 0px medium; background-color: #dbdbd3;\
                border-radius: 3px; font-size: 12px;")
                self.delete_task_from_todo_section.clicked.connect(self.delete_task_from_todo_section_button_clicked)

                self.clear_tasks_from_todo_section = QPushButton(self)
                self.clear_tasks_from_todo_section.setText("Clear Section")
                self.clear_tasks_from_todo_section.resize(120, 35)
                self.clear_tasks_from_todo_section.move(510, 295)
                self.clear_tasks_from_todo_section.setStyleSheet("border: 0px medium; background-color: #dbdbd3;\
                border-radius: 3px; font-size: 12px;")
                self.clear_tasks_from_todo_section.clicked.connect(self.clear_tasks_from_todo_section_button_clicked)

                self.mark_complete = QPushButton(self)
                self.mark_complete.move(510, 345)
                self.mark_complete.resize(120, 35)
                self.mark_complete.setText("Mark Complete")
                self.mark_complete.setStyleSheet("border: 0px medium; background-color: #dbdbd3;\
                border-radius: 3px; font-size: 12px;")
                self.mark_complete.clicked.connect(self.mark_complete_button_clicked)

                default_done_button = QPushButton(self)
                default_done_button.move(260, 480)
                default_done_button.resize(100, 33)
                default_done_button.setText("Done")
                default_done_button.setStyleSheet("border: 0px medium; background-color: black; border-radius: 3px;\
                font-size: 13px; color: white;")
                default_done_button.clicked.connect(self.default_done_button_clicked)

            def add_task_to_todo_section_button_clicked(self):

                self.todo_section.addItem(str(self.text_for_todo_window_functions.text()))
                self.text_for_todo_window_functions.setText("")

            def delete_task_from_todo_section_button_clicked(self):

                current_row = self.todo_section.currentRow()
                self.todo_section.takeItem(current_row)

            def clear_tasks_from_todo_section_button_clicked(self):

                self.todo_section.clear()

            def mark_complete_button_clicked(self):

                current_row = self.todo_section.currentRow()
                current_item = self.todo_section.currentItem().text() + str("  < Completed > ")
                self.todo_section.takeItem(current_row)
                self.todo_section.insertItem(current_row, current_item)

            def default_done_button_clicked(self):

                self.close()

        self.todowindow = TodoWindow()
        self.todowindow.show()

    def convert_pdf_to_audiobook(self):

        class PdfToAudiobook(QWidget):
            def __init__(self):
                super().__init__()

                self.audio_format = ""
                self.pdf_to_audiobook_window_height = 470
                self.pdf_to_audiobook_window_width = 630
                self.pdf_to_audiobook_window_configuration()
                self.pdf_to_audiobook_window_user_interface()

            def pdf_to_audiobook_window_configuration(self):

                self.setGeometry(350, 90, self.pdf_to_audiobook_window_height, self.pdf_to_audiobook_window_width)
                self.setFixedHeight(self.pdf_to_audiobook_window_height)
                self.setFixedWidth(self.pdf_to_audiobook_window_width)
                self.setWindowTitle("Convert PDF to Audiobook")
                self.setFont(font)

            def pdf_to_audiobook_window_user_interface(self):

                window_label = QLabel(self)
                window_label.move(220, 60)
                window_label.setText("Convert Pdfs to Audiobook")
                window_label.setStyleSheet("font-size: 13px; ")

                location_label = QLabel(self)
                location_label.move(80, 175)
                location_label.setText("Location")
                location_label.setStyleSheet("background-color: auto; font-size: 13px;")

                self.get_location_of_pdf = QLineEdit(self)
                self.get_location_of_pdf.move(155, 165)
                self.get_location_of_pdf.resize(300, 35)
                self.get_location_of_pdf.setPlaceholderText("Location of the PDF".center(40))
                self.get_location_of_pdf.setStyleSheet("background-color:#dbdbd3; font-size: 13px;\
                padding-right: 15px; padding-left: 15px; border: 0px medium;")

                dialog_button = QPushButton(self)
                dialog_button.move(460, 165)
                dialog_button.resize(35, 35)
                dialog_button.setText("…")
                dialog_button.setStyleSheet("border: 0px medium; border-radius: 3px; background-color: #dbdbd3;\
                padding-left: 7px; padding-right: 7px; font-size: 20px; color: black;")
                dialog_button.clicked.connect(self.location_for_pdf)

                self.convert_audiobook = QPushButton(self)
                self.convert_audiobook.move(250, 250)
                self.convert_audiobook.resize(120, 33)
                self.convert_audiobook.setText("Convert")
                self.convert_audiobook.setStyleSheet("border: 0px medium; background-color: black; font-size: 13px;\
                padding-right: 10px; padding-left: 10px; color: white; border-radius: 3px;")
                self.convert_audiobook.clicked.connect(self.convert_button_clicked)
                
                footer_note = QLabel(self)
                footer_note.setText("*Please enter valid locations and wait 3s before converting another pdf")
                footer_note.move(100, 420)
                footer_note.setStyleSheet("font-size: 11px;")

            def location_for_pdf(self):

                raw_location = QFileDialog.getOpenFileName(self, "Select PDF", "", "Pdf (*.pdf);;")
                self.pdf_location = raw_location[0]

                if self.pdf_location == "":
                    if __name__ == "__main__":
                        thread = threading.Thread(target=speaking_engine, args=" Select a valid pdf file")
                        thread.start()

                else:
                    self.get_location_of_pdf.setText(self.pdf_location)

            def convert_button_clicked(self):

                initial_location = QFileDialog.getSaveFileName(self, "Save File", "", "MP3 File (*.mp3);;\
                WAV File (*.wav);;WEBM (*.wav);;")

                output_file_name_and_location = initial_location[0]

                if output_file_name_and_location == "":
                    thread = threading.Thread(target=speaking_engine, args="Please use a valid filename and location")
                    thread.start()

                else:
                    file = open(self.pdf_location, "rb")
                    data = ""
                    pdf_reader = PyPDF2.PdfFileReader(file)
                    for page in range(int(pdf_reader.getNumPages())):
                        page_object = pdf_reader.getPage(page)
                        data += page_object.extractText()

                    file.close()

                    # saving the file

                    engine = pyttsx3.init()
                    engine.setProperty("rate", 180)
                    engine.save_to_file(data, output_file_name_and_location)
                    engine.runAndWait()

        self.pdf_to_audiobook_window = PdfToAudiobook()
        self.pdf_to_audiobook_window.show()

    def summarize(self):

        class SummarizeWindow(QWidget):

            self.summary = ''

            def __init__(self):
                super().__init__()

                self.summarize_window_height = 570
                self.summarize_window_width = 650
                self.summarize_window_configuration()
                self.summarize_window_user_interface()

            def summarize_window_configuration(self):

                self.setGeometry(350, 90, self.summarize_window_height, self.summarize_window_width)
                self.setFixedHeight(self.summarize_window_height)
                self.setFixedWidth(self.summarize_window_width)
                self.setWindowTitle("Text Summarizer")
                self.setFont(font)

            def summarize_window_user_interface(self):

                window_label = QLabel(self)
                window_label.move(270, 40)
                window_label.setText("Text Summarizer")
                window_label.setStyleSheet("font-size: 13px;")

                self.get_original_text_for_summarizing = QTextEdit(self)
                self.get_original_text_for_summarizing.move(37, 100)
                self.get_original_text_for_summarizing.resize(575, 250)
                self.get_original_text_for_summarizing.setFont(font)
                self.get_original_text_for_summarizing.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.get_original_text_for_summarizing.setStyleSheet("font-size: 13px; padding-right: 10px; \
                background-color: #dbdbd3;padding-left: 10px; padding-top: 10px; padding-bottom: 10px; \
                border: 0px medium; border-radius: 3px;")

                import_clipboard_button = QPushButton(self)
                import_clipboard_button.move(460, 370)
                import_clipboard_button.setText("Import Clipboard")
                import_clipboard_button.resize(140, 32)
                import_clipboard_button.setStyleSheet("border: 0px medium; background-color: black; border: 0px medium;\
                border-radius: 3px; color: white; font-size: 12px;")
                import_clipboard_button.clicked.connect(self.import_clipboard_button_clicked)

                self.summarize_button = QPushButton(self)
                self.summarize_button.move(270, 470)
                self.summarize_button.resize(130, 34)
                self.summarize_button.setText("Summarize")
                self.summarize_button.setStyleSheet("border: 0px medium; font-size: 12px;\
                background-color: black; color: white; border-radius: 3px;")
                self.summarize_button.clicked.connect(self.summarize_button_clicked)

                self.export_button = QPushButton(self)
                self.export_button.move(270, 470)
                self.export_button.resize(130, 34)
                self.export_button.setText("Export")
                self.export_button.setStyleSheet("border: 0px medium; font-size: 12px;\
                background-color: black; color: white; border-radius: 3px;")
                self.export_button.clicked.connect(self.export_button_clicked)
                self.export_button.close()

            def import_clipboard_button_clicked(self):
                
                data = QApplication.clipboard().text().strip()
                self.get_original_text_for_summarizing.setText(str(data))

            def summarize_button_clicked(self):

                text = self.get_original_text_for_summarizing.toPlainText()

                if self.get_original_text_for_summarizing.toPlainText().strip() == "":
                    if __name__ == "__main__":
                        thread = threading.Thread(target=speaking_engine, args="Please use valid text in the box above.")
                        thread.start()

                else:
                    stopWords = set(stopwords.words("english"))
                    words = word_tokenize(text)

                    word_frequencies = dict()
                    for word in words:
                        word = word.lower()
                        if word in stopWords:
                            continue
                        if word in word_frequencies:
                            word_frequencies[word] += 1
                        else:
                            word_frequencies[word] = 1

                    sentences = sent_tokenize(text)
                    sentence_value = dict()

                    for sentence in sentences:
                        for word, freq in word_frequencies.items():
                            if word in sentence.lower():
                                if sentence in sentence_value:
                                    sentence_value[sentence] += freq
                                else:
                                    sentence_value[sentence] = freq

                    sumValues = 0
                    for sentence in sentence_value:
                        sumValues += sentence_value[sentence]

                    average = int(sumValues / len(sentence_value))

                    self.summary = ''
                    for sentence in sentences:
                        if (sentence in sentence_value) and (sentence_value[sentence] > (1.2 * average)):
                            self.summary += " " + sentence

                    self.summarize_button.close()
                    self.export_button.show()

            def export_button_clicked(self):

                initial_location = QFileDialog.getSaveFileName(self, "Save File", "", "Text File(*.txt);;")
                complete_location = initial_location[0]

                file = open(complete_location, "w", encoding="utf-8")
                file.write(self.summary)
                file.close()

        self.summarize_window = SummarizeWindow()
        self.summarize_window.show()

    def settings_window(self):

        class SettingsWindow(QWidget):

            def __init__(self):
                super().__init__()

                self.settings_window_height = 470
                self.settings_window_width = 600
                self.settings_window_configuration()
                self.settings_window_user_interface()

            def settings_window_configuration(self):

                self.setGeometry(350, 90, self.settings_window_height, self.settings_window_width)
                self.setFixedHeight(self.settings_window_height)
                self.setFixedWidth(self.settings_window_width)
                self.setWindowTitle("Settings")
                self.setFont(font)

            def settings_window_user_interface(self):

                window_label = QLabel(self)
                window_label.setText("User Settings")
                window_label.move(250, 40)
                window_label.setStyleSheet("font-size: 13px;")

                help_button = QPushButton(self)
                help_button.move(80, 140)
                help_button.resize(140, 35)
                help_button.setText("Get Help")
                help_button.setStyleSheet("border: 0px medium; border-radius: 3px; background-color: #c9c9c5;\
                font-size: 13px; padding-right: 10px; padding-left: 10px; padding-bottom:5px; \
                padding-top: 5px;")
                help_button.clicked.connect(self.help_button_clicked)

                about_button = QPushButton(self)
                about_button.move(80, 190)
                about_button.resize(140, 35)
                about_button.setText("About Us")
                about_button.setStyleSheet("border: 0px medium; border-radius: 3px; background-color: #c9c9c5;\
                font-size: 13px;padding-right: 10px; padding-left: 10px; padding-bottom:5px; \
                padding-top: 5px;")
                about_button.clicked.connect(self.about_button_clicked)

                footer_note = QLabel(self)
                footer_note.move(170, 420)
                footer_note.setText(" *Click on any button to get information")
                footer_note.setStyleSheet("font-size: 11px;")

            def help_button_clicked(self):

                class HelpWindow(QWidget):
                    def __init__(self):
                        super().__init__()

                        self.help_window_height = 580
                        self.help_window_width = 650
                        self.help_window_configuration()
                        self.help_window_user_interface()

                    def help_window_configuration(self):

                        self.setGeometry(350, 70, self.help_window_height, self.help_window_width)
                        self.setFixedHeight(self.help_window_height)
                        self.setFixedWidth(self.help_window_width)
                        self.setWindowTitle("Help Section")
                        self.setFont(font)

                    def help_window_user_interface(self):

                        window_label = QLabel(self)
                        window_label.move(280, 40)
                        window_label.setStyleSheet("font-size: 13px;")
                        window_label.setText("Help Section")

                        help_section = QTextEdit(self)
                        help_section.move(50, 90)
                        help_section.resize(550, 420)
                        help_section.setReadOnly(True)
                        help_section.setFont(font)
                        help_section.setAcceptRichText(True)
                        help_section.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                        help_section.setStyleSheet("background-color: #dbdbd3; color: black; \
                        padding-right: 15px; padding-left: 15px; padding-top: 15px; padding-bottom: 15px;\
                        border: 0px medium; border-radius: 2px; font-size: 13px;")

                        alpha_help_file = open("Help Section.txt", "r")
                        data = alpha_help_file.read()
                        alpha_help_file.close()

                        help_section.setText(data)

                self.help_window = HelpWindow()
                self.help_window.show()

            def about_button_clicked(self):

                class AboutWindow(QWidget):
                    def __init__(self):
                        super().__init__()

                        self.about_window_height = 580
                        self.about_window_width = 650
                        self.about_window_configuration()
                        self.about_window_user_interface()

                    def about_window_configuration(self):

                        self.setGeometry(350, 70, self.about_window_height, self.about_window_width)
                        self.setFixedHeight(self.about_window_height)
                        self.setFixedWidth(self.about_window_width)
                        self.setWindowTitle("About Us")
                        self.setFont(font)

                    def about_window_user_interface(self):

                        window_label = QLabel(self)
                        window_label.move(250, 80)
                        window_label.setText("About My Learning App")
                        window_label.setStyleSheet("font-size: 13px;")

                        about_us_note = QLabel(self)
                        about_us_note.move(150, 180)
                        about_us_note.setText("My Learning App is a fully featured learning app\nmeant for "
                                              "students.The main features of the app\nincludes creating new files, "
                                              "opening files,to-do,\nconverting pdfs into audiobooks, "
                                              "summarizing\nlarge text and converting them to paragraphs. Do\n"
                                              "enjoy my application.")
                        about_us_note.setStyleSheet("font-size: 13px;")

                        close_button = QPushButton(self)
                        close_button.setText("Close")
                        close_button.move(280, 360)
                        close_button.resize(100, 35)
                        close_button.setStyleSheet("border: 0px medium; border-radius: 3px; padding-right: 10px;\
                        padding-left: 10px; font-size: 13px; background-color: black; color: white;")

                        close_button.clicked.connect(self.close_button_clicked)

                    def close_button_clicked(self):

                        self.close()

                self.about_window = AboutWindow()
                self.about_window.show()

        self.settings_window = SettingsWindow()
        self.settings_window.show()


application = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(application.exec_())
