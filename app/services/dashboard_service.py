from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date

from app.models.ticket import Ticket


# =========================================================
# 📊 BASIC DASHBOARD STATS
# =========================================================
def get_dashboard_stats(db: Session):
    return {
        "total_tickets": db.query(func.count(Ticket.id)).scalar(),
        "open_tickets": db.query(func.count(Ticket.id)).filter(Ticket.status == "open").scalar(),
        "in_progress_tickets": db.query(func.count(Ticket.id)).filter(Ticket.status == "in_progress").scalar(),
        "closed_tickets": db.query(func.count(Ticket.id)).filter(Ticket.status == "closed").scalar(),
    }


# =========================================================
# 📈 TICKETS OVER TIME (LINE CHART)
# =========================================================
def get_ticket_trends_chart(db: Session):
    rows = db.query(
        cast(Ticket.created_at, Date).label("date"),
        func.count(Ticket.id).label("count")
    ).group_by(
        cast(Ticket.created_at, Date)
    ).order_by(
        cast(Ticket.created_at, Date)
    ).all()

    return [
        {
            "date": str(r.date),
            "count": r.count
        }
        for r in rows
    ]


# =========================================================
# 🟢 STATUS DISTRIBUTION (PIE CHART)
# =========================================================
def get_ticket_status_distribution(db: Session):
    rows = db.query(
        Ticket.status,
        func.count(Ticket.id).label("count")
    ).group_by(Ticket.status).all()

    return [
        {
            "status": r.status,
            "count": r.count
        }
        for r in rows
    ]


# =========================================================
# 👥 TICKETS PER USER (BAR CHART)
# =========================================================
def get_tickets_per_user_chart(db: Session):
    rows = db.query(
        Ticket.created_by,
        func.count(Ticket.id).label("count")
    ).group_by(Ticket.created_by).all()

    return [
        {
            "user": r.created_by,
            "count": r.count
        }
        for r in rows
    ]


# =========================================================
# 👨‍💻 WORKLOAD (ASSIGNED TICKETS - BAR CHART)
# =========================================================
def get_workload_chart(db: Session):
    rows = db.query(
        Ticket.assigned_to,
        func.count(Ticket.id).label("count")
    ).filter(
        Ticket.status != "closed"
    ).group_by(Ticket.assigned_to).all()

    return [
        {
            "user": r.assigned_to or "Unassigned",
            "count": r.count
        }
        for r in rows
    ]


# =========================================================
# ⚠️ SLA BREACH LIST (RAW DATA)
# =========================================================
def get_sla_breaches(db: Session):
    rows = db.query(Ticket).filter(
        Ticket.resolved_at.isnot(None),
        func.extract('epoch', Ticket.resolved_at - Ticket.created_at) / 3600 > Ticket.sla_hours
    ).all()

    return [
        {
            "id": t.id,
            "title": t.title,
            "created_at": t.created_at,
            "resolved_at": t.resolved_at,
            "sla_hours": t.sla_hours
        }
        for t in rows
    ]


# =========================================================
# 📉 SLA BREACH TREND (LINE CHART)
# =========================================================
def get_sla_breach_trend_chart(db: Session):
    rows = db.query(Ticket).filter(
        Ticket.resolved_at.isnot(None)
    ).all()

    data = []

    for t in rows:
        resolution_hours = (t.resolved_at - t.created_at).total_seconds() / 3600
        data.append({
            "date": str(t.created_at.date()),
            "breached": 1 if resolution_hours > t.sla_hours else 0
        })

    return data


# =========================================================
# ⏱ AVERAGE RESOLUTION TIME
# =========================================================
def get_avg_resolution_time(db: Session):
    value = db.query(
        func.avg(
            func.extract('epoch', Ticket.resolved_at - Ticket.created_at) / 3600
        )
    ).filter(Ticket.resolved_at.isnot(None)).scalar()

    return {
        "avg_resolution_hours": round(value or 0, 2)
    }


# =========================================================
# 📦 FULL DASHBOARD PAYLOAD (ONE CALL FOR FRONTEND)
# =========================================================
def get_dashboard_analytics(db: Session):
    return {
        "stats": get_dashboard_stats(db),

        "charts": {
            "trends": get_ticket_trends_chart(db),
            "status_distribution": get_ticket_status_distribution(db),
            "tickets_per_user": get_tickets_per_user_chart(db),
            "workload": get_workload_chart(db),
            "sla_trend": get_sla_breach_trend_chart(db),
        },

        "kpis": {
            "avg_resolution": get_avg_resolution_time(db),
        }
    }