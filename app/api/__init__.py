from fastapi import FastAPI

from .routes import employee, team


def add_app_routes(app: FastAPI):
    app.include_router(employee.router, prefix="/employee", tags=["Employee"])
    app.include_router(team.router, prefix="/team", tags=["Team"])
