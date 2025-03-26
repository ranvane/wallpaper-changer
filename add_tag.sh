echo  "设置Git代理"
# 设置http、https::
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy https://127.0.0.1:7897
# 设置socks:
git config --global http.proxy 'socks5://127.0.0.1:7897'
git config --global https.proxy 'socks5://127.0.0.1:7897'

# 从 VERSION 文件读取版本号
VERSION=$(cat VERSION)

# git添加tag
git tag -a v$VERSION -m "Version $VERSION"
git push origin v$VERSION

## 取消代理
echo  "取消Git代理"
git config --global --unset http.proxy
git config --global --unset https.proxy
echo "按任意键继续..."
read -n 1 -s
echo