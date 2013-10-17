# This class does nothing and ALWAYS returns False!!
class Null(object):
  # Null objects always and reliably "do nothing"
  def __init__(sefl, *args, **kwargs): pass
  def __call__(self, *args, **kwargs): return self
  def __repr__(sefl): return "Null()"
  def __nonzero__(self): return 0

  def __getattr__(self, name): return self
  def __setattr__(self, name, value): return self
  def __delattr__(self, name): return self