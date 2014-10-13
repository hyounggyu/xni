import uuid
import pickle
import json

from . import tasks

__all__ = ['scatter', 'gather', 'get_status_json']


RESULTS = dict()
RESULTS_TMP = dict()
STATUS = dict()


def scatter(sender, task_name, args_list, task_final=None):
    global RESULTS_TMP, STATUS

    task_id = uuid.uuid4()
    length = len(args_list)
    index = 0

    for args in args_list:
        sender.send_pyobj([task_id, task_name, length, {index: args}, task_final])
        index = index + 1

    RESULTS_TMP[task_id] = dict()
    STATUS[task_id] = 'RUNNING'


def gather(msg):
    global RESULTS, RESULTS_TMP, STATUS

    task_id, task_name, length, result, task_final = pickle.loads(msg[0]) # It will always be multipart
    RESULTS_TMP[task_id].update(result)
    STATUS[task_id] = 'FINISHED {}/{}'.format(len(RESULTS_TMP[task_id].items()), length)

    if length == len(RESULTS_TMP[task_id].items()):
        RESULTS[task_id] = [RESULTS_TMP[task_id][index] for index in sorted(RESULTS_TMP[task_id])]
        if task_final != None:
            STATUS[task_id] = 'FINALIZE'
            final = getattr(tasks, task_final)
            final(RESULTS[task_id])
        STATUS[task_id] = 'SUCCESS'


def get_status_json():
    status = dict()
    for key, value in STATUS.items():
        status.update({str(key): value})
    return json.dumps(status)
