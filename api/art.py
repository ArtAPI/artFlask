"""
.. currentmodule:: api.art

Art API
-------
.. http:get:: /art

   Search art: returns a list of Art entities. GET requests to this URL without query
   parameters will return 501 (Not Implemented), as requests to dump all the Art data
   is discouraged.

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: nothing found

.. http:get:: /art/(art_id)
.. http:get:: /art/(art_id)/(action)

   Returns the Art entity for the given art_id. If the action is ``picture`` , ``thumbnail``,
   ``qrcode``, return image from filesystem. If ``view`` return artView.html template

   **Example request**:

   .. sourcecode:: http

      GET /art/68b4f17f-bd76-4338-a59f-15b4a097a31b HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: no such art

.. http:post:: /art

   Uploads a new file, returning the newly created art id. At this time, the thumbnail,
   watermarked web sized image, and QR code for the view should be generated. For now,
   these will be stored in the ``upload`` folder and given filenames of
   <id>-web.png, <id>-tn.png, and <id>-qr.png where <id> is the Art ID field.
   Note image funtions are in api/artImageFunctions.py (see test() method).
   Original uploaded binary will be deleted.

   :form file: File to be uploaded
   :form title: Title of the work
   :form description: Description of the work
   :form buyURL: E-commerce website to buy work
   :form venue: Venue ID
   :form medium: Artwork materials and style
   :form sold: Whether the work is sold
   :form series: List of Art IDs for related works
   :form parent_work: Art ID of work that is the parent, or provides some other context
   :form alt_urls: List of alternate URLs to display.

   :statuscode 201: Art Created
   :statuscode 404: Error uploading

.. http:put:: /art/(art_id)

   Update artwork by sending a json object for a given work. Note, if a new image is
   uploaded, you must re-generate the -web and -tn images using artImageFunctions.py

   :jsonparam string file: base64 encoded bytes for the image
   :jsonparam string title: Title of the work
   :jsonparam string description: Description of the work
   :jsonparam string buyURL: Ecommerce website to buy work
   :jsonparam string venue: Venue ID
   :jsonparam string medium: Artwork materials and style
   :jsonparam boolean sold: Whether the work is sold
   :jsonparam series: List of Art IDs for related works
   :jsonparam parent_work: Art ID of work that is the parent, or provides some other context
   :jsonparam alt_urls: List of alternate URLs to display.

   :statuscode 200: Update Successful
   :statuscode 404: Error uploading

.. http:delete:: /art/(art_id)

   Delete an artwork (must be owned by the person).

   :statuscode 200: Delete Successful
   :statuscode 404: Not found

"""
__author__ = 'Michael Schwartz'

from flask import send_file, request,render_template
from flask.ext.restful import Resource, Api
from utils.helpers import  upload_file, jsonify
from bson import json_util
from utils.app_ctx import ApplicationContext
from utils.Properies import Properties
import json
import io

class Art(Resource):

    def get(self):
      app_ctx =ApplicationContext('art')
      items = app_ctx.query_from_context()
      return json_util.dumps(items)
      
#Commenting this out until I figure out a decent way to give it a proper route
    # def get(self, art_id=None, action_type=None):
    #     app_ctx =ApplicationContext('art')
    #     try:
    #       item = app_ctx.get_item(art_id)
    #       if action_type=='view':
    #           return render_template('artView.html',art=item)
    #       if action_type==None:
    #           return jsonify(item)
    #     except Exception ,e:
    #         return str(e), 404

    #     try:
    #         # Get the upload dir
    #         imagedir = ""
    #         fn = ""
    #         try:
    #             p = Properties.load("../artFlask.properties")
    #             imagedir = p.getProperty('imagedir')
    #         except:
    #             return 'Imagedir property not found in artFlask.properties', 404
    #         if action_type=="thumbnail":
    #             fn = '%s/%s_tn.png' % (imagedir, art_id)
    #         if action_type=="picture":
    #             fn = '%s/%s_web.png' % (imagedir, art_id)
    #         if action_type=="qrcode":
    #             fn = '%s/%s_qrcode.png' % (imagedir, art_id)
    #         return send_file(io.BytesIO(filename=fn))
    #     except Exception , e:
    #         return str(e), 404

    def post(self):
        # Get params and write
        # Convert image to web size
        # Write file
        # Convert image to thumbnail
        # Write file
        # Create db entry for art
        try:
          app_ctx = ApplicationContext('art')
          if 'file' in request.files:
            upload_file()
          item_id = app_ctx.create_item_from_context()
          return "%s"%item_id,201
        except Exception, e:
          return str(e),404


    def put(self,art_id=None):
      try:
        app_ctx = ApplicationContext('art')
        app_ctx.create_item_from_context(art_id)
        if 'file' in request.files:
            upload_file()
        return '',200
      except Exception, e:
        return str(e),404

    def delete(self,art_id=None):
      try:
        app_ctx = ApplicationContext('art')
        app_ctx.remove_record(art_id)
        return '',200 
      except Exception, e:
        return str(e),404
