from pydantic import BaseModel


def apply_update(model: object, payload: BaseModel) -> None:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(model, field, value)
