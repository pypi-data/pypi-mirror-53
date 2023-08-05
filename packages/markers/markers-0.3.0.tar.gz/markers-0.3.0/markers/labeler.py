import ipywidgets as widgets # type: ignore
from traitlets import Unicode, Dict, List # type: ignore

def noop(*args): pass

@widgets.register
class Labeler(widgets.DOMWidget):
    """A data labeling widget to be used with Markers.ai."""
    _view_name = Unicode('AnnotationView').tag(sync=True)
    _model_name = Unicode('AnnotationModel').tag(sync=True)
    _view_module = Unicode('markers').tag(sync=True)
    _model_module = Unicode('markers').tag(sync=True)
    _view_module_version = Unicode('^0.3.0').tag(sync=True)
    _model_module_version = Unicode('^0.3.0').tag(sync=True)

    metadata = Dict({}).tag(sync=True)

    def __init__(self, project, cycle_id=None, document_ids=None, **kwargs):
        super(Labeler, self).__init__(**kwargs)

        self.metadata = {
            'apiUrl': project._api.api_url,
            'apiKey': project._api.api_key,
            'projectId': project.id,
            'cycleId': cycle_id,
            'externalDocumentIds': document_ids
        }

        self.on_msg(self._handle_message)

    def _handle_message(self, _, content, buffers):
        handlers = {
            'close_widget': self._handle_close,
        }
        handler = handlers.get(content['event'], noop)
        handler(content.get('data', None))

    def _handle_close(self, *args):
        self.close()
