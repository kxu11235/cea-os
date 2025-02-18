class Logger():
  def __init__(self) -> None:
      raise NotImplementedError
      
  def set_refresh_rate(self): #set refresh rate of data logging
      raise NotImplementedError
      
  def send_logs(self):  #send logs to database using client established by Connection object
      raise NotImplementedError
      
  def set_sensor(self): #set a sensor that is being logged
      raise NotImplementedError
      
  def get_sensor(self):  #returns sensor that is being logged
      raise NotImplementedError
    
