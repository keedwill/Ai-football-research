"""
utils/async_helper.py — Helper for running async functions in sync context.

Handles the case where an event loop is already running (e.g., in FastAPI).
"""

import asyncio
from typing import Coroutine, TypeVar

T = TypeVar('T')


def run_async(coro: Coroutine) -> T:
    """
    Run an async function from sync context.
    
    Handles both cases:
    - No event loop running: uses asyncio.run()
    - Event loop already running: uses nest_asyncio or creates task
    
    Args:
        coro: Coroutine to run
    
    Returns:
        Result of the coroutine
    """
    try:
        # Try to get the running loop
        loop = asyncio.get_running_loop()
        # If we get here, a loop is running - we need to handle this
        # We'll use asyncio.ensure_future and wait for it
        import concurrent.futures
        import threading
        
        # Run in a new thread with its own event loop
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
            
    except RuntimeError:
        # No event loop running, use asyncio.run()
        return asyncio.run(coro)
