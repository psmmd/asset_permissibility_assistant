"""Load the rules documents into pgvector, one node per rule.

Run: uv run python -m app.ingest

Idempotent: each document's existing nodes are deleted before its new nodes are
inserted, so running it twice never creates duplicates and removed rules disappear.
"""

import re
from pathlib import Path

from llama_index.core.schema import NodeRelationship, RelatedNodeInfo, TextNode
from llama_index.embeddings.openai import OpenAIEmbedding

from app.config import settings
from app.store import get_vector_store

RULES_DIR = Path(__file__).resolve().parent.parent / "data" / "rules"

# A rule runs from its "### XX-YY-NN — Title" heading up to the next "##"/"###" heading.
RULE_PATTERN = re.compile(
    r"^### (?P<rule_id>[A-Z]{2}-[A-Z]{2}-\d{2}) — (?P<title>.+?)$.*?(?=^##|\Z)",
    re.MULTILINE | re.DOTALL,
)
ASSET_TYPE_PATTERN = re.compile(r"\*\*Asset type:\*\* `(\w+)`")


def parse_rules(path: Path) -> list[TextNode]:
    """Split one rules document (e.g. LU_UL.md) into one node per rule."""
    doc_id = path.stem
    country, product = doc_id.split("_")
    nodes = []
    for match in RULE_PATTERN.finditer(path.read_text()):
        text = match.group(0).strip()
        metadata = {
            "rule_id": match["rule_id"],
            "country": country,
            "product": product,
            "title": match["title"],
        }
        if asset_type := ASSET_TYPE_PATTERN.search(text):
            metadata["asset_type"] = asset_type.group(1)
        node = TextNode(id_=match["rule_id"], text=text, metadata=metadata)
        # The source document is what store.delete(ref_doc_id) matches on.
        node.relationships[NodeRelationship.SOURCE] = RelatedNodeInfo(node_id=doc_id)
        nodes.append(node)
    return nodes


def main() -> None:
    store = get_vector_store()
    embed_model = OpenAIEmbedding(model=settings.embedding_model, api_key=settings.openai_api_key)

    total = 0
    for path in sorted(RULES_DIR.glob("*.md")):
        nodes = parse_rules(path)
        # Embed only the rule text; metadata is used for filtering, not for similarity.
        embeddings = embed_model.get_text_embedding_batch([node.text for node in nodes])
        for node, embedding in zip(nodes, embeddings):
            node.embedding = embedding
        # Embed first, then replace, so a failed API call never leaves a document missing.
        store.delete(ref_doc_id=path.stem)
        store.add(nodes)
        total += len(nodes)
        print(f"{path.stem}: {len(nodes)} rules")
    print(f"Done: {total} rules ingested")


if __name__ == "__main__":
    main()
