import json

from api.sanity import SanityAPI
from misc.decorators import handle_error
from misc.utils import slugify


class ContentService:
    KEY_CREATE = "create"
    TYPE_ARTICLE = "article"

    def __init__(self):
        self.sanity = SanityAPI()

    def get_recent_processed_checklist_ids(self):
        query = """
        *[_type == 'article' && dateTime(_createdAt) > dateTime(now()) - 60*60*24] 
        | order(_createdAt desc) {
            source
        }['source']
        """

        data = self.sanity.query(query)
        return [source.split("/")[-1] for source in data["result"]]

    @staticmethod
    def _to_blocks(paragraphs):
        return [
            {
                "_key": str(i),
                "_type": "block",
                "style": "normal",
                "children": [{"_type": "span", "text": par}],
            }
            for i, par in enumerate(paragraphs)
        ]

    def _prepare_for_publication(self, data):
        content = data.pop("content")
        paragraphs = [p for p in content.split("\n") if len(p)]
        title = paragraphs.pop(0).replace("**", "").strip()

        return {
            "mutations": [
                {
                    self.KEY_CREATE: {
                        "_type": self.TYPE_ARTICLE,
                        "title": title,
                        "slug": f"{data['id'].lower()}-{slugify(title)}",
                        "body": self._to_blocks(paragraphs),
                        "tags": [data["province"], *data["participants"]],
                        "source": data["source"],
                        "metadata": json.dumps(data),
                    }
                }
            ]
        }

    @handle_error
    def publish(self, data):
        body = self._prepare_for_publication(data)
        return self.sanity.mutate(body)
