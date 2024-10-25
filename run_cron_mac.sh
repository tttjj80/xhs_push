# 获取脚本所在的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 切换到脚本所在的目录
cd "$SCRIPT_DIR"

source myenv/bin/activate


caffeinate python3 basic_sign_server.py

caffeinate python3 main.py
