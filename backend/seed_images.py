"""
Seed all test images (excluding scene files) into the `images` table.
Safe to call multiple times — uses INSERT OR IGNORE so no duplicates.
"""
import os
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Image

# Resolve test_images/ relative to this file's location (backend/)
TEST_IMAGES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "test_images")
)

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".jfif"}


def seed_images(db: Session) -> int:
    """Insert all non-scene images into the DB. Returns count of newly added rows."""
    if not os.path.isdir(TEST_IMAGES_DIR):
        print(f"[Seeder] WARNING: test_images directory not found at {TEST_IMAGES_DIR}")
        return 0

    # Collect filenames that exist in DB already (for fast lookup)
    existing = {row.filename for row in db.query(Image.filename).all()}

    added = 0
    for filename in sorted(os.listdir(TEST_IMAGES_DIR)):
        # Skip scene images — those belong to Story mode only
        if "scene" in filename.lower():
            continue

        ext = os.path.splitext(filename)[1].lower()
        if ext not in VALID_EXTENSIONS:
            continue

        if filename in existing:
            continue  # Already seeded, skip

        db.add(Image(filename=filename))
        added += 1

    if added:
        db.commit()
        print(f"[Seeder] Added {added} new image(s) to the database.")
    else:
        print(f"[Seeder] All images already seeded — nothing to add.")

    return added


def run_seeder():
    """Convenience entry point called from main.py on startup."""
    db = SessionLocal()
    try:
        seed_images(db)
    finally:
        db.close()
