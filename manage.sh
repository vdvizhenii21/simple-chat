# . dc_dev.sh exec app python manage.py "$@"

# Check production mode
production=false

while getopts "p" flag
do
    case "${flag}" in
        p) production=true;;
    esac
done

shift $(($OPTIND - 1))

# Run
if "$production" != true; then
    ./dc.sh -p exec app python src/manage.py "$@"
else
    ./dc.sh exec app python src/manage.py "$@"
fi