from flask import Blueprint, render_template, abort, url_for

from database import get_db
from helpers import get_public_base_url


stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/stats/<code>")
def stats(code):
    with get_db() as conn:
        link = conn.execute("""
            SELECT *
            FROM links
            WHERE code = ?
        """, (code,)).fetchone()

        if not link:
            abort(404)

        scans = conn.execute("""
            SELECT *
            FROM scans
            WHERE link_id = ?
            ORDER BY id DESC
        """, (link["id"],)).fetchall()

    short_url = get_public_base_url() + url_for("qr.short_redirect", code=code)

    return render_template(
        "stats.html",
        link=link,
        scans=scans,
        short_url=short_url
    )