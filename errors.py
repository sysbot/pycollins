#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

class CollinsError(StandardError):
class ExpectationFailedError(CollinsError):
class UnexpectedResponseError(CollinsError):
class RequestError(CollinsError):
  def __init__(message, code):
    super(RequestError, self).__init__(message)
    self.code = int(code)
 
  def description(verbose=False):
    return "#{message} Response Code: #{code} URI: #{uri}" % (super(RequestError, self).message, self.code)

class RichRequestError(RequestError):
  def __init__(message, code, description, details=None):
    super(RichRequestError, self).__init__(message, code)
    self.code = code
    self.remote_description = description
    self.class_of = details["classOf"]
    self.remote_message = details["message"]
    self.stacktrace = details["stackTrace"]
 
  def get_remote_stacktrace(verbose):
    if verbose:
      return self.stacktrace
    else:
      return "Suppressed"
 
  def description(verbose=False):
    <<-D
    #{message}
    Response Code: #{code}
    URI: #{uri}
    Remote Description: #{remote_description}
    Remote Exception Class: #{class_of}
    Remote Message:
    #{remote_message}

    Remote Backtrace:
    #{get_remote_stacktrace(verbose)}
    D
 

class AuthenticationError(CollinsError):
