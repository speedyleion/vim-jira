" This is the main plug-in entry for Jira it has the mappings as well as
" the setting of the global variables.

if &cp || exists('g:loaded_jira')
    finish
endif
let g:loaded_jira=1

" Config settings {{{1
" let g:jira_width = get(g:, 'jira_width', 80)
" let g:jira_botright = get(g:, 'jira_botright', 1)
let g:jira_vertical = get(g:, 'jira_vertical', 1)
let g:jira_url = get(g:, 'jira_url', 'https://jira.atlassian.com')
" }}}
 
" Commands {{{1
    " TODO need to see about working with completion on these
    
command! -nargs=? JiraOpen call jira#OpenWindow(<args>)

    " TODO this needs an actual test, currently not tested :(
command! -nargs=? JiraBrowse call jira#BrowseIssue(<args>)
"}}}

