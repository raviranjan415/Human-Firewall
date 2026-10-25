"""Safe database schema migration script for Human Firewall."""

import sqlite3
from app import create_app
from app.extensions import db
from app.models.organization import generate_org_code
from app.services.seed import run_seed

def migrate():
    conn = sqlite3.connect('instance/cyberquest.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(organizations)')
    existing_cols = {row[1] for row in cursor.fetchall()}

    new_columns = [
        ('org_code', "VARCHAR(32)"),
        ('domain', "VARCHAR(120)"),
        ('require_passcode', "BOOLEAN DEFAULT 0"),
        ('passcode_hash', "VARCHAR(255)"),
        ('require_approval', "BOOLEAN DEFAULT 0"),
        ('seats_purchased', "INTEGER DEFAULT 50"),
        ('subscription_plan', "VARCHAR(32) DEFAULT 'starter'"),
        ('subscription_status', "VARCHAR(32) DEFAULT 'active'"),
        ('subscription_expires_at', "DATETIME"),
        ('contact_email', "VARCHAR(255)"),
        ('contact_name', "VARCHAR(160)"),
    ]

    for col_name, col_type in new_columns:
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE organizations ADD COLUMN {col_name} {col_type}")
            print(f"Added column: {col_name}")

    cursor.execute('SELECT id, org_code FROM organizations')
    for org_id, code in cursor.fetchall():
        if not code:
            new_code = generate_org_code()
            cursor.execute("UPDATE organizations SET org_code = ? WHERE id = ?", (new_code, org_id))
            print(f"Set org_code for org {org_id}: {new_code}")

    conn.commit()
    conn.close()

    # Now create any missing tables
    app = create_app('development')
    with app.app_context():
        db.create_all()
        seed_lines = run_seed(with_demo=True)
        print("Seed result:", seed_lines)

if __name__ == "__main__":
    migrate()
