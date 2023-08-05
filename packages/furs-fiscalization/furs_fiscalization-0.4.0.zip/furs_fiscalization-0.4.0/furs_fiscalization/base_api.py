import json

from OpenSSL import crypto
from jose import jws
from requests import codes
from requests.exceptions import Timeout

from furs_fiscalization.connector import Connector
from furs_fiscalization.exceptions import ConnectionException, ConnectionTimedOutException, FURSException


class FURSBaseAPI(object):
    def __init__(self, p12_path, p12_password, p12_buffer=None, production=True, request_timeout=2.0, proxy=None):
        self.connector = Connector(p12_path=p12_path,
                                   p12_password=p12_password,
                                   p12_buffer=p12_buffer,
                                   production=production,
                                   request_timeout=request_timeout,
                                   proxy=proxy)

    def is_server_accessible(self, message='ping'):
        """
        Check if FURS server is accessible. Will return False if server responds with anything else
        than HTTP Code: 200 or if the request timeouts.

        :return: (boolean) True for ok, False if there was a problem accessing server.
        """
        try:
            return self.connector.send_echo(message).status_code == codes.ok
        except Timeout as e:
            return False

    def _send_request(self, path, data):
        """
        Sends request to the FURS Server and decodes response.

        :param path: (string) Server path
        :param data: (dict) Data to be sent
        :return: (dict) Received response

        :raises:
            ConnectionTimedOutException: If connection timed out
            ConnectionException: If FURS responded with status code different than 200
            FURSException: If server responded with error
        """
        try:
            response = self.connector.post(path=path, json=data)

            if response.status_code == codes.ok:
                # TODO - we should verify server signature!
                if 'json' in response.headers.get('Content-Type'):
                    response_data = response.json()['token']
                    json_data = jws.get_unverified_claims(response_data)
                    decoded_json_data = json_data.decode('utf-8')
                    server_response = json.loads(decoded_json_data)
                    return self._check_for_errors(server_response)
                else:
                    raise ConnectionException(code=415,
                                              message='Response content is not in JSON format [' + str(
                                                  response.content) + "].")
            else:
                raise ConnectionException(code=response.status_code,
                                          message=response.text)

        except Timeout as e:
            raise ConnectionTimedOutException(e)

    def _check_for_errors(self, server_response):
        """
        Check if server response contains FURS Error message and raise FURSException if it does
        :param server_response: (dict) FURS Server response data
        :return: server_response: (dict) FURS Server response data

        :raises
            FURSException: If response contains error
        """

        error = server_response[list(server_response.keys())[0]].get('Error', None)
        if error:
            raise FURSException(code=error['ErrorCode'],
                                message=error['ErrorMessage'])

        return server_response

    def _sign(self, content, digest='SHA256'):
        pkey = self.connector.p12.get_privatekey()

        return crypto.sign(pkey=pkey, data=content, digest=digest)
