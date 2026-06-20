from sqlalchemy.orm import Session
from app.models.notification import Notification


# ------------------------
# GET USER NOTIFICATIONS
# ------------------------
def get_notifications(db: Session, user_id: str):
    return db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(
        Notification.created_at.desc()
    ).all()


# ------------------------
# CREATE NOTIFICATION
# ------------------------
def create_notification(db: Session, user_id: str, message: str):
    notification = Notification(
        user_id=user_id,
        message=message,
        is_read=False
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification