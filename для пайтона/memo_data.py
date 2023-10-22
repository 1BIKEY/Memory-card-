from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from random import randint, shuffle


new_quest_templ = 'Нове запитання' 
new_answer_templ = 'Нове питання'

text_wrong = 'Невірно'
text_correct = 'Вірно'

class Question():
    ''' зберігає інформацію про одине питання'''
    def __init__(self, question=new_quest_templ, answer=new_answer_templ, 
                       wrong_answer1='', wrong_answer2='', wrong_answer3=''):
        self.question = question 
        self.answer = answer 
        self.wrong_answer1 = wrong_answer1 
        self.wrong_answer2 = wrong_answer2 
        self.wrong_answer3 = wrong_answer3 
        self.is_active = True 
        self.attempts = 0 
        self.correct = 0 
    def got_right(self):
        ''' змінює статистику, отримавши правильну відповідь'''
        self.attempts += 1
        self.correct += 1
    def got_wrong(self):
        ''' змінює статистику, отримавши неправильну відповідь'''
        self.attempts += 1

class QuestionView():
    ''' зіставляє дані і виджети для відображення питання'''
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        self.frm_model = frm_model  
        self.question = question
        self.answer = answer
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3  
    def change(self, frm_model):
        ''' оновлення даних, вже звʼязаних з інтерфейсом '''
        self.frm_model = frm_model
    def show(self):
        ''' вивід на екран всіх даних з обʼєкта '''
        self.question.setText(self.frm_model.question)
        self.answer.setText(self.frm_model.answer)
        self.wrong_answer1.setText(self.frm_model.wrong_answer1)
        self.wrong_answer2.setText(self.frm_model.wrong_answer2)
        self.wrong_answer3.setText(self.frm_model.wrong_answer3)

class QuestionEdit(QuestionView):
    ''' використовується, якщо потрібно редагувати форму: встановлює обробники подій, які зберігають текст'''
    def save_question(self):
        ''' зберігає текст питання '''
        self.frm_model.question = self.question.text() 
    def save_answer(self):
        ''' зберігає текст правильної відповіді '''
        self.frm_model.answer = self.answer.text() 
    def save_wrong(self):
        ''' зберігає всі правильні відповіді 
        (якщо у наступній версії програми число неправильних відповідей стане змінним 
        і вони будуть вводиться у список, можна буде змінити цей метод) '''
        self.frm_model.wrong_answer1 = self.wrong_answer1.text()
        self.frm_model.wrong_answer2 = self.wrong_answer2.text()
        self.frm_model.wrong_answer3 = self.wrong_answer3.text()
    def set_connects(self):
        ''' встановлюємо обробник подій у віджетах так, щоб зберігати дані дані '''
        self.question.editingFinished.connect(self.save_question)
        self.answer.editingFinished.connect(self.save_answer)
        self.wrong_answer1.editingFinished.connect(self.save_wrong) 
        self.wrong_answer2.editingFinished.connect(self.save_wrong)
        self.wrong_answer3.editingFinished.connect(self.save_wrong)
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):

        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.set_connects()

class AnswerCheck(QuestionView):
    ''' вважаючи, що питання анкети візуалізуються чек-боксами, перевіряє, чи вибрана правильна відповідь.'''
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3, showed_answer, result):
        ''' запамʼятовує всі властивості. showed_answer - це віджет, в якому записується правильна відповідь (буде показуватися пізніше)
        result - це віджет, в який буде записаний txt_right або txt_wrong'''
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.showed_answer = showed_answer
        self.result = result
    def check(self):
        ''' відповідь заносится в статистику, але перемикання у формі не відбувається: 
        цей клас ничого не знає про панелі на формі '''
        if self.answer.isChecked():
            self.result.setText(text_correct) 
            self.showed_answer.setText(self.frm_model.answer) 
            self.frm_model.got_right() 
        else:
            
            self.result.setText(text_wrong)
            self.showed_answer.setText(self.frm_model.answer)
            self.frm_model.got_wrong()
            
class QuestionListModel(QAbstractListModel):
    ''' в даних знаходиться список обʼєктів типу Question, 
    а також список активних питань, щоб показати його на екрані '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_list = []
    def rowCount(self, index):
        ''' число елементів для показу: обовʼязковий метод для моделі, з якою буде звʼязаний віжет "список"'''
        return len(self.form_list)
    def data(self, index, role):
        ''' обовʼязковий метод для моделі: які дані вона дає по запиту від інтерфейсу'''
        if role == Qt.DisplayRole:
            form = self.form_list[index.row()]
            return form.question
    def insertRows(self, parent=QModelIndex()):
        ''' цей метод викликається, щоб вставити у список обʼєктів нові дані;
        генерується і вставляєтся одине пусте питання.'''
        position = len(self.form_list) 
        self.beginInsertRows(parent, position, position) 
        self.form_list.append(Question()) 
        self.endInsertRows() 
        QModelIndex()
        return True 
    def removeRows(self, position, parent=QModelIndex()):
        ''' стандартний метод для видалення рядків - після видалення з моделі рядок автоматично видаляється з екрану'''
        self.beginRemoveRows(parent, position, position) 
        self.form_list.pop(position) 
           

            
        self.endRemoveRows() 
        return True 
    def random_question(self):
        ''' Выдаёт случайный вопрос '''
        total = len(self.form_list)
        current = randint(0, total - 1)
        return self.form_list[current]

def random_AnswerCheck(list_model, w_question, widgets_list, w_showed_answer, w_result):
    '''возвращает новый экземпляр класса AnswerCheck, 
     случайным вопросом и случайным разбросом ответов по виджетам'''
    frm = list_model.random_question()
    shuffle(widgets_list)
    frm_card = AnswerCheck(frm, w_question, widgets_list[0], widgets_list[1], widgets_list[2], widgets_list[3], w_showed_answer, w_result)
    return frm_card