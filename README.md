# Personal Playbox: AI Coach

A terminal coach that remembers you between sessions.

```
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python -m coach.main
```

Memory (profile, goals, commitments, session notes) lives in `data/memory.json`
(git-ignored). Edit it by hand any time. Tune the personality in `coach/prompt.py`.
