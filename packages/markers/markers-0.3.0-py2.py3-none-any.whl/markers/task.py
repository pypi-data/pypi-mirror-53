from typing import List, Optional, Dict

from .label import Label
from .document import Document

class Task:
    def __init__(self, id, status, document, type):
        self.id = id
        self.status = status
        self.document = Document.deserialize(document)
        self.labels = []
        self.type = type

    @classmethod
    def deserialize(cls, response):
        task = cls(response['id'], response['status'].lower(), response['document'], response['type'])
        for label_obj in response['labels']:
            label = Label.deserialize_from_task(task, label_obj)
            task.labels.append(label)
        return task

    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'status': self.status,
            'type': self.type
        }
