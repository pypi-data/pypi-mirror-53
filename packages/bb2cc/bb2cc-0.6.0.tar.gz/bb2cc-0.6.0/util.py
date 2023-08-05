"""Utility module with shared functionality."""

import os
import re
import yaml


class IncompatibleDocument(ValueError):
    """Exception raised when a document is not in a compatible format."""

    def __init__(self, message, file=None):
        """Initialize an error for the given file with a specified message."""
        subject = os.path.basename(file) if file else 'Content'
        super().__init__(
            '{} is not in the right format: {}'.format(subject, message))


def parse_file(file):
    """Parse the frontmatter and body of a file in Markdown format."""
    with open(file, 'r') as f:
        content = f.read()
    return parse_content(content, file)


def parse_content(content, file=None):
    """Parse the frontmatter and body of some Markdown content."""
    try:
        _, frontmatter, body = re.split(r'\s*---\n\s*', content, 2)
    except ValueError:
        raise IncompatibleDocument(
            'Document frontmatter must be fenced by "---" lines.', file)

    try:
        frontmatter = yaml.safe_load(frontmatter)
    except yaml.error.YAMLError:
        raise IncompatibleDocument(
            'Document frontmatter should be valid YAML.', file)

    if 'page_id' not in frontmatter:
        raise IncompatibleDocument('The page_id property is required.', file)

    return frontmatter, body
