#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/../"

docker push stephane-klein/clean-gitlab-backup:latest