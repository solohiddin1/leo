from apps.user.repositories.job_repo import JobRepo


class JobService:

    @staticmethod
    def get_all_jobs():
        return JobRepo.get_all()