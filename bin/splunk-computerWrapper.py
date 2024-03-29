# Copyright (c) 2015 - 2016 Code42 Software, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from _base import SplunkScript

import json
import os
import sys

class ComputerWrapper(SplunkScript):
    def main(self):
        #############################################################
        ## RUN THE COMPUTERS EXPORTER & REFORMAT EVENTS FOR SPLUNK ##
        #############################################################

        # Set up variables
        pyScript = os.path.join(self.appHome, 'utils', 'computers.py')
        eventsDir = os.path.join(self.appHome, 'events')
        tmpEventFile = os.path.join(eventsDir, 'computers.txt')

        if not os.path.exists(eventsDir):
            os.makedirs(eventsDir)

        args = [ pyScript,
                 tmpEventFile
        ];
        self.python(args)

        with open(tmpEventFile, 'r') as data_file:
            # first line of file is '['
            data_file.readline()
            for line in data_file:
                if line.strip() not in [',',']']:
                    sys.stdout.write(json.dumps(json.loads(line)) + "\n")

        os.remove(tmpEventFile)


script = ComputerWrapper()
script.run()
