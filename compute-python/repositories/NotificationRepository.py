from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

class NotificationRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _get_notification_by_id(self, notification_id):
        return self.session.query(Notification).get(notification_id)

    def create_notification(self, user_id, message):
        notification = Notification(user_id=user_id, message=message)
        self.session.add(notification)
        self.session.commit()
        return notification

    def get_notifications_by_user(self, user_id):
        return self.session.query(Notification).filter_by(user_id=user_id).all()

    def update_notification_status(self, notification_id, is_read):
        notification = self._get_notification_by_id(notification_id)
        if notification:
            notification.is_read = is_read
            self.session.commit()
        return notification

    def delete_notification(self, notification_id):
        notification = self._get_notification_by_id(notification_id)
        if notification:
            self.session.delete(notification)
            self.session.commit()
