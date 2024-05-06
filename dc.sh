# Write docker-compose override
if [ ! -f "docker-compose.override.yml" ]; then
  cat <<EOF >> docker-compose.override.yml
version: "3.0"
EOF
fi

set -o allexport
source ./.env

# Run
if  [ "$DEBUG" == "1" ]
then
#   echo 'Development mode'
  docker-compose -f docker-compose.yml -f docker-compose.override.yml "$@"
else
#   echo 'Production mode'
  docker-compose -f docker-compose.yml -f docker-compose.override.yml "$@"
fi

set +o allexport