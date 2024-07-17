from decouple import config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.db import database
from app.db import models
from app.routers import posts, comments, teams

models.Base.metadata.create_all(bind=database.engine)
allow_origins = config("ALLOW_ORIGINS", default="").split(",")

apps = FastAPI()
apps.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

apps.include_router(posts.router, prefix="/posts", tags=["posts"])
apps.include_router(comments.router, prefix="/comments", tags=["comments"])
apps.include_router(teams.router, prefix="/teams", tags=["teams"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(apps, host="0.0.0.0", port=18000)
