from sqlalchemy import Column, String, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# ORM model Base Class
Base = declarative_base()

# General Use Classes
class App(Base):
    __tablename__ = 'app'
    __table_args__ = {'schema': 'operations'}

    app_code = Column(String(50), primary_key=True)
    app_name = Column(String(255), nullable=False)

    pipelines = relationship('Pipeline', back_populates='apps')
    jobs = relationship('Job', back_populates='apps')

    def to_dict(self):
        return {
            'app_code': self.app_code,
            'app_name': self.app_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            app_code=data.get('app_code'),
            app_name=data.get('app_name')
        )

class Pipeline(Base):
    __tablename__ = 'pipeline'
    __table_args__ = {'schema': 'operations'}

    pipeline_code = Column(String(50), primary_key=True)
    pipeline_name = Column(String(255), nullable=False)
    app_code = Column(String(50), ForeignKey('operations.app.app_code'), nullable=False)

    apps = relationship('App', back_populates='pipelines')
    tasks = relationship('Task', back_populates='pipelines')

    def to_dict(self):
        return {
            'app_code': self.app_code,
            'pipeline_code': self.pipeline_code,
            'pipeline_name': self.pipeline_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            app_code=data.get('app_code'),
            pipeline_code=data.get('pipeline_code'),
            pipeline_name=data.get('pipeline_name')
        )

class Job(Base):
    __tablename__ = 'job'
    __table_args__ = {'schema': 'operations'}

    job_id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=False)
    memory_usage_start = Column(Float, nullable=False)
    cpu_usage_start = Column(Float, nullable=False)
    memory_usage_end = Column(Float, nullable=False)
    cpu_usage_end = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    exception = Column(Text, nullable=True)
    duration = Column(Float, nullable=True)
    memory_usage = Column(Float, nullable=True)
    cpu_usage = Column(Float, nullable=True)
    host_name = Column(String(255), nullable=False)
    execution_user = Column(String(255), nullable=False)
    process_id = Column(Integer, nullable=False)
    number_of_tasks = Column(Integer, nullable=False)
    app_code = Column(String(50), ForeignKey('operations.app.app_code'), nullable=False)
    app_name = Column(String(255), nullable=False)

    apps = relationship('App', back_populates='jobs')
    tasks = relationship('Task', back_populates='jobs')

    def to_dict(self):
        return {
            'job_id': self.job_id,
            'name': self.name,
            'memory_usage_start': self.memory_usage_start,
            'cpu_usage_start': self.cpu_usage_start,
            'memory_usage_end': self.memory_usage_end,
            'cpu_usage_end': self.cpu_usage_end,
            'status': self.status,
            'exception': self.exception,
            'duration': self.duration,
            'memory_usage': self.memory_usage,
            'cpu_usage': self.cpu_usage,
            'host_name': self.host_name,
            'execution_user': self.execution_user,
            'process_id': self.process_id,
            'number_of_tasks': self.number_of_tasks,
            'app_code': self.app_code,
            'app_name': self.app_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            job_id=data.get('job_id'),
            name=data.get('name'),
            memory_usage_start=data.get('memory_usage_start'),
            cpu_usage_start=data.get('cpu_usage_start'),
            memory_usage_end=data.get('memory_usage_end'),
            cpu_usage_end=data.get('cpu_usage_end'),
            status=data.get('status'),
            exception=data.get('exception'),
            duration=data.get('duration'),
            memory_usage=data.get('memory_usage'),
            cpu_usage=data.get('cpu_usage'),
            host_name=data.get('host_name'),
            execution_user=data.get('execution_user'),
            process_id=data.get('process_id'),
            number_of_tasks=data.get('number_of_tasks'),
            app_code=data.get('app_code'),
            app_name=data.get('app_name')
        )


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {'schema': 'operations'}

    task_id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    memory_usage_start = Column(Float, nullable=False)
    cpu_usage_start = Column(Float, nullable=False)
    memory_usage_end = Column(Float, nullable=False)
    cpu_usage_end = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    location_status = Column(Float, nullable=True)
    task_image = Column(String(255), nullable=False)
    task_image_status = Column(String(50), nullable=True)
    exception = Column(Text, nullable=True)
    duration = Column(Float, nullable=True)
    records_processed = Column(Integer, nullable=True)
    memory_usage = Column(Float, nullable=True)
    cpu_usage = Column(Float, nullable=True)
    job_id = Column(String(50), ForeignKey('operations.job.job_id'), nullable=False)
    pipeline_code = Column(String(50), ForeignKey('operations.pipeline.pipeline_code'), nullable=False)

    jobs = relationship('Job', back_populates='tasks')
    pipelines = relationship('Pipeline', back_populates='tasks')

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'name': self.name,
            'location': self.location,
            'memory_usage_start': self.memory_usage_start,
            'cpu_usage_start': self.cpu_usage_start,
            'memory_usage_end': self.memory_usage_end,
            'cpu_usage_end': self.cpu_usage_end,
            'status': self.status,
            'location_status': self.location_status,
            'task_image': self.task_image,
            'task_image_status': self.task_image_status,
            'exception': self.exception,
            'duration': self.duration,
            'records_processed': self.records_processed,
            'memory_usage': self.memory_usage,
            'cpu_usage': self.cpu_usage,
            'job_id': self.job_id,
            'pipeline_code': self.pipeline_code
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_id=data.get('task_id'),
            name=data.get('name'),
            location=data.get('location'),
            memory_usage_start=data.get('memory_usage_start'),
            cpu_usage_start=data.get('cpu_usage_start'),
            memory_usage_end=data.get('memory_usage_end'),
            cpu_usage_end=data.get('cpu_usage_end'),
            status=data.get('status'),
            location_status=data.get('location_status'),
            task_image=data.get('task_image'),
            task_image_status=data.get('task_image_status'),
            exception=data.get('exception'),
            duration=data.get('duration'),
            records_processed=data.get('records_processed'),
            memory_usage=data.get('memory_usage'),
            cpu_usage=data.get('cpu_usage'),
            job_id=data.get('job_id'),
            pipeline_code=data.get('pipeline_code')
        )