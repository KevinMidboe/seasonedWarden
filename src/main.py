from flask import Flask, request, jsonify
from types import SimpleNamespace
from dataclasses import dataclass
from typing import List
import json

from .warden import findBest

app = Flask(__name__)


@dataclass
class Torrent:
  name: str
  magnet: str
  uploader: str
  size: str
  date: str
  seed: int
  leech: str
  url: str
  release_type: List[str]

  @property
  def bytes(self):
    UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    [numStr, unit] = self.size.split(' ')

    if unit not in UNITS:
      return -1

    exponent = UNITS.index(unit) * 3
    return float(numStr) * pow(10, exponent)

  def __lt__(self, other):
    return self.bytes < other.bytes

  def __gt__(self, other):
    return self.bytes > other.bytes

  def __repr__(self):
    return 'Name: {}, size: {}'.format(self.name, self.size)

@app.route('/api/v1')
def index():
  return "Hello world"

@app.route('/api/v1/determine', methods=['POST'])
def determine():
  data = request.data
  torrents = []

  try:
    torrents = json.loads(data, object_hook=lambda d: Torrent(**d))
  except json.decoder.JSONDecodeError as error:
    return closeWithErrorAndCode('Some json error happened', 422, error)
  except TypeError as error:
    errorMessage = str(error)

    if 'required positional argument' in errorMessage:
      argument = errorMessage.split(': ')[-1]
      return closeWithErrorAndCode('Missing required argument: {}'.format(argument), 422)
    elif 'unexpected keyword argument' in errorMessage:
      argument = errorMessage.split('keyword argument ')[-1]
      return closeWithErrorAndCode('Found unexpected argument: {}'.format(argument), 422)
    return closeWithErrorAndCode('Unable to understand json data, got error.', 422, error)
  except:
    return closeWithErrorAndCode('Unexpected error occured, could not determine anything here.')

  if len(torrents) == 0:
    return closeWithErrorAndCode('Parsable but no torrents found, nothing to do.')

  luckyBoyBest = findBest(torrents)

  data = {
    'message': 'Found a lucky boy bby',
    'torrent': luckyBoyBest,
    'success': True
  }

  return data, 200


def closeWithSuccessAndMessage(message):
  data = {
    'message': message,
    'success': True,
  }

  return data, 200

def closeWithErrorAndCode(message=None, statusCode=500, error=None):
  data = {
    'message': message or 'Unexpected error occured.',
    'success': False
  }

  if error is not None:
    data['error'] = str(error)

  return data, statusCode