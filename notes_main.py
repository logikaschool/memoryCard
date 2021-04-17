from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,  QPushButton,
 QHBoxLayout, QVBoxLayout, QLabel, 
 QMessageBox, QRadioButton, QGroupBox, QButtonGroup, QLineEdit,
 QTextEdit, QListWidget, QInputDialog)

import json

app = QApplication([])


notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900,600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')

button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметку по тегу')

field_text = QTextEdit() 

layout_notes = QHBoxLayout()

col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
col_2.addLayout(row_1)

col_2.addWidget(button_note_save)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)

col_2.addWidget(field_tag)

row_2 = QHBoxLayout()
row_2.addWidget(button_tag_add)
row_2.addWidget(button_tag_del)
col_2.addLayout(row_2)
col_2.addWidget(button_tag_search)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)

notes_win.setLayout(layout_notes)
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавление заметки', 'Заметка:')
    if note_name != '' and ok:
        notes[note_name] = {'текст':'','теги':[]}
        list_notes.addItem(note_name)
        print(notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, ensure_ascii=False, sort_keys=True)
        print(notes)
    else:
        print('Не выбрана заметка для удаления')

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, ensure_ascii=False, sort_keys=True)
        print(notes)
    else:
        print('Не выбрана заметка для сохранения')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag != '' and not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        else:
            print('пустой тег или такой тег уже есть у заметки')
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, ensure_ascii=False, sort_keys=True)
        print(notes)
    else:
        print('Не выбрана заметка для добавления тега')
def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, ensure_ascii=False, sort_keys=True)
        print(notes)
    else:
        print('Не выбрана заметка для удаления тега')

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать заметку по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]


        button_tag_search.setText('Сбросить фильтр')
        list_notes.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == 'Сбросить фильтр':
        field_tag.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметку по тегу')
        list_tags.clear()

button_tag_search.clicked.connect(search_tag)
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)



notes_win.show()


with open('notes_data.json', 'r') as file:
    notes = json.load(file)

list_notes.addItems(notes)


app.exec_()