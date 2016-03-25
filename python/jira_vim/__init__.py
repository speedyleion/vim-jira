#!/usr/bin/env python
# -*- coding: utf-8 -*-


import jira
import vim

# Remote debugging
# import sys
# sys.path.append('c:/Program Files (x86)/JetBrains/PyCharm 5.0.3/debug-eggs/pycharm-debug.egg')
# import pydevd

#: A list of dictionaries where the keys are attributes in a :attr:`JIRA.issue` and the
#: values are strings to be used to display in the buffer
SECTIONS = [{'summary': 'Summary:'}, {'status': 'Status:'}, {'assignee': 'Assignee:'},
            {'description': 'Description:'}]


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

    # For empty buffers appending always leaves a blank line, so check for it and clean up
    # when done
    if len(buf) == 1 and not buf[0]:
        delete_first_line = True
    else:
        delete_first_line = False

    # Go through each section and add the section title followed by the section contents
    for section in SECTIONS:
        for key in section:
            buf.append(section[key])
            content = getattr(jira_issue.fields, key)

            # Favor display name, and then name, and then finally hopefully it's a text
            # element
            if hasattr(content, 'displayName'):
                content = content.displayName
            elif hasattr(content, 'name'):
                content = content.name

            buf.append(content)
            buf.append('\n')

    if delete_first_line:
        del buf[0]
