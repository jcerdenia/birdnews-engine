from api.sanity import SanityAPI


class ContentService:
    def __init__(self):
        self.sanity = SanityAPI()

    def get_last_saved_checklist_id(self):
        query = """
        *[_type == 'article'] 
        | order(_createdAt desc) { 
            source 
        }[0]['source']
        """

        data = self.sanity.query(query)
        source = data["result"]

        return source.split("/")[-1]

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
        content = data["content"]
        paragraphs = [p for p in content.split("\n") if len(p)]
        title = paragraphs.pop(0).replace("**", "").strip()

        return {
            "mutations": [
                {
                    "create": {
                        "_type": "article",
                        "title": title,
                        "slug": data["id"].lower(),
                        "body": self._to_blocks(paragraphs),
                        "tags": [data["province"], *data["participants"]],
                        "source": data["source"],
                    }
                }
            ]
        }

    def publish(self, data):
        body = self._prepare_for_publication(data)
        return self.sanity.mutate(body)
