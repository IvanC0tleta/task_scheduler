from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def index():
    return {"server status": "ok"}


@app.get("/tasks", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.post("/tasks/new", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate = Depends(), db: Session = Depends(get_db)):
    db_task = models.Task(name=task.name, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.patch("/tasks/{task_id}/update_status", response_model=schemas.Task)
async def update_task_status(task_id: int, status: models.TaskStatus, db: Session = Depends(get_db)):
    db_task = await get_task(task_id, db)
    if db_task:
        db_task.status = status
        db.commit()
        db.refresh(db_task)
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.patch("/tasks/{task_id}/edit", response_model=schemas.Task)
async def update_task(task_id: int, task_update: schemas.TaskUpdate = Depends(), db: Session = Depends(get_db)):
    db_task = await get_task(task_id, db)
    if db_task:
        if task_update.name is not None:
            db_task.name = task_update.name
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.status is not None:
            db_task.status = task_update.status
        db.commit()
        db.refresh(db_task)
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = await get_task(task_id, db)
    if db_task:
        db.delete(db_task)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"delete": "ok"}
