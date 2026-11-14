<!-- content-revision: 1; source: th -->
# 开始使用 SPACE8 LABS harness

需要 Python 3.11+、Git、tools/ci/godot-version.txt 中指定的 Godot 版本，以及运行 TypeScript 示例所需的 Node 22.18+。面向 macOS/Linux；Windows 使用 WSL，原生 Windows 尚未验证。

在仓库根目录运行。预期 Godot 9/9、三个 TypeScript 测试以及当前工具测试通过。doctor 只检查可执行文件是否存在，不执行配置中的命令。请查看 Evidence 路径中的 JSON 结果。

初学者：修改一条 score 规则及其测试。独立开发者：使用简短任务说明与工作树。小团队：声明文件归属与依赖，并指定一名集成人员负责共享文件。

```sh
python3 tools/harness.py inspect
python3 tools/harness.py doctor
python3 tools/harness.py check
# Generic example, no Godot required:
python3 tools/harness.py --config examples/typescript/harness.json check
# Existing compatibility entry points:
tools/test.sh test_score
tools/shot.sh main shots/main.png
```
