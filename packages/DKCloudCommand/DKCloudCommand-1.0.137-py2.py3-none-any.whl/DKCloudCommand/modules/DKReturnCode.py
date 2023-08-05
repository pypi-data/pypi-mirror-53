import six


# coalesce all errors from using the DataKitchen API into one simple structure
class DKReturnCode:
    _DK_STATUS = 'status'  # dictionary key
    _DK_MESSAGE = 'message'  # dictionary key
    _DK_PAYLOAD = 'payload'  # dictionary key
    DK_SUCCESS = 'success'  # value
    DK_FAIL = 'fail'  # value

    def __init__(self):
        self.rc = dict()
        self.rc[self._DK_STATUS] = None
        self.rc[self._DK_MESSAGE] = None
        self.rc[self._DK_PAYLOAD] = None

    def set(self, status, message, payload=None):
        if status != self.DK_SUCCESS and status != self.DK_FAIL:
            raise ValueError('DKReturnCode.set() invalid value for status: %s' % status)
        self.rc[self._DK_STATUS] = status
        self.rc[self._DK_MESSAGE] = message
        self.rc[self._DK_PAYLOAD] = payload

    def ok(self):
        if self.rc[self._DK_STATUS] == self.DK_SUCCESS:
            return True
        else:
            return False

    def get_message(self):
        if self.rc[self._DK_MESSAGE] is None:
            return ''
        else:
            return self.rc[self._DK_MESSAGE]

    def get_payload(self):
        return self.rc[self._DK_PAYLOAD]

    def set_message(self, msg):
        self.rc[self._DK_MESSAGE] = msg

    def __str__(self):
        return "DKReturnCode {status: %s,\n message: %s,\n payload: %s}" % (
            self.rc[self._DK_STATUS], self.rc[self._DK_MESSAGE], self.rc[self._DK_PAYLOAD]
        )


# wrap the error returned from the DataKitchen API
class DKAPIReturnCode:

    def __init__(self, rdict, response=None):
        if isinstance(rdict, dict) is True and 'message' in rdict:
            self.rd = rdict
        else:
            self.rd = None
        self.response = response

    # put all the logic here to dig out the error message from the API call
    def get_message(self):
        # got an rdict, look in there
        if self.rd is not None and isinstance(self.rd, dict):
            if 'message' in self.rd:
                contents = self.rd['message']
                if isinstance(contents, dict) and 'error' in contents:
                    ret = contents['error']
                    if 'issues' in contents:
                        if contents['issues'] is not None:
                            for issue in contents['issues']:
                                issueMessage = '\n%s - %s - %s' % (
                                    issue['severity'], issue['file'], issue['description']
                                )
                                ret += issueMessage
                    return ret
                elif isinstance(contents, six.string_types):
                    return contents
                else:
                    return 'TODO: figure out this case'
        # no rdict, just have the HTTP response
        if self.response is not None:
            if isinstance(self.response.text, six.string_types):
                return self.response.text
        return ''


'''
The rdict varies.  Here are some examples

{
u'status': 500,
u'message': u'Internal Server Error'
}

{
  u'message': {
    u'status': u'failed',
    u'error': u'unable to delete a branched-from-base-test-kitchen_ut_gil kitchen '
  }
}
'''
