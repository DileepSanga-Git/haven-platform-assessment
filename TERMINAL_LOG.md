git status
git diff
terraform -chdir=terraform plan -refresh=false
python -m pytest -v
python scripts/cost_tag_check.py fixtures/plan.json