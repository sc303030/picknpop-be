from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.db import database
from app.db import models
from app.routers import posts

models.Base.metadata.create_all(bind=database.engine)

apps = FastAPI()
apps.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 허용할 오리진
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드
    allow_headers=["*"],  # 허용할 헤더
)
apps.include_router(posts.router, prefix="", tags=["posts"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(apps, host="0.0.0.0", port=18000)
