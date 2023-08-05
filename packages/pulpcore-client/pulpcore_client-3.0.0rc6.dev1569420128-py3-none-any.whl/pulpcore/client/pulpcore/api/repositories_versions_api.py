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


class RepositoriesVersionsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create(self, repository_href, data, **kwargs):  # noqa: E501
        """Create a repository version  # noqa: E501

        Trigger an asynchronous task to create a new repository version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create(repository_href, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_href: URI of Repository. e.g.: /pulp/api/v3/repositories/1/ (required)
        :param RepositoryVersionCreate data: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncOperationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_with_http_info(repository_href, data, **kwargs)  # noqa: E501

    def create_with_http_info(self, repository_href, data, **kwargs):  # noqa: E501
        """Create a repository version  # noqa: E501

        Trigger an asynchronous task to create a new repository version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_with_http_info(repository_href, data, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_href: URI of Repository. e.g.: /pulp/api/v3/repositories/1/ (required)
        :param RepositoryVersionCreate data: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncOperationResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['repository_href', 'data']  # noqa: E501
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
        # verify the required parameter 'repository_href' is set
        if ('repository_href' not in local_var_params or
                local_var_params['repository_href'] is None):
            raise ApiValueError("Missing the required parameter `repository_href` when calling `create`")  # noqa: E501
        # verify the required parameter 'data' is set
        if ('data' not in local_var_params or
                local_var_params['data'] is None):
            raise ApiValueError("Missing the required parameter `data` when calling `create`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repository_href' in local_var_params:
            path_params['repository_href'] = local_var_params['repository_href']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data' in local_var_params:
            body_params = local_var_params['data']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Basic']  # noqa: E501

        return self.api_client.call_api(
            '{repository_href}versions/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncOperationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete(self, repository_version_href, **kwargs):  # noqa: E501
        """Delete a repository version  # noqa: E501

        Trigger an asynchronous task to delete a repositroy version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete(repository_version_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_version_href: URI of Repository Version. e.g.: /pulp/api/v3/repositories/1/versions/1/ (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncOperationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.delete_with_http_info(repository_version_href, **kwargs)  # noqa: E501

    def delete_with_http_info(self, repository_version_href, **kwargs):  # noqa: E501
        """Delete a repository version  # noqa: E501

        Trigger an asynchronous task to delete a repositroy version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_with_http_info(repository_version_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_version_href: URI of Repository Version. e.g.: /pulp/api/v3/repositories/1/versions/1/ (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncOperationResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['repository_version_href']  # noqa: E501
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
        # verify the required parameter 'repository_version_href' is set
        if ('repository_version_href' not in local_var_params or
                local_var_params['repository_version_href'] is None):
            raise ApiValueError("Missing the required parameter `repository_version_href` when calling `delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repository_version_href' in local_var_params:
            path_params['repository_version_href'] = local_var_params['repository_version_href']  # noqa: E501

        query_params = []

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
            '{repository_version_href}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncOperationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list(self, repository_href, **kwargs):  # noqa: E501
        """List repository versions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list(repository_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_href: URI of Repository. e.g.: /pulp/api/v3/repositories/1/ (required)
        :param str ordering: Which field to use when ordering the results.
        :param float number:
        :param float number__lt: Filter results where number is less than value
        :param float number__lte: Filter results where number is less than or equal to value
        :param float number__gt: Filter results where number is greater than value
        :param float number__gte: Filter results where number is greater than or equal to value
        :param float number__range: Filter results where number is between two comma separated values
        :param str created__lt: Filter results where _created is less than value
        :param str created__lte: Filter results where _created is less than or equal to value
        :param str created__gt: Filter results where _created is greater than value
        :param str created__gte: Filter results where _created is greater than or equal to value
        :param str created__range: Filter results where _created is between two comma separated values
        :param str content: Content Unit referenced by HREF
        :param str created: ISO 8601 formatted dates are supported
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
        :return: InlineResponse2002
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_with_http_info(repository_href, **kwargs)  # noqa: E501

    def list_with_http_info(self, repository_href, **kwargs):  # noqa: E501
        """List repository versions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_with_http_info(repository_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_href: URI of Repository. e.g.: /pulp/api/v3/repositories/1/ (required)
        :param str ordering: Which field to use when ordering the results.
        :param float number:
        :param float number__lt: Filter results where number is less than value
        :param float number__lte: Filter results where number is less than or equal to value
        :param float number__gt: Filter results where number is greater than value
        :param float number__gte: Filter results where number is greater than or equal to value
        :param float number__range: Filter results where number is between two comma separated values
        :param str created__lt: Filter results where _created is less than value
        :param str created__lte: Filter results where _created is less than or equal to value
        :param str created__gt: Filter results where _created is greater than value
        :param str created__gte: Filter results where _created is greater than or equal to value
        :param str created__range: Filter results where _created is between two comma separated values
        :param str content: Content Unit referenced by HREF
        :param str created: ISO 8601 formatted dates are supported
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
        :return: tuple(InlineResponse2002, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['repository_href', 'ordering', 'number', 'number__lt', 'number__lte', 'number__gt', 'number__gte', 'number__range', 'created__lt', 'created__lte', 'created__gt', 'created__gte', 'created__range', 'content', 'created', 'limit', 'offset', 'fields']  # noqa: E501
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
        # verify the required parameter 'repository_href' is set
        if ('repository_href' not in local_var_params or
                local_var_params['repository_href'] is None):
            raise ApiValueError("Missing the required parameter `repository_href` when calling `list`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repository_href' in local_var_params:
            path_params['repository_href'] = local_var_params['repository_href']  # noqa: E501

        query_params = []
        if 'ordering' in local_var_params:
            query_params.append(('ordering', local_var_params['ordering']))  # noqa: E501
        if 'number' in local_var_params:
            query_params.append(('number', local_var_params['number']))  # noqa: E501
        if 'number__lt' in local_var_params:
            query_params.append(('number__lt', local_var_params['number__lt']))  # noqa: E501
        if 'number__lte' in local_var_params:
            query_params.append(('number__lte', local_var_params['number__lte']))  # noqa: E501
        if 'number__gt' in local_var_params:
            query_params.append(('number__gt', local_var_params['number__gt']))  # noqa: E501
        if 'number__gte' in local_var_params:
            query_params.append(('number__gte', local_var_params['number__gte']))  # noqa: E501
        if 'number__range' in local_var_params:
            query_params.append(('number__range', local_var_params['number__range']))  # noqa: E501
        if 'created__lt' in local_var_params:
            query_params.append(('_created__lt', local_var_params['created__lt']))  # noqa: E501
        if 'created__lte' in local_var_params:
            query_params.append(('_created__lte', local_var_params['created__lte']))  # noqa: E501
        if 'created__gt' in local_var_params:
            query_params.append(('_created__gt', local_var_params['created__gt']))  # noqa: E501
        if 'created__gte' in local_var_params:
            query_params.append(('_created__gte', local_var_params['created__gte']))  # noqa: E501
        if 'created__range' in local_var_params:
            query_params.append(('_created__range', local_var_params['created__range']))  # noqa: E501
        if 'content' in local_var_params:
            query_params.append(('content', local_var_params['content']))  # noqa: E501
        if 'created' in local_var_params:
            query_params.append(('_created', local_var_params['created']))  # noqa: E501
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
            '{repository_href}versions/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2002',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def read(self, repository_version_href, **kwargs):  # noqa: E501
        """Inspect a repository version  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read(repository_version_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_version_href: URI of Repository Version. e.g.: /pulp/api/v3/repositories/1/versions/1/ (required)
        :param str fields: A list of fields to include in the response.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: RepositoryVersion
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.read_with_http_info(repository_version_href, **kwargs)  # noqa: E501

    def read_with_http_info(self, repository_version_href, **kwargs):  # noqa: E501
        """Inspect a repository version  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_with_http_info(repository_version_href, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str repository_version_href: URI of Repository Version. e.g.: /pulp/api/v3/repositories/1/versions/1/ (required)
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
        :return: tuple(RepositoryVersion, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['repository_version_href', 'fields']  # noqa: E501
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
        # verify the required parameter 'repository_version_href' is set
        if ('repository_version_href' not in local_var_params or
                local_var_params['repository_version_href'] is None):
            raise ApiValueError("Missing the required parameter `repository_version_href` when calling `read`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'repository_version_href' in local_var_params:
            path_params['repository_version_href'] = local_var_params['repository_version_href']  # noqa: E501

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
            '{repository_version_href}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RepositoryVersion',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
