#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/../"

export DOCKER_BUILDKIT=1

docker build . -t stephane-klein/clean-gitlab-backup:latest