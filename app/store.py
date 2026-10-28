from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy.engine import make_url

from app.config import settings

TABLE_NAME = "rules"  # LlamaIndex creates it as "data_rules"


def connection_string(driver: str = "psycopg2") -> str:
    # render_as_string: str(URL) would mask the password as "***"
    url = make_url(settings.database_url).set(drivername=f"postgresql+{driver}")
    return url.render_as_string(hide_password=False)


def get_vector_store() -> PGVectorStore:
    """pgvector-backed store holding one node per rule, shared by ingestion and retrieval."""
    return PGVectorStore.from_params(
        connection_string=connection_string("psycopg2"),
        async_connection_string=connection_string("asyncpg"),
        table_name=TABLE_NAME,
        embed_dim=settings.embedding_dim,
        use_jsonb=True,  # metadata as JSONB so country/product filters run in SQL
    )
