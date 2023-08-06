import os


BIGQUERY_PROJECT = "beneath"
PYTHON_CLIENT_ID = "beneath-python"

MAX_READ_MB = 10
READ_BATCH_SIZE = 1000

DEV = os.environ.get('ENV') in ['dev', 'development']

if DEV:
  BENEATH_FRONTEND_HOST = "http://localhost:3000"
  BENEATH_CONTROL_HOST = "http://localhost:4000"
  BENEATH_GATEWAY_HOST = "http://localhost:5000"
  BENEATH_GATEWAY_HOST_GRPC = "localhost:50051"
else:
  BENEATH_FRONTEND_HOST = "https://beneath.network"
  BENEATH_CONTROL_HOST = "https://control.beneath.network"
  BENEATH_GATEWAY_HOST = "https://data.beneath.network"
  BENEATH_GATEWAY_HOST_GRPC = "grpc.data.beneath.network"


def read_secret():
  with open(_secret_file_path(), "r") as f:
    return f.read()


def write_secret(secret):
  with open(_secret_file_path(), "w") as f:
    return f.write(secret)


def _secret_file_path():
  name = "secret_dev.txt" if DEV else "secret.txt"
  return os.path.join(_config_dir(), name)


def _config_dir():
  p = os.path.expanduser("~/.beneath")
  if not os.path.exists(p):
    os.makedirs(p)
  return p
