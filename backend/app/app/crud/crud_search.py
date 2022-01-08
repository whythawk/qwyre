from typing import List
from neomodel import db, Q

from app.core.config import settings
from app.models import WorkMetadata, Work
from app.schema_types import WorkStateType


class CRUDSearch:
    @db.read_transaction
    def get_random(self, *, skip: int = 0, limit: int = 100) -> List[WorkMetadata]:
        db_objs = Work.nodes.order_by("?").filter(Q(state=WorkStateType.PUBLISHED.value.upper()))[skip : limit + skip]
        return [w.metadata.single() for w in db_objs]

    def _make_query_safe(self, *, query: str) -> str:
        # https://stackoverflow.com/a/23996445/295606
        return query.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}).strip()

    def get_search_suggestions(self, *, query: str) -> List[str]:
        query = self._make_query_safe(query=query)
        indices = [
            (
                "titles",
                5,
                "title",
                f" MATCH (node)<--(work:Work) WHERE work.state = '{WorkStateType.PUBLISHED.upper()}'",
            ),
            ("creators", 3, "creator", " WHERE NOT node.isPrivate"),
            ("subjects", 1, "term", ""),
        ]
        q = "CALL { "
        for e, (index, boost, key, context) in enumerate(indices):
            q += f"CALL db.index.fulltext.queryNodes('{index}', '{query}~^{boost}') YIELD node, score {context} RETURN node.{key} AS response, score "
            if e < len(indices) - 1:
                q += "UNION ALL "
        q += " } RETURN response, sum(score) AS totalScore ORDER BY totalScore DESC "
        q += f"LIMIT {settings.NEO4J_SUGGESTION_LIMIT}"
        results, _ = db.cypher_query(q)
        return [r[0] for r in results]

    def get_search_results(self, *, query: str) -> List[WorkMetadata]:
        query = self._make_query_safe(query=query)
        indices = [
            (
                "titles",
                5,
                "metadata",
                f" MATCH (metadata)<--(work:Work) WHERE work.state = '{WorkStateType.PUBLISHED.upper()}'",
            ),
            (
                "descriptions",
                3,
                "metadata",
                f" MATCH (metadata)<--(work:Work) WHERE work.state = '{WorkStateType.PUBLISHED.upper()}'",
            ),
            (
                "creators",
                4,
                "node",
                f" MATCH (node)-[AUTHORED]->(metadata:WorkMetadata)<-[DESCRIBED_BY]-(work:Work) WHERE NOT node.isPrivate AND work.state = '{WorkStateType.PUBLISHED.upper()}'",
            ),
            (
                "subjects",
                1,
                "node",
                f" MATCH (node)<-[DESCRIBES_WORK]-(metadata:WorkMetadata)<-[DESCRIBED_BY]-(work:Work) WHERE work.state = '{WorkStateType.PUBLISHED.upper()}'",
            ),
        ]
        q = "CALL { "
        for e, (index, boost, node, context) in enumerate(indices):
            q += f"CALL db.index.fulltext.queryNodes('{index}', '{query}~^{boost}') YIELD node AS {node}, score {context} RETURN metadata, score "
            if e < len(indices) - 1:
                q += "UNION ALL "
        q += " } RETURN metadata, sum(score) AS totalScore ORDER BY totalScore DESC "
        q += f"LIMIT {settings.NEO4J_RESULTS_LIMIT}"
        results, _ = db.cypher_query(q)
        return [WorkMetadata.inflate(r[0]) for r in results]


search = CRUDSearch()
