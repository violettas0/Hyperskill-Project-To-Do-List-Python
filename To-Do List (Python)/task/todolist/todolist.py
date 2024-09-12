from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'

    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())
    id = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return self.task

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


while True:
    print('1) Today\'s tasks')
    print('2) Week\'s tasks')
    print('3) All tasks')
    print('4) Missed tasks')
    print('5) Add a task')
    print('6) Delete a task')
    print('0) Exit')
    choice = int(input())
    today = datetime.now().date()

    if choice == 0:
        print('Bye!')
        break
    elif choice == 1:
        print(f'Today {datetime.today().strftime("%b %d")}:')
        rows = session.query(Task).filter(Task.deadline == datetime.today().date()).all()
        if rows:
            seq = 0
            for row in rows:
                seq += 1
                print(f'{seq}. {row}')
        else:
            print('Nothing to do!')
    elif choice == 2:
        seven_days_later = today + timedelta(days=7)

        tasks_next_week = session.query(Task).filter(Task.deadline >= today, Task.deadline < seven_days_later).all()

        tasks_by_date = {today + timedelta(days=i): [] for i in range(7)}

        for task in tasks_next_week:
            task_date = task.deadline
            if task_date in tasks_by_date:
                tasks_by_date[task_date].append(task)

        for date, tasks in tasks_by_date.items():
            print(f"\n{date.strftime('%A %d %b')}:")
            if tasks:
                seq = 0
                for task in tasks:
                    seq += 1
                    print(f"{seq}. {task}")
            else:
                print("Nothing to do!")
    elif choice == 3:
        rows = session.query(Task).order_by(Task.deadline).all()
        if rows:
            seq = 0
            for row in rows:
                seq += 1
                print(f'{seq}. {row}. {row.deadline.strftime("%d %b")}')
        else:
            print('Nothing to do!')
    elif choice == 4:
        print('Missed tasks:')
        tasks_missed = session.query(Task).filter(Task.deadline < today).order_by(Task.deadline).all()
        if tasks_missed:
            seq = 0
            for row in tasks_missed:
                seq += 1
                print(f'{seq}. {row}. {row.deadline.strftime("%d %b")}')
            print('\n')
        else:
            print('All tasks have been completed!')
    elif choice == 5:
        print('Enter a task')
        task_input = input()
        print('Enter a deadline')
        deadline_input = input()
        new_task = Task(task=task_input,
                        deadline=datetime.strptime(deadline_input, '%Y-%m-%d'))
        session.add(new_task)
        session.commit()
        print('The task has been added!')
    elif choice == 6:
        print('Choose the number of the task you want to delete:')
        rows = session.query(Task).order_by(Task.deadline).all()
        if rows:
            seq = 0
            for row in rows:
                seq += 1
                print(f'{seq}. {row}. {row.deadline.strftime("%d %b")}')
        delete_task_input = int(input())
        session.delete(rows[delete_task_input - 1])
        session.commit()
        print('The task has been deleted!')
