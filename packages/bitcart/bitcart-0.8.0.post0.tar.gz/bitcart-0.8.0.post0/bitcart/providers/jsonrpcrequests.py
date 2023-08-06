from typing import Any, Optional, Union, Callable

ASYNC = False

try:
    if ASYNC:
        import aiohttp
        from jsonrpcclient.clients.aiohttp_client import AiohttpClient as RPC
    else:
        import requests
        from jsonrpcclient.clients.http_client import HTTPClient as RPC
except (ModuleNotFoundError, ImportError):
    pass  # probably during CI build


class RPCProxy:
    def __init__(
        self: "RPCProxy",
        url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        xpub: Optional[str] = None,
        session: Optional[Union["aiohttp.ClientSession", "requests.Session"]] = None,
        verify: Optional[bool] = True,
    ):
        self.url = url
        self.username = username
        self.password = password
        self.xpub = xpub
        self.verify = verify
        self.session: Union["aiohttp.ClientSession", "requests.Session"]
        if session:
            self.sesson = session
        else:
            self.create_session()
        if ASYNC:
            self.rpc = RPC(endpoint=self.url, session=self.session)
        else:
            self.rpc = RPC(endpoint=self.url)
            self.rpc.session = self.session

    def create_session(self: "RPCProxy") -> None:
        if ASYNC:
            self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=self.verify),
                auth=aiohttp.BasicAuth(self.username, self.password),  # type: ignore
            )
        else:
            self.session = requests.Session()
            self.session.auth = (self.username, self.password)  # type: ignore

    def __getattr__(
        self: "RPCProxy", method: str, *args: Any, **kwargs: Any
    ) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return (
                self.rpc.request(
                    method, validate_against_schema=False, *args, **kwargs
                )
            ).data.result

        return wrapper

    def _close(self: "RPCProxy") -> None:
        self.session.close()  # type: ignore
