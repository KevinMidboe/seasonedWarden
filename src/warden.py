from pprint import pprint

def acceptableSeedCount(torrent):
  return int(torrent.seed) > 1

def unacceptable4K(torrent):
  name = torrent.name.lower()
  return '2160p' in name or '4k' in name

def unacceptableSmall(torrent):
  cutoff = 6500000000 # 6.5 GB
  return torrent.bytes < cutoff

def unacceptableLarge(torrent):
  cutoff = 25000000000 # 25 GB
  return torrent.bytes > cutoff

def findBest(torrents):
  if len(torrents) == 0:
    return None

  startingLength = len(torrents)
  candidates = torrents.copy()

  for torrent in torrents:
    if not acceptableSeedCount(torrent):
      candidates.remove(torrent)
    elif unacceptable4K(torrent):
      candidates.remove(torrent)
    elif unacceptableSmall(torrent):
      candidates.remove(torrent)
    elif unacceptableLarge(torrent):
      candidates.remove(torrent)


  candidates = sorted(candidates, reverse=True)

  print('Found {} candidates from {} torrents'.format(len(candidates), startingLength))

  pprint(candidates)

  return candidates[0]