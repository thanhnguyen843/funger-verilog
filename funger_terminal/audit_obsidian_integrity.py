import os
import re

vault_root = r"D:\Obsidian"
funger_dir = r"D:\Obsidian\Funger"

def audit_obsidian():
    vault_targets = {}
    for root, dirs, files in os.walk(vault_root):
        for f in files:
            if f.endswith(".md"):
                stem = f[:-3]
                rel_vault = os.path.relpath(os.path.join(root, f), vault_root).replace("\\", "/")[:-3]
                rel_funger = os.path.relpath(os.path.join(root, f), funger_dir).replace("\\", "/")[:-3]
                vault_targets[stem] = f
                vault_targets[rel_vault] = f
                vault_targets[rel_funger] = f

    print(f"[*] Indexed {len(vault_targets)} valid target stems across vault.")

    broken_links = []
    fence_errors = []
    table_errors = []
    math_errors = []

    link_re = re.compile(r"\[\[(.*?)\]\]")

    for root, dirs, files in os.walk(funger_dir):
        for f in files:
            if not f.endswith(".md"):
                continue
            fp = os.path.join(root, f)
            rel_file = os.path.relpath(fp, funger_dir).replace("\\", "/")
            with open(fp, "r", encoding="utf-8") as fh:
                text = fh.read()
                lines = text.splitlines()

            # 1. Code Fences
            fences = [l for l in lines if l.strip().startswith("```")]
            if len(fences) % 2 != 0:
                fence_errors.append((rel_file, len(fences)))

            # 2. Wikilinks
            for match in link_re.findall(text):
                target = match.split("|")[0].strip().split("#")[0].strip().replace(".md", "")
                if not target:
                    continue
                base_target = os.path.basename(target)
                if target not in vault_targets and base_target not in vault_targets:
                    broken_links.append((rel_file, match, target))

            # 3. Table Column Alignment
            in_code = False
            for idx, line in enumerate(lines):
                s = line.strip()
                if s.startswith("```"):
                    in_code = not in_code
                    continue
                if in_code:
                    continue

                if s.startswith("|") and s.endswith("|"):
                    # Check divider lines |---|---|
                    if re.match(r"^\|(\s*:?-+:?\s*\|)+$", s):
                        cols = len(s.split("|")) - 2
                        # Check header above
                        if idx > 0 and lines[idx - 1].strip().startswith("|"):
                            prev_cols = len(lines[idx - 1].strip().split("|")) - 2
                            if cols != prev_cols:
                                table_errors.append((rel_file, idx + 1, f"Divider cols ({cols}) != Header cols ({prev_cols})"))

    print(f"[*] Audit Results:")
    print(f"    - Broken Wikilinks : {len(broken_links)}")
    print(f"    - Unbalanced Fences: {len(fence_errors)}")
    print(f"    - Table Col Errors : {len(table_errors)}")

    if broken_links:
        print("\n[!] Broken Links:")
        for r, m, t in broken_links:
            print(f"    {r} -> [[{m}]]")
    if fence_errors:
        print("\n[!] Unbalanced Code Fences:")
        for r, c in fence_errors:
            print(f"    {r} -> {c} fences")
    if table_errors:
        print("\n[!] Table Alignment Errors:")
        for r, l, m in table_errors:
            print(f"    {r} (Line {l}) -> {m}")

    if len(broken_links) == 0 and len(fence_errors) == 0 and len(table_errors) == 0:
        print("\n>>> ALL OBSIDIAN NOTES, TABLES & LINKS ARE 100% HEALTHY & VALID! <<<")
        return 0
    return 1

if __name__ == "__main__":
    exit(audit_obsidian())
