# Copyright 2015 Google Inc. All rights reserved.
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

# [START all]
import webapp2

#from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
from google.appengine.api import images
from google.appengine.api import urlfetch
import re

#appspot
FILEUPLOAD_API_URL= 'https://fileupload-api.appspot.com/uploadurl'

# A custom datastore model for associating users with uploaded files.
class UserPhoto(ndb.Model):
  user = ndb.StringProperty()
  # blob_key = blobstore.BlobReferenceProperty()
  blob_key = ndb.BlobKeyProperty()


class PhotoUploadFormHandler(webapp2.RequestHandler):
    def get(self):
        # [START upload_url]        
        
        result = urlfetch.fetch(FILEUPLOAD_API_URL)
        if result.status_code == 200:
          upload_url = result.content
        
        
        #upload_url = blobstore.create_upload_url('/upload_photo')
        #upload_url = re.sub('/$', '', upload_url)
        logging.info('NEIL: upload_url = %s' % upload_url)
        # [END upload_url]
        # [START upload_form]
        # The method must be "POST" and enctype must be set to "multipart/form-data".
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write('''Upload File: <input type="file" name="file"><br> <input type="submit"
            name="submit" value="Submit"> </form></body></html>''')
        # [END upload_form]


logging.getLogger().setLevel(logging.DEBUG)

app = webapp2.WSGIApplication([('/', PhotoUploadFormHandler),
                              ], debug=True)


