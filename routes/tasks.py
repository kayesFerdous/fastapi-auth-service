from typing import List
from typing_extensions import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from crud.tasks import get_tasks_for_user, delete_task, update_task, create_task, get_task_for_user
from database import get_db
from schemas.task import TaskCreate, TaskUpdate, Task, TaskOut, TaskIn
from schemas.users import User
from security.token import get_current_user
from rate_limiter import limiter


router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)



@router.get('/', response_model=List[TaskOut], status_code=status.HTTP_200_OK)
async def read_all_tasks(
        skip:int=0, 
        limit:int=10, 
        sort_by:str='id', 
        search:Optional[str]=None,
        is_done:Optional[bool]=None, 
        db: AsyncSession = Depends(get_db), 
        user: User = Depends(get_current_user)
)-> List[TaskOut]:
    return await get_tasks_for_user(user.id, db, sort_by, skip, limit, search, is_done)



@router.get('/{task_id}', response_model=TaskOut, status_code=status.HTTP_200_OK)
async def read_task_by_id(
        task_id: UUID,
        db: AsyncSession = Depends(get_db),
        user:User = Depends(get_current_user)
)-> TaskOut:
    task = await get_task_for_user(task_id,user, db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task with id {task_id} not found'
        )

    print(task.title)
    return task



@router.post('/', response_model=Task, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_new_task(
        request: Request, # Add this
        new_task: TaskIn,
        user:User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> Task: 
    new_task_data = TaskCreate(**new_task.model_dump(), owner=user.id)
    return await create_task(new_task_data, db)



@router.put('/{task_id}', response_model=Task, status_code=status.HTTP_200_OK)
async def update_existing_task(
        task_id: UUID,
        task: TaskUpdate,
        db: AsyncSession = Depends(get_db),
        user:User = Depends(get_current_user)
) -> Task:
    updated_task = await update_task(task_id, task, user, db)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task with id {task_id} not found'
        )
    return updated_task



@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db), 
    user:User = Depends(get_current_user)
) -> None: 

    deleted_task = await delete_task(task_id, user, db)
    if not deleted_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task with id {task_id} not found'
        )
    return None