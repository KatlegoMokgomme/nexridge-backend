from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role

from app.services.dashboard_service import (
    get_dashboard_stats,
    get_tickets_per_user_chart,
    get_workload_chart,
    get_sla_breaches,
    get_avg_resolution_time,
    get_ticket_trends_chart,
    get_ticket_status_distribution,
    get_sla_breach_trend_chart,
    get_dashboard_analytics
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# =========================================================
# 📊 BASIC STATS
# =========================================================
@router.get("/stats")
def stats(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_dashboard_stats(db)


# =========================================================
# 👥 TICKETS PER USER
# =========================================================
@router.get("/users")
def users(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_tickets_per_user_chart(db)


# =========================================================
# ⚠️ SLA BREACHES (LIST)
# =========================================================
@router.get("/sla-breaches")
def sla_breaches(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_sla_breaches(db)


# =========================================================
# ⏱ AVERAGE RESOLUTION TIME
# =========================================================
@router.get("/avg-resolution")
def avg_resolution(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_avg_resolution_time(db)


# =========================================================
# 👨‍💻 WORKLOAD
# =========================================================
@router.get("/workload")
def workload(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_workload_chart(db)


# =========================================================
# 📈 TICKET TRENDS (LINE CHART)
# =========================================================
@router.get("/trends")
def trends(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_ticket_trends_chart(db)


# =========================================================
# 🟢 STATUS DISTRIBUTION (PIE CHART)
# =========================================================
@router.get("/status")
def status_distribution(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_ticket_status_distribution(db)


# =========================================================
# 📉 SLA BREACH TREND (LINE CHART)
# =========================================================
@router.get("/sla-trend")
def sla_trend(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_sla_breach_trend_chart(db)


# =========================================================
# 🚀 FULL ANALYTICS DASHBOARD (ONE CALL FOR FRONTEND)
# =========================================================
@router.get("/analytics")
def analytics(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return get_dashboard_analytics(db)