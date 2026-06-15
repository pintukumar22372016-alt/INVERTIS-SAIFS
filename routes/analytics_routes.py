"""
SAIFS - Analytics Routes
Analytics dashboard with rich chart data.
"""
from flask import Blueprint, render_template
from utils.auth_utils import login_required
from services.analytics_service import AnalyticsService

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/")
@login_required
def analytics():
    data = AnalyticsService.dashboard_data()
    return render_template("features/analytics.html", **data)