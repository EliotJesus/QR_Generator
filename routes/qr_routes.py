import io

import qrcode
from flask import Blueprint, redirect, send_file, abort, request, url_for

from database import get_db
from helpers import now_text, get_public_base_url


qr_bp = Blueprint("qr", __name__)


@qr_bp.route("/q/<code>")
def short_redirect(code):
    with get_db() as conn:
        link = conn.execute("""
            SELECT *
            FROM links
            WHERE code = ?
        """, (code,)).fetchone()

        if not link:
            abort(404)

        scanned_at = now_text()
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent", "")[:300]

        conn.execute("""
            UPDATE links
            SET scans = scans + 1,
                last_scan_at = ?
            WHERE id = ?
        """, (scanned_at, link["id"]))

        conn.execute("""
            INSERT INTO scans (link_id, scanned_at, ip, user_agent)
            VALUES (?, ?, ?, ?)
        """, (link["id"], scanned_at, ip, user_agent))

    return redirect(link["original_url"])


@qr_bp.route("/qr/<code>.png")
def qr_image(code):
    with get_db() as conn:
        link = conn.execute("""
            SELECT *
            FROM links
            WHERE code = ?
        """, (code,)).fetchone()

    if not link:
        abort(404)

    short_url = get_public_base_url() + url_for("qr.short_redirect", code=code)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3
    )

    qr.add_data(short_url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="#121212",
        back_color="#FFFFFF"
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")


@qr_bp.route("/download/<code>")
def download_qr(code):
    with get_db() as conn:
        link = conn.execute("""
            SELECT *
            FROM links
            WHERE code = ?
        """, (code,)).fetchone()

    if not link:
        abort(404)

    short_url = get_public_base_url() + url_for("qr.short_redirect", code=code)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3
    )

    qr.add_data(short_url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="#121212",
        back_color="#FFFFFF"
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    filename = f"qr_{code}.png"

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name=filename
    )