from abc import ABC, abstractmethod
from typing import Any
import requests
try:
    from requests_ip_rotator import ApiGateway
except ImportError:
    ApiGateway = None

class RequestError(Exception):
    """
    Exception raised when a request to the allabolag.se website fails.
    """
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Request failed with status code {status_code}: {message}")

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
class BaseRequestClient(ABC):
    @abstractmethod
    def get(self, url: str, *args, **kwargs) -> Any:
        """
        Send a GET request to the specified URL.

        This method must be implemented by child classes.

        Args:
            url (str): The URL to send the GET request to.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The response from the GET request.

        Raises:
            NotImplementedError: If the method is not implemented in a child class.
            RequestError: If the request fails.
        """
        raise NotImplementedError("This method must be implemented in a child class.")


class RequestsRequestClient(BaseRequestClient):
    def __init__(self, extra_headers: dict = {}):
        self.headers = {**DEFAULT_HEADERS, **extra_headers}

    def get(self, url: str, *args, **kwargs) -> requests.Response:
        """
        Send a GET request to the specified URL.

        Args:
            url (str): The URL to send the GET request to.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            requests.Response: The response from the GET request.

        Raises:
            RequestError: If the request fails.
        """
        response = requests.get(url, headers=self.headers, *args, **kwargs)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise RequestError(response.status_code, response.text) from e
        return response



class AWSGatewayRequestClient(BaseRequestClient):
    """
    A request client that uses rotating IP addresses through AWS API Gateway.

    This client is designed to make requests to the allabolag.se website while
    rotating IP addresses to avoid rate limiting or IP-based blocking.

    Set up AWS credentials
    To use this client, you need to set up AWS credentials and ensure your IAM user or role has the necessary permissions. The required IAM statements include:

    1. Permission to create API Gateway resources: This allows the client to set up the necessary API Gateway endpoints for IP rotation.
    2. Permission to delete API Gateway resources: This enables the client to clean up resources when they're no longer needed.
    3. Permission to describe EC2 regions: This allows the client to gather information about available regions for IP rotation.

    Specifically, your IAM policy should grant "Allow" effect for the following actions:
    - apigateway:POST
    - apigateway:DELETE
    - ec2:DescribeRegions

    These permissions should be applied to all resources ("*") to ensure proper functionality across different AWS regions.

    Do use AWS credentials you may either:
    1. Set the AWS_PROFILE environment variable:
        export AWS_PROFILE=your_profile_name
    2. Set individual AWS credential environment variables:
        export AWS_ACCESS_KEY_ID=your_access_key
        export AWS_SECRET_ACCESS_KEY=your_secret_key

    """

    def __init__(self, aws_regions: list = ["eu-north-1"], extra_headers: dict = {}):
        """
        Initialize the AWSGatewayRequestClient.        

        Args:
            aws_regions (list): List of AWS regions to use for IP rotation.
                                Defaults to ["eu-north-1"].
            extra_headers (dict): Additional headers to include in requests.
                                  Defaults to an empty dictionary.

        Raises:
            ImportError: If the requests_ip_rotator package is not installed.
        """
        self.base_url = "https://www.allabolag.se"
        if ApiGateway is None:
            raise ImportError("requests_ip_rotator not installed")
        self.gateway = ApiGateway(self.base_url, regions=aws_regions)
        self.gateway.start()
        self.session = requests.Session()
        self.session.mount(self.base_url, self.gateway)
        self.headers = {**DEFAULT_HEADERS, **extra_headers}

    def get(self, url: str, *args, **kwargs) -> requests.Response:
        """
        Send a GET request to the specified URL using a rotating IP.

        Args:
            url (str): The URL to send the GET request to.
            *args: Variable length argument list to pass to requests.get().
            **kwargs: Arbitrary keyword arguments to pass to requests.get().

        Returns:
            requests.Response: The response from the GET request.

        Raises:
            RequestError: If the request fails.
        """
        if not url.startswith(self.base_url):
            url = f"{self.base_url}{url}"
        try:
            response = self.session.get(url, headers=self.headers, *args, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            raise RequestError(response.status_code, response.text) from e

    def __del__(self):
        """
        Destructor method to ensure the API Gateway is shut down properly.
        """
        try:
            self.gateway.shutdown()
        except Exception as e:
            pass
            print(f"Error shutting down API Gateway: {e}")
