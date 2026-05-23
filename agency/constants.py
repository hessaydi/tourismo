PACKAGE_CATEGORY_CHOICES = [
    ("adventure", "Adventure"),
    ("cultural", "Cultural"),
    ("beach", "Beach & Relaxation"),
    ("safari", "Safari"),
    ("city", "City Break"),
    ("cruise", "Cruise"),
]

PACKAGE_STATUS_CHOICES = [
    ("active", "Active"),
    ("inactive", "Inactive"),
    ("soldout", "Sold Out"),
]

BOOKING_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("cancelled", "Cancelled"),
    ("completed", "Completed"),
]

BOOKING_PAYMENT_STATUS_CHOICES = [
    ("unpaid", "Unpaid"),
    ("partial", "Partial"),
    ("paid", "Paid"),
    ("refunded", "Refunded"),
]

BOOKING_REF_PREFIX = "TRM"
BOOKING_REF_DIGITS = 7
