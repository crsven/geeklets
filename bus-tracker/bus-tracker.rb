#!/usr/bin/ruby

require 'rubygems'
require 'typhoeus'
require 'nokogiri'

response = Typhoeus.get('http://www.nextbus.com/webkit/predsForStop.jsp?a=lametro&r=720&d=720_329_0&s=8385&standalone#_predictions')
html = Nokogiri::HTML(response.body)
full_prediction = html.css(".largePrediction").first.content
prediction = full_prediction.gsub(/(.*)(\(.+\))([0-9].+)(\(.+\))/,"\\1\\3")
puts prediction
