"""
Tests for passing invalid endpoints which require a target ID to be given.
"""

from urllib.parse import urljoin

import pytest
import requests
from requests import codes

from common.constants import ResultCodes
from tests.mock_vws.utils import Endpoint, assert_vws_failure
from tests.utils import VuforiaServerCredentials
from vws._request_utils import authorization_header, rfc_1123_date


@pytest.mark.usefixtures('verify_mock_vuforia')
class TestInvalidGivenID:
    """
    Tests for giving an invalid ID to endpoints which require a target ID to
    be given.
    """

    def test_not_real_id(self,
                         vuforia_server_credentials: VuforiaServerCredentials,
                         endpoint_which_takes_target_id: Endpoint,  # noqa: E501 pylint: disable=redefined-outer-name
                         ) -> None:
        """
        A `NOT_FOUND` error is returned when an endpoint is given a target ID
        of a target which does not exist.
        """
        request_path = endpoint_which_takes_target_id.example_path
        date = rfc_1123_date()

        authorization_string = authorization_header(
            access_key=vuforia_server_credentials.access_key,
            secret_key=vuforia_server_credentials.secret_key,
            method=endpoint_which_takes_target_id.method,
            content=endpoint_which_takes_target_id.content,
            content_type=endpoint_which_takes_target_id.content_type or '',
            date=date,
            request_path=request_path,
        )

        headers = {
            "Authorization": authorization_string,
            "Date": date,
        }

        # TODO: Set this url in the Endpoint
        url = urljoin('https://vws.vuforia.com/', request_path)
        response = requests.request(
            method=endpoint_which_takes_target_id.method,
            url=url,
            headers=headers,
            data=endpoint_which_takes_target_id.content,
        )

        assert_vws_failure(
            response=response,
            status_code=codes.NOT_FOUND,
            result_code=ResultCodes.UNKNOWN_TARGET,
        )
