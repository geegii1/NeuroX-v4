#!/bin/bash
set -e

echo "==> Pushing to GitHub..."
git push origin main

echo "==> Pulling on neurox-vm..."
ssh neurox-vm "cd ~/NeuroX && git pull"

echo "==> Restarting services..."
ssh neurox-vm "sudo systemctl restart neurox.service neurox-dashboard.service && systemctl status neurox.service neurox-dashboard.service --no-pager"

echo "==> Deploy complete."
