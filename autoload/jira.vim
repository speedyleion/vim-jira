" This is the main functionality for the jira plug-in.  This handles creating,
" or jumping to, a __Jira__ window.

" Python imports {{{1
let s:plugin_path = escape( expand( '<sfile>:p:h:h' ), '\' )
py import sys
" May want to consider prepending this
exe 'python sys.path = sys.path + ["' . s:plugin_path . '/python"]' 
py import jira_vim
"}}}

" Initialization {{{1
let s:window_name = '__Jira__'
" }}}

" jira#OpenWindow()
" Parameters:
"   Issue(string): The issue information to fill the buffer with.
"       This can be empty
"       {{{1
function! jira#OpenWindow(...) abort
    let l:buf_num = bufnr('%')
    " let openpos = g:jira_botright ? 'botright ' : 'topleft ' 
    let split = g:jira_vertical ? 'vsplit ' : 'split '
    " exe 'silent keepalt ' . openpos . g:jira_width . split
    exe 'silent keepalt botright ' . split . s:window_name
    

    setlocal filetype=jira

    " Get the Issue information
    if a:0 > 0
        let b:issue = a:1
        exe 'python jira_vim.get_issue("'.b:issue.'", url="https://jira.atlassian.com")'
    endif

endfunction
" }}}

