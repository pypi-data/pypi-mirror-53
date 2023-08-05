import pandas as pd

from .queries import LABELS_FOR_PROJECT_QUERY

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class LabelBatch:
    def __init__(self, project_id, data):
        self.project_id = project_id
        self.data = data

        self.__cat_map = {}
        for cat in self.data['categories']['nodes']:
            self.__cat_map[cat['id']] = cat['name']

    def __len__(self):
        return len(self.data['labels']['nodes'])

    def __repr__(self):
        return f'<LabelBatch (project_id="{self.project_id}", label_count="{len(self)}")>'

    @classmethod
    def load(cls, project, filter={}, **kwargs):
        label_filter = { 'taskAction': { 'equalTo': 'create' } }
        for k in filter.keys():
            label_filter[to_camel_case(k)] = { 'equalTo': filter[k] }

        response = project._api.graphql(LABELS_FOR_PROJECT_QUERY, {
            'projectId': project.id,
            'labelFilter': label_filter
        })

        label_batch = cls(project.id, response['data']['projectById'])
        return label_batch

    def __category_id_to_name(self, category_id):
        return self.__cat_map[category_id]

    def __document_category_for_label(self, label):
        try:
            return self.__category_id_to_name(label['contents']['categoryId'])
        except KeyError:
            return None

    def __annotations_for_label(self, label):
        try:
            return [
                [
                    annotation['start'],
                    annotation['end'],
                    self.__category_id_to_name(annotation['categoryId']),
                    annotation['selectedText']
                ]
                for annotation in label['contents']['annotations']
            ]
        except (TypeError, KeyError):
            return None

    def to_df(self):
        # TODO-2: simplify this if there are no annotations, all source == 'INTERNAL' (in which case, omit source and review_result)
        df = pd.DataFrame(columns=['document_id', 'label', 'annotations', 'source', 'review_result'])

        for label in self.data['labels']['nodes']:
            df = df.append({
                'document_id': label['document']['externalId'],
                'label': self.__document_category_for_label(label),
                'annotations': self.__annotations_for_label(label),
                'source': label['source'],
                'review_result': label['reviewResult']
            }, ignore_index=True)

        return df
