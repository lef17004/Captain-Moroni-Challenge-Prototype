
import json
import datetime
from turtle import Turtle
from user_defaults import UserDefaults

class Task:
    def __init__(self, title, description, completed):
        self.title = title
        self.description = description
        self.completed = completed

        self.id = None
        self.notification = None

    def dict_clone(self):
        dictionary = {
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'id': self.id,
            'notification': self.notification
        }
        return dictionary
    
    def toggle(self):
        if not self.completed:
            self.completed = True
        else:
            self.completed = False

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'{self.title}'

class TaskHolder:
    def __init__(self, task_dict):
        self.daily_tasks = self.create_daily_tasks(task_dict['daily'])

    def create_daily_tasks(self, daily_task_dict_list):
        daily_tasks = []
        for task in daily_task_dict_list:
            daily_tasks.append(Task(task['title'], '', task['completed']))
        return daily_tasks

    def gather_daily_task_data(self):
        data = []
        for task in self.daily_tasks:
            data.append(task.dict_clone())
        return data

    def all_tasks_complete(self):
        for task in self.daily_tasks:
            if not task.completed:
                return False
        return True

    def toggle_completed(self, index):
        if len(self.daily_tasks) > index - 1 and index - 1 >= 0:
            self.daily_tasks[index - 1].toggle()

    def display_tasks(self):
        count = 1
        for task in self.daily_tasks:
            print(count, task.completed, ' - ', task)
            count += 1
        

def load_tasks():
    with open('tasks.json') as file:
        task_data = json.load(file)
        holder = TaskHolder(task_data)
        return holder


def start_up(user_defaults):
    date_text = user_defaults['date']
    date = None
    task_holder = None


    if not date_text:
        date = datetime.date.today()
        todays_tasks = load_tasks()
        user_defaults['today'] = todays_tasks.gather_daily_task_data()
        user_defaults['date'] = f"{date.strftime('%Y')}-{date.strftime('%m')}-{date.strftime('%d')}"
        return todays_tasks


    year, month, day = date_text.split('-')
    date = datetime.date(int(year), int(month), int(day))

    
    today = datetime.date.today()

    if date == today:
        task_holder = TaskHolder({'daily': user_defaults['today']})
    elif date == today - datetime.timedelta(1):
        user_defaults['yesterday'] = user_defaults['today']
        todays_tasks = load_tasks()
        user_defaults['today'] = todays_tasks.gather_daily_task_data()

        yesterday_tasks = TaskHolder({'daily': user_defaults['yesterday']})
        if yesterday_tasks.all_tasks_complete():
            total = user_defaults['total']
            total += 1
            user_defaults['total'] = total
        else:
            user_defaults['temp_total'] = user_defaults['total']
            user_defaults['total'] = 0

        task_holder = todays_tasks
        
    else:
        user_defaults['total'] = 0
        user_defaults['temp_total'] = 0
        user_defaults['yesterday'] = user_defaults['today']
        todays_tasks = load_tasks()
        user_defaults['today'] = todays_tasks.gather_daily_task_data()
        task_holder = todays_tasks

    return task_holder


   

def main():
    # Load task data
    # Check store
    data = UserDefaults()
    task_holder = start_up(data)
    task_holder.display_tasks()

    user_input = None
    while user_input != 'quit':
        user_input = input('<?>')
        if user_input.isnumeric():
            task_holder.toggle_completed(int(user_input))
            task_holder.display_tasks()
            data['today'] = task_holder.gather_daily_task_data()





if __name__ == '__main__':
    main()