#!/usr/bin/env bash

helm install \
  prometheus \
  prometheus \
  --repo https://prometheus-community.github.io/helm-charts \
  --version "27.31.0" \
  --values values.yml
