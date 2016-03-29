#!/usr/bin/env python
# -*- coding: utf-8 -*-


import jira
import vim
import operator
import textwrap
import time
import calendar
import netrc

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

    # HACK not fond of this but want an easy way to not hard code username and password
    basic_auth = None
    try:
        user_net = netrc.netrc()
        if url in user_net.hosts:
            info = user_net.authenticators(url)
            basic_auth = (info[0], info[2])
    except netrc.NetrcParseError:
        pass

    local_jira = jira.JIRA(options=options, basic_auth=basic_auth)
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
        name = comment.author.displayName.encode('ascii', errors='replace')
        comment_time = format_time(comment.created, "%x %X")

        # For comments have first line be name and then push the time all the way out by the
        # width
        buf.append('{}{:>{width}}'.format('    ' + name, comment_time,
                   width=width-len(name)))

        content = comment.body
        buf.append(wrapper.wrap(content))
        buf.append('\n')

    if delete_first_line:
        del buf[0]


def format_time(time_str, format):
    """
    This will take a time from Jira and format it into the specified string.  The time will
    also be converted from UTC to local time.

    Jira time format is assumed to be, "YYYY-MM-DDTHH:MM:SS.ssss+0000". Where "T" is the
    literal character guessing it means "time". "ssss" are interpreted as fractions of
    seconds "+0000" is the timezone offset from UTC.

    Args:
        time_str (string): Time returned from :class:`jira.issue`

        format (string): String to specify how to format the resultant time.  You'll want to
                       look at :func:`time.strftime` for the format options.

    Returns: A string representing the local version of `time` formated according to
             `format`.

    """

    # Strip off the trailing timezone
    # HACK FOR NOW ALWAYS ASSUME "+0000"
    just_time, zone = time_str.split('+')

    # Just drop the fractional seconds
    just_time, _ = just_time.split('.')

    parsed_time = time.strptime(just_time, "%Y-%m-%dT%H:%M:%S")

    # Convert from UTC to seconds and from seconds to local
    local_time = time.gmtime(calendar.timegm(parsed_time))

    return time.strftime(format, local_time)
