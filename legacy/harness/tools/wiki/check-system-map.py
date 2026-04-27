#!/usr/bin/env python3
"""
check-system-map.py — System-map 实例清单同步检查 & 自动同步工具

从代码中提取 GPO/Mode/AB/AE/Weapon 实例，与 system-map.md §三 对比，
输出差异报告（新增/删除/数量不一致）。

用法：
  python3 aigc/harness/tools/wiki/check-system-map.py              # 检查差异
  python3 aigc/harness/tools/wiki/check-system-map.py --verbose     # 详细输出
  python3 aigc/harness/tools/wiki/check-system-map.py --sync        # 自动同步：新增插骨架行，删除标注 ⚠️

依赖：无（纯 Python 标准库）
"""

import os
import re
import sys
from pathlib import Path


def find_project_root():
    d = Path(__file__).resolve()
    for _ in range(10):
        d = d.parent
        if (d / 'aigc').is_dir() and (d / 'Assets').is_dir():
            return d
    print("❌ 找不到项目根目录", file=sys.stderr)
    sys.exit(1)


# ═══════════════════════════════════════════════════════════
# 从代码中提取实例
# ═══════════════════════════════════════════════════════════

def extract_modes(root: Path) -> list[str]:
    """从 ModeData.cs 的 ModeEnum 提取所有模式名"""
    mode_file = root / "Assets/Scripts/Data/ModeData.cs"
    if not mode_file.exists():
        return []
    content = mode_file.read_text(encoding="utf-8")
    # 提取 enum ModeEnum { ... } 中的值
    m = re.search(r'enum\s+ModeEnum\s*\{([^}]+)\}', content, re.DOTALL)
    if not m:
        return []
    enum_body = m.group(1)
    modes = []
    for line in enum_body.split('\n'):
        line = line.strip()
        if line.startswith('//') or not line or line.startswith('None'):
            continue
        # 去掉 #if UGC / #endif
        if line.startswith('#'):
            continue
        # 匹配枚举值名
        em = re.match(r'(Mode\w+)', line)
        if em:
            name = em.group(1)
            if name not in ('ModeOver', 'ModeError'):
                modes.append(name)
    return sorted(modes)


def extract_gpo(root: Path) -> list[str]:
    """从 ServerAIWorld_Switch.cs 提取 GPO case 分支"""
    switch_file = root / "Assets/Scripts/GamePlay/Server/AI/Components/ServerAIWorld_Switch.cs"
    if not switch_file.exists():
        return []
    content = switch_file.read_text(encoding="utf-8")
    gpos = re.findall(r'case\s+GpoTypeSet\.(Id_\w+)', content)
    return sorted(set(gpos))


def extract_gpo_detail(root: Path) -> dict[str, dict]:
    """提取 GPO 详细信息：{Id_Xxx: {server: ..., client: ...}}"""
    result = {}
    # Server
    server_file = root / "Assets/Scripts/GamePlay/Server/AI/Components/ServerAIWorld_Switch.cs"
    if server_file.exists():
        content = server_file.read_text(encoding="utf-8")
        for m in re.finditer(
            r'case\s+GpoTypeSet\.(Id_\w+):\s*\n\s*system\s*=\s*\w+\.AddSystem<(\w+)>',
            content
        ):
            gpo_id = m.group(1)
            if gpo_id not in result:
                result[gpo_id] = {'server': '', 'client': ''}
            result[gpo_id]['server'] = m.group(2)
    # Client
    client_file = root / "Assets/Scripts/GamePlay/Client/AI/Component/ClientAIWorld_Switch.cs"
    if client_file.exists():
        content = client_file.read_text(encoding="utf-8")
        for m in re.finditer(
            r'case\s+GpoTypeSet\.(Id_\w+):\s*\n\s*system\s*=\s*\w+\.AddSystem<(\w+)>',
            content
        ):
            gpo_id = m.group(1)
            if gpo_id not in result:
                result[gpo_id] = {'server': '', 'client': ''}
            result[gpo_id]['client'] = m.group(2)
    return result


def extract_ugc_gpo(root: Path) -> list[str]:
    """从 GpoTypeSet_UGC.cs 提取 UGC GPO ID"""
    ugc_file = root / "Assets/Scripts/UGC/Template/gpo/GpoTypeSet_UGC.cs"
    if not ugc_file.exists():
        return []
    content = ugc_file.read_text(encoding="utf-8")
    ids = re.findall(r'public\s+const\s+int\s+(Id_\w+)', content)
    return sorted(set(ids))


def extract_ab(root: Path) -> list[str]:
    """从 ServerAbilityManager_SwitchAB.cs 提取 AB 名称"""
    switch_file = root / "Assets/Scripts/GamePlay/Server/Ability/ServerAbilityManager_SwitchAB.cs"
    if not switch_file.exists():
        return []
    content = switch_file.read_text(encoding="utf-8")
    abs_ = re.findall(r'case\s+(AbilityM_\w+)\.AbilityTypeID', content)
    return sorted(set(abs_))


def extract_ae(root: Path) -> list[str]:
    """从 ServerAbilityManager_SwitchAE.cs 提取 AE 名称"""
    switch_file = root / "Assets/Scripts/GamePlay/Server/Ability/ServerAbilityManager_SwitchAE.cs"
    if not switch_file.exists():
        return []
    content = switch_file.read_text(encoding="utf-8")
    aes = re.findall(r'case\s+(AbilityM_\w+)\.AbilityTypeID', content)
    return sorted(set(aes))


def extract_weapons(root: Path) -> list[str]:
    """从 ServerWeaponManager.cs 提取专属武器"""
    switch_file = root / "Assets/Scripts/GamePlay/Server/Weapon/ServerWeaponManager.cs"
    if not switch_file.exists():
        return []
    content = switch_file.read_text(encoding="utf-8")
    weapons = re.findall(r'case\s+\w+\.(Id_\w+)', content)
    return sorted(set(weapons))


# ═══════════════════════════════════════════════════════════
# 从 system-map.md 解析现有表格
# ═══════════════════════════════════════════════════════════

def parse_system_map_section(content: str, section_name: str, pattern: str) -> list[str]:
    """从 system-map.md 的指定章节解析表格中的标识符"""
    # 找到章节开始
    section_start = content.find(section_name)
    if section_start == -1:
        return []
    # 找到下一个 ### 或 --- 结束
    section_end = len(content)
    for marker in ['### §', '---']:
        pos = content.find(marker, section_start + len(section_name))
        if pos != -1 and pos < section_end:
            section_end = pos
    section_text = content[section_start:section_end]
    return re.findall(pattern, section_text)


def parse_system_map(root: Path) -> dict:
    """解析 system-map.md 中的实例清单"""
    sm_file = root / "aigc/wiki/knowledge/system-map.md"
    if not sm_file.exists():
        return {}
    content = sm_file.read_text(encoding="utf-8")
    
    result = {}
    
    # 用 ### 标题定位各章节（支持 §9.X / 6.X / 3.X 多种编号）
    section_positions = {}
    for m in re.finditer(r'### (?:§9|6|3)\.(\d)', content):
        section_positions[f'{m.group(1)}'] = m.start()
    
    def get_section(start_key, end_key=None):
        start = section_positions.get(start_key, -1)
        if start == -1:
            return ''
        if end_key and end_key in section_positions:
            end = section_positions[end_key]
        else:
            end = len(content)
        return content[start:end]
    
    # §6.1 / §9.1 游戏模式
    mode_section = get_section('1', '2')
    modes = re.findall(r'\|\s*`(Mode\w+)`', mode_section)
    modes = [m for m in modes if not m.startswith('ModeData')]
    result['modes'] = sorted(set(modes))
    
    # §6.3 / §9.3 GPO
    gpo_section = get_section('3', '4')
    gpos = re.findall(r'\|\s*`(Id_\w+)`', gpo_section)
    result['gpo'] = sorted(set(gpos))
    
    # §6.4 / §9.4 AB
    ab_section = get_section('4', '5')
    abs_ = re.findall(r'\|\s*`(AbilityM_\w+)`', ab_section)
    result['ab'] = sorted(set(abs_))
    
    # §6.5 / §9.5 AE
    ae_section = get_section('5')
    aes = re.findall(r'\|\s*`(AbilityM_\w+)`', ae_section)
    result['ae'] = sorted(set(aes))
    
    return result


# ═══════════════════════════════════════════════════════════
# 差异报告
# ═══════════════════════════════════════════════════════════

def diff_lists(name: str, code_list: list, map_list: list, verbose: bool = False) -> tuple[int, set, set]:
    """对比两个列表，输出差异，返回 (差异数, 新增集合, 删除集合)"""
    code_set = set(code_list)
    map_set = set(map_list)
    
    added = code_set - map_set  # 代码有但 map 没有
    removed = map_set - code_set  # map 有但代码没有
    
    if not added and not removed:
        print(f"  ✅ {name}：代码 {len(code_list)} ↔ system-map {len(map_list)} — 一致")
        if verbose:
            for item in sorted(code_list):
                print(f"     · {item}")
        return 0, set(), set()
    else:
        diff_count = len(added) + len(removed)
        print(f"  ⚠️  {name}：代码 {len(code_list)} ↔ system-map {len(map_list)} — 差异 {diff_count}")
        if added:
            print(f"     🆕 代码新增（system-map 缺少）:")
            for item in sorted(added):
                print(f"        + {item}")
        if removed:
            print(f"     🗑️  system-map 多余（代码中不存在）:")
            for item in sorted(removed):
                print(f"        - {item}")
        return diff_count, added, removed


# ═══════════════════════════════════════════════════════════
# --sync：自动同步 system-map.md
# ═══════════════════════════════════════════════════════════

def kebab(name: str, prefix: str = '') -> str:
    """PascalCase / snake_case → kebab-case，可选前缀"""
    # Id_Hero10MechanicalArm → hero10-mechanical-arm
    # AbilityM_Hero10Dash → hero10-dash
    s = name.replace('Id_', '').replace('AbilityM_', '')
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', s)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', s)
    k = s.lower().replace('_', '-')
    return f'{prefix}{k}' if prefix else k


def sync_system_map(root: Path,
                    gpo_added: set, gpo_removed: set, gpo_detail: dict,
                    ab_added: set, ab_removed: set,
                    ae_added: set, ae_removed: set):
    """自动往 system-map.md §三 插入/标注行"""
    sm_file = root / "aigc/wiki/knowledge/system-map.md"
    content = sm_file.read_text(encoding="utf-8")
    lines = content.split('\n')
    changes = 0

    # ── GPO 新增：在 UGC 行之前（或章节末尾）插入 ──
    if gpo_added:
        # 找到 §3.3 GPO 表格的最后一行（UGC 行之前）
        insert_idx = None
        ugc_idx = None
        gpo_section_start = None
        for i, line in enumerate(lines):
            if '### 3.3' in line or '§3.3' in line or '§9.3' in line:
                gpo_section_start = i
            if gpo_section_start and '`Id_UGC' in line:
                ugc_idx = i
                break
        # 找 UGC 之前的最后一个 | 行
        if ugc_idx:
            insert_idx = ugc_idx
        elif gpo_section_start:
            # 没有 UGC 行，找表格末尾
            for i in range(len(lines) - 1, gpo_section_start, -1):
                if lines[i].startswith('|') and '`Id_' in lines[i]:
                    insert_idx = i + 1
                    break
        if insert_idx:
            new_lines = []
            for gpo_id in sorted(gpo_added):
                detail = gpo_detail.get(gpo_id, {})
                server = detail.get('server', '❓')
                client = detail.get('client', '❓')
                feat = kebab(gpo_id)
                new_lines.append(
                    f'| `{gpo_id}` | `{server}` | `{client}` '
                    f'| ⚠️ TODO | ⚠️ TODO | [[{feat}]] |'
                )
            for nl in reversed(new_lines):
                lines.insert(insert_idx, nl)
            changes += len(new_lines)

    # ── GPO 删除：标注 ⚠️ REMOVED（排除 UGC 条件编译项）──
    non_ugc_removed = {g for g in gpo_removed if 'UGC' not in g}
    if non_ugc_removed:
        for i, line in enumerate(lines):
            for gpo_id in non_ugc_removed:
                if f'`{gpo_id}`' in line and '⚠️ REMOVED' not in line:
                    lines[i] = line.rstrip() + ' ⚠️ REMOVED |'
                    changes += 1

    # ── AB 新增：在表格末尾插入 ──
    if ab_added:
        insert_idx = None
        ab_section_start = None
        for i, line in enumerate(lines):
            if '### 3.4' in line or '§3.4' in line or '§9.4' in line:
                ab_section_start = i
        if ab_section_start:
            for i in range(len(lines) - 1, ab_section_start, -1):
                if lines[i].startswith('|') and '`AbilityM_' in lines[i]:
                    insert_idx = i + 1
                    break
        if insert_idx:
            new_lines = []
            for ab_name in sorted(ab_added):
                feat = kebab(ab_name, prefix='ab-')
                new_lines.append(
                    f'| `{ab_name}` | ⚠️ TODO | [[{feat}]] |'
                )
            for nl in reversed(new_lines):
                lines.insert(insert_idx, nl)
            changes += len(new_lines)

    # ── AB 删除：标注 ──
    if ab_removed:
        for i, line in enumerate(lines):
            for ab_name in ab_removed:
                if f'`{ab_name}`' in line and '⚠️ REMOVED' not in line:
                    lines[i] = line.rstrip() + ' ⚠️ REMOVED |'
                    changes += 1

    # ── AE 新增：在表格末尾插入 ──
    if ae_added:
        insert_idx = None
        ae_section_start = None
        for i, line in enumerate(lines):
            if '### 3.5' in line or '§3.5' in line or '§9.5' in line:
                ae_section_start = i
        if ae_section_start:
            for i in range(len(lines) - 1, ae_section_start, -1):
                if lines[i].startswith('|') and '`AbilityM_' in lines[i]:
                    insert_idx = i + 1
                    break
        if insert_idx:
            new_lines = []
            for ae_name in sorted(ae_added):
                feat = kebab(ae_name, prefix='ae-')
                new_lines.append(
                    f'| `{ae_name}` | ⚠️ TODO | [[{feat}]] |'
                )
            for nl in reversed(new_lines):
                lines.insert(insert_idx, nl)
            changes += len(new_lines)

    # ── AE 删除：标注 ──
    if ae_removed:
        for i, line in enumerate(lines):
            for ae_name in ae_removed:
                if f'`{ae_name}`' in line and '⚠️ REMOVED' not in line:
                    lines[i] = line.rstrip() + ' ⚠️ REMOVED |'
                    changes += 1

    # ── 更新数量统计 ──
    # 重新计算各章节表格行数
    new_content = '\n'.join(lines)
    gpo_count = len(re.findall(r'\|\s*`Id_\w+`', new_content))
    ab_count = len(re.findall(r'\|\s*`AbilityM_\w+`.*\|\s*\[\[ab-', new_content))
    ae_count = len(re.findall(r'\|\s*`AbilityM_\w+`.*\|\s*\[\[ae-', new_content))

    # 更新清单数量行
    for i, line in enumerate(lines):
        if 'GPO 功能' in line and '§3.3' in line or 'gpo-功能清单' in line:
            lines[i] = re.sub(r'\d+ 种', f'{gpo_count} 种', line)
        if 'AB 功能' in line and '§3.4' in line or 'ab-功能清单' in line:
            lines[i] = re.sub(r'\d+ 种', f'{ab_count} 种', line)
        if 'AE 功能' in line and '§3.5' in line or 'ae-功能清单' in line:
            lines[i] = re.sub(r'\d+ 种', f'{ae_count} 种', line)

    if changes > 0:
        sm_file.write_text('\n'.join(lines), encoding='utf-8')
        print(f"\n  📝 已写入 system-map.md（{changes} 处变更）")
        print(f"     ⚠️  标记 TODO 的行需要 AI 补充：描述、类型、feature wiki-link")
    else:
        print(f"\n  ✅ system-map.md 无需变更")

    return changes


def main():
    verbose = "--verbose" in sys.argv
    sync = "--sync" in sys.argv
    
    root = find_project_root()
    
    print()
    print("═══════════════════════════════════════════════════════════")
    print("  System-map 实例清单同步检查")
    print(f"  项目: {root.name}")
    if sync:
        print("  模式: --sync（自动同步）")
    print("═══════════════════════════════════════════════════════════")
    print()
    
    # 从代码提取
    code_modes = extract_modes(root)
    code_gpo = extract_gpo(root)
    code_ugc_gpo = extract_ugc_gpo(root)
    code_ab = extract_ab(root)
    code_ae = extract_ae(root)
    gpo_detail = extract_gpo_detail(root) if sync else {}
    
    # 合并 GPO（PGC + UGC）
    all_gpo = sorted(set(code_gpo + code_ugc_gpo))
    
    # 从 system-map 解析
    sm = parse_system_map(root)
    
    total_diff = 0
    
    print("【§3.1 游戏模式】")
    d, _, _ = diff_lists("游戏模式", code_modes, sm.get('modes', []), verbose)
    total_diff += d
    print()
    
    print("【§3.3 GPO 功能】")
    d, gpo_added, gpo_removed = diff_lists("GPO", all_gpo, sm.get('gpo', []), verbose)
    total_diff += d
    print()
    
    print("【§3.4 AB 功能】")
    d, ab_added, ab_removed = diff_lists("AB", code_ab, sm.get('ab', []), verbose)
    total_diff += d
    print()
    
    print("【§3.5 AE 功能】")
    d, ae_added, ae_removed = diff_lists("AE", code_ae, sm.get('ae', []), verbose)
    total_diff += d
    print()
    
    # 汇总
    print("═══════════════════════════════════════════════════════════")
    if total_diff == 0:
        print(f"  ✅ 全部一致（Mode:{len(code_modes)} GPO:{len(all_gpo)} AB:{len(code_ab)} AE:{len(code_ae)}）")
    else:
        print(f"  ⚠️  发现 {total_diff} 处差异")
    print("═══════════════════════════════════════════════════════════")
    
    # --sync 自动写入
    if sync and total_diff > 0:
        # Mode 不自动同步（结构不同，频率极低）
        sync_changes = sync_system_map(
            root,
            gpo_added, gpo_removed, gpo_detail,
            ab_added, ab_removed,
            ae_added, ae_removed,
        )
    
    print()
    
    # 自动日志
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from wiki_log import append_wiki_log
        action = "sync" if sync else "lint"
        append_wiki_log(action, "system-map 同步检查",
                        f"Mode:{len(code_modes)} GPO:{len(all_gpo)} AB:{len(code_ab)} AE:{len(code_ae)}，差异:{total_diff}")
    except Exception:
        pass
    
    sys.exit(1 if total_diff > 0 and not sync else 0)


if __name__ == "__main__":
    main()
