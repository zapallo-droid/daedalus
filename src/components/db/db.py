import os
import uuid
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base
from tables.scripts.ptrepack import recreate_indexes

from core.lib.model_operations import (App as AppORM, Pipeline as PipelineORM, Job as JobORM, Task as TaskORM,
                                       Source as SourceORM, TaskType as TaskTypeORM,
                                       PipelineDomain as PipelineDomainORM)
from core.lib.sql_helper import DBSession, DBInitializer
import logging


class DB:
    def __init__(self, db_config: dict, orm_objects: Optional[list[declarative_base]] =None ):
        self.dbconfig = db_config
        self.orm_objects = orm_objects

        db_session = DBSession(**db_config)
        self.session = db_session.create()

        self.db_init()

    def db_init(self):
        try:
            logging.info('Initializing DB')
            db_init = DBInitializer(session=DBSession(**self.dbconfig))
            self.session.begin()  # Start transaction

            if self.orm_objects is not None:
                db_init.db_init(self.orm_objects)
                self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Error initializing DB: {e}")
            raise

    def get_session(self):
        return self.Session()

    def records_loader(self, model: declarative_base, records: list[dict], commit=True):

        primary_keys = list(model.__table__.primary_key.columns.keys())

        if len(primary_keys) > 1:
            raise ValueError(f"Composite primary keys are not supported: {primary_keys}")

        primary_key = primary_keys[0]

        ### When a record don't have a primary_key key will be treated as a new record (by default the DB will create
        # for each record a UUID)
        logging.info('Getting records to insert')
        insert_records = [record for record in records if primary_key not in record.keys()]

        logging.info('Getting records to update Keys')
        update_records = [record for record in records if primary_key in record.keys()]

        existing_keys = {
            key for (key,) in self.session.query(getattr(model, primary_key))
            .filter(getattr(model, primary_key).in_([record.get(primary_key) for record in update_records]))
        }
        logging.info('Getting records to update')
        update_records = [record for record in update_records if record.get(primary_key) in existing_keys]

        logging.info('Loading data to the DB')
        try:
            if update_records:
                logging.info(f"Records to update: {len(update_records)}")
                self.session.bulk_update_mappings(model, update_records)
            if insert_records:
                logging.info(f"Records to insert: {len(insert_records)}")
                self.session.bulk_insert_mappings(model, insert_records)

            if commit:
                self.session.commit()

            return {"updated": len(update_records),
                    "inserted": len(insert_records),
                    "skipped": len(records) - len(update_records) - len(insert_records)}


        except Exception as e:
            self.session.rollback()
            logging.error(f"Error during bulk load: {e}")
            logging.debug(f"Failed insert records: {insert_records}")
            logging.debug(f"Failed update records: {update_records}")
            raise


if __name__ == '__main__':
    # Config and Parameters
    load_dotenv()
    c_path = os.getenv('COSMOS_PATH')
    f_path = os.getenv('FRAMEWORKS_PATH')
    s_path = os.getcwd()

    daedalus_config = {'db_user': os.getenv('DB_USER'),
                       'db_pass': os.getenv('DB_PASS'),
                       'db_host': os.getenv('DAEDALUS_DEV_HOST'),
                       'db_port': os.getenv('DAEDALUS_DEV_PORT'),
                       'db_name': 'daedalus_dev'}

    # DB Init
    db = DB(db_config=daedalus_config,
            orm_objects=[AppORM, PipelineORM, SourceORM, JobORM, TaskTypeORM, TaskORM, PipelineDomainORM])

    db.db_init()

    #db.records_loader(model=AppORM, records=[{'app_name': 'daedalus', 'app_name': 'hephaestus'}])

    #db.records_loader(model=TaskTypeORM, records=[{'task_type_code': 'E' , 'task_type_name': 'extract'},
    #                                              {'task_type_code': 'T' , 'task_type_name': 'transform'},
    #                                              {'task_type_code': 'L' , 'task_type_name': 'load'}])

    #db.records_loader(model=PipelineDomainORM, records=[{'pipeline_domain_name': 'Parliamentary - Argentina'},
    #                                                     {'pipeline_domain_name': 'International Labour Organization'}])



