class Logger():
  def __init__(self) -> None:
      raise NotImplementedError
      
  def configure(self):
      raise NotImplementedError
      
  def send_logs(self):
      raise NotImplementedError
      
  def set_bed(self, bed):
      raise NotImplementedError
      
  def set_pollrate(self):
      pass
    
