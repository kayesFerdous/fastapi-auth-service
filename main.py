from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from routes import tasks_router, users_router, auths_router, emails_router, files_router
from rate_limiter import limiter


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) #type: ignore

app.include_router(router=tasks_router)
app.include_router(router=users_router)
app.include_router(router=auths_router)
app.include_router(router=emails_router)
app.include_router(router=files_router)


@app.get('/')
def root():
    return {"message": "go to the task dir"}

