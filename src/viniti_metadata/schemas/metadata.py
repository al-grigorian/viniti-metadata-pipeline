from pydantic import BaseModel, Field, field_validator
import re

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9<>]+")

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
    
    @field_validator("doi", mode="before")
    @classmethod
    def normalize_doi(cls, value: object) -> str | None:
        """Приводит DOI к канонической форме: без URL-префикса, в нижнем регистре

        Отклоняет строки, не содержащие DOI, - ошибка валидации
        возвращается Instructor'у как сигнал для повторного запроса к LLM.
        """

        if value is None:
            return None
        text = str(value).strip()
        if not text:
            return None # пустую строку трактуем как отсутствие DOI
        match = DOI_RE.search(text)
        if match is None:
            raise ValueError(f"Строка не содержит корректного DOI: {text!r}")
        return match.group(0).rstrip(".,;:").lower()



