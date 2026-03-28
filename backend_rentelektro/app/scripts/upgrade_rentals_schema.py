from sqlalchemy import text

from app.core.database import SessionLocal


ALTER_STATEMENTS = [
    """
    ALTER TABLE rentals
    ADD COLUMN IF NOT EXISTS is_paid integer NOT NULL DEFAULT 0
    """,
    """
    ALTER TABLE rentals
    ADD COLUMN IF NOT EXISTS paid_at timestamp NULL
    """,
    """
    ALTER TABLE rentals
    ADD COLUMN IF NOT EXISTS handed_over_at timestamp NULL
    """,
    """
    ALTER TABLE rentals
    ADD COLUMN IF NOT EXISTS returned_at timestamp NULL
    """,
    """
    ALTER TABLE rentals
    ADD COLUMN IF NOT EXISTS renter_seen_at timestamp NULL
    """,
    """
    UPDATE rentals
    SET is_paid = CASE
        WHEN status IN ('paid_not_rented', 'paid_rented', 'fulfilled') THEN 1
        ELSE COALESCE(is_paid, 0)
    END
    """,
    """
    UPDATE rentals
    SET handed_over_at = COALESCE(handed_over_at, start_date)
    WHERE status IN ('paid_rented', 'fulfilled')
    """,
    """
    UPDATE rentals
    SET returned_at = COALESCE(returned_at, end_date)
    WHERE status = 'fulfilled'
    """,
]


def main() -> None:
    with SessionLocal() as session:
        for statement in ALTER_STATEMENTS:
            session.execute(text(statement))
        session.commit()

    print("Rentals schema upgraded.")


if __name__ == "__main__":
    main()
