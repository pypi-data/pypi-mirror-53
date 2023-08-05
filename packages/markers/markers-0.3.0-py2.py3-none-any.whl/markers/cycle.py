from typing import List, Optional, Dict
from uuid import uuid4, UUID
import pandas as pd # type: ignore

from .utils import chunker
from .labeler import Labeler
from .document import Document
from .task import Task


MAX_FILE_UPLOAD_BATCH_SIZE = 50

# TODO-2: this should use LabelBatch rather than maintaining its own list of labels
class Cycle:
    def __init__(self, project, cycle_data: Dict = {}): # TODO-3: fix project type, can't import due to circular import issue
        if cycle_data.get('id', None):
            self.id: str = cycle_data.get('id')
            self._is_new = False
        else:
            self.id: str = Cycle.generate_id()
            self._is_new = True

        self.project = project

        self.tasks: List[Task] = []
        self.documents: List[Document] = []

        self.deserialize_tasks(cycle_data.get('tasks', []))

    def __repr__(self):
        return f'<Cycle (id="{self.id}", document_count={len(self.documents)}, completed_tasks={len(self.completed_tasks)}, incomplete_tasks={len(self.incomplete_tasks)}, skipped_tasks=={len(self.skipped_tasks)})>'

    @property
    def completed_tasks(self):
        return [task for task in self.tasks if task.status == 'complete']

    @property
    def incomplete_tasks(self):
        return [task for task in self.tasks if task.status == 'incomplete']

    @property
    def skipped_tasks(self):
        return [task for task in self.tasks if task.status == 'skipped']

    @property
    def metadata(self):
        return {
            'task_counts': {
                'total': len(self.tasks),
                'complete': len(self.completed_tasks),
                'incomplete': len(self.incomplete_tasks),
                'skipped': len(self.skipped_tasks),
            }
        }

    @classmethod
    def load(cls, project, cycle_id):
        cycle_data = project._api.get(f'projects/{project.id}/cycles/{cycle_id}')
        return cls(project, cycle_data)

    @staticmethod
    def generate_id():
        return str(uuid4())[:8]

    @property
    def labels(self):
        labels = []
        # TODO-3: replace with
        #         return [label for task in self.tasks for label in task.labels]
        #         ?
        for task in self.tasks:
            for label in task.labels:
                labels.append(label)
        return labels

    def deserialize_tasks(self, tasks):
        for task_response in tasks:
            task = Task.deserialize(task_response)
            self.tasks.append(task)
            self.documents.append(task.document)

    def to_df(self):
        df = pd.DataFrame(columns=['document_id', 'label', 'annotations'])
        for task in self.tasks:
            if len(task.labels) == 0:
                # TODO-3: create a SkippedLabel class?
                skipped_label = { 'document_id': task.document.external_id, 'label': None, 'annotations': None }
                df = df.append(skipped_label, ignore_index=True)
            for label in task.labels:
                df = df.append(label.serialize(format='df', project=self.project), ignore_index=True)
        return df.set_index('document_id')

    def add_label(self, task, label):
        current_task = next(t for t in self.tasks if t.id == task.id)
        current_task.labels.append(label)
        current_task.status = 'complete'

        data = {
            'cycle_id': str(self.id),
            'task_id': str(current_task.id),
            'label': label.serialize(format='api')
        }

        self.project._api.post(f'projects/{self.project.id}/labels', data)

    def _add_document(self, external_id, document):
        metadata_keys = set(document.keys())
        metadata_keys.remove('contents')

        new_doc = Document(None, external_id, document['contents'], { key: document[key] for key in metadata_keys })
        self.documents.append(new_doc)

    def add_documents(self, from_df=None):
        if from_df is not None:
            for index, doc in from_df.iterrows():
                self._add_document(index, doc)
        else:
            raise Exception('You must provide a collection of documents to add to the cycle.')

    def serialize(self):
        return { 'id': self.id }

    def save(self):
        if self._is_new:
            cycle = self.project._api.post(f'projects/{self.project.id}/cycles', self.serialize())

        for document_batch in chunker(self.documents, MAX_FILE_UPLOAD_BATCH_SIZE):
            document_data = {
                'documents': [doc.serialize() for doc in document_batch]
            }
            data = self.project._api.post('documents/upload', document_data)

            # TODO-3: refactor this, this is inefficient and mutates self.documents
            for doc in document_batch:
                for created in data['documents']:
                    if doc.external_id == created['externalId']:
                        doc.id = created['id']

        created_document_ids = [doc.id for doc in self.documents]
        cycle = self.project._api.post(f'projects/{self.project.id}/cycles/{self.id}/tasks', { 'document_ids': created_document_ids })

        # for now, we just overwrite everything
        self.id = cycle['id']
        self.tasks = []
        self.documents = []
        self.deserialize_tasks(cycle['tasks'])
        self._is_new = False

    def label(self):
        labeler = Labeler(self.project, self)
        display(labeler)

        return self

    def next_task(self, skipped_tasks=[]):
        for _, task in enumerate(self.tasks):
            if task.status == 'incomplete':
                return task
        raise IndexError('No incomplete tasks found.')

    def skip_task(self, task):
        task.status = 'skipped'
        self.project._api.put(f'projects/{self.project.id}/tasks/{task.id}', {'status': 'skipped'})
