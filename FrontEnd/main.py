from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ['http://localhost:5500', 'http://127.0.0.1:5500']

app.add_middleware(CORSMiddleware,
                   allow_origins = origins,
                   allow_credentials = True,
                   allow_methods = ['*'],
                   allow_headers = ['*'])

class Task(BaseModel):
    id: int | None
    description: str
    responsible: str | None
    level: int
    situation: str | None
    priority: int


tasks: list[Task] = []

#GET methods
@app.get('/tasks')
def all_tasks(skip: int | None = None, take: int | None = None):
    inicio = skip

    if skip and take:
        fim = skip + take
    else:
        fim = None
    
    return tasks[inicio:fim]


@app.get('/tasks/{task_id}')
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task Not Found")


@app.get('/tasks/level/{level_search}')
def get_task_level(level_search: int):
    tasks_level = []
    for task in tasks:
        if task.level == level_search:
            tasks_level.append(task)
    
    if len(tasks_level) > 0:
        return tasks_level
    else: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="task not found with requested level")


@app.get('/tasks/priority/{priority_search}')
def get_task_priority(priority_search: int):
    tasks_priority = []
    for task in tasks:
        if task.priority == priority_search:
            tasks_priority.append(task)
    
    if len(tasks_priority) > 0:
        return tasks_priority
    else: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="task not found with requested priority")


@app.get('/tasks/situation/{situation_search}')
def get_task_situation(situation_search: int):
    tasks_situation = []
    for task in tasks:
        if task.situation == situation_search:
            tasks_situation.append(task)
    
    if len(tasks_situation) > 0:
        return tasks_situation
    else: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="task not found with requested status")


#POST method
@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def new_task(task: Task):
    task.id = len(tasks) + 1
    task.situation = "New"
    tasks.append(task)

    return task


#DELETE method
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return "Task Deleted"
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task Not Found")


#PUT methods
@app.put('/tasks/{task_id}/cancel')
def cancel_task(task_id: int):
    for index in range(len(tasks)):
        current_task = tasks[index]
        if current_task.id == task_id:
            current_task.situation = "Canceled"
            tasks[index] = current_task
            return current_task
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task Not Found")


@app.put('/tasks/{task_id}/complete')
def complete_task(task_id: int):
    for index in range(len(tasks)):
        current_task = tasks[index]
        if current_task.id == task_id:
            if current_task.situation == "In Progress":
                current_task.situation = "Completed"
                tasks[index] = current_task
                return current_task
            else:
                return "Only In Progress tasks can be completed"
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task Not Found")


@app.put('/tasks/{task_id}/ongoing')
def in_progress_task(task_id: int):
    for index in range(len(tasks)):
        current_task = tasks[index]
        if current_task.id == task_id:
            if current_task.situation == "New" or current_task.situation == "Suspend":
                current_task.situation = "In Progress"
                tasks[index] = current_task
                return current_task
            else:
                return "Only new or pending tasks can be in progress"
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task Not Found")


@app.put('/tasks/{task_id}/suspend')
def suspend_task(task_id: int):
    for index in range(len(tasks)):
        current_task = tasks[index]
        if current_task.id == task_id:
            if current_task.situation == "New" or current_task.situation == "In Progress":
                current_task.situation = "Suspend"
                tasks[index] = current_task
                return current_task
            else:
                return "Only new or in progress tasks can be in suspend"
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task Not Found")


    