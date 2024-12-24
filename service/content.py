import json

from api import SanityAPI
from misc.decorators import handle_error
from misc.utils import slugify


class ContentService:
    KEY_CREATE = "create"
    KEY_DELETE = "delete"
    TYPE_ARTICLE = "article"

    def __init__(self, sanity_api: SanityAPI):
        self.sanity = sanity_api

    def get_published_data_from_last_24h(self):
        query = """
        *[_type == 'article' && dateTime(_createdAt) > dateTime(now()) - 60*60*24] 
        | order(_createdAt desc) {
            _id,
            slug,
            metadata
        }
        """

        data = self.sanity.query(query)

        unpacked = []
        for d in data["result"]:
            if "drafts" not in d["_id"]:
                metadata = json.loads(d["metadata"])
                unpacked.append(
                    {
                        "id": d["_id"],
                        "slug": d["slug"],
                        "datetime": f"{metadata['date']} {metadata['time']}",
                        "metadata": metadata,
                    }
                )

        return sorted(unpacked, key=lambda d: d["datetime"], reverse=True)

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

    def _format_to_publish(self, data):
        content = data.pop("content")
        source = data.pop("source")

        paragraphs = [p for p in content.split("\n") if len(p)]
        title = paragraphs.pop(0).replace("**", "").strip()
        slug = f"{data['id'].lower()}-{slugify(title)}"
        tags = [data["province"], *data["participants"]]

        return {
            self.KEY_CREATE: {
                "_type": self.TYPE_ARTICLE,
                "title": title,
                "slug": slug,
                "body": self._to_blocks(paragraphs),
                "tags": tags,
                "source": source,
                "metadata": json.dumps(data),
            }
        }

    @handle_error
    def publish(self, *args):
        body = {"mutations": [self._format_to_publish(data) for data in args]}
        return self.sanity.mutate(body)

    @handle_error
    def delete_by_id(self, *args):
        body = {"mutations": [{self.KEY_DELETE: {"id": id}}] for id in args}
        return self.sanity.mutate(body)
