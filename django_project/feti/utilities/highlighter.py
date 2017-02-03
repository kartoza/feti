from haystack.utils import Highlighter
import re


class QueryHighlighter(Highlighter):
    """
    Highlight query results
    """
    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        highlighted_chunk = self.text_block
        queries = list(self.query_words)

        highlighted_chunk = re.sub(
                '(?i)(' + '|'.join(map(re.escape, queries)) + ')', r'<mark>\1</mark>',
                highlighted_chunk)

        return highlighted_chunk
