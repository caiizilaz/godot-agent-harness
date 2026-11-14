<!-- content-revision: 1; source: th -->
# 接入现有项目

先创建独立分支或工作树并记录原有检查结果，不覆盖项目的 AGENTS.md。

参考 examples/typescript/harness.json 在项目根目录创建 harness.json，将 argv 设为已有的 test/lint/build 命令，将 cwd 设为项目内部目录。调用本工具仓库的 tools/harness.py，并传入 --config /absolute/project/harness.json。

预演：先执行 inspect 和 doctor，再用 check 执行真实命令。无需移动游戏文件或修改旧命令。回退时只删除新增的 harness.json，并恢复使用旧命令；不要删除无关文件或用户缓存。
