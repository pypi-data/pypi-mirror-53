"""App Center crashes API wrappers."""

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import datetime
import logging
import os
from typing import Iterator, Optional
import urllib.parse

import deserialize

import appcenter.constants
from appcenter.derived_client import AppCenterDerivedClient
from appcenter.models import (
    ErrorGroups,
    ErrorGroupListItem,
    ErrorGroupState,
    HandledError,
    HandledErrors,
    SymbolType,
    SymbolUploadBeginResponse,
    SymbolUploadEndRequest,
    SymbolUploadStatus,
)


class AppCenterCrashesClient(AppCenterDerivedClient):
    """Wrapper around the App Center crashes APIs.

    :param token: The authentication token
    :param parent_logger: The parent logger that we will use for our own logging
    """

    def __init__(self, token: str, parent_logger: logging.Logger) -> None:
        super().__init__("crashes", token, parent_logger)

    def get_error_groups(
        self,
        *,
        owner_name: str,
        app_name: str,
        start_time: datetime.datetime,
        end_time: Optional[datetime.datetime] = None,
        version: Optional[str] = None,
        app_build: Optional[str] = None,
        group_state: Optional[ErrorGroupState] = None,
        error_type: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: int = 30,
    ) -> Iterator[ErrorGroupListItem]:
        """Get the error groups for an app.

        :param str owner_name: The name of the app account owner
        :param str app_name: The name of the app
        :param datetime.datetime start_time: The time to start getting error groups from
        :param Optional[datetime.datetime] end_time: The end time to get error groups from
        :param Optional[str] version: The version of the app to restrict the search to (if any)
        :param Optional[str] app_build: The build to restrict the search to (if any)
        :param Optional[ErrorGroupState] group_state: Set to filter to just this group state (open, closed, ignored)
        :param Optional[str] error_type: Set to filter to specific types of error (all, unhandledError, handledError)
        :param Optional[str] order_by: The order by parameter to pass in (this will be encoded for you)
        :param Optional[str] limit: The max number of results to return per request (should not go past 100)

        :returns: An iterator of ErrorGroupListItem
        """

        # pylint: disable=too-many-locals

        request_url = self.generate_url(owner_name=owner_name, app_name=app_name)
        request_url += f"/errors/errorGroups?"

        parameters = {"start": start_time.replace(microsecond=0).isoformat()}

        if end_time:
            parameters["end"] = end_time.replace(microsecond=0).isoformat()

        if version:
            parameters["version"] = version

        if app_build:
            parameters["app_build"] = app_build

        if group_state:
            parameters["groupState"] = group_state.value

        if error_type:
            parameters["errorType"] = error_type

        if order_by:
            parameters["$orderby"] = order_by

        if limit:
            parameters["$top"] = str(limit)

        request_url += urllib.parse.urlencode(parameters)

        page = 0

        while True:

            page += 1

            self.log.info(f"Fetching page {page} of crash groups")

            response = self.get(request_url, retry_count=3)

            error_groups = deserialize.deserialize(ErrorGroups, response.json())

            yield from error_groups.errorGroups

            if error_groups.nextLink is None:
                break

            request_url = appcenter.constants.API_BASE_URL + error_groups.nextLink.replace(
                "/api", "", 1
            )

        # pylint: disable=too-many-locals

    def errors_in_group(
        self,
        *,
        owner_name: str,
        app_name: str,
        error_group_id: str,
        start_time: datetime.datetime,
        end_time: Optional[datetime.datetime] = None,
        model: Optional[str] = None,
        operating_system: Optional[str] = None,
    ) -> Iterator[HandledError]:
        """Get the errors in a group.

        :param str owner_name: The name of the app account owner
        :param str app_name: The name of the app
        :param str error_group_id: The ID of the group to get the errors from
        :param datetime.datetime start_time: The time to start getting error groups from
        :param Optional[datetime.datetime] end_time: The end time to get error groups from
        :param Optional[str] model: The device model to restrict the search to (if any)
        :param Optional[str] operating_system: The OS to restrict the search to (if any)

        :returns: An iterator of HandledError
        """

        request_url = self.generate_url(owner_name=owner_name, app_name=app_name)
        request_url += f"/errors/errorGroups/{error_group_id}/errors?"

        parameters = {"start": start_time.replace(microsecond=0).isoformat()}

        if end_time:
            parameters["end"] = end_time.replace(microsecond=0).isoformat()

        if model:
            parameters["model"] = model

        if operating_system:
            parameters["os"] = operating_system

        request_url += urllib.parse.urlencode(parameters)

        page = 0

        while True:

            page += 1

            self.log.info(f"Fetching page {page} of crashes for group {error_group_id}")

            response = self.get(request_url, retry_count=3)

            errors = deserialize.deserialize(HandledErrors, response.json())

            yield from errors.errors

            if errors.nextLink is None:
                break

            request_url = appcenter.constants.API_BASE_URL + errors.nextLink.replace("/api", "", 1)

    def begin_symbol_upload(
        self,
        *,
        owner_name: str,
        app_name: str,
        symbols_name: str,
        symbol_type: SymbolType,
        build_number: Optional[str] = None,
        version: Optional[str] = None,
    ) -> SymbolUploadBeginResponse:
        """Upload debug symbols

        :param str owner_name: The name of the app account owner
        :param str app_name: The name of the app
        :param str symbols_path: The path to the symbols
        :param str symbol_type: The type of symbols being uploaded
        :param Optional[str] build_number: The build number (required for Android)
        :param Optional[str] version: The build version (required for Android)

        :raises ValueError: If the build number or version aren't specified and it's an Android upload

        :returns: SymbolUploadBeginResponse
        """

        if symbol_type == SymbolType.proguard:
            if build_number is None:
                raise ValueError("The build number is required for Android")

            if version is None:
                raise ValueError("The version is required for Android")

        request_url = self.generate_url(owner_name=owner_name, app_name=app_name)
        request_url += f"/symbol_uploads"

        data = {"symbol_type": symbol_type.value, "file_name": symbols_name}

        if build_number:
            data["build"] = build_number

        if version:
            data["version"] = version

        response = self.post(request_url, data=data)

        return deserialize.deserialize(SymbolUploadBeginResponse, response.json())

    def commit_symbol_upload(
        self, *, owner_name: str, app_name: str, upload_id: str
    ) -> SymbolUploadEndRequest:
        """Commit a symbol upload operation

        :param str owner_name: The name of the app account owner
        :param str app_name: The name of the app
        :param str upload_id: The ID of the symbols upload to commit

        :returns: The App Center symbol upload end response
        """

        request_url = self.generate_url(owner_name=owner_name, app_name=app_name)
        request_url += f"/symbol_uploads/{upload_id}"

        data = {"status": "committed"}

        response = self.patch(request_url, data=data)

        return deserialize.deserialize(SymbolUploadEndRequest, response.json())

    def upload_symbols(
        self,
        *,
        owner_name: str,
        app_name: str,
        symbols_path: str,
        symbol_type: SymbolType,
        build_number: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        """Upload debug symbols

        :param str owner_name: The name of the app account owner
        :param str app_name: The name of the app
        :param str symbols_path: The path to the symbols
        :param str symbol_type: The type of symbols being uploaded
        :param Optional[str] build_number: The build number (required for Android)
        :param Optional[str] version: The build version (required for Android)

        :raises Exception: If something goes wrong
        """

        begin_upload_response = self.begin_symbol_upload(
            owner_name=owner_name,
            app_name=app_name,
            symbols_name=os.path.basename(symbols_path),
            symbol_type=symbol_type,
            build_number=build_number,
            version=version,
        )

        with open(symbols_path, "rb") as symbols_file:
            self.azure_blob_upload(begin_upload_response.upload_url, file_stream=symbols_file)

        commit_response = self.commit_symbol_upload(
            owner_name=owner_name,
            app_name=app_name,
            upload_id=begin_upload_response.symbol_upload_id,
        )

        if commit_response.status != SymbolUploadStatus.committed:
            raise Exception("Failed to upload symbols")
