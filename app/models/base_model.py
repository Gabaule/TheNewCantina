# models/base_model.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # CREATE operations
    def save(self):
        """Save the model to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def create(cls, **kwargs):
        """Create a new instance and save it"""
        instance = cls(**kwargs)
        return instance.save()
    
    @classmethod
    def bulk_create(cls, data_list):
        """Create multiple instances at once"""
        instances = [cls(**data) for data in data_list]
        try:
            db.session.add_all(instances)
            db.session.commit()
            return instances
        except IntegrityError as e:
            db.session.rollback()
            raise e
    
    # READ operations
    @classmethod
    def get_by_id(cls, id):
        """Get single record by ID"""
        return cls.query.get(id)
    
    @classmethod
    def get_or_404(cls, id):
        """Get by ID or raise 404"""
        return cls.query.get_or_404(id)
    
    @classmethod
    def get_all(cls, limit=None, offset=None):
        """Get all records with optional pagination"""
        query = cls.query
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_by(cls, **kwargs):
        """Get records by specified criteria"""
        return cls.query.filter_by(**kwargs).all()
    
    @classmethod
    def get_first_by(cls, **kwargs):
        """Get first record matching criteria"""
        return cls.query.filter_by(**kwargs).first()
    
    @classmethod
    def count(cls):
        """Count all records"""
        return cls.query.count()
    
    @classmethod
    def paginate(cls, page=1, per_page=20, error_out=False):
        """Paginate records"""
        return cls.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=error_out
        )
    
    # UPDATE operations
    def update(self, **kwargs):
        """Update instance with new values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()
    
    @classmethod
    def update_by_id(cls, id, **kwargs):
        """Update record by ID"""
        instance = cls.get_by_id(id)
        if instance:
            return instance.update(**kwargs)
        return None
    
    @classmethod
    def bulk_update(cls, criteria, values):
        """Update multiple records matching criteria"""
        try:
            result = cls.query.filter_by(**criteria).update(values)
            db.session.commit()
            return result
        except IntegrityError as e:
            db.session.rollback()
            raise e
    
    # DELETE operations
    def delete(self):
        """Delete the instance"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def delete_by_id(cls, id):
        """Delete record by ID"""
        instance = cls.get_by_id(id)
        if instance:
            return instance.delete()
        return False
    
    @classmethod
    def delete_by(cls, **kwargs):
        """Delete records matching criteria"""
        try:
            result = cls.query.filter_by(**kwargs).delete()
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def bulk_delete(cls, ids):
        """Delete multiple records by IDs"""
        try:
            result = cls.query.filter(cls.get_primary_key().in_(ids)).delete(synchronize_session=False)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
    
    # Utility methods
    def to_dict(self):
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def refresh(self):
        """Refresh model from database"""
        db.session.refresh(self)
        return self
    
    @classmethod
    def get_primary_key(cls):
        """Get primary key column"""
        return next(iter(cls.__table__.primary_key.columns))
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.get_primary_key().name}={getattr(self, self.get_primary_key().name)}>'
