<!-- content-revision: 1; source: th -->
# TKR 与 HMP 的经验

TKR 使用 Godot 客户端与 TypeScript 服务端，HMP 使用 Godot 和无界面测试。这两个 SPACE8 LABS 游戏项目为此流程提供了经验。

让逻辑可测试、明确接口约定、避免多人同时修改共享文件、在玩家可见内容变更后检查渲染结果，并限制诊断日志大小。

此版本将进程运行器与 Godot 分离，并提供通用命令适配器。尚未证明 Unity/Unreal 支持或端到端 token 节省效果。测量限制见 benchmarks/protocol.md 与 results.json。
