__version__ = [1, 1, 0]
"""list: of `[major, minor, bugfix]` version numbers for the package.
"""
# from gevent import monkey
# monkey.patch_all()

import asyncio
import threading
import logging
import time

log = logging.getLogger(__name__)

loops = {}
"""dict: keys are thread names; values are :class:`asyncio.AbstractEventLoop`
event loops running in a separate thread for handling the async aspects of the
web server.
"""
loop_threads = {}
"""dict: keys are therad names; values are :class:`threading.Thread` that
contains the running event loop.
"""
loop_events = {}
"""dict: keys are thread names; values are :class:`threading.Event` to track
whether the loop (in the thread with the same name) has been initialized and is
running.
"""
master_loop_name = None
"""str: name of the master event loop's thread that configured the
dependencies for the app, and which can also take them down.
"""

def _create_loop(name):
    """Creates a new event loop on whatever thread this function is run on.

    .. note:: The loop is set to `run_forever` after it is created. Submit
        coroutines using :func:`run_coroutine_threadsafe`.

    Args:
        name (str): name given to thread that the loop will run on.
    """
    global loops
    policy = asyncio.get_event_loop_policy()
    loops[name] = policy.new_event_loop()
    asyncio.set_event_loop(loops[name])
    loop_events[name].set()
    loops[name].run_forever()

def create_loops(num_loops=1):
    """Creates new event loops in a separate threads for handling async functionality.

    Args:
        num_loops (int): number of event loop threads to create.

    Returns:
        str: name of the master (first) loop.
    """
    global loop_thread, master_loop_name, loop_events
    for i in range(num_loops):
        name = f"dc-{len(loop_events)}"
        loop_events[name] = threading.Event()
        loop_threads[name] = threading.Thread(target=_create_loop, name=name, args=(name,))
        log.debug(f"Starting new thread for loop {name}.")
        loop_threads[name].start()

        if len(loop_events) == 1:
            # We just started the master loop. Store its thread name. Also, wait
            # for it to start so we don't have undefined references later on.
            master_loop_name = name
            loop_events[name].wait()

    return master_loop_name

def stop_all_loops(future):
    """Stops all the event loops in their threads.
    """
    for name, _loop in loops.items():
        log.debug(f"Stopping event loop {name}.")
        _loop.call_soon_threadsafe(_loop.stop)

    # Next, wait for all the loop threads to join, meaning that the loops have
    # actually stopped.
    for name, _thread in loop_threads.items():
        _thread.join()
        log.debug(f"Loop stop succeeded in thread {name}.")

def get_master_loop():
    """Returns the first event loop created in a separate thread (with index 0).
    """
    loop_events[master_loop_name].wait(5)
    return loops[master_loop_name]

def get_event_loop(index):
    """Returns the event loop with the given index.
    """
    return loops.get(f"dc-{index}")

def get_version():
    """Returns the version of the package formatted as a string.
    """
    return '.'.join(map(str, __version__))

def application_ready():
    """Checks to see if the application has finished initializing *and* the
    agents have all finished initializing by checking the :class:`threading.Event`
    flags.
    """
    from datacustodian.datacustodian_app import started
    from datacustodian.dlt import agent_events
    agents_ready = False
    for agent_name, event in agent_events.items():
        agents_ready = agents_ready and event.is_set()
        if not agents_ready:
            break

    return agents_ready and started.is_set()
