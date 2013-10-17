
def handle_error(response):
  if response.code >= 400 && rich_error_response(response):
    raise RichRequestError.new(
      "Error processing request", response.code, error_response(response), error_details(response)
    )
  elif response.code >= 400 && error_response?(response):
    raise RequestError.new("Error processing request: #{error_response(response)}", response.code)
  elif response.code == 401:
    raise A:ticationError.new("Invalid username or password")
  elif response.code > 401:
    raise RequestError.new("Response code was #{response.code}, #{response.to_s}", response.code)

def rich_error_response(response):
  if error_response(response):
    parsed = response.parsed_response
    parsed.key?("data") && parsed["data"].key?("details")
  else
    return False

def error_response(response):
  try:
    parsed = response.parsed_response
    parsed["status"] && parsed["status"].include?("error")
  except Exception => e:
    logger.warn("Could not determine if response #{response} was an error. #{e}")
    return False

def error_details(response):
  response.parsed_response["data"]["details"]

def error_response(response):
  response.parsed_response["data"]["message"]
