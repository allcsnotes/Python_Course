#!/bin/zsh
cd "${0:A:h}"
./apply.sh v5 >/dev/null
cp steps/vx/extras.py allcs/app/routers/extras.py
cat steps/vx/worker_add.py >> allcs/app/worker.py
python3 - <<'PY'
p='allcs/app/main.py'; s=open(p).read()
s=s.replace("    enrollments,\n    students,\n)","    enrollments,\n    extras,\n    students,\n)").replace("app.include_router(dashboard.router)","app.include_router(dashboard.router)\napp.include_router(extras.router)")
open(p,'w').write(s)
PY
(cd allcs && docker build -q -t m20l04-api:vx .)
