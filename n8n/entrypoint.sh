#!/bin/sh
set -e

MARKER=/home/node/.n8n/.provisioned

if [ ! -f "$MARKER" ]; then
  echo "Premier démarrage détecté : import des workflows..."
  n8n import:workflow --separate --input=/home/node/.n8n/provisioning/workflows
  n8n publish:workflow --id=0cVhNtyAr5iEaFqd
  n8n publish:workflow --id=ag5a1nzvgpaGQMvV
  n8n publish:workflow --id=DxBABB3a86Yjea8Y
  n8n publish:workflow --id=JivNpCgAEBoKFBYZ
  n8n publish:workflow --id=M00HQvdq8ymJxHXa
  n8n publish:workflow --id=O0XvkPntWdIiYNpN
  n8n publish:workflow --id=RikYRrHLBSVzc2Cq
  n8n publish:workflow --id=U7kJa25opKF9sU3c

  touch "$MARKER"
fi

exec n8n start
