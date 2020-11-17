import asyncio
import logging
import unittest
from tests.utils import TestHarness, tasks

logging.basicConfig(level=logging.INFO)

finally_flag = False


@tasks.bind()
def hello_workflow(first_name, last_name):
    return tasks.send(_say_hello, first_name, last_name)


@tasks.bind()
def hello_and_goodbye_workflow(first_name, last_name):
    return tasks.send(_say_hello, first_name, last_name).continue_with(_say_goodbye, goodbye_message="see you later!")


@tasks.bind()
def _say_hello(first_name, last_name):
    return f'Hello {first_name} {last_name}'


@tasks.bind(worker_name='async_worker')
async def _say_goodbye(greeting, goodbye_message):
    await asyncio.sleep(0)
    return f'{greeting}.  So now I will say {goodbye_message}'


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_harness = TestHarness()

    def test_pipeline(self):
        pipeline = tasks.send(hello_workflow, 'Jane', 'Doe')
        result = self.test_harness.run_pipeline(pipeline)
        self.assertEqual(result, 'Hello Jane Doe')

    def test_pipeline_using_kwargs(self):
        pipeline = tasks.send(hello_workflow, first_name='Jane', last_name='Doe')
        result = self.test_harness.run_pipeline(pipeline)
        self.assertEqual(result, 'Hello Jane Doe')

    def test_pipeline_with_continuation(self):
        pipeline = tasks.send(hello_and_goodbye_workflow, 'Jane', last_name='Doe')
        result = self.test_harness.run_pipeline(pipeline)
        self.assertEqual(result, 'Hello Jane Doe.  So now I will say see you later!')


if __name__ == '__main__':
    unittest.main()
