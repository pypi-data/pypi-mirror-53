from . import (
    security,
    security_data
)

# Classes
data = security_data.security_data
security = security.security

def from_csv(file):
    return security().from_csv(file)

def from_json(file):
    return security().from_json(file)

def from_rest(ticker = None, days = 262):
    return security().from_rest(ticker, days)

def previous_business_day(days = 1):
    return security_data.last_business_day(days)