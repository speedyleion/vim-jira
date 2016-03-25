" This is the syntax highlighting for jira buffers.

if exists("b:current_syntax")
    finish
endif

" This is the text between section headers.  Note per Vim syntax documentation,
" you don't actually have to find an end, thus the last one until the end of the
" file will still look good
syntax region JiraSectionBody matchgroup=JiraSectionHeader start='^\S\+\:$' end='\(^\S\+\:$\)\@=' contains=JiraIssue
syntax match JiraIssue /\<\u\+-\d\+\>/ contained


highlight default link JiraSectionHeader Title
highlight default link JiraIssue Identifier

" Not sure this one is needed
highlight default link JiraSectionBody Normal 
let b:current_syntax = "jira"
