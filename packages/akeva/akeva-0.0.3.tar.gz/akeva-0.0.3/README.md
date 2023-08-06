A GCP Secrets Manager Connector library.

In order to update library in PyPI, we must update the version in `setup.py` and `git push`.

Enviromental variables:
* `GCS_SECRET_MANAGEMENT_HOST` - Can be the name of the ClusterIP of the secret manager in Kubernetes 
* `GCS_SECRET_MANAGEMENT_PORT` - The port of the secret manager