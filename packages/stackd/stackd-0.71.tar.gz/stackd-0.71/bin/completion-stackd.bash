#!/usr/bin/env bash

completeServiceName ()
{
  local comp_word=$1
  local stackname=$("${COMP_WORDS[0]}" getname)
  local stackname_len=${#stackname}
  local services=$(docker service ls \
    --filter label=com.docker.stack.namespace=$stackname \
    --format "{{.Name}}" \
  )
  local service
  local serviceShortnames=()

  while IFS= read -r service
  do
    serviceShortnames+=( "${service:$((stackname_len+1))}" )
  done < <(printf '%s\n' "$services")

  local serviceShortnamesStr=$( IFS=$'\n'; echo "${serviceShortnames[*]}" )

  COMPREPLY=( $( compgen -W '$serviceShortnamesStr' $comp_word ) )
}

_stackd_completions()
{
  local cmds=()
  cmds+=("env")
  cmds+=("infos")
  cmds+=("getname")
  cmds+=("deploy")
  cmds+=("up")
  cmds+=("rm")
  cmds+=("remove")
  cmds+=("ls")
  cmds+=("ps")
  cmds+=("compo")
  cmds+=("compo-freeze")
  cmds+=("pull")
  cmds+=("getimagelist")
  cmds+=("printenv")
  cmds+=("deploy-with-portainer")
  cmds+=("rm-with-portainer")
  cmds+=("config-prune")
  cmds+=("logs")
  cmds+=("build")
  cmds+=("bundle")
  cmds+=("vc")
  cmds+=("clear")
  cmds+=("before-clear")
  cmds+=("after-clear")
  cmds+=("reset")
  cmds+=("exec")
  cmds+=("sh")
  cmds+=("bash")
  cmdsStr=$( IFS=$'\n'; echo "${cmds[*]}" )

  local cmd="${COMP_WORDS[1]}"
  local words_len=${#COMP_WORDS[@]}

  COMPREPLY=()

  if [ "$cmd" = "logs" ]; then

    if [ ! $words_len -eq 3 ]; then
      return
    fi

    completeServiceName ${COMP_WORDS[2]}


  elif [ "$cmd" = "exec" ] || [ "$cmd" = "sh" ] || [ "$cmd" = "bash" ]; then

    if [ "${COMP_WORDS[2]}" = "" ] && [ $words_len -eq 2 ]; then
      COMPREPLY=( $( compgen -W '$cmdsStr' $cmd ) )
      return
    fi


    local stackname=$("${COMP_WORDS[0]}" getname)

    local args_len=0
    local servicename
    local containerID
    for word in "${COMP_WORDS[@]}"; do
      if [ "${word:0:1}" != "-" ]; then
        ((args_len+=1))
        if [ $args_len -eq 3 ]; then
          servicename="${word}"
        fi
        if [ $args_len -eq 4 ]; then
          containerID="${word}"
        fi
      fi
    done

    if [ $args_len -eq 3 ]; then
      completeServiceName $servicename
      return
    fi
    if [ ! $args_len -eq 4 ]; then
      return
    fi

    local stackname_len=${#stackname}
    local servicename_len=${#servicename}

    local serviceContainerNames=$(docker container ls \
      --filter "label=com.docker.stack.namespace=${stackname}" \
      --filter "label=com.docker.swarm.service.name=${stackname}_${servicename}" \
      --format {{.Names}} \
    )

    local serviceContainerIDs=()
    while IFS= read -r serviceContainerID
    do
      serviceContainerIDs+=( "${serviceContainerID:$((stackname_len+servicename_len+2))}" )
    done < <(printf '%s\n' "$serviceContainerNames")
    local serviceContainerIDsStr=$( IFS=$'\n'; echo "${serviceContainerIDs[*]}" )

    COMPREPLY=( $( compgen -W '$serviceContainerIDsStr' $containerID ) )

  else

    if [ ! $words_len -eq 2 ]; then
      return
    fi
    COMPREPLY=( $( compgen -W '$cmdsStr' $cmd ) )
  fi
}

complete -F _stackd_completions stackd