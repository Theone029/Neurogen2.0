# � NEUROGEN Upgrade Tracker
_A living log of module status, known weak points, and upgrade targets._

## ��� Snapshot: 2025-03-23

| Module                | Status       | Known Weak Points                                   | Upgrade Candidates                                   |
|-----------------------|--------------|-----------------------------------------------------|------------------------------------------------------|
| `memory_store.py`     | ��✅ Working   | No schema enforcement, basic indexing only          | Add validation, indexed queries, version tagging     |
| `auto_tag.py`         | ✅ Working   | Heuristic only, lacks semantic depth                | Swap in GPT tagging or keyword embedding model       |
| `memory_synthesizer.py`| ✅ Working  | Relies only on tags, no semantic query matching     | Add similarity vector lookup                         |
| `digest_cron.py`      | ✅ Working   | Uses placeholder summaries                          | Use actual AI-generated chat logs + summarization    |
| `distill.py`          | ✅ Working   | Basic compression                                   | Upgrade to LLM distillation or token-aware pruning   |

---

## � Protocol:
- Update this file **every time** a module is modified or upgraded.
- When tagging a release (`v1.1`, etc), snapshot this table.
- NEUROGEN agents can parse this file for recursive evolution planning.

