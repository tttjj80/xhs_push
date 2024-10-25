# 在linux上运行
# 获取脚本所在的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 切换到脚本所在的目录
cd "$SCRIPT_DIR"

#新建虚拟环境
python3 -m venv myenv

# 激活虚拟环境
source myenv/bin/activate

# 安装依赖
pip3 install -r requirements.txt

nohup python3 basic_sign_server.py > basic_sign_server_nohup.out 2>&1 &
nohup python3 main.py > main_nohup.out 2>&1 &
