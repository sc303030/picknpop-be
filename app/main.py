from decouple import config
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.db import database
from app.db import models
from app.routers import posts, comments, teams, emotions

# 데이터베이스 모델 초기화
models.Base.metadata.create_all(bind=database.engine)

# 환경 변수에서 허용된 도메인 읽어오기 (콤마로 구분된 도메인 목록)
allow_origins = config("ALLOW_ORIGINS", default="").split(",")

# FastAPI 애플리케이션 생성
apps = FastAPI()

# CORS 미들웨어 설정
apps.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # 허용된 도메인 설정
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


@apps.middleware("http")
async def check_origin_or_referer(request: Request, call_next):
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")

    if origin and any(allowed_origin in origin for allowed_origin in allow_origins):
        response = await call_next(request)
        return response
    elif referer and any(allowed_origin in referer for allowed_origin in allow_origins):
        response = await call_next(request)
        return response
    else:
        raise HTTPException(
            status_code=403, detail="Access forbidden: Invalid origin or referer"
        )


# API 라우터 설정
apps.include_router(posts.router, prefix="/posts", tags=["posts"])
apps.include_router(comments.router, prefix="/comments", tags=["comments"])
apps.include_router(teams.router, prefix="/teams", tags=["teams"])
apps.include_router(emotions.router, prefix="/emotions", tags=["emotions"])

# 애플리케이션 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(apps, host="0.0.0.0", port=18000)
