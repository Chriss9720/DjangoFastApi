from pydantic import BaseModel

class AppModel(BaseModel):
    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = True
            return BaseModel.dict(self, *args, **kwargs)

class Message(AppModel):
    folio: str
