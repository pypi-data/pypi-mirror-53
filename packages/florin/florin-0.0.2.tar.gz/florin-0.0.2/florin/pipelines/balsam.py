"""Distributed processing pipeline using Balsam.

Classes
-------
BalsamPipeline
    Pipeline for distributed processing using the Balsam job manager.
"""

import os
import subprocess
import uuid

from florin.pipelines.pipeline import Pipeline
from florin.pipelines.serial import SerialPipeline


class BalsamPipeline(Pipeline):
    """Pipeline for distributed processing using the Balsam job manager.

    """

    def run(self, data, name=None, queue='default', n_workers=128, time=120):
        pipe_path = os.path.join(os.path.abspath('.'), '.balsam_pipeline.pkl')
        with open(pipe_path, 'w') as f:
            bpipe = SerialPipeline()
            bpipe.operations = self.operations
            bpipe.dump(f)

        if not isinstance(name, str):
            name = str(uuid.uuid4())
        subprocess.check_call(
            ['balsam', 'app', '--name', name, '--executable',
             'python', '-m', 'florin.run'])

        for i, d in enumerate(data):
            args = ['balsam', 'job', '--name', f'{name}_{i}', '--application',
                    name, '--args', f'"{pipe_path} {d}"']
            subprocess.check_call(args)

        uses_mpi = any(map(lambda x: x.__name__ == 'MPIPipeline',
                           self.operations.nodes))
        mode = 'mpi' if uses_mpi else 'serial'
        subprocess.check_call(['balsam', 'submit-launch', '-A', 'Project',
                               '-q', queue, '-n', str(n_workers), '-t',
                               str(time), f'--job-mode={mode}'])
