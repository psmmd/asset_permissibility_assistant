"""Step 2: retrieve the rules for the policy's country and product."""

from functools import cache

from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
from llama_index.embeddings.openai import OpenAIEmbedding

from app.config import settings
from app.schemas import Country, Extraction, Product, Rule
from app.store import get_vector_store


@cache
def get_index() -> VectorStoreIndex:
    embed_model = OpenAIEmbedding(model=settings.embedding_model, api_key=settings.openai_api_key)
    return VectorStoreIndex.from_vector_store(get_vector_store(), embed_model=embed_model)


def build_query(extraction: Extraction) -> str:
    """Search with the extracted facts, not the raw email, to keep small talk out of the query."""
    parts = [extraction.asset_type or "", extraction.asset_description, *extraction.facts]
    return ". ".join(p for p in parts if p)


def retrieve(extraction: Extraction, country: Country, product: Product, top_k: int | None = None) -> list[Rule]:
    # Hard filter on metadata: rules from another country or product must never reach the decision step.
    filters = MetadataFilters(
        filters=[MetadataFilter(key="country", value=country), MetadataFilter(key="product", value=product)]
    )
    retriever = get_index().as_retriever(similarity_top_k=top_k or settings.retrieval_top_k, filters=filters)
    results = retriever.retrieve(build_query(extraction))
    return [Rule(rule_id=r.node.id_, text=r.node.get_content()) for r in results]
