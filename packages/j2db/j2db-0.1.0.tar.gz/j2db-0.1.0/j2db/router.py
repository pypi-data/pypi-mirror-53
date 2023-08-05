from fastapi import Form, FastAPI

from j2db.models import JsonRequestModel, EventModel
from j2db.handler import EventHandler


def register(app: FastAPI, handler: "EventHandler"):
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.post("/api/json/form")
    def json_upload_form(
            *, table: str = Form(...), action: str = Form(...), content: str = Form(...), secret: str = Form(...),
    ):
        new_event = EventModel(table, action, content, secret)
        return handler.handle(new_event)

    @app.post("/api/json/raw")
    def json_upload_raw(*, request: JsonRequestModel):
        new_event = EventModel(request.table, request.action, request.content, request.secret)
        return handler.handle(new_event)
