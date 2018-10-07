import multiprocessing
import time
import sys


class JobScheduler:

    class Job:

        def __init__(self, job):
            self._is_started = False
            self._job = job

        def start(self):
            self._job.start()
            self._is_started = True

        def is_running(self):
            return self._is_started and self._job.is_alive()

        def is_done(self):
            return self._is_started and not self._job.is_alive()

    def __init__(self, jobs, num_threads, file=sys.stdout, delay=0):
        self.jobs = [JobScheduler.Job(job) for job in jobs]
        self.num_threads = num_threads
        self._top = 0
        self._file = file
        self._delay = delay
        self._total_jobs = len(self.jobs)

    def _get_num_running_jobs(self):
        num_running_jobs = 0
        for job in self.jobs:
            if job.is_running():
                num_running_jobs += 1
        return num_running_jobs

    def _get_num_done_jobs(self):
        num_done_jobs = 0
        for job in self.jobs:
            if job.is_done():
                num_done_jobs += 1
        return num_done_jobs

    def run_and_wait(self):
        cur = 0
        while True:
            if self._get_num_done_jobs() >= self._total_jobs:
                break
            if self._get_num_running_jobs() < self.num_threads and self._top < self._total_jobs:
                self.jobs[self._top].start()
                self._top += 1
                time.sleep(self._delay)
                continue
            if cur % 10 == 0:
                print('JobScheduler    total_jobs:{0:<10}done:{1:<10}running:{2:10}'.format(self._total_jobs, self._get_num_done_jobs(), self._get_num_running_jobs()), file=self._file)
                cur = 0
            cur += 1
            time.sleep(1)


if __name__ == '__main__':
    def hoge(number):
        time.sleep(1 * number + 0.1)

    jobs = []
    for i in range(20):
        p = multiprocessing.Process(target=hoge, args=(i,))
        jobs.append(p)

    num_threads = 10
    job_scheduler = JobScheduler(jobs, num_threads, file=sys.stdout)
    job_scheduler.run_and_wait()
    print('! Done')
