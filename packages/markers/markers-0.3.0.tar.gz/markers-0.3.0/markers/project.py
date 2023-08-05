from IPython.display import display, HTML # type: ignore
from typing import List, Optional, Dict
from uuid import uuid4, UUID
import pandas as pd

from .labeler import Labeler
from .uploader import DocumentUploader, LabelUploader, LabelUploadError
from .label_batch import LabelBatch
from .queries import PROJECT_QUERY, ASSIGN_DOCUMENTS_MUTATION, CREATE_CYCLE_MUTATION, PROJECT_CYCLES_QUERY

class Project:
    def __init__(self, api, project_id: UUID, project_data):
        self._api = api
        self.id = project_id
        self.name = project_data['name']

    def __repr__(self):
        return f'<Project (id="{self.id}", name="{self.name}")>'

    @classmethod
    def load(cls, api, project_id): # TODO-3: clean project names
        response = api.graphql(PROJECT_QUERY, { 'projectId': project_id })
        return cls(api, project_id, response['data']['projectById'])

    def get_labels(self, **kwargs):
        return LabelBatch.load(self, **kwargs)

    def get_cycles(self):
        response = self._api.graphql(PROJECT_CYCLES_QUERY, { 'projectId': self.id })
        cycles = []
        for cycle in response['data']['projectById']['cycles']['nodes']:
            cycles.append({
                'id': cycle['id'],
                'document_count': cycle['documentCount'],
                'label_count': cycle['labelCount'],
                'task_count': cycle['tasks']['totalCount'],
                'created_at': cycle['createdAt']
            })
        return cycles

    def create_cycle(self):
        # TODO-2: allow passing in settings (default task type, task action)
        result = self._api.graphql(CREATE_CYCLE_MUTATION, { 'projectId': self.id })
        return result['data']['createCycle']['cycle']['id']

    def create_tasks(self, cycle_id = None, document_ids = None, label_ids = None, assignee_role = None):
        to_self = True if not assignee_role else False

        self._api.graphql(ASSIGN_DOCUMENTS_MUTATION, {
            'projectId': self.id,
            'cycleId': cycle_id,
            'externalDocumentIds': document_ids,
            'labelIds': label_ids,
            'toSelf': to_self,
            'toRole': assignee_role
        })

    def upload_documents(self, documents_df, create_tasks = False, assignee_role = None):
        DocumentUploader(self._api).upload_df(documents_df)

        if create_tasks:
            external_document_ids = list(documents_df.index)
            self.create_tasks(document_ids=external_document_ids, assignee_role=assignee_role)

    def upload_labels(self, labels_df, create_tasks = False, assignee_role = None):
        created_labels = LabelUploader(self._api, self).upload_df(labels_df)

        if create_tasks:
            label_ids, external_document_ids = zip(*[[x['id'], x['document_id']] for x in created_labels])
            self.create_tasks(document_ids=external_document_ids, label_ids=label_ids, assignee_role=assignee_role)

    def label(self, df = None, cycle_id: str = None):
        # shortcut method
        if df is not None:
            if not ('contents' in df):
                raise Exception('Invalid dataframe schema; must contain contents.')

            self.upload_documents(df, create_tasks=True)
            document_ids = list(df.index)
        else:
            document_ids = None

        labeler = Labeler(self, cycle_id=cycle_id, document_ids=document_ids)
        display(labeler)

    def review(self, df = None, cycle_id: str = None):
        # shortcut method
        if df is not None:
            if not ('contents' in df and ('label' in df or 'annotations' in df)):
                raise Exception('Invalid dataframe schema; must contain contents AND (label AND/OR annotations).')

            self.upload_documents(df)
            self.upload_labels(df, create_tasks=True)
            document_ids = list(df.index)
        else:
            document_ids = None

        labeler = Labeler(self, cycle_id=cycle_id, document_ids=document_ids)
        display(labeler)

    def open_app(self):
        s = f'<script type="text/javascript">window.open("{self._api.api_url}/projects/{self.id}")</script>'
        display(HTML(s))
