import urllib.parse, urllib.request
import lxml.etree as ET
from xml.sax.handler import feature_external_ges
from xml import sax
import os, sys
from py_asciimath.translator.translator import MathML2Tex
from svgmath.mathhandler import MathHandler
from svgmath.tools.saxtools import XMLGenerator

# Uses the untangle lib to make the walpha api's xml output into a python object
# NOT ANYMORE!!! we're using lxml now

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

        self.steps = []

        self.XML = ET.parse(self.resp)
        self.parsedResp = self.XML.getroot()

        # self.parsedResp = self.parsedResp.findall('.//subpod[@title=Possible intermediate steps]/mathml')

        for i in self.parsedResp:
            if i.tag == 'pod' and i.attrib['title'] == 'Solutions':
                for j in i:
                    if j.tag == 'subpod' and j.attrib['title'] == 'Possible intermediate steps':
                        self.steps.append(j)

        with open('source', 'wb') as source:
            source.write(ET.tostring(self.steps[0], prettyprint=True))

        print(self.callURL)

    def makeSVG(self):
        config = open('svgmath.xml', "rb")
        output = open('output.svg', 'w+')
        source = open('source.mml', 'rb')

        saxoutput = XMLGenerator(output, encoding)
        handler = MathHandler(saxoutput, config)

        if not standalone:
            handler = MathFilter(saxoutput, handler)

        parser = sax.make_parser()
        parser.setFeature(feature_external_ges, True)
        parser.setFeature(sax.handler.feature_namespaces, 1)
	# parser.setEntityResolver(MathEntityResolver())
        parser.setContentHandler(handler)
        parser.parse(source)
