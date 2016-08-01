Vim-Jira
=========

This is a Vim plug-in for working with Jira issues.  It is meant for viewing
issues in a dedicated buffer as well as **eventually** editing/updating them.

Using It
--------
Start up Vim and run ``:JiraOpen "CORE-177"`` if you haven't changed the
settings you should get something like.

    ::
    Summary:
        Please add license info to the pom

    Status:
        Open

    Assignee:

Status
------

This is currently very early in development.

It only supports displaying issues from the configured Jira URL, ``g:jira_url``,
with anonymous access.

License
-------

This is licensed using the `unlicense <http://unlicense.org>`_.  Basically do
what you will with this as long has you have fun.

Installation
------------

Simply clone this repo where it can be accessed and sourced by Vim.

Like most Vim plug-ins the suggestion is to use one of the great plug-in
managers:

- `Pathogen <https://github.com/tpope/vim-pathogen>`_
- `Vundle <https://github.com/VundleVim/Vundle.vim>`_
- `VAM <https://github.com/MarcWeber/vim-addon-manager>`_
- And many more (on channel four).

Dependencies
^^^^^^^^^^^^

- Vim compiled with python support. Doing the following in Vim 
  ``:echo has('python')`` should display a nice ``1``.
  Python 3 may work, but this author is stuck back on 2.7 so hasn't ensured
  Python 3 compatibility.

- The python package Jira, which has many of its own dependencies.  On most
  machines ``pip install jira``.

Similar Plug-ins
----------------

- https://github.com/markabe/vim-jira-open
- https://github.com/mnpk/vim-jira-complete

Contributing
------------

The repo is here https://github.com/speedyleion/vim-jira.  Submit pull requests.
