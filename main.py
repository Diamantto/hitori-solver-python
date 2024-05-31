"""Entry point of the application."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import auth, solver

app = FastAPI()


@app.get("/")
async def root():
    """Basic root."""
    return {"message": "Hello World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(solver.router)
