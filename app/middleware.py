from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.logger import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)

        logger.info(f"Incoming request: {method} {url} from {client_ip}")
        logger.info(f"Headers: {headers}")

        response = await call_next(request)
        return response
