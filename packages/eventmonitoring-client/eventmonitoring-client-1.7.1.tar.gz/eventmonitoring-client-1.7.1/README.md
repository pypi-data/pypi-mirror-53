# EM client

# Install
    Install using `pip`...
    
        pip install eventmonitoring-client
        
# Usage
```python
# setting.py
from event_monitoring import EMConfig
EMConfig(
    SYSTEM_EVENT_TOKEN='<token>',
    SYSTEM_EVENT_URL='<url>',
    SYSTEM_EVENT_NAME='<name>',
    em_notify=True, # if wanna telegram notification else False
    debug=True # True or False
)   

# your logic
from event_monitoring import event, run, log_exception

# decoration you function
@event(keys=['integration_id', 'cred_login'], list_value="task_list", iter_key='key')
def test(task_list: list, key: int):
    ...


# if u wanna log exceptions to server
try:
    ...
except Exception as e:
    name = create_event_name(['integration_id', 'cred_login'], task_list, key)
    log_exception(name, str(e))
```