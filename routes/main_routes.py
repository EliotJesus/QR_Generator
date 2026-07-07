from flask import Blueprint, render_template, request, redirect, url_for, flash

from database import get_db
from helpers import is_valid_url, generate_code, now_text, get_public_base_url


main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    with get_db() as conn:
        links = conn.execute("""
            SELECT *
            FROM links
            ORDER BY id DESC
        """).fetchall()

        total_links = conn.execute("""
            SELECT COUNT(*) AS total
            FROM links
        """).fetchone()["total"]

        total_scans = conn.execute("""
            SELECT COALESCE(SUM(scans), 0) AS total
            FROM links
        """).fetchone()["total"]

        most_used = conn.execute("""
            SELECT *
            FROM links
            ORDER BY scans DESC
            LIMIT 1
        """).fetchone()

        recent_scans = conn.execute("""
            SELECT scans.*, links.title, links.code
            FROM scans
            INNER JOIN links ON scans.link_id = links.id
            ORDER BY scans.id DESC
            LIMIT 5
        """).fetchall()

    return render_template(
        "index.html",
        links=links,
        base_url=get_public_base_url(),
        total_links=total_links,
        total_scans=total_scans,
        most_used=most_used,
        recent_scans=recent_scans
    )


@main_bp.route("/create", methods=["POST"])
def create_link():
    title = request.form.get("title", "").strip()
    original_url = request.form.get("original_url", "").strip()

    if not is_valid_url(original_url):
        flash("Ingresa una URL válida que empiece con http:// o https://", "error")
        return redirect(url_for("main.index"))

    code = generate_code()
    created_at = now_text()

    with get_db() as conn:
        conn.execute("""
            INSERT INTO links (title, original_url, code, created_at)
            VALUES (?, ?, ?, ?)
        """, (title, original_url, code, created_at))

    flash("QR creado correctamente.", "success")
    return redirect(url_for("main.index"))


@main_bp.route("/delete/<code>", methods=["POST"])
def delete_link(code):
    with get_db() as conn:
        link = conn.execute("""
            SELECT id
            FROM links
            WHERE code = ?
        """, (code,)).fetchone()

        if link:
            conn.execute("""
                DELETE FROM scans
                WHERE link_id = ?
            """, (link["id"],))

            conn.execute("""
                DELETE FROM links
                WHERE id = ?
            """, (link["id"],))

            flash("QR eliminado correctamente.", "success")

    return redirect(url_for("main.index"))