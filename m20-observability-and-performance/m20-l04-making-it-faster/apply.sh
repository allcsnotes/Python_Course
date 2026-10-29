#!/bin/zsh
# usage: apply.sh vN  -> copies step N into allcs and builds image m20l04-api:vN
cd "${0:A:h}"; V=$1
find allcs/migrations/versions -name 'a7c3e1f09b52*' -delete
cp steps/v0/models.py allcs/app/models.py; cp steps/v0/main.py allcs/app/main.py; cp steps/v0/worker.py allcs/app/worker.py; rm -f allcs/app/routers/extras.py; cp steps/v0/enrollments.py allcs/app/routers/enrollments.py
cp steps/$V/dashboard.py allcs/app/routers/dashboard.py
if [[ $V == v2 || $V == v3 || $V == v4 || $V == v5 ]]; then cp steps/v2/models.py allcs/app/models.py; cp steps/v2/migrations/*.py allcs/migrations/versions/; fi
[[ -f steps/$V/enrollments.py ]] && cp steps/$V/enrollments.py allcs/app/routers/enrollments.py
(cd allcs && docker build -q -t m20l04-api:$V . )
