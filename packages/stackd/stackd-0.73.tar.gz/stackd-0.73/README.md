# stackd

## Installation

```bash
sudo apt install -y python3 python3-pip httpie jq

pip --user install stackd --upgrade

sudo ln -s -f $(which completion-stackd.bash) /etc/bash_completion.d/stackd
source $(which completion-stackd.bash)
```

## Usage

```bash
cd /srv/traefik/
export STACKD_ENV=local,production

# default is current directory name
export STACKD_STACK_NAME=traefik

# default: docker-stack.yml
export STACKD_COMPOSE_FILE_BASE=docker-stack.yml

stackd up
```

## .env precedence
- .env.default (always in first, put it in your git repository)
- .env (create it relatively to host, put it in your gitignore)
- .env.*

The `*` can be anything defined in $ENV, you can define ENV in cli or in .env
the .env extra files can be from repository or created relatively to host.
You can add multiple extra env, by separating them with comma, precedence is defined by the order you provided.

### directory layout
```bash
$ tree /srv/traefik/
/srv/traefik/
  ├── docker-stack.local.yml
  ├── docker-stack.yml
  ├── .env
  ├── .env.default
  ├── .env.local
  ├── .env.production
  ├── .gitignore
```

## License
[MIT](https://choosealicense.com/licenses/mit/)