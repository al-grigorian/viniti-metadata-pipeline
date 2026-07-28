import pytest
from pydantic import ValidationError

from viniti_metadata.schemas.metadata import ArticleMetadata

CANONICAL = "10.1038/s41586-020-2012-7"


@pytest.mark.parametrize(
    "raw_doi, expected",
    [
        (CANONICAL, CANONICAL),
        (f"https://doi.org/{CANONICAL}", CANONICAL),
        (f"{CANONICAL}.", CANONICAL),
        ("10.1038/S41586-020-2012-7", CANONICAL),
        (f"DOI: {CANONICAL}", CANONICAL),
    ],
    ids=[
        "clean_doi",
        "with_url_prefix",
        "with_trailing_dot",
        "uppercase_letters",
        "with_label_prefix",
    ],
)
def test_doi_normalization(raw_doi: str, expected: str) -> None:
    """Валидатор приводит различные формы записи DOI к канонической."""
    article = ArticleMetadata(title="Тестовая статья", doi=raw_doi)
    assert article.doi == expected


@pytest.mark.parametrize(
    "raw_doi",
    ["not-a-doi-string", "10.12/short", "просто текст без идентификатора"],
    ids=["garbage", "too_short_prefix", "cyrillic_text"],
)
def test_doi_rejects_invalid(raw_doi: str) -> None:
    """Некорректный DOI вызывает ошибку валидации — сигнал для повтора запроса к LLM."""
    with pytest.raises(ValidationError):
        ArticleMetadata(title="Тестовая статья", doi=raw_doi)


@pytest.mark.parametrize("empty_value", [None, "", "   "], ids=["none", "empty", "spaces"])
def test_doi_absent(empty_value: str | None) -> None:
    """Отсутствие DOI — штатная ситуация, а не ошибка."""
    article = ArticleMetadata(title="Тестовая статья", doi=empty_value)
    assert article.doi is None