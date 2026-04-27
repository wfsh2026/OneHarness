# 项目 Wiki 健康检查规则

## 结论

项目 wiki 健康检查只确认入口可达、来源明确、边界正确和低 token 检索成立。

## 最小检查

- `{project_wiki_root}/INDEX.md` 存在。
- `INDEX.md` 只做路由，不复制正文。
- 可检索页面包含 `read_when`。
- 项目事实有来源文件、验证记录或用户确认。
- 项目 wiki 没有写入通用 AIGC。
- 默认读取不会展开大目录或历史运行记录。

## 异常内容

- 大段源码、日志、终端输出。
- 没有来源的稳定结论。
- 具体项目事实出现在通用 `AIGC/wiki`。
- 通用规则被复制到项目 wiki，而不是通过链接引用。
- 多个项目共享同一个项目 wiki。

## 处理

- 缺入口：执行 `project-wiki-bootstrap.md`。
- 缺来源：补 `source-map/` 或降级为开放问题。
- 信息过期：执行 `project-wiki-update.md`。
- 边界错误：移出错误位置，保留到正确 wiki 或运行记录。
