"""Convert a Markdown document to Confluence-compatible HTML."""

import html
import os
import re

from textwrap import dedent
from urllib.parse import urljoin

import mistune

from util import parse_file


class ConfluenceRenderer(mistune.Renderer):
    """Class that renders HTML that can be uploaded to a Confluence page."""

    def __init__(self, client=None, repository_url=None):
        """Initialize a renderer for the given Confluence client and repo URL.

        The client is used for resolving links to other Confluence resources
        (e.g. users or other pages).

        The repository URL is used in cases where the file doesn't exist
        locally (but it might exist in the repository).
        """
        self.client = client
        self.repository_url = repository_url
        super().__init__()

    @property
    def host(self):
        """Convenience property for returning self.client.host or None."""
        return getattr(self.client, 'host', None)

    def autolink(self, link, is_email=False):
        """Render an automatic link.

        For links to other Confluence pages, use the nifty inline card macro.
        """
        if not is_email and self.host and link.startswith(self.host):
            page_id_match = re.search(r'/pages/(\d+)', link)
            if page_id_match:
                page_id = page_id_match.group(1)
                page_data = self.client.get_page(page_id)
                return (
                    '<ac:link ac:card-appearance="inline">'
                    '<ri:page ri:content-title="{title}" />'
                    '<ac:link-body>{title}</ac:link-body>'
                    '</ac:link>'
                ).format(title=page_data['title'])

        return super().autolink(link, is_email)

    def block_code(self, code, language=None):
        """Render a block of source code.

        This method introduces a special case for the code block syntax where
        the "language" is set to `panel:<type>`.
        """
        panel_match = re.match(r'^panel:(info|warning|success|error)$',
                               language or '')

        if panel_match:
            return self.info_panel(panel_match.group(1),
                                   render_to_html(code, self.host,
                                                  self.repository_url))

        return super().block_code(code, language)

    def image(self, src, title, alt_text):
        """Render an image.

        For relative links, update the src to point to the image in the
        Bitbucket repository.
        """
        if self._is_relative_link(src):
            src = urljoin(self.repository_url + '/',
                          'raw/HEAD/{}'.format(src))

        markup = '<ac:image'
        if title:
            markup += ' ac:title="{title}"'.format(title=html.escape(title))
        if alt_text:
            markup += ' ac:alt="{alt_text}"'.format(
                alt_text=html.escape(alt_text))
        markup += '><ri:url ri:value="{url}" />'.format(url=src)
        markup += '</ac:image>'
        return markup

    def link(self, link, title, content):
        """Render a link to another page.

        For relative links, update the href to point to the corresponding page
        in Confluence where possible.
        """
        if self._is_relative_link(link):
            # Removing leading slashes to make this path relative to the root
            # of the repository (which should be the working directory).
            path = re.sub(r'^/', '', link)

            # By default, update every relative link to point to the file in
            # the repository.
            if self.repository_url:
                link = urljoin(self.repository_url + '/',
                               'src/HEAD/{}'.format(path))

            # If possible, update the link to point to the corresponding page
            # in Confluence.
            if (self.host and os.path.exists(path) and
                    re.search(r'\.(?:md|markdown)$', path)):
                try:
                    frontmatter, body = parse_file(path)
                    link = urljoin(
                        self.host, 'pages/viewpage.action?pageId={}'.format(
                            frontmatter['page_id']))
                except ValueError:
                    # Not every Markdown file in the repository will
                    # necessarily have a corresponding Confluence page. That's
                    # fine!
                    pass

        return super().link(link, title, content)

    def list(self, body, ordered=False):
        """Render a list.

        For GFM-style checklists, render a Confluence task list.
        """
        if re.match(r'^\s*<ac:task>', body):
            return '<ac:task-list>{body}</ac:task-list>'.format(body=body)
        return super().list(body, ordered)

    def list_item(self, text):
        """Render a list item.

        For GFM-style checkboxes, render a Confluence task.
        """
        task_match = re.match(r'^\[([x ])\]\s*(.*)', text, re.IGNORECASE)

        if not task_match:
            return super().list_item(text)

        task_status = ('complete' if task_match.group(1).lower() == 'x'
                       else 'incomplete')
        return (
            '<ac:task>'
            '<ac:task-status>{status}</ac:task-status>'
            '<ac:task-body>{body}</ac:task-body>'
            '</ac:task>'
        ).format(status=task_status,
                 body=render_to_html(task_match.group(2), self.client,
                                     self.repository_url))

    def text(self, text):
        """Strip non-semantic whitespace from a text node."""
        return re.sub(r'\s+', ' ', super().text(text))

    def status_lozenge(self, color, label):
        """Render a status lozenge with the given color and label."""
        return (
            '<ac:structured-macro ac:name="status">'
            '<ac:parameter ac:name="colour">{color}</ac:parameter>'
            '<ac:parameter ac:name="title">{label}</ac:parameter>'
            '</ac:structured-macro>'
        ).format(color=color, label=label)

    def user_mention(self, username, fallback):
        """Render a mention for the user with the given username.

        If the user isn't found, return a fallback string.
        """
        if self.client is None:
            return fallback

        account_id = self.client.lookup_user(username)
        if account_id is None:
            return fallback

        return (
            '<ac:link>'
            '<ri:user ri:username="{account_id}" />'
            '</ac:link>'
        ).format(account_id=account_id)

        return fallback

    def info_panel(self, style, body):
        """Render a panel with the given style (e.g. info) and body."""
        def map_panel_type(panel_type):
            # The type strings that Confluence uses for its panels are not
            # very intuitive!
            if panel_type == 'info':
                return 'info'
            elif panel_type == 'warning':
                return 'note'
            elif panel_type == 'success':
                return 'tip'
            elif panel_type == 'error':
                return 'warning'
            raise ValueError('Invalid panel type: {}'.format(panel_type))

        return (
            '<ac:structured-macro ac:name="{style}">'
            '<ac:rich-text-body>{body}</ac:rich-text-body>'
            '</ac:structured-macro>'
        ).format(style=map_panel_type(style), body=body)

    def header_panel(self):
        """Render the header panel to put at the top of the page.

        If the repository_url attribute is set, the header informs the reader
        that the page is kept in sync with a Bitbucket repository. Otherwise,
        it indicates only that the page was created using bb2cc.
        """
        if self.repository_url:
            content = dedent('''
                This page is kept in sync with {repository_url} using the
                [bb2cc](https://bitbucket.org/dtao/bb2cc) library.

                Any changes you make to this page in Confluence will be
                overridden on the next push to the repository.
            ''').format(repository_url=self.repository_url)
        else:
            content = dedent('''
                This page was created automatically from a Markdown file using
                the [bb2cc](https://bitbucket.org/dtao/bb2cc) library.
            ''')

        # Remove leading & trailing whitespace to avoid unwanted blank lines.
        content = content.strip()

        return self.info_panel('info', render_to_html(content, self.client,
                                                      self.repository_url))

    def table_of_contents(self):
        """Render a table of contents macro."""
        return '<ac:structured-macro ac:name="toc" />'

    def _is_relative_link(self, url):
        return not re.match(r'^https?:', url)


class ConfluenceInlineGrammar(mistune.InlineGrammar):
    """Custom inline grammar extending Markdown with some Confluence extras."""

    # This is identical to mistune's build-in text rule, with the addition of
    # `@` as a character to break on.
    text = re.compile(r'^[\s\S]+?(?=[\\<!\[_*`~@]|https?://| {2,}\n|$)')


class ConfluenceLexer(mistune.InlineLexer):
    """Class that parses custom syntax for various Confluence macros."""

    grammar_class = ConfluenceInlineGrammar

    def __init__(self, *args, **kwargs):
        """Initialize and enable new grammar rules."""
        super().__init__(*args, **kwargs)
        self.enable_status_lozenge()
        self.enable_user_mention()

    def add_default_rule(self, rule_name):
        """Add a new default syntax rule."""
        text_index = self.default_rules.index('text')

        # Insert *before* text (which catches everything).
        self.default_rules.insert(text_index, rule_name)

    def enable_status_lozenge(self):
        """Enable a new `[[Label|Color]]` syntax for status lozenges."""
        self.rules.status_lozenge = re.compile(
            r'\[\['                  # [[
            r'([^:]+(?::[^:\]]+)?)'  # "Label:Color" or just "Label"
            r'\]\](?!\])'            # ]]
        )

        self.add_default_rule('status_lozenge')

    def output_status_lozenge(self, match):
        """Render a status lozenge for the given re.Match object."""
        text = match.group(1)
        if ':' in text:
            title, color = text.split(':')
        else:
            title = text
            color = 'Grey'

        return self.renderer.status_lozenge(color, title)

    def enable_user_mention(self):
        """Enable a new `@username` syntax for user mentions."""
        self.rules.user_mention = re.compile(
            r'(?:^|\s)'  # either the start of the line or whitespace
            r'@(\w+)'    # "@username"
            r'(?:\s|$)'  # either a space of the end of the line
        )

        self.add_default_rule('user_mention')

    def output_user_mention(self, match):
        """Render a user mention for the given re.Match object."""
        username = match.group(1)
        return self.renderer.user_mention(username, match.string)


def render_to_html(text, client=None, repository_url=None,
                   include_header=False, include_toc=False):
    """Render some Markdown text to Confluence-compatible HTML."""
    renderer = ConfluenceRenderer(client, repository_url)
    lexer = ConfluenceLexer(renderer)
    html = renderer.header_panel() if include_header else ''
    if include_toc:
        html += renderer.table_of_contents()
    markdown = mistune.Markdown(renderer=renderer, inline=lexer)
    html += markdown(text)
    return html.strip()
