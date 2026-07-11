from pydantic import BaseModel, Field

class Author(BaseModel):
    """Автор публикации в том виде, в каком он указан на первой странице PDF"""

    surname: str = Field(min_length=1, description="Фамилия автора")
    initials: str | None = Field(default=None, description="Инициалы, например «И.И.»")
    affiliation_marker: str | None = Field(
        default=None,
        description="Маркер аффилиации у фамилии: цифра или символ («1», «*»)",
    )

class ArticleMetadata(BaseModel):
    """Метаданные научной статьи"""

    title: str = Field(min_length=1, description="Полное название статьи")
    authors: list[Author] = Field(
        default_factory=list,
        description="Список авторов в порядке указания в статье"
    )
    keywords: list[str] = Field(
        default_factory=list,
        description="Ключевые слова из соответствующего раздела"
    )
    affiliations: dict[str, str] = Field(
        default_factory=dict,
        description="Соответствие маркера аффилиации названию организации"
    )
    udc: str | None = Field(default=None, description="УДК статьи, если указан")
    doi: str | None = Field(default=None, description="DOI статьи, если указан")
    pages: str | None = Field(
        default=None,
        description="Диапазон страниц статьи в издании, например «12–19»"
    )
