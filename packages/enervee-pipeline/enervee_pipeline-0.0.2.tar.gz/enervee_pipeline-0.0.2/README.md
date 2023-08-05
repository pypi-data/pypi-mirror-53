# README

### What is this repository for?
* Handles sending, receiving and saving data through queues and cloud storage
* Version 0.0.1

### How do I get set up to test the enervee_pipeline repo?
This can help you get setup with the proper environment and begin local development of this repo.

* Configuration -- Python 3.7.3
    ```python
    pip install pipenv
    ```

* Ensure you've downloaded python [3.7.3](https://www.python.org/downloads/release/python-373/)
    ```python
    which -a python3
    ```

* Startup pipenv pointing to the location of your `python3` if needed
    ```python
    pipenv --python /usr/local/bin/python3
    ```

* Use Pipfile to install necessary packages. This will update all dependencies
    ```python
    pipenv install
    ```

* To activate this project's virtualenv
    ```python
    pipenv shell
    ```


### How do I make use of this repo as an imported package?

#### Install enervee_pipeline

Using test PyPi package version (helpful during local development)
```bash
pip install -i https://test.pypi.org/simple/ enervee-pipeline==0.0.1
```

Using PyPi package
```bash
pip install enervee-pipeline
```


#### Pass Through Example
Using dummy lambda function that returns None and takes in 2 dummy params:
```python
from enervee_pipeline.queue_processor import QueueProcessor
from enervee_pipeline.utils.queue import enqueue_message_by_queue_name
test_processor = QueueProcessor(processor_function=lambda x, y: None, input_queue_names=['test-input-queue'], should_delete_message=True)
message_body = {}
enqueue_message_by_queue_name('test-input-queue', message_body)
test_processor.run()
```

Using defined `my_processor_function` that takes in a queue message's `message_body` and `message_id` as its parameters:

```python
def my_processor_function(message_body, message_id):
    print('Processing message_id: %s, attr_1: %s, attr_2: %s' % (
        message_id,
        message_body.get('attr_1'),
        message_body.get('attr_2')
    ))
    
from enervee_pipeline.queue_processor import QueueProcessor
from enervee_pipeline.utils.queue import enqueue_message_by_queue_name
test_processor = QueueProcessor(processor_function=my_processor_function, input_queue_names=['test-input-queue'], should_delete_message=True)
message_body = {'attr_1': 'attributed', 'attr_2': 'attribution'}
enqueue_message_by_queue_name('test-input-queue', message_body)
test_processor.run()
```

