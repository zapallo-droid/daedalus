import os
from dotenv import load_dotenv
from core.lib.model_operations import (App as AppORM, Pipeline as PipelineORM, Job as JobORM, Task as TaskORM,
                                       Source as SourceORM, TaskType as TaskTypeORM)
from core.lib.sql_helper import DBSession, DBInitializer

# Config and Parameters
load_dotenv()
c_path = os.getenv('COSMOS_PATH')
f_path = os.getenv('FRAMEWORKS_PATH')
s_path = os.getcwd()

daedalus_conn = {'db_user': os.getenv('DB_USER'),
                 'db_pass': os.getenv('DB_PASS'),
                 'db_host': os.getenv('DAEDALUS_DEV_HOST'),
                 'db_port': os.getenv('DAEDALUS_DEV_PORT'),
                 'db_name': 'daedalus_dev'}

def db_maker(daedalus_config:dict):

    db_session = DBSession(**daedalus_config)
    session = db_session.create()

    db_init = DBInitializer(session=db_session)
    db_init.db_init([AppORM, PipelineORM, SourceORM, JobORM, TaskTypeORM, TaskORM])

db_maker(daedalus_config=daedalus_conn)