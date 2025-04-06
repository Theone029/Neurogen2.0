# Auto-commit snapshot zip
os.system(f"git add context/{snapshot_name} && git commit -m \\"[snapshot] {version_tag}\\"")
