from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import noload
from uuid import UUID

from schemas import TaskCreate, TaskUpdate, Task, TaskOut
from models import Task_db
from schemas.task import TaskIn, TaskOut
from schemas.users import User

    
async def get_tasks_for_user(
        user_id:UUID,
        db:AsyncSession,
        sort_by:str,
        skip:int, 
        limit:int,
        search:Optional[str]=None,
        is_done:Optional[bool] = None
) -> List[TaskOut]:
    query = select(Task_db).filter(Task_db.owner == user_id)

    if is_done is not None:
        query = query.filter(Task_db.is_done == is_done)

    if search is not None:
        query = query.filter(Task_db.title.ilike(f'%{search}%'))

    if hasattr(Task_db, sort_by):
        query = query.order_by(getattr(Task_db, sort_by))
    
    result = await db.execute(query.offset(skip).limit(limit))
    tasks = result.scalars().all()

    if tasks:
        return [TaskOut.model_validate(task, from_attributes=True) for task in tasks]
    return []



async def get_task_for_user(task_id:UUID, user: User, db:AsyncSession) -> Optional[TaskOut]:
    result = await db.execute(select(Task_db).options(noload(Task_db.user)).filter(Task_db.id == task_id, Task_db.owner == user.id))
    task = result.scalar_one_or_none()

    if task:
        return TaskOut.model_validate(task, from_attributes=True)
    return None



async def delete_task(task_id:UUID,user: User, db:AsyncSession) -> Optional[TaskOut]:
    result = await db.execute(select(Task_db).filter(Task_db.id == task_id, Task_db.owner == user.id))
    task = result.scalar_one_or_none()
    if task:
        await db.delete(task)
        await db.commit()
        return TaskOut.model_validate(task, from_attributes=True)
    return None



async def create_task(task: TaskCreate, db:AsyncSession) -> Task:
    new_task = Task_db(**task.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return Task.model_validate(new_task, from_attributes=True)



async def update_task(task_id: UUID, task: TaskUpdate, user: User, db:AsyncSession) -> Optional[Task]:
    result = await db.execute(select(Task_db).filter(Task_db.id == task_id, Task_db.owner == user.id))
    db_task = result.scalar_one_or_none()

    if db_task:
        update_data = task.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_task, key, value)

        await db.commit()
        await db.refresh(db_task)
        return Task.model_validate(db_task, from_attributes=True)
    return None
