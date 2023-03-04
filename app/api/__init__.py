from fastapi import FastAPI

from .routes import employee, team, vacation


def add_app_routes(app: FastAPI):
    app.include_router(employee.router, prefix="/employee", tags=["Employee"])
    app.include_router(team.router, prefix="/team", tags=["Team"])
    app.include_router(vacation.router, prefix="/vacation", tags=["Vacation"])
