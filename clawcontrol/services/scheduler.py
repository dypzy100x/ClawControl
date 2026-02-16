"""Task Scheduler - Cron-style automation"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}
    
    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
    
    def add_job(self, job_id: str, func, cron_expression: str):
        job = self.scheduler.add_job(
            func,
            'cron',
            **self._parse_cron(cron_expression),
            id=job_id
        )
        self.jobs[job_id] = job
        return job
    
    def _parse_cron(self, expression: str) -> dict:
        # Simple cron parser
        return {"minute": "*/5"}  # Every 5 minutes
    
    def remove_job(self, job_id: str):
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]

task_scheduler = TaskScheduler()
