IN=$1

APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cat "$1"|$APP_DIR/IntensiveRL.py | sort  -rn |tee  "$1".rank
