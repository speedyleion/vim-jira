#!/usr/bin/env python
# encoding: utf-8

import unittest
import vimrunner
import os

dirname = os.path.dirname(os.path.abspath(__file__))


class VimTest(unittest.TestCase):
    """
    This is the class that all tests for working with Vim should derive from.

    If you are playing on windows you may need to hack up vimrunner to work.  The biggest
    issue is telling vimrunner to use splitlines() instead of split('\n').

    Do to the use of vimrunner and its backend functionality these don't seem to work with
    nose2.  As such just call them directly or try running unittest.

    Attributes:
        vim(vimrunner.Server): Main vim server.  Not sure this really needs to be exposed.

        client(vimrunner.Client): This is the remote client that is started for tests.  All
                                  queries and commands should be ran through this.

    """
    def setUp(self):
        """
        This just creates a vim server instance.
        """
        # initialize vim server, make sure to tell GVIM not to load the user
        # .gvimrc,
        self.vim = vimrunner.Server(extra_args=['-n', '-U "NONE"'])

        # start GVIM as server and get a client connected to it
        self.client = self.vim.start_gvim()
        self.client.add_plugin(dirname + '/../', 'plugin/jira.vim')

        # Add Netrw,
        self.client.add_plugin(os.path.dirname(self.vim.executable),
                               'plugin/netrwPlugin.vim')

    def tearDown(self):
        self.client.quit()


class TestWindowCreation(VimTest):
    """
    This is the class that tests the basic creation of the jira window.
    """
    def testDefaultOpenWindow(self):
        """
        This will test the opening of the window and that it is in the correct
        location and it obeys the global variables set.
        """
        self.client.command('JiraOpen "DEMO-4589"')

        winnr = self.client.eval('winnr()')
        self.assertEqual(winnr, '2', "Jira window should be the second one")

        # Check the sizing of the window
        sizes = self.client.eval('winrestcmd()')
        expected_sizes = '1resize 23|vert 1resize 39|2resize 23|vert 2resize 40|'
        self.assertEqual(sizes, expected_sizes,
                         "Window didn't appear to split vertically")

        # TODO this should probably be a temp file for the issue
        bufname = self.client.eval('bufname("")')

        self.assertEqual(bufname, 'DEMO-4589', "Expecting "
                         "`DEMO-4589`; Got %s"
                         % (bufname))

        # Check the contents were retrieved for the issue
        buf_contents = self.client.read_buffer(1, '"$"').splitlines()
        expected_contents = ['Test July issue in jira', 'Disription to first Jira ticket.']
        self.assertEqual(buf_contents, expected_contents,
                         'Incorrect content data or formatting.')

    def testURL(self):
        """
        This will test for a non default setting to `g:jira_url`.

        I just did a quick scrape for a publicly visible Jira server so this test may be a
        little fragile, though I would hope Apache keeps it around for a while.

        """
        self.client.command('let g:jira_url="https://issues.apache.org/jira"')
        self.client.command('JiraOpen "SPARK-9278"')

        buf_contents = self.client.read_buffer(1, '"$"').splitlines()
        expected_summary = 'DataFrameWriter.insertInto inserts incorrect data'
        self.assertEqual(buf_contents[0], expected_summary,
                         'Incorrect Summary for SPARK-9278.')

    def testHorizontal(self):
        """
        This will test with `g:jira_vertical` set to 0, meaning open a horizontal window.

        """
        self.client.command('let g:jira_vertical=0')
        self.client.command('JiraOpen "DEMO-9266"')

        sizes = self.client.eval('winrestcmd()')
        expected_sizes = '1resize 11|vert 1resize 80|2resize 11|vert 2resize 80|'
        self.assertEqual(sizes, expected_sizes,
                         "Window didn't appear to split horizontally")

if __name__ == '__main__':
    unittest.main()
