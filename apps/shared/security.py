from django.contrib.auth.hashers import Argon2PasswordHasher
from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle, UserRateThrottle


class TunedArgon2Hasher(Argon2PasswordHasher):
    memory_cost = 46080
    parallelism = 2
    time_cost = 2


class GeneralThrottle(AnonRateThrottle):
    scope = "general"

    def __init__(self):
        super().__init__()
        self.num_requests = 3
        self.duration = 10


class GeneralUserThrottle(UserRateThrottle):
    scope = "general"

    def __init__(self):
        super().__init__()
        self.num_requests = 3
        self.duration = 10


class IpRateThrottle(SimpleRateThrottle):
    scope = "ip_rate"

    def __init__(self):
        super().__init__()
        self.num_requests = 3
        self.duration = 10

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }
