from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy.engine import make_url

from app.config import settings

TABLE_NAME = "rules"  # LlamaIndex creates it as "data_rules"


def get_vector_store() -> PGVectorStore:
    """pgvector-backed store holding one node per rule, shared by ingestion and retrieval."""
    url = make_url(settings.database_url)
    # render_as_string: str(URL) would mask the password as "***"
    return PGVectorStore.from_params(
        connection_string=url.set(drivername="postgresql+psycopg2").render_as_string(hide_password=False),
        async_connection_string=url.set(drivername="postgresql+asyncpg").render_as_string(hide_password=False),
        table_name=TABLE_NAME,
        embed_dim=settings.embedding_dim,
        use_jsonb=True,  # metadata as JSONB so country/product filters run in SQL
    )
