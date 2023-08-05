from typing import Dict
from uuid import uuid4
from tqdm import tqdm
from math import ceil
import pandas as pd

from .utils import chunker
from .queries import CREATE_EXTERNAL_LABEL_MUTATION

MAX_FILE_UPLOAD_BATCH_SIZE = 50


class LabelUploadError(Exception): pass
class InvalidAnnotation(Exception): pass

class DocumentUploader():
    def __init__(self, api):
        self._api = api

    def upload_df(self, documents_df):
        upload_queue = []
        for index, document in documents_df.iterrows():
            metadata_keys = set(document.keys())
            try:
                metadata_keys.remove('contents')
                metadata_keys.remove('label')
                metadata_keys.remove('annotations')
            except KeyError:
                pass

            new_doc = {
                'external_id': index,
                'contents': document['contents'],
                'metadata': { key: document[key] for key in metadata_keys }
            }
            upload_queue.append(new_doc)

        num_batches = ceil(len(upload_queue) / MAX_FILE_UPLOAD_BATCH_SIZE)
        for document_batch in tqdm(chunker(upload_queue, MAX_FILE_UPLOAD_BATCH_SIZE), f'Uploading documents in {num_batches} batches (batch_size = {MAX_FILE_UPLOAD_BATCH_SIZE})'):
            document_data = {
                'documents': [
                    {'external_id': doc['external_id'], 'contents': doc['contents'], 'metadata': doc['metadata']}
                    for doc in document_batch
                ]
            }
            data = self._api.post('documents/upload', document_data) # TODO-2: convert to graphql


class LabelUploader():
    def __init__(self, api, project, cycle=None):
        self._api = api
        self._project = project
        self._cycle = cycle

    def upload_df(self, labels_df):
        created = []
        for index, label in tqdm(labels_df.iterrows(), f'Uploading {len(labels_df)} labels'):
            created.append(self.__upload_label(index, label))
        return created

    def __upload_label(self, external_id, row):
        label_contents = {}

        if row.get('label'):
            label_contents['class'] = row['label']

        if isinstance(row.get('annotations'), list):
            label_contents['annotations'] = self.__transform_annotations(external_id, row['annotations'])

        if len(label_contents.keys() & ('class', 'annotations')) == 0:
            raise LabelUploadError('You must provide either a `label` or `annotations` column.')

        variables = {
            'projectId': self._project.id,
            'cycleId': self._cycle.id if self._cycle else None,
            'externalDocumentId': external_id,
            'contents': label_contents,
            # 'metadata': metadata
        }

        try:
            res: Dict = self._api.graphql(CREATE_EXTERNAL_LABEL_MUTATION, variables)
            return {
                'id': res['data']['createExternalLabel']['label']['id'],
                'document_id': res['data']['createExternalLabel']['label']['document']['externalId']
            }
        except TypeError:
            raise LabelUploadError('An unknown error occured. Are your label/annotation classes correct?') from None
        except Exception as e:
            res_json = e.response.json()
            first_error = res_json['errors'][0]
            print(f'The operation failed with message: {first_error["message"]}')

    def __transform_annotations(self, external_id, annotations):
        if not isinstance(annotations[0], list):
            raise LabelUploadError('Invalid annotations; the value must be a list of lists')

        # label contents = { start: int, end: int, classId: UUID, selectedText?: string, notes?: string}
        new_annotations = []
        for annotation in annotations:
            if len(annotation) != 3:
                raise InvalidAnnotation(f'Annotation schema is incorrect for document id: {external_id}')

            start, end, label = annotation
            annotation = {
                'start': start,
                'end': end,
                'class': label
            }

            new_annotations.append(annotation)

        return new_annotations
