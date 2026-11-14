<!-- content-revision: 1; source: th -->
# 排查问题

missing：安装 doctor 指出的程序或修正 PATH。engine_version_mismatch：使用固定的完整版本号。

timeout/log_limit：查看 Evidence 日志，先修复卡住原因再提高限制。import_errors/missing_imports：检查导入日志并在工作树内重新导入。工具会重试，但不会自动删除缓存。

display_unavailable：使用图形会话。必需检查被跳过不代表通过。即使已打印通过摘要，SCRIPT ERROR 仍会失败。macOS 沙箱阻止编辑器设置时，应获取适当权限，而不是忽略错误。
