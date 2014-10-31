require 'json'
require 'hashie'

class JsonParser
  
  attr_accessor :data
  
  def initialize
    
  end
  
  def load_data(data)
    self.data = JSON.parse(data)
  end
  
  def data_contains_value? (key, value)
    keys = key.split("/")
    
    puts keys
    filtered_values = self.get_filtered_values(self.data, keys)
    puts filtered_values
    filtered_values.include? value
  end
  
  def get_filtered_values(data, keys)    
    values = []
    
    data.extend Hashie::Extensions::DeepFind
    data.deep_find_all(keys.shift).each do |subpart|
      if subpart.respond_to?(:each)
        values += get_filtered_values(subpart, keys)
      else
        values += [subpart]
      end
    end
    
    values
  end
end
