from sqlalchemy.orm import Session
from app.models.ticket import Ticket


def create_ticket(db: Session, data, user_id: str):
    ticket = Ticket(
        title=data.title,
        description=data.description,
        priority=data.priority,
        status="open",
        created_by=user_id
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def get_ticket(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def get_my_tickets(db: Session, user_id: str):
    return db.query(Ticket).filter(Ticket.created_by == user_id).all()


def assign_ticket(db: Session, ticket_id: int, technician_id: str):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return None

    ticket.assigned_to = technician_id
    ticket.status = "in_progress"

    db.commit()
    db.refresh(ticket)
    return ticket


def update_status(db: Session, ticket_id: int, status: str):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return None

    ticket.status = status

    db.commit()
    db.refresh(ticket)
    return ticket