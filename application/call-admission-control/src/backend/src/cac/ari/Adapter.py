import ari

class AriAdapter:
  @staticmethod
  def connect(host, username, password):
    return ari.connect(host, username, password)
