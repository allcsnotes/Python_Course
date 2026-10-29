FROM python:3.14-slim
RUN apt-get update -qq && apt-get install -y -qq git >/dev/null && rm -rf /var/lib/apt/lists/* \
 && git config --global --add safe.directory '*' \
 && pip install -q --root-user-action=ignore pytest==9.1.1 freezegun==1.5.5 hatchling==1.32.4 hatch-vcs==0.5.0
COPY entry.sh /entry.sh
ENTRYPOINT ["/entry.sh"]
