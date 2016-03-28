#!/usr/bin/env python
# -*- coding: utf-8 -*-


import jira
import vim
import operator
import textwrap

# Remote debugging
# import sys
# sys.path.append('c:/Program Files (x86)/JetBrains/PyCharm 5.0.3/debug-eggs/pycharm-debug.egg')
# import pydevd

#: A list of dictionaries where the keys are attributes in a :attr:`JIRA.issue` and the
#: values are strings to be used to display in the buffer
SECTIONS = [{'summary': 'Summary:'}, {'status': 'Status:'}, {'assignee': 'Assignee:'},
            {'description': 'Description:'}]


def get_issue(issue, url=None, sections=None):
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

    if not sections:
        sections = SECTIONS

    local_jira = jira.JIRA(options=options)
    jira_issue = local_jira.issue(issue)

    buf = vim.current.buffer

    # For empty buffers appending always leaves a blank line, so check for it and clean up
    # when done
    if len(buf) == 1 and not buf[0]:
        delete_first_line = True
    else:
        delete_first_line = False

    # Handle wrapping of text
    width = int(vim.eval('&tw'))
    if not width:
        width = 80
    wrapper = textwrap.TextWrapper(width=width, initial_indent='    ',
                                   break_on_hyphens=False)

    # Go through each section and add the section title followed by the section contents
    for section in sections:
        for key in section:
            buf.append(section[key])
            content = operator.attrgetter(key)(jira_issue.fields)
            buf.append(wrapper.wrap(content))
            buf.append('\n')


    # pydevd.settrace('localhost', port=25252, stdoutToServer=True, stderrToServer=True)

    # Comments get handled special, really should handle this in main sections but for now
    # leave it separate
    buf.append('Comments:')
    wrapper.initial_indent += '    '
    for comment in jira_issue.fields.comment.comments:
        # HACK need to get better handling for non english characters
        buf.append('    ' + comment.author.displayName.encode('ascii', errors='replace') +
                   '    ' + comment.created)

        content = comment.body
        buf.append(wrapper.wrap(content))
        buf.append('\n')

    if delete_first_line:
        del buf[0]
