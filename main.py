# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import jinja2
import os
import time
import json
import xml.etree.ElementTree as ET

from google.appengine.api import mail

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                            autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class mainpageHandler(Handler):
    def get(self):
        self.render('index.html')

class moviesiteHandler(Handler):
    def get(self):
        self.render('movies.html')

class presentationHandler(Handler):
    def get(self):
        self.render('presentation.html')

        
class contactHandler(Handler):
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        request = self.request.get('request')
        phone_number = self.request.get('phone-number')
        
        mail.send_mail(
            sender='TimPortfolioSite@timsearcyportfolio.appspotmail.com',
            to='Tim Searcy <timmyzsearcy@gmail.com>',
            subject='%s is contacting you.' % name,
            body='Request email: %s\n Phone number: %s \nRequest Body: \n%s' % (email,phone_number, request))
        
        self.write("Your email has been received!")

class greenButtonHandler(Handler):
    def get(self):
        self.render('chartist_greenbutton.html')

class greenButtonDataHandler(Handler):
    def get(self):
        tree = ET.parse('data/CEN_D_THIRDPARTY_12345_CONSUMPTION_20151029_20151029131558_ESPI2-1_01-01.xml')
        root = tree.getroot()
        timestamps = []
        values = []
        for i in range(1, len(root[14][5][0])):
            timestamps.append(root[14][5][0][i][1][1].text)
            values.append(root[14][5][0][i][2].text)

        json_response = {
                'timestamps': timestamps,
                'values': values
            }
        self.write(json.dumps(json_response))


app = webapp2.WSGIApplication([
    ('/', mainpageHandler),
    ('/moviesite', moviesiteHandler),
    ('/presentation', presentationHandler),
    ('/email_form', contactHandler),
    ('/greenbutton', greenButtonHandler),
    ('/greenbuttondata', greenButtonDataHandler),
], debug=True)
