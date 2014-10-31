require 'rexml/document'

class XmlParser
  
  attr_accessor :data
  
  def initialize
    
  end
  
  def load_data(input)
    self.data = REXML::Document.new(input)
  end
  
  def data_contains_value? (key, value)
    self.data.elements.each(key) do |ele|
       return true if ele.text == value.to_s
    end
    return false
  end
end
