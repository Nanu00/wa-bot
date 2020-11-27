import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

# Uses the untangle lib to make the walpha api's xml output into a python object
# NOT ANYMORE!!! we're using ET now

class WaResponse:

    parsedURL = {       # Dictionary used to construct the final URL
            'scheme'  : 'http',
            'netloc'  : 'api.wolframalpha.com',
            'path'    : '/v2/query',
            'params'  : '',
            'query'   : '',
            'fragment': ''
            }
    callURL = ''        #Final URL variable, print this to see the xml file for debugging
    params = {}         #Parameters to be passed to the api

    def __init__(self, api_key):
        self.params['appid'] = api_key  # Gets the api key

#    def getInput(self, instr):
#        self.params['input'] = [instr]

    def add2params(self, paramName, paramStr):
        self.params[paramName] = [paramStr]

    def getResp(self):

        #The next 4 lines construct the URL
        self.parsedURL['query'] = urllib.parse.urlencode(self.params, doseq=True)
        self.callURL = urllib.parse.urlunparse(self.parsedURL.values())


        #Sending the URL to the api
        self.resp = urllib.request.urlopen(self.callURL)

        # return self.parsedResult    # returns the xml file

    def getUsrQues(self, inStr, **inParams):

        self.add2params('input', inStr)
        for p, val in inParams.items():
            self.add2params(p, val)


        self.rques = inStr

    def parseResp(self):

        self.parsedResp = ET.parse(self.resp)
        steps = self.parsedResp.findall(".//*[@title='Possible intermediate steps']/mathml")
        for i in steps:
            ET.dump(i)
        print(self.parsedResp.findall(".//*[@title='Possible intermediate steps']/mathml"))
        print(self.callURL)
