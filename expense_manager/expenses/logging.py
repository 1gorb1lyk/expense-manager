import logging
import time
from functools import wraps
from rest_framework.response import Response

logger = logging.getLogger(__name__)

def log_request_and_exception(func):
    """
    A decorator to log request details, execution time, and handle exceptions.
    """
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        # Log the request details
        logger.info(f"Request: {request.method} {request.path}")

        start_time = time.time()
        try:
            # Execute the original function
            response = func(self, request, *args, **kwargs)
        except Exception as e:
            # Log exceptions and return a 500 response
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            return Response({"error": "Internal Server Error"}, status=500)

        # Calculate execution time and log the response status
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Response Status: {response.status_code} | Time: {execution_time:.4f}s")
        return response

    return wrapper