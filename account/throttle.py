from rest_framework.throttling import AnonRateThrottle


class ResetPasswordRateThrottle(AnonRateThrottle):
    scope = 'reset_password_request'
