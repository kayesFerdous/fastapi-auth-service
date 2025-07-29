from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from logging.config import dictConfig

from log_config import LOGGING_CONFIG
from routes import tasks_router, users_router, auths_router, emails_router, files_router
from rate_limiter import limiter

dictConfig(LOGGING_CONFIG)


api = FastAPI()

api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) #type: ignore

api.include_router(router=tasks_router)
api.include_router(router=users_router)
api.include_router(router=auths_router)
api.include_router(router=emails_router)
api.include_router(router=files_router)


@api.get('/')
def root():
    return {"message": "go to the task dir"}

