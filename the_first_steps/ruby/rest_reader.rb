require 'net/http'
require 'json'

class RestReader
  
  attr_accessor :response
  
  def initialize
    
  end
  
  def send_get_request(url, params = [])
    i = 0
    params.each do |name, param|
      if i == 0
        url += "?"
      else
        url += "&"
      end
      url += "#{name}=#{param}&"
      i += 1
    end
    
    uri = URI(url)
    self.response = Net::HTTP.get_response(uri)   
  end
  
  def send_post_request(url, params)
    uri = URI(url)
    http = Net::HTTP.new(uri.host, uri.port)
    #http.use_ssl = true

    request = Net::HTTP::Post.new(uri.path, {'Content-Type' =>'application/json'})
    # request.basic_auth 'user', 'pass'
    request.body = params.to_json

    self.response = http.request(request)    
  end
  
  def get_response_headers
    self.response.to_hash
  end
  
  def get_response_body
    self.response.body
  end
end
