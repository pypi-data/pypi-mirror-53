"""Basic Confluence Cloud API client library."""

import json

from urllib.parse import urljoin

import requests


class Confluence(object):
    """Client for interacting with the Confluence Cloud API."""

    def __init__(self, host, username, password):
        """Initialize a client object for the given host and credentials."""
        self.host = host
        self.session = requests.Session()
        self.session.auth = (username, password)

    def update_page(self, page_id, title=None, content=None, node=None):
        """Update a Confluence page with the given title and HTML content.

        This method attempts to only update the page if necessary. In order to
        make this determination, it sets two properties in the page's metadata:
        `node`, which contains the hash of the commit the page has been sync'd
        to; and `sync_version`, which contains the version of the page as of
        the last sync.

        These properties allow the code to run only when either the local copy
        has changed (i.e. the hash has changed) or the remote copy has changed
        (i.e. someone has edited the page in Confluence), or both. If both
        values remain unchanged then no update is necessary.
        """
        current_page_data = self.get_page(page_id)
        current_version = current_page_data['version']['number']
        page_properties = current_page_data['metadata']['properties']
        expected_version = page_properties.get('sync_version', {}).get('value')
        current_node = page_properties.get('node', {}).get('value')

        if (node is not None and current_node == node and
                current_version == expected_version):
            return False

        payload = {
            'type': 'page',
            'version': {
                'number': current_version + 1
            }
        }

        if title is not None:
            payload['title'] = title

        if content is not None:
            payload['body'] = {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }

        url = urljoin(self.host, 'rest/api/content/%(page_id)s') % {
            'page_id': page_id
        }
        response = self.session.put(
            url, headers={'Content-Type': 'application/json'},
            data=json.dumps(payload))
        self.raise_for_status(response)

        response_data = response.json()

        self._update_page_property(current_page_data, 'sync_version',
                                   response_data['version']['number'])
        if node is not None:
            self._update_page_property(current_page_data, 'node', node)

        return response_data

    def get_page(self, page_id):
        """Get a Confluence page."""
        url = urljoin(self.host, 'rest/api/content/%(page_id)s') % {
            'page_id': page_id
        }
        response = self.session.get(url, params={
            'expand': ','.join(['metadata.properties.node',
                                'metadata.properties.sync_version',
                                'version'])
        })
        self.raise_for_status(response)

        return response.json()

    def lookup_user(self, username):
        """Look up a user's accountId based on their username."""
        url = urljoin(self.host, 'rest/api/user/bulk/migration')
        response = self.session.get(url, params={
            'username': username
        })
        self.raise_for_status(response)

        response_data = response.json()

        return response_data['results'][0].get('accountId')

    def raise_for_status(self, response):
        """For non-2xx responses, print the body and raise an exception."""
        if not 200 <= response.status_code < 300:
            print('{}: {}'.format(response.status_code, response.content))
            response.raise_for_status()

    def _update_page_property(self, page_data, key, value):
        property_data = page_data['metadata']['properties'].get(key)
        if property_data is None:
            property_url = urljoin(page_data['_links']['self'] + '/',
                                   'property')
            response = self.session.post(property_url, json={
                'key': key,
                'value': value
            })
        else:
            property_url = property_data['_links']['self']
            property_version = property_data['version']['number']
            payload = {
                'value': value,
                'version': {
                    'number': property_version + 1
                }
            }
            response = self.session.put(
                property_url, headers={'Content-Type': 'application/json'},
                data=json.dumps(payload))

        self.raise_for_status(response)

        return response.json()
