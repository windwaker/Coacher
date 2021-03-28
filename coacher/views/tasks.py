from fastapi import BackgroundTasks
from coacher import app, templates
import time
from datetime import datetime


def _run_task(name: str, id=None):
    time.sleep(15)
    with open("tasks_out.txt", mode="a+") as file:
        now = datetime.now()
        content = f"{name} [{id}]: {now}\n"
        file.write(content)


@app.post("/task/run/{name}/{id}")
async def task_run(name: str, id: int, background_tasks: BackgroundTasks):
    """
    Run a given task
    :param name:
    :param id:
    :param background_tasks:
    :return:
    """
    background_tasks.add_task(_run_task, name, id)
    return {"message": f"Task {name} ID {id} is being run ...\n"}














