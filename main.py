import streamlit as st
#
from task import Task
from jokes import generate_joke

if "joke" not in st.session_state:
    api_key = st.secrets['jokes_api']['api_key']
    st.session_state.joke = generate_joke(api_key)


if "task_list" not in st.session_state:
    st.session_state.task_list = []

task_list = st.session_state.task_list

def add_task(task_name: str):
    task_list.append(Task(name=task_name, is_done=False))

def delete_task(idx: int):
    del task_list[idx]

def mark_done(task: Task):
    task.is_done = True

def mark_not_done(task: Task):
    task.is_done = False

with st.sidebar:
    task = st.text_input("Enter a task")
    if st.button("Add task", type="primary"):
        if len(task.strip()) > 0:
            add_task(task.strip())


st.info(st.session_state.joke)


total_tasks = len(task_list)
completed_tasks = sum(1 for task in task_list if task.is_done)

metric_display = f"{completed_tasks}/{total_tasks} done"
st.metric("Task completion", metric_display, delta=None)

st.header("Today's to-dos:", divider="grey")

#st.info(f"task_list: {task_list}")

for idx, task in enumerate(task_list):
    task_col, delete_col = st.columns([0.8, 0.2])

    if task.is_done:
        # Зачеркнутый текст (Markdown)
        label = f'~~{task.name}~~'
    else:
        label = task.name
    
    checked = task_col.checkbox(label, task.is_done, key=f"task_{idx}")
    # Если пользователь установил галочку
    # Оператор "and" позволяет избежать бесконечного цицла
    if checked and not task.is_done:
        mark_done(task)
        # Обновить frontend
        st.rerun()
    elif not checked and task.is_done:
        mark_not_done(task)
        # Обновить frontend
        st.rerun()
    
    if delete_col.button("Delete", key=f'delete_{idx}'):
        delete_task(idx)
        # После того как изменился список task_list
        # нужно еще раз обновить frontend
        st.rerun()

