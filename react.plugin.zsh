#autoload

function react() {
    python3 $ZSH/plugins/react/react.py $@
}


_react() {
    local curcontext="$curcontext" state line _opts ret=1

    # _arguments '-n --name[component name]' '--path[componet path]'
    _arguments -C \
        '1: :->cmds' \
        '*:: :->args' && ret=0

        case "$state" in
            cmds)
                _values "Create component" \
                "create_component[Create Class Component]" && ret=0
            ;;
            args)
                case $line[1] in
                    create_component)
                        _arguments \
                        '(-n --name)'{-n,--name}'[Component name]' \
                        '(-p --path)'{-p,--path}'[Component path]' \
                        '(-c --no_css)'{-c,--no_css}'[No css import]' \
                        '(-t --type)'{-t,--type}'[Component type]' && ret=0
                    ;;
                esac
            ;;
        esac
    _describe "react" subcmds
    return ret
}
compdef _react react rcc


function create_react_app() {
    npx create-react-app $@
}

_create_react_app() {
    local _1st_arguments ret=1
   _1st_arguments=(
        {'-V','--version'}':output the version number]' \
        '--verbose:print additional logs' \
        "--info:print environment debug info" \
        "--scripts-version:<alternative-package>  use a non-standard version of react-scripts" \
        "--template:<path-to-template> specify a template for the created project" \
        "--use-pnp" \
        {'-h','--help'}':output usage information'
    )

    _describe "create_react_app <project-directory> [options] " _1st_arguments && ret=0

    return ret
}

compdef _create_react_app create_react_app cra

alias cra="create_react_app"
alias rcc='react'

