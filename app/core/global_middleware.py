# app/core/global_middleware.py
import logging
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class GlobalMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        logging.info(f"Request: {request.method} {request.url}")
        
        # Catat waktu mulai
        start_time = time.time()
        
        try:
            # Proses request
            response = await call_next(request)
            
            # Hitung durasi proses
            process_time = time.time() - start_time
            
            # Log detail proses
            logging.info(
                f"Request processed: {request.method} {request.url} - "
                f"Status {response.status_code} - "
                f"Process time: {process_time:.4f} seconds"
            )
            
            return response
        
        except Exception as e:
            # Log error jika terjadi
            logging.error(f"Error processing request: {str(e)}")
            raise