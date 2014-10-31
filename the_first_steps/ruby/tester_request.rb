
class TesterRequest
  attr_accessor :response, :tests, :failures
  
  def initialize(response)
    self.response = response
    self.tests = 0
    self.failures = 0
  end
  
  def status_ok
    puts "\nTest #{self.tests + 1}: Status OK"
    
    if self.response.code == '200'
      puts "Success: Response code is 200"
      self.log_success
    else
      puts "! Fail:  Response code is #{self.response.code}"
      self.log_failure
    end    
  end
  
  def log_success
    self.tests += 1
  end

  def log_failure
    self.tests += 1
    self.failures += 1
  end
  
  def summary
    puts "\nTests summary:"
    puts "\tTests:\t#{self.tests}"
    puts "\tOK: \t#{self.tests - self.failures}"
    puts "\tFails:\t#{self.failures}\n\n"
  end
end
