# General libraries for DB
from sqlalchemy import Column, Float, Integer, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

# Complementary Resources
import uuid
import logging
from datetime import datetime

# ORM model Base Class
Base = declarative_base()

# General Use Classes
class App(Base):
    __tablename__ = 'app'
    __table_args__ = {'schema': 'operations'}

    app_code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_name = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    pipelines = relationship('Pipeline', back_populates='apps')
    jobs = relationship('Job', back_populates='apps')

    def to_dict(self):
        return {
            'app_code': self.app_code,
            'app_name': self.app_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            app_code=data.get('app_code'),
            app_name=data.get('app_name')
        )

class PipelineDomain(Base):
    __tablename__ = 'pipeline_domain'
    __table_args__ = {'schema': 'operations'}

    pipeline_domain_code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_domain_name = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    pipelines = relationship('Pipeline', back_populates='pipeline_domains')

    def to_dict(self):
        return {
            'pipeline_domain_code': self.pipeline_domain_code,
            'pipeline_domain_name': self.pipeline_domain_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Pipeline(Base):
    __tablename__ = 'pipeline'
    __table_args__ = {'schema': 'operations'}

    pipeline_code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_name = Column(Text, nullable=False)
    pipeline_domain_code = Column(UUID, ForeignKey('operations.pipeline_domain.pipeline_domain_code') ,
                                  nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    app_code = Column(UUID, ForeignKey('operations.app.app_code'), nullable=False)

    apps = relationship('App', back_populates='pipelines')
    tasks = relationship('Task', back_populates='pipelines')
    sources = relationship('Source', back_populates='pipelines')
    pipeline_domains = relationship('PipelineDomain', back_populates='pipelines')

    def to_dict(self):
        return {
            'app_code': self.app_code,
            'pipeline_domain_code': self.pipeline_domain_code,
            'pipeline_domain_name': self.pipeline_domain_name,
            'pipeline_code': self.pipeline_code,
            'pipeline_name': self.pipeline_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            app_code=data.get('app_code'),
            pipeline_domain_code=data.get('pipeline_domain_code'),
            pipeline_domain_name=data.get('pipeline_domain_name'),
            pipeline_code=data.get('pipeline_code'),
            pipeline_name=data.get('pipeline_name')
        )

# General Use Classes
class Source(Base):
    __tablename__ = 'source'
    __table_args__ = {'schema': 'operations'}

    source_code = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_name = Column(Text, nullable=False)
    location_type = Column(Text, nullable=False)
    location = Column(Text, nullable=True) # URL
    location_endpoint = Column(Text, nullable=True) # Only for API
    extension = Column(Text, nullable=True)
    extract_type = Column(Text, nullable=False)
    params = Column(JSON, nullable=True)
    headers = Column(JSON, nullable=True)
    timeout = Column(Float, nullable=True)
    pipeline_code = Column(UUID, ForeignKey('operations.pipeline.pipeline_code'), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    pipelines = relationship('Pipeline', back_populates='sources')
    tasks = relationship('Task', back_populates='sources')

    def to_dict(self):
        return {
            'source_code': self.source_code,
            'source_name': self.source_name,
            'location_type': self.location_type,
            'location_endpoint': self.location_endpoint,
            'location': self.location,
            'extension': self.extension,
            'extract_type': self.extract_type,
            'params': self.params,
            'headers': self.headers,
            'timeout': self.timeout,
            'pipeline_code': self.pipeline_code,
            'active': self.active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            source_code=data.get('source_code'),
            source_name=data.get('source_name'),
            location_type=data.get('location_type'),
            location_endpoint=data.get('location_endpoint'),
            location=data.get('location'),
            extension=data.get('extension'),
            extract_type=data.get('extract_type'),
            params=data.get('params'),
            headers=data.get('headers'),
            timeout=data.get('timeout'),
            pipeline_code=data.get('pipeline_code')
        )

class Job(Base):
    __tablename__ = 'job'
    __table_args__ = {'schema': 'operations'}

    job_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(Text, nullable=False)
    memory_usage_start = Column(Float, nullable=False)
    cpu_usage_start = Column(Float, nullable=False)
    memory_usage_end = Column(Float, nullable=False)
    cpu_usage_end = Column(Float, nullable=False)
    status = Column(Text, nullable=False)
    exception = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)
    duration = Column(Float, nullable=True)
    memory_usage = Column(Float, nullable=True)
    cpu_usage = Column(Float, nullable=True)
    host_name = Column(Text, nullable=False)
    execution_user = Column(Text, nullable=False)
    process_id = Column(Integer, nullable=False)
    number_of_tasks = Column(Integer, nullable=False)
    app_code = Column(UUID, ForeignKey('operations.app.app_code'), nullable=False)

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
            'started_at': self.started_at,
            'ended_at': self.ended_at,
            'duration': self.duration,
            'memory_usage': self.memory_usage,
            'cpu_usage': self.cpu_usage,
            'host_name': self.host_name,
            'execution_user': self.execution_user,
            'process_id': self.process_id,
            'number_of_tasks': self.number_of_tasks,
            'app_code': self.app_code
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
            started_at=data.get('started_at'),
            ended_at=data.get('ended_at'),
            duration=data.get('duration'),
            memory_usage=data.get('memory_usage'),
            cpu_usage=data.get('cpu_usage'),
            host_name=data.get('host_name'),
            execution_user=data.get('execution_user'),
            process_id=data.get('process_id'),
            number_of_tasks=data.get('number_of_tasks'),
            app_code=data.get('app_code')
        )

class TaskType(Base):
    __tablename__ = 'task_type'
    __table_args__ = {'schema': 'operations'}

    task_type_code = Column(Text, primary_key=True)
    task_type_name = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    tasks = relationship('Task', back_populates='task_types')

    def to_dict(self):
        return {
            'task_type_code': self.task_type_code,
            'task_type_name': self.task_type_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_type_code=data.get('task_type_code'),
            task_type_name=data.get('task_type_name')
        )


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {'schema': 'operations'}

    task_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(Text, nullable=False)
    source_code = Column(UUID, ForeignKey('operations.source.source_code'), nullable=False)
    location = Column(Text, nullable=False)
    memory_usage_start = Column(Float, nullable=False)
    cpu_usage_start = Column(Float, nullable=False)
    memory_usage_end = Column(Float, nullable=False)
    cpu_usage_end = Column(Float, nullable=False)
    status = Column(Text, nullable=False)
    location_status = Column(Float, nullable=True)
    task_image = Column(Text, nullable=True)
    task_image_status = Column(Text, nullable=True)
    exception = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)
    duration = Column(Float, nullable=True)
    records_processed = Column(Integer, nullable=True)
    memory_usage = Column(Float, nullable=True)
    cpu_usage = Column(Float, nullable=True)
    job_id = Column(UUID, ForeignKey('operations.job.job_id'), nullable=False)
    pipeline_code = Column(UUID, ForeignKey('operations.pipeline.pipeline_code'), nullable=False)
    task_type_code = Column(Text, ForeignKey('operations.task_type.task_type_code'), nullable=False)

    jobs = relationship('Job', back_populates='tasks')
    pipelines = relationship('Pipeline', back_populates='tasks')
    sources = relationship('Source', back_populates='tasks')
    task_types = relationship('TaskType', back_populates='tasks')

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
            'started_at': self.started_at,
            'ended_at': self.ended_at,
            'duration': self.duration,
            'records_processed': self.records_processed,
            'memory_usage': self.memory_usage,
            'cpu_usage': self.cpu_usage,
            'job_id': self.job_id,
            'pipeline_code': self.pipeline_code,
            'task_type_code': self.task_type_code
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
            started_at=data.get('started_at'),
            ended_at=data.get('ended_at'),
            duration=data.get('duration'),
            records_processed=data.get('records_processed'),
            memory_usage=data.get('memory_usage'),
            cpu_usage=data.get('cpu_usage'),
            job_id=data.get('job_id'),
            pipeline_code=data.get('pipeline_code'),
            task_type_code=data.get('task_type_code')
        )