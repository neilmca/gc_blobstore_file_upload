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




class GetUploadUrlHandler(webapp2.RequestHandler):
    def get(self):
        # [START get upload_url to pass to front end]
        upload_url = blobstore.create_upload_url('/upload_photo')
        self.response.out.write(upload_url)


# [START upload_handler calle when file uplosd starts]
class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            self.redirect('/servingurl/%s' % upload.key())

        except:
            self.error(500)
# [END upload_handler]

# [START get serving url for the upladed image]
class GetServingUrlHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, image_uploaded_key):
        if not blobstore.get(image_uploaded_key):
            self.error(404)
        else:
            serving_url = images.get_serving_url(image_uploaded_key)
            logging.info('serving_url = %s' % serving_url)
            #self.send_blob(image_uploaded_key)
            self.response.write('image serving_url = %s' % serving_url)
# [END download_handler]

logging.getLogger().setLevel(logging.DEBUG)


app = webapp2.WSGIApplication([('/upload_photo', PhotoUploadHandler),
                               ('/servingurl/([^/]+)?', GetServingUrlHandler),
                               ('/uploadurl', GetUploadUrlHandler),
                              ], debug=True)
# [END all]
