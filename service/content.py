import json
import random

import pydash

from api import SanityAPI
from misc.decorators import handle_error
from misc.utils import slugify


class ContentService:
    KEY_CREATE = "create"
    KEY_DELETE = "delete"
    TYPE_ARTICLE = "article"

    def __init__(self, sanity_api: SanityAPI):
        self.sanity = sanity_api
        self.publications = None

    def get_published_data_from_last_24h(self):
        query = """
        *[_type == 'article' && dateTime(_createdAt) > dateTime(now()) - 60*60*24] 
        | order(_createdAt desc) {
            _id,
            slug,
            title,
            body[0],
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
                        "title": d["title"],
                        "lead": pydash.get(d, "body.children.0.text"),
                        "metadata": metadata,
                    }
                )

        self.publications = sorted(
            unpacked,
            key=lambda d: d["datetime"],
            reverse=True,
        )

        return self.publications

    def curate_articles(self, articles, max_articles=10):
        # Group articles by region for diversity
        region_groups = {}
        for article in articles:
            region = pydash.get(article, "metadata.province")
            if region not in region_groups:
                region_groups[region] = []
            region_groups[region].append(article)

        # Select one article per region, then fill up to max_articles
        curated = []
        for region, region_articles in region_groups.items():
            # Pick a random article from the region
            curated.append(random.choice(region_articles))

        # If fewer than max_articles, fill the remaining spots with unique random articles
        if len(curated) < max_articles:
            remaining = [a for a in articles if a not in curated]
            curated.extend(
                random.sample(
                    remaining,
                    min(max_articles - len(curated), len(remaining)),
                )
            )

        return sorted(
            curated[:max_articles],
            key=lambda d: d["datetime"],
            reverse=True,
        )

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

        paragraphs = [p.replace("**", "") for p in content.split("\n") if len(p)]
        title = paragraphs.pop(0).strip()
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
