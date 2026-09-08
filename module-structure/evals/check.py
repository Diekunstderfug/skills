#!/usr/bin/env python3
"""Validate routing cases; optionally score independently recorded observations."""
import argparse
import json
from pathlib import Path


def check(cases, observations=None):
    errors = []
    ids = [c['id'] for c in cases]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate case IDs')
    for c in cases:
        if c['route'] not in {'none', 'cohesion-locality', 'modularity-review'}:
            errors.append(f"{c['id']}: invalid initial route")
        if c['should_route'] != (c['route'] != 'none'):
            errors.append(f"{c['id']}: should_route conflicts with route")
        if c['expected']['route'] != c['route']:
            errors.append(f"{c['id']}: expected route conflicts with route")
        path = c['expected'].get('path')
        if path is not None and (path[0] if path else 'none') != c['route']:
            errors.append(f"{c['id']}: path conflicts with initial route")
    if observations is not None:
        observed_ids = [r['id'] for r in observations]
        if len(observed_ids) != len(set(observed_ids)):
            errors.append('Duplicate observation IDs')
        for extra in set(observed_ids) - set(ids):
            errors.append(f'{extra}: unknown observation')
        by_id = {r['id']: r for r in observations}
        for c in cases:
            row = by_id.get(c['id'])
            if row is None:
                errors.append(f"{c['id']}: missing observation")
                continue
            if not row.get('evidence'):
                errors.append(f"{c['id']}: missing transcript evidence")
            for key, value in c['expected'].items():
                actual = row.get('observed', {}).get(key)
                if type(actual) is not type(value) or actual != value:
                    errors.append(f"{c['id']}.{key}: expected {value!r}, got {actual!r}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path)
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name('routing-queries.json').read_text())
    observations = json.loads(args.results.read_text()) if args.results else None
    errors = check(cases, observations)
    for error in errors:
        print(error)
    label = 'Observation scoring' if args.results else 'Dataset validation (not a behavioral run)'
    print(f'{label}: {len(cases)} cases, {len(errors)} errors')
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
