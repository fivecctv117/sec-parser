from __future__ import annotations

from typing import TYPE_CHECKING

from sec_parser.processing_steps.abstract_elementwise_processing_step import (
    AbstractElementwiseProcessingStep,
    ElementwiseProcessingContext,
)
from sec_parser.semantic_elements.highlighted_text_element import (
    HighlightedTextElement,
    TextStyle,
)
from sec_parser.semantic_elements.semantic_elements import TextElement

if TYPE_CHECKING:  # pragma: no cover
    from sec_parser.semantic_elements.abstract_semantic_element import (
        AbstractSemanticElement,
    )


class HighlightedTextClassifier(AbstractElementwiseProcessingStep):
    """
    HighlightedText class for converting elements into HighlightedText instances.

    This step scans through a list of semantic elements and changes it,
    primarily by replacing suitable candidates with HighlightedText instances.
    """

    def __init__(
        self,
        types_to_process: set[type[AbstractSemanticElement]] | None = None,
        types_to_exclude: set[type[AbstractSemanticElement]] | None = None,
    ) -> None:
        super().__init__(
            types_to_process=types_to_process,
            types_to_exclude=types_to_exclude,
        )

    def _process_element(
        self,
        element: AbstractSemanticElement,
        _: ElementwiseProcessingContext,
    ) -> AbstractSemanticElement:
        if not isinstance(element, TextElement):
            return element
        styles_metrics = element.html_tag.get_text_styles_metrics()
        style: TextStyle = TextStyle.from_style_string(styles_metrics)
        if not style:
            return element
        return HighlightedTextElement.create_from_element(element, style=style)
