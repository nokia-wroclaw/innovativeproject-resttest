Dir["../lib/*.rb"].each {|file| require file }

require 'test/unit'

class RestTest < Test::Unit::TestCase
  def test_xml
    parser = XmlParser.new
    reader = RestReader.new
    params = {
      :postalcode => '50316',
      :username => 'indor'
    }

    reader.send_get_request("http://api.geonames.org/postalCodeSearch", params)
    
    data = reader.get_response_body
    parser.load_data(data)
    
    key = "geonames/code/name"
    
    result = parser.data_contains_value?(key, "Wrocław")    
    assert_equal(true, result)
    
    result2 = parser.data_contains_value?(key, "Żyrardów")    
    assert_equal(false, result2)
  end
  
  def test_json
    parser = JsonParser.new
    reader = RestReader.new
    params = {
      :postalcode => '50316',
      :username => 'indor'
    }

    reader.send_get_request("http://api.geonames.org/postalCodeLookupJSON", params)
    
    data = reader.get_response_body
    parser.load_data(data)
    
    key = "postalcodes/placeName"
    
    result = parser.data_contains_value?(key, "Wrocław")    
    assert_equal(true, result)
    
    result2 = parser.data_contains_value?(key, "Żyrardów")    
    assert_equal(false, result2)
  end
end
