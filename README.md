neurogen/
├── README.md                  ← Your system manifesto & AI-readable docs (the playbook for genius)
├── core/                      ← The powerhouse: memory, tagging, and bot control logic
│   ├── bot.py                 ← Discord bot wizardry and command handling
│   ├── memory_store.py        ← MongoDB-backed memory engine—your external, versioned brain
│   ├── auto_tag.py            ← Automatic tagging to keep your data hyper-organized
│   ├── memory_synthesizer.py  ← Distills and assembles context from your memory vault
│   ├── distill.py             ← Purges redundancy and prevents hallucination with smart data distillation
│   ├── digest_cron.py         ← Cron-powered daily digest creation for non-stop progress logging
│   └── context_pipeline.py    ← The express lane for injecting context exactly where it’s needed
├── config/                    ← Your secure control center for environment settings
│   ├── settings.yaml          ← System configuration (readable by humans and AI alike)
│   └── env.template           ← A fortress for your sensitive tokens—no leaks allowed
├── scripts/                   ← CLI tools to deploy, prune, and back up your masterpiece
│   ├── deploy.sh              ← One-click deployment magic
│   ├── prune_docker.sh        ← Trim those Docker images to perfection
│   └── auto_backup.sh         ← Auto-commit and push changes, so you never lose a spark of genius
├── docker/                    ← Containerized build scripts for rock-solid deployment
│   ├── Dockerfile             ← Blueprint for creating your containerized brain
│   └── setup.sh               ← Automated Docker setup to get you running in no time
├── data/
│   ├── samples/               ← Public test data to simulate real-world scenarios
│   └── test_inputs/           ← Local dev inputs for rapid-fire debugging and iteration
├── logs/                      ← Daily logs capturing every step of your evolution
│   └── log-YYYY-MM-DD.md      ← Your daily chronicle of success (or near-misses)
├── requirements.txt           ← Lean, mean, and dependency-clean—no bloat here
└── .gitignore                 ← Keeps your repo pristine by blocking clutter
# NEUROGEN 2.0
# NeuroFusion
