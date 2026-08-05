from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth.hashers import Argon2PasswordHasher

class TunedArgon2Hasher(Argon2PasswordHasher):
    memory_cost = 46080
    parallelism = 2
    time_cost = 2

class GeneralThrottle(AnonRateThrottle):
    scope = 'general'

    def __init__(self):
        super().__init__()
        self.num_requests = 3
        self.duration = 10
