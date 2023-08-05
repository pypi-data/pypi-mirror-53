# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from pulpcore.client.pulpcore.api_client import ApiClient
from pulpcore.client.pulpcore.exceptions import (
    ApiTypeError,
    ApiValueError
)


class ArtifactsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create(self, **kwargs):  # noqa: E501
        """Create an artifact  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param file file: The stored file.
        :param int size: The size of the file in bytes.
        :param str md5: The MD5 checksum of the file if available.
        :param str sha1: The SHA-1 checksum of the file if available.
        :param str sha224: The SHA-224 checksum of the file if available.
        :param str sha256: The SHA-256 checksum of the file if available.
        :param str sha384: The SHA-384 checksum of the file if available.
        :param str sha512: The SHA-512 checksum of the file if available.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Artifact
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_with_http_info(**kwargs)  # noqa: E501

    def create_with_http_info(self, **kwargs):  # noqa: E501
        """Create an artifact  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param file file: The stored file.
        :param int size: The size of the file in bytes.
        :param str md5: The MD5 checksum of the file if available.
        :param str sha1: The SHA-1 checksum of the file if available.
        :param str sha224: The SHA-224 checksum of the file if available.
        :param str sha256: The SHA-256 checksum of the file if available.
        :param str sha384: The SHA-384 checksum of the file if available.
        :param str sha512: The SHA-512 checksum of the file if available.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Artifact, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['file', 'size', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if ('md5' in local_var_params and
                len(local_var_params['md5']) < 1):
            raise ApiValueError("Invalid value for parameter `md5` when calling `create`, length must be greater than or equal to `1`")  # noqa: E501
        if ('sha1' in local_var_params and
                len(local_var_params['sha1']) < 1):
            raise ApiValueError("Invalid value for parameter `sha1` when calling `create`, length must be greater than or equal to `1`")  # noqa: E501
        if ('sha224' in local_var_params and
                len(local_var_params['sha224']) < 1):
            raise ApiValueError("Invalid value for parameter `sha224` when calling `create`, length must be greater than or equal to `1`")  # noqa: E501
        if ('sha256' in local_var_params and
                len(local_var_params['sha256']) < 1):
            raise ApiValueError("Invalid value for parameter `sha256` when calling `create`, length must be greater than or equal to `1`")  # noqa: E501
        if ('sha384' in local_var_params and
                len(local_var_params['sha384']) < 1):
            raise ApiValueError("Invalid value for parameter `sha384` when calling `create`, length must be greater than or equal to `1`")  # noqa: E501
        if ('sha512' in local_var_params and
                len(local_var_params['sha512']) < 1):
            raise ApiValueError("Invalid value for parameter `sha512` when calling `create`, length must be greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in local_var_params:
            local_var_files['file'] = local_var_params['file']  # noqa: E501
        if 'size' in local_var_params:
            form_params.append(('size', local_var_params['size']))  # noqa: E501
        if 'md5' in local_var_params:
            form_params.append(('md5', local_var_params['md5']))  # noqa: E501
        if 'sha1' in local_var_params:
            form_params.append(('sha1', local_var_params['sha1']))  # noqa: E501
        if 'sha224' in local_var_params:
            form_params.append(('sha224', local_var_params['sha224']))  # noqa: E501
        if 'sha256' in local_var_params:
            form_params.append(('sha256', local_var_params['sha256']))  # noqa: E501
        if 'sha384' in local_var_params:
            form_params.append(('sha384', local_var_params['sha384']))  # noqa: E501
        if 'sha512' in local_var_params:
            form_params.append(('sha512', local_var_params['sha512']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '/pulp/api/v3/artifacts/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Artifact',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete(self, artifact_href, **kwargs):  # noqa: E501
        """Delete an artifact  # noqa: E501

        Remove Artifact only if it is not associated with any Content.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete(artifact_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str artifact_href: URI of Artifact. e.g.: /pulp/api/v3/artifacts/1/ (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.delete_with_http_info(artifact_href, **kwargs)  # noqa: E501

    def delete_with_http_info(self, artifact_href, **kwargs):  # noqa: E501
        """Delete an artifact  # noqa: E501

        Remove Artifact only if it is not associated with any Content.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_with_http_info(artifact_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str artifact_href: URI of Artifact. e.g.: /pulp/api/v3/artifacts/1/ (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['artifact_href']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'artifact_href' is set
        if ('artifact_href' not in local_var_params or
                local_var_params['artifact_href'] is None):
            raise ApiValueError("Missing the required parameter `artifact_href` when calling `delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'artifact_href' in local_var_params:
            path_params['artifact_href'] = local_var_params['artifact_href']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '{artifact_href}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list(self, **kwargs):  # noqa: E501
        """List artifacts  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_version: Repository Version referenced by HREF
        :param str md5: Filter results where md5 matches value
        :param str sha1: Filter results where sha1 matches value
        :param str sha224: Filter results where sha224 matches value
        :param str sha256: Filter results where sha256 matches value
        :param str sha384: Filter results where sha384 matches value
        :param str sha512: Filter results where sha512 matches value
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str fields: A list of fields to include in the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_with_http_info(**kwargs)  # noqa: E501

    def list_with_http_info(self, **kwargs):  # noqa: E501
        """List artifacts  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_version: Repository Version referenced by HREF
        :param str md5: Filter results where md5 matches value
        :param str sha1: Filter results where sha1 matches value
        :param str sha224: Filter results where sha224 matches value
        :param str sha256: Filter results where sha256 matches value
        :param str sha384: Filter results where sha384 matches value
        :param str sha512: Filter results where sha512 matches value
        :param int limit: Number of results to return per page.
        :param int offset: The initial index from which to return the results.
        :param str fields: A list of fields to include in the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(InlineResponse200, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['repository_version', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'limit', 'offset', 'fields']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'repository_version' in local_var_params:
            query_params.append(('repository_version', local_var_params['repository_version']))  # noqa: E501
        if 'md5' in local_var_params:
            query_params.append(('md5', local_var_params['md5']))  # noqa: E501
        if 'sha1' in local_var_params:
            query_params.append(('sha1', local_var_params['sha1']))  # noqa: E501
        if 'sha224' in local_var_params:
            query_params.append(('sha224', local_var_params['sha224']))  # noqa: E501
        if 'sha256' in local_var_params:
            query_params.append(('sha256', local_var_params['sha256']))  # noqa: E501
        if 'sha384' in local_var_params:
            query_params.append(('sha384', local_var_params['sha384']))  # noqa: E501
        if 'sha512' in local_var_params:
            query_params.append(('sha512', local_var_params['sha512']))  # noqa: E501
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'fields' in local_var_params:
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '/pulp/api/v3/artifacts/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse200',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read(self, artifact_href, **kwargs):  # noqa: E501
        """Inspect an artifact  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read(artifact_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str artifact_href: URI of Artifact. e.g.: /pulp/api/v3/artifacts/1/ (required)
        :param str fields: A list of fields to include in the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Artifact
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.read_with_http_info(artifact_href, **kwargs)  # noqa: E501

    def read_with_http_info(self, artifact_href, **kwargs):  # noqa: E501
        """Inspect an artifact  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_with_http_info(artifact_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str artifact_href: URI of Artifact. e.g.: /pulp/api/v3/artifacts/1/ (required)
        :param str fields: A list of fields to include in the response.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Artifact, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['artifact_href', 'fields']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method read" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'artifact_href' is set
        if ('artifact_href' not in local_var_params or
                local_var_params['artifact_href'] is None):
            raise ApiValueError("Missing the required parameter `artifact_href` when calling `read`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'artifact_href' in local_var_params:
            path_params['artifact_href'] = local_var_params['artifact_href']  # noqa: E501

        query_params = []
        if 'fields' in local_var_params:
            query_params.append(('fields', local_var_params['fields']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '{artifact_href}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Artifact',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
