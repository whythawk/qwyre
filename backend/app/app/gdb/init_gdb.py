import inspect
from neomodel import StructuredNode, ClientError, install_labels

# from neomodel import config
# from app.core.config import settings

import app.models

# from app.gdb import NeomodelConfig

# NeomodelConfig().ready()

# config.DATABASE_URL = "bolt://neo4j:neo4j@172.18.0.5:7687"
# config.FORCE_TIMEZONE = settings.NEO4J_FORCE_TIMEZONE
# config.MAX_CONNECTION_POOL_SIZE = settings.NEO4J_MAX_CONNECTION_POOL_SIZE


def init_gdb() -> None:
    # Neo4j / neomodel requires nodes to be created, but labels on the nodes
    # can be created at run-time without a specific migration step
    # https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
    for node in [
        node
        for _, node in inspect.getmembers(app.models)
        if inspect.isclass(node) and issubclass(node, (StructuredNode))
    ]:
        try:
            install_labels(node)
        except ClientError as e:
            if not str(e.message).lower().startswith("an equivalent constraint already exists"):
                raise e

