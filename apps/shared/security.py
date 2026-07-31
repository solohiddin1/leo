from rest_framework.throttling import AnonRateThrottle


class GeneralThrottle(AnonRateThrottle):
    scope = 'general'

    def __init__(self):
        super().__init__()
        self.num_requests = 3
        self.duration = 300