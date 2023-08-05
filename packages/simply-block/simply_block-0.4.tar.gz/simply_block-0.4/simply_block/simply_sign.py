import hmac
import json
import hashlib
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class SimplySign:

    def __init__(self, private_key, public_key):
        """
        Constructor
        :param private_key: Token Private Key
        :param public_key: Token Public Key
        """
        self.public_key = public_key
        self.private_key = private_key
        self.data = None
        self.signed_data = None

    def generate_signature(self, data):
        """
        Generate Signature from the Request.
        Files are not used for generating Signatures
        :param data: Request Data
        :return: Signed Data
        """

        self.data = data
        print(str(data))
        self.signed_data = hmac.new(
            self.private_key.encode('utf-8'), str(data).encode('utf-8'), digestmod=hashlib.sha384
        ).hexdigest()
        return self.signed_data

    def gateway_request(self, url, data, files=None, **kwargs):
        """
        For API Gateway Request
        :param url: API URI
        :param data: Request Data
        :param files: Request Files
        :param kwargs: If Any
        :return: Response
        """

        if files is None:
            files = {}
        if files:

            # Get Data
            fields = data

            # Generate Signature
            signed_data = self.generate_signature(fields)

            # Append Files according to multipart encoder
            for file_name, file_path in files.items():
                files[file_name] = (file_path, open(file_path, 'rb'), 'text/plain')
            fields.update(files)

            # Append Fields
            fields['public_key'] = self.public_key
            fields['signed_data'] = signed_data

            # Request
            mp_encoder = MultipartEncoder(fields=fields)
            response = requests.post(url, data=mp_encoder, headers={'Content-Type': mp_encoder.content_type}, **kwargs)
        else:
            # Generate Signature
            signed_data = self.generate_signature(data)

            # Generate Data
            request_data = {
                'public_key': self.public_key,
                'signed_data': signed_data,
                'data': data
            }

            # Request
            response = requests.post(
                url, data=json.dumps(request_data), headers={'Content-Type': 'application/json'}, **kwargs
            )
        return response
