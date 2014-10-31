require_relative 'rest_reader.rb'
require_relative 'tester_request.rb'

class Tester
  def initialize
    
  end
  
  def self.get(url, params = [])
    puts "\n\n*** Testing #{url} ***"
    
    rest_reader = RestReader.new
    rest_reader.send_get_request(url, params)
    
    return TesterRequest.new(rest_reader.response)
  end
end
