"""Step 2: retrieve the rules for the policy's country and product."""

import re
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
    rules = [Rule(rule_id=r.node.id_, text=r.node.get_content()) for r in results]
    return rules + fetch_referenced_rules(rules, country, product)


def fetch_referenced_rules(rules: list[Rule], country: Country, product: Product) -> list[Rule]:
    """Add rules cited by ID in the retrieved ones (e.g. LU-UL-05 says 'professional investor under LU-UL-02').

    Similarity search does not follow these dependencies, so we resolve them explicitly. One level deep,
    and only within the same document, which keeps the filter guarantee.
    """
    pattern = re.compile(rf"\b{country}-{product}-\d{{2}}\b")
    have = {r.rule_id for r in rules}
    referenced = sorted({rid for r in rules for rid in pattern.findall(r.text)} - have)
    if not referenced:
        return []
    nodes = get_index().vector_store.get_nodes(node_ids=referenced)
    return [Rule(rule_id=n.id_, text=n.get_content()) for n in sorted(nodes, key=lambda n: n.id_)]
