_openapi_cli()
{
  cur=${COMP_WORDS[COMP_CWORD]}
  COMPREPLY=($(compgen -W "$(${COMP_WORDS[@]} --dry-run 2>&1 >/dev/null | grep -Po "(?<={)[^}]+" | tr , ' ')" -- $cur))
}
complete -F _openapi_cli openapi-cli