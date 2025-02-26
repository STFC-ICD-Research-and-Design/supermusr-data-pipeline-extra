#!/usr/bin/env bash

helm install \
  prometheus \
  prometheus \
  --repo https://prometheus-community.github.io/helm-charts \
  --version "25.21.0" \
  --values values.yml
