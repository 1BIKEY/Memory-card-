from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from memo_app import app
from memo_data import *
from memo_main_layout import *
from memo_card_layout import *
from memo_edit_layout import txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3


main_width, main_height = 1000, 450 
card_width, card_height = 600, 500 
time_unit = 60000   
                  


questions_listmodel = QuestionListModel() 
frm_edit = QuestionEdit(0, txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3) 
radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4] 
frm_card = 0 
timer = QTimer() 
win_card = QWidget() 
win_main = QWidget() 

def testlist():
    
    frm = Question('Якщо температура в пустелі досягла мінімуму, які інші обставини могли бути "самими кінцевими" для виживання?', 'Наявність питної води.', 'Відсутність каміння.', 'Відсутність піску.', 'Наявність пальми.')
    questions_listmodel.form_list.append(frm)
    frm = Question('Якщо ви розглядаєте останню сторінку улюбленої книги, яка щойно закінчилася, що б ви хотіли побачити там?', 'Заключний епілог.', 'Продовження історії.', 'Список головних персонажів.', 'Авторські коментарі.')
    questions_listmodel.form_list.append(frm)
    frm = Question('Якщо ви стоїте на вершині гори, яка може бути вашою останньою дією, що вам хочеться зробити?', 'Загадати бажання.', 'Посміхнутися на фотографію.', ' Зробити скелелазіння.', 'Випити гарячого шоколаду.')
    questions_listmodel.form_list.append(frm)
    frm = Question('Якщо ви мали б можливість обирати бескінечну їжу на обід, що ви б обрали?', 'Спеціїйований обід з усіма вашими улюбленими стравами.', 'Суші.', 'Пасту з соусом.', 'Десерт, наприклад, морозиво.')
    questions_listmodel.form_list.append(frm)
    frm = Question('Яке число "Пі" (π) представляє відношення довжини кола до його діаметру?','3.14', '2.71', '2.71', '4.76')
    questions_listmodel.form_list.append(frm)
    frm = Question('Що вивчає наука етимологія?', 'Походження та значення слів', 'Технології обробки даних', ' Вчення про мікроорганізми', 'Способи вирощування рослин')
    questions_listmodel.form_list.append(frm)
    frm = Question('Який фахівець відповідає за діагностику та лікування очних захворювань?', 'Офтальмолог', 'Психолог', 'Лікар-стоматолог', 'Лікар-терапевт')
    questions_listmodel.form_list.append(frm)


def set_card():
    ''' задає вигляд вікна карточки'''
    win_card.resize(card_width, card_height)
    win_card.move(300, 300)
    win_card.setWindowTitle('Memory Card')
    win_card.setLayout(layout_card)
    window = QMainWindow()
    palette = QPalette()
    background_color = QColor(0, 100, 160)  
    palette.setColor(QPalette.Window, background_color)
    win_main.setPalette(palette)

def sleep_card():
    ''' карточка ховається на деякий ча, який вказаний на таймері'''
    win_card.hide()
    timer.setInterval(time_unit * box_Minutes.value() )
    timer.start()

def show_card():
    ''' показує вікно (по таймеру), таймер зупиняється'''
    win_card.show()
    timer.stop()

def show_random():
    ''' показує випадкове питання '''
    global frm_card 
    frm_card = random_AnswerCheck(questions_listmodel, lb_Question, radio_list, lb_Correct, lb_Result)
    frm_card.show() 
    show_question() 

def click_OK():
    ''' перевіряє питання або загружає нове питання '''
    if btn_OK.text() == 'Наступне запитання':
        frm_card.check()
        show_result()
    else:
        show_random()

def back_to_menu():
    win_card.hide()
    win_main.showNormal()
def set_main():
    ''' задає як виглядає основне вікно'''
    win_main.resize(main_width, main_height)
    win_main.move(100, 100)
    win_main.setWindowTitle('Список запитань')
    win_main.setLayout(layout_main)
    window = QMainWindow()
    palette = QPalette()
    background_color = QColor(115, 81, 132)  
    palette.setColor(QPalette.Window, background_color)
    win_main.setPalette(palette)

def edit_question(index): 
    if index.isValid():
        i = index.row()
        frm = questions_listmodel.form_list[i]
        frm_edit.change(frm)
        frm_edit.show()

def add_form():
    questions_listmodel.insertRows() 
    last = questions_listmodel.rowCount(0) - 1      
    index = questions_listmodel.index(last) 
    list_questions.setCurrentIndex(index) 
    edit_question(index)   
    txt_Question.setFocus(Qt.TabFocusReason) 

def del_form():
    questions_listmodel.removeRows(list_questions.currentIndex().row())
    edit_question(list_questions.currentIndex())

def start_test():
    ''' на початку тесту форма звʼязується з випадковим питанням і показується'''
    show_random()
    win_card.show()
    win_main.showMinimized()


def connects():
    list_questions.setModel(questions_listmodel) 
    list_questions.clicked.connect(edit_question) 
    btn_add.clicked.connect(add_form) 
    btn_delete.clicked.connect(del_form)
    btn_start.clicked.connect(start_test) 
    btn_OK.clicked.connect(click_OK) 
    btn_Menu.clicked.connect(back_to_menu) 
    timer.timeout.connect(show_card) 
    btn_Sleep.clicked.connect(sleep_card) 


testlist()
set_card()
set_main()
connects()
win_main.show()
app.exec_()