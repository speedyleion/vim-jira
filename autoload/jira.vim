" This is the main functionality for the jira plug-in.  This handles creating,
" or jumping to, a __Jira__ window.

" Python imports {{{1
let s:plugin_path = escape( expand( '<sfile>:p:h:h' ), '\' )
py import sys
" May want to consider prepending this
exe 'python sys.path = sys.path + ["' . s:plugin_path . '/python"]' 
py import jira_vim
"}}}


" jira#OpenWindow()
" Parameters:
"   Issue(string): The issue information to fill the buffer with.
"       {{{1
function! jira#OpenWindow(issue) abort

    let split = g:jira_vertical ? 'vsplit ' : 'split '

    " Open the buffer
    exe 'silent keepalt botright ' . split . a:issue

    setlocal filetype=jira

    " Adding '-' to the keyword since Jira issues are usually JIRA-1234
    setlocal iskeyword+=-

    " Add a variable for holding the issue number
    let b:issue=a:issue

    " Get the Issue information
    exe 'python jira_vim.get_issue("'.a:issue.'", url="'.g:jira_url.'")'

endfunction
" }}}

" jira#BrowseIssue()
" Parameters:
"   Issue(string): The issue to launch in a browser
"       This can be empty then b:issue will be used.  If neither is given this
"       will return 0
"       {{{1
function! jira#BrowseIssue(...) abort
    " Get the Issue information
    if a:0 > 0
        let l:issue = a:1
    else
        try
            let l:issue = b:issue
        catch /^Vim\%((\a\+)\)\=:E121/	
            return 0
        endtry
    endif

    " Stitch the jira url and the issue number together then kick off NETRW
    let l:issue_url = g:jira_url . '/browse/' . l:issue
    call netrw#NetrwBrowseX(l:issue_url, 0)
    return 1
endfunction
" }}}

