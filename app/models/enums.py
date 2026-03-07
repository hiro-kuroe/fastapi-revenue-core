from enum import Enum

class SubscriptionStatus(str, Enum):
    FREE = "free"
    PRO = "pro"
    CANCELED = "canceled"
    EXPIRED = "expired"