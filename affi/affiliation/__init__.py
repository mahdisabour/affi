class OrderStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    ON_HOLD = "on-hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    FAILED = "failed"
    TRASH = "trash"

    CHOICES = [
        (PENDING, "pending"),
        (PROCESSING, "processing"),
        (ON_HOLD, "on-hold"),
        (COMPLETED, "completed"),
        (CANCELLED, "cancelled"),
        (REFUNDED, "refunded"),
        (FAILED, "failed"),
        (TRASH, "trash"),
    ]