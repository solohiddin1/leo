from apps.user.models import Job


class JobRepo:

    @staticmethod
    def get_all():
        return Job.objects.all()

    @staticmethod
    def get_by_id(job_id: int) -> Job | None:
        return Job.objects.filter(id=job_id).first()