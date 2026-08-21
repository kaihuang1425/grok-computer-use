from __future__ import annotations
import argparse, json
from pathlib import Path

def score_trace(path: Path) -> dict:
    events=[]
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip(): events.append(json.loads(line))
    actions=sum(1 for e in events if e.get('event')=='action')
    verifs=[e for e in events if e.get('event')=='verification']
    passes=sum(bool(e.get('payload',{}).get('passed')) for e in verifs)
    return {
        'actions': actions,
        'verification_count': len(verifs),
        'verification_pass_rate': passes/len(verifs) if verifs else 0,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument('trace', type=Path)
    args=p.parse_args()
    print(json.dumps(score_trace(args.trace), indent=2))
