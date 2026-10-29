#!/usr/bin/env bash
# Runs on the CI machine: sends one command to the server.
#   MODE=exec  rehearsal: docker exec into the local "server"
#   MODE=ssh   AWS: ssh, keys from EC2 Instance Connect
#   MODE=ssm   AWS: Run Command, no open port (if allowed)
set -euo pipefail
action="$*"
case "${MODE:-exec}" in
  exec)
    docker exec "${SERVER:-m19b13-server}" \
      bash /opt/allcs/deploy.sh $action ;;
  ssh)
    # port 22 is open to one address only (a /32 rule)
    ssh -o StrictHostKeyChecking=accept-new "ec2-user@$HOST" \
      sudo bash /opt/allcs/deploy.sh $action ;;
  ssm)
    params="$(printf '{"commands":["bash /opt/allcs/deploy.sh %s 2>&1"]}' "$action")"
    id="$(aws ssm send-command --region us-east-1 --instance-ids "$INSTANCE_ID" \
      --document-name AWS-RunShellScript --parameters "$params" \
      --query Command.CommandId --output text)"
    while :; do
      st="$(aws ssm get-command-invocation --region us-east-1 --command-id "$id" \
        --instance-id "$INSTANCE_ID" --query Status --output text 2>/dev/null || echo Pending)"
      case "$st" in InProgress|Pending|Delayed) sleep 3 ;; *) break ;; esac
    done
    aws ssm get-command-invocation --region us-east-1 --command-id "$id" \
      --instance-id "$INSTANCE_ID" --query StandardOutputContent --output text
    [ "$st" = Success ] ;;
esac
