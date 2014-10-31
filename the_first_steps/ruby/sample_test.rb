require_relative 'tester.rb'

response = Tester.get "http://www.wp.pl"
response.status_ok
response.summary

response2 = Tester.get "http://api.geonames.org/postalCodeSearch", {"postalcode" => '50316', "username" => 'indor'}
response2.status_ok
response2.summary

response3 = Tester.get "http://api.geonames.org/wrongAddress", {"postalcode" => '50316', "username" => 'indor'}
response3.status_ok
response3.summary
