#!/usr/bin/env python
# -*- coding: utf-8 -*-


import jira
import vim

# Remote debugging
import sys
sys.path.append('c:/Program Files (x86)/JetBrains/PyCharm 5.0.3/debug-eggs/pycharm-debug.egg')
import pydevd

def get_issue(issue, url=None):
    """
    This will get the `issue` information from the Jira server at `url`. The
    `issue` information will be placed into the buffer at the current cursor
    location.

    Args:
        issue (string): A valid Jira issue for `url`

    Kwargs:
        url (string): Url for the Jira server.  If no URL is given then the
                      default test server will be used
                      "http://localhost:2990/jira"

    Returns: This returns nothing and instead modifies :meth:vim.current.buffer

    """

    if url:
        options = {'server': url}
    else:
        options = None

    # pydevd.settrace('localhost', port=25252, stdoutToServer=True, stderrToServer=True)
    local_jira = jira.JIRA(options=options)
    jira_issue = local_jira.issue(issue)

    buf = vim.current.buffer
    buf.append(jira_issue.fields.summary)
    buf.append(jira_issue.fields.description)
