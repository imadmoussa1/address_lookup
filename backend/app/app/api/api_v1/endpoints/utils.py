from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import crud, models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email
from app.db.elasticsearch_session import ElasticsearchSession

from sqlalchemy.orm import Session
from starlette.responses import FileResponse


from app.core.logger import Logger
log = Logger.log(__name__)

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(msg: schemas.Msg, current_user: models.User = Depends(deps.get_current_active_superuser),) -> Any:
  """
  Test Celery worker.
  """
  celery_app.send_task("app.worker.test_celery", args=[msg.msg])
  return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
  """
  Test emails.
  """
  send_test_email(email_to=email_to)
  return {"msg": "Test email sent"}

@router.post("/address/etl", response_model=schemas.Msg, status_code=201)
def test_celery(current_user: models.User = Depends(deps.get_current_active_superuser),) -> Any:
  """
  Worker for address
  """
  celery_app.send_task("app.worker.get_address", args=[])
  return {"msg": "Running the service"}

@router.get("/address/", response_model=schemas.Address, status_code=201)
def address_lookup(
    address: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
  a = ElasticsearchSession.search(address)
  address = {}
  if a:
    address = a[0]['_source']
  return address
