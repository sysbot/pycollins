import errors

def parse_response(response, options):
  do_raise = options['raise'] != False
  if options.include?(:expects) && ![options[:expects]].flatten.include?(response.code):
    handle_error(response) if do_raise
    if options.include?(:default):
      return options[:default]
    else
      raise UnexpectedResponseError.new("Expected code #{options[:expects]}, got #{response.code}")

  handle_error(response) if do_raise
  json = response.parsed_response
  if options.include?(:as):
    case options[:as]
    when :asset
      json = Collins::Asset.from_json(json)
    when :bare_asset
      json = Collins::Asset.from_json(json, true)
    when :data
      json = json["data"]
    when :status
      json = json["data"]["SUCCESS"]
    when :message
      json = json["data"]["MESSAGE"]
    when :paginated
      json = json["data"]["Data"]

  if block_given?:
    yield(json)
  else
    json
