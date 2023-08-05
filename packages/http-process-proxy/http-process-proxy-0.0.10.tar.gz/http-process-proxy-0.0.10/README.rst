http-process-proxy
==================

Live-reloading HTTP reverse proxy for web development.

Installation
~~~~~~~~~~~~

First, `install Watchman
<https://facebook.github.io/watchman/docs/install.html>`_.

Then::

   pip install http-process-proxy

Optionally, install a `LiveReload extension
<http://livereload.com/extensions/>`_ on your development web browser. The
extension lets you choose to _automatically_ refresh the page after files
change.

Usage
~~~~~

First, you need a web server for http-process-proxy to invoke. Then wrap it::

    http-process-proxy localhost:8000 8001 \
        --pattern 'src/**/*' \
        --exclude 'src/**/test_*' \
        --exec python ./manage.py runserver --noreload 8001

That is::

    http-process-proxy BIND:BINDPORT BACKEND:PORT [OPTIONS ...] --exec BACKENDCOMMAND ...

Where:

* ``BIND:PORT`` is the address and port to listen on (e.g., ``0.0.0.0:8000``,
  ``localhost:9000``, ...)

* ``BACKEND:PORT`` is the address of the server we're proxying

* ``BACKENDCOMMAND ...`` is the command to run the web-server we're developing,
  which must listen on ``BACKEND:PORT``.

* ``OPTIONS`` can include:

  * ``--pattern`` with any number of glob-style paths. Files matching *any* of
    the patterns (and not matching an ``--exclude`` pattern) can trigger a
    reload. (If unset, *any* file change triggers a reload -- the same effect
    as ``**/*``.)

  * ``--exclude`` with any number of glob-style paths. Files matching *any* of
    the patterns will never trigger a reload -- regardless of ``--pattern``.

Features
~~~~~~~~

* Starts and proxies your web server, sending it all HTTP requests.

* Supports WebSockets.

* Queues HTTP requests until your web server is ready to respond.

* Adds `Forwarded
  <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Forwarded>`_
  header so your web server knows the correct hostname.

* Prints your web server's standard output and standard error.

* Kills your server ``SIGKILL`` and restarts when its files change.

* Responds with `503 Service Unavailable` if your web server crashes.

* Closes keep-alive connections when responses may change.

* Forwards Chunked-encoded responses, even when keep-alive is set.

* Watches the current working directory for file modifications with
  `Watchman <https://facebook.github.io/watchman/>`_.

* Respects `.watchmanconfig
  <https://facebook.github.io/watchman/docs/config.html>`_.

Develop
~~~~~~~

#. Run ``pip3 install --user -e .[dev]`` to install development tools.
#. Change some code.
#. If needed, modify the *Features* and *Usage* sections in this file.
#. Fix styles with ``./reformat-source.sh``
#. Manually test according to the *Features* and *Usage* sections in this file.
   (This project is an experiment; it's missing automated tests.)
#. Submit a pull request.

A useful test procedure (for testing everything but Websockets)::

    python3 -m httpprocessproxy localhost:8010 localhost:8011 \
         --exec sh -c 'sleep 0.1 && python3 -m http.server 8011'

    # browse to http://localhost:8010 for a directory listing
    # Turn on LiveReload
    touch x  # browser should show an extra file
    rm x  # browser should hide the extra file

For websockets, a super-simple echo server::

    python3 -m httpprocessproxy localhost:8010 localhost:8011 \
         --exec python3 ./test/servewebsockets.py

    # send a request
    echo 'test' | ws ws://localhost:8010/ws

    # keep a request open...
    ws ws://localhost:8010/ws
    # at this point, `touch x && rm x` would close the connection, because it
    # switches from "running" to "killing"

Maintain
~~~~~~~~

Use `semver <https://semver.org/>`_.

#. Merge pull requests.
#. Change: ``__version__`` in ``httpprocessproxy/__init__.py``.
#. Add ``CHANGELOG.rst`` entry to the top of the file.
#. Commit: ``git commit CHANGELOG.rst httpprocessproxy/__init__.py -m 'vX.X.X'`` but don't push.
#. Tag: ``git tag vX.X.X``
#. Push the new tag: ``git push --tags && git push``

TravisCI will push to PyPi.

Design
~~~~~~

This proxy server cycles through states. Each state decides how to respond to
connections and what to do when files change.

1. *Loading*: starts the backend (your server) and pings with HTTP requests.
    * Incoming connections will queue.
    * State changes:
        * If a file is modified, kill the backend and transition to *Killing*.
        * If a ping succeeds, transition to *Running* and pass queued incoming
          connections to that state.
        * If backend exits, transition to *Error* and respond to all buffered
          incoming connections.
2. *Running*: the backend is alive.
    * Incoming connections will pass through.
    * State changes:
        * If a file is modified, kill the backend and transition to *Killing*.
          Existing HTTP connections will 
          Drop all live HTTP connections.
        * If the backend exits, transition to *Error*. Drop all live HTTP
          connections.
3. *Error*: the web server exited of its own accord.
    * Incoming connections will lead to `503 Service Unavailable` errors.
    * State changes:
        * If a file is modified, transition to *Loading*.
          Complete all live HTTP connections.
4. *Killing*: 
    * Incoming connections will buffer.
    * State changes:
        * If a file is modified, do nothing.
        * When the subprocess exits, transition to *Loading*.

If the user hits ``Ctrl+C``, everything stops -- no matter what the state.

License
~~~~~~~

Copyright (c) 2019 Adam Hooper. MIT license.
