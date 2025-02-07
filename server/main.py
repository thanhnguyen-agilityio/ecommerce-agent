from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.chat import router as chat_router
from routers.health import router as health_router
from routers.history import router as history_router

app = FastAPI(
    title="IVY Moda Customer Support Chat Bot Server",
    version="0.1.0",
    description="IVY Moda Customer Support Chat Bot Server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

for router in [health_router, chat_router, history_router]:
    app.include_router(router)
