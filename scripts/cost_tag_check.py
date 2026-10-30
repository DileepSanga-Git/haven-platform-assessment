"""
B2, part 2 — implement the cost-tagging check.

Read fixtures/plan.json for the shape of a `terraform show -json` plan: a `resource_changes`
list, where each entry has a `type`, an `address`, and `change.after.tags`.

Implement check_plan() so it:
  - Looks at every resource being created or changed (skip anything not in
    change.actions, e.g. a pure "no-op" / "read" change).
  - Fails (returns a non-zero exit code) if the resource is missing the tag that identifies
    the real billing unit, per README.md's domain model — not whatever tag the resource
    happens to already carry.
  - Is idempotent: running this twice against the same plan file produces the same result,
    with no duplicate output and no flipped pass/fail.
  - Prints which specific resource address(es) are missing the tag.

Run manually: python scripts/cost_tag_check.py fixtures/plan.json
"""
import json
import sys


def check_plan(plan_path: str) -> int:
  with open(plan_path, encoding="utf-8") as file:
    plan = json.load(file)
  missing = set()
  for resource in plan.get("resource_changes",[]):
    change = resource.get("change") or {} 
    actions = change.get("actions") or []
    if not any(action in actions for action in ("create", "update")):
      continue
    after = change.get("after") or {}
    tags = after.get("tags") or {}
    if not isinstance(tags,dict) or not tags.get("landlord_account_id"):
      address = resource.get("address","<unkown resource>")
      missing.add(address)
  for address in sorted(missing):
    print (f"Missing landlord_account_id tag:{address}")
  return 1 if missing else 0         
if __name__ == "__main__":
  if len(sys.argv)!= 2:
    print(
      f"Usage: python{sys.argv[0]} PLAN_JSON",
      file=sys.stderr,
    )
    sys.exit(2)
  sys.exit(check_plan(sys.argv[1]))
