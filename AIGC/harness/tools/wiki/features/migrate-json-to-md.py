#!/usr/bin/env python3
"""
migrate-json-to-md.py — Feature JSON → MD 迁移工具

将 features/ 下的 *.json 文件转换为 YAML frontmatter + MD 正文格式。

用法：
  python3 aigc/harness/tools/wiki/features/migrate-json-to-md.py            # 预览
  python3 aigc/harness/tools/wiki/features/migrate-json-to-md.py --write    # 执行
  python3 aigc/harness/tools/wiki/features/migrate-json-to-md.py --single gpo/feiyu.json  # 单文件

依赖：PyYAML（pip install pyyaml）
"""

import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ 需要安装 PyYAML: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def find_features_dir():
    """查找 features 目录"""
    d = Path(__file__).resolve()
    for _ in range(10):
        d = d.parent
        if (d / 'aigc').is_dir():
            raw_dir = d / 'aigc' / 'wiki' / 'raw'
            # 直接路径
            if (raw_dir / 'features').is_dir():
                return raw_dir / 'features'
            # 子目录探测
            if raw_dir.exists():
                for child in raw_dir.iterdir():
                    if child.is_dir() and (child / 'features').is_dir():
                        return child / 'features'
    print("❌ 找不到 features 目录", file=sys.stderr)
    sys.exit(1)


def json_to_md(json_path: Path) -> str:
    """将单个 JSON 转换为 MD 格式"""
    with open(json_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # frontmatter
    fm = {
        'name': data.get('name', json_path.stem),
        'display_name': data.get('display_name', data.get('name', '')),
        'category': data.get('category', 'unknown'),
        'version': data.get('version', '1.0.0'),
        'dependencies': data.get('dependencies', []),
    }
    if data.get('uses'):
        fm['uses'] = data['uses']
    
    # YAML frontmatter
    yaml_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
    
    # 正文
    lines = []
    lines.append(f"# {fm['display_name']}")
    lines.append('')
    
    desc = data.get('description', '')
    if desc:
        lines.append(desc)
        lines.append('')
    
    # 文件清单
    files = data.get('files', {})
    
    code_files = files.get('code', [])
    if code_files:
        lines.append('## 代码文件')
        lines.append('')
        lines.append('| 路径 |')
        lines.append('|------|')
        for fp in code_files:
            lines.append(f'| `{fp}` |')
        lines.append('')
    
    config_files = files.get('config', [])
    if config_files:
        lines.append('## 配置文件')
        lines.append('')
        lines.append('| 路径 |')
        lines.append('|------|')
        for fp in config_files:
            lines.append(f'| `{fp}` |')
        lines.append('')
    
    asset_files = files.get('asset', [])
    if asset_files:
        lines.append('## 资源文件')
        lines.append('')
        lines.append('| 路径 |')
        lines.append('|------|')
        for fp in asset_files:
            lines.append(f'| `{fp}` |')
        lines.append('')
    
    template_files = files.get('template', [])
    if template_files:
        lines.append('## 模板文件')
        lines.append('')
        lines.append('| 路径 |')
        lines.append('|------|')
        for fp in template_files:
            lines.append(f'| `{fp}` |')
        lines.append('')
    
    # 场景
    scenes = data.get('scenes', [])
    if scenes:
        lines.append('## 场景')
        lines.append('')
        lines.append('| 路径 |')
        lines.append('|------|')
        for s in scenes:
            lines.append(f'| `{s}` |')
        lines.append('')
    
    # notes
    notes = data.get('notes', '')
    if notes:
        lines.append('## 备注')
        lines.append('')
        lines.append(notes)
        lines.append('')
    
    body = '\n'.join(lines)
    return f"---\n{yaml_str}\n---\n\n{body}"


def main():
    write = '--write' in sys.argv
    single = None
    if '--single' in sys.argv:
        idx = sys.argv.index('--single')
        if idx + 1 < len(sys.argv):
            single = sys.argv[idx + 1]
    
    features_dir = find_features_dir()
    skip = {'graph.json'}
    
    # 收集要转换的 JSON 文件
    if single:
        json_files = [features_dir / single]
    else:
        json_files = sorted(
            p for p in features_dir.rglob('*.json')
            if p.name not in skip
        )
    
    print(f"Features 目录: {features_dir}")
    print(f"待转换文件: {len(json_files)}")
    print()
    
    converted = 0
    for json_path in json_files:
        if not json_path.exists():
            print(f"  ⚠️ 不存在: {json_path}")
            continue
        
        md_path = json_path.with_suffix('.md')
        rel = json_path.relative_to(features_dir)
        
        try:
            md_content = json_to_md(json_path)
        except Exception as e:
            print(f"  ❌ 转换失败: {rel} — {e}")
            continue
        
        if write:
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            json_path.unlink()  # 删除原 JSON
            print(f"  ✅ {rel} → {md_path.name}")
        else:
            print(f"  📄 {rel} → {md_path.name}")
            if single:
                print()
                print(md_content)
        
        converted += 1
    
    print()
    if write:
        print(f"✅ 已转换 {converted} 个文件")
        print(f"💡 请运行 wiki-resolve.py --build 重建索引")
    else:
        print(f"📋 预览完成，{converted} 个文件待转换")
        print(f"💡 加 --write 执行转换")


if __name__ == "__main__":
    main()
