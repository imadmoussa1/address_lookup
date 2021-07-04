from datetime import datetime
import csv
import json
import os
import glob
import shutil
import pandas as pd
from pymongo import UpdateOne, InsertOne
from pymongo.errors import BulkWriteError
from celery.schedules import crontab
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from raven import Client
from sqlalchemy.orm import Session
from app.db.elasticsearch_session import ElasticsearchSession
from app.db.mongo_session import MongoSession
from app.db.session import get_pg_db
from app import crud
from app.core.config import settings
from app.core.celery_app import celery_app
from app.core.logger import Logger
log = Logger.log(__name__)

client_sentry = Client(settings.SENTRY_DSN)

db: Session = get_pg_db()


@celery_app.task(bind=True, acks_late=True, track_started=True)
def test_celery(word: str):
  return {"msg": "test task return {word}"}


@celery_app.task(bind=True, acks_late=True, track_started=True, autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def get_address(self):
  """Method to download address file and added to mongoDB and elastic search"""
  # try:
  status = ElasticsearchSession.celery_status(result_name=self.name, status="PROGRESS")
  if not self.request.called_directly:
    self.update_state(state="PROGRESS")
    for file_name in glob.glob('app/address_data/*.csv'):
      db_query = []
      df = pd.read_csv(file_name)
      df = df.drop(columns=['ID'])
      df = df.fillna('/')
      df['address'] = df[['NUMBER', 'STREET', 'UNIT', 'DISTRICT', 'CITY', 'REGION']].apply(lambda row: ' '.join(row.values.astype(str)).replace(' /', '').strip(), axis=1)
      df['address']
      df.reset_index(inplace=True)
      data_dict = df.to_dict("records")
      for address in data_dict:
        db_query.append(UpdateOne({'HASH': address['HASH']}, {"$set": address}, upsert=True))
        ElasticsearchSession.index_data(address)
      # Insert collection
      MongoSession.spain_address_collection().bulk_write(db_query)
  return {"msg": "done Transforming address"}
  # except Exception as e:
  #   log.error(e)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  if settings.SETUP_PERIODIC_TASKS == True:
    """Periodic task: we setup the celery that will be start after a specific time"""
    sender.add_periodic_task(10600.0, get_address.s(), name="get_address")
