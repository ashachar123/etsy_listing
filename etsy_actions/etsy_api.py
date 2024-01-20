import requests
import etsyv3
from etsyv3.enums import WhenMade, WhoMade, ListingType
from etsyv3.models.listing_request import CreateDraftListingRequest
import os
from etsyv3.models.file_request import UploadListingFileRequest, UploadListingImageRequest
from datetime import datetime, timedelta




class EtsyActions:
    def __init__(self, api_key, refresh_token, shop_id):
        self.api_key = api_key
        self.refresh_token = refresh_token
        self.shop_id = shop_id

    @staticmethod
    def convert_bytes(file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    def refresh_etsy_token(self):
        token_url = 'https://api.etsy.com/v3/public/oauth/token'
        payload = {
            'grant_type': 'refresh_token',
            'client_id': self.api_key,
            'refresh_token': self.refresh_token
        }

        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            new_tokens = response.json()
            new_access_token = new_tokens['access_token']
            new_refresh_token = new_tokens['refresh_token']
            # Calculate the new expiry time
            expires_in = new_tokens['expires_in']
            expiry_time = datetime.utcnow() + timedelta(seconds=expires_in)
            return new_access_token, new_refresh_token, expiry_time
        else:
            raise Exception("Failed to refresh token")

    def post_listing(self, project_path):
        token, refresh_token, expiry = self.refresh_etsy_token()
        api = etsyv3.EtsyAPI(keystring="xuaafzb74heexv0ige5doz1r",
                             token=token,
                             refresh_token=refresh_token,
                             expiry=expiry
                             )

        listing_example = api.get_listing(1657105643)
        listing = CreateDraftListingRequest(
            quantity=998,
            title="title",
            description="description",
            price=15,
            who_made=WhoMade.I_DID,
            when_made=WhenMade.TWENTY_TWENTIES,
            taxonomy_id=2078,
            tags=[],
            is_taxable=True,
            listing_type=ListingType.DOWNLOAD,
            should_auto_renew=True,

        )
        # /Users/amitshachar/Documents/etsy/31/Product
        pngs = [f"{project_path}/Mockup/{file}" for file in
                os.listdir(f"{project_path}Mockup") if file.endswith('.jpg')]
        files = [f"{project_path}Product/{file}" for file in
                 os.listdir(f"{project_path}Product") if file.endswith('.zip')]
        new_listing = api.create_draft_listing(shop_id=self.shop_id, listing=listing)
        for index, image in enumerate(pngs):
            rank = int(image.split("/")[-1].split(".")[0]) + 2 if int(image.split("/")[-1].split(".")[0]) != 4 else 1
            api.upload_listing_image(shop_id=self.shop_id, listing_id=new_listing.get("listing_id"),
                                     listing_image=UploadListingImageRequest(image_bytes=open(image, 'rb'), rank=rank))
        for file in files:
            api.upload_listing_file(shop_id=self.shop_id, listing_id=new_listing.get("listing_id"),
                                    listing_file=UploadListingFileRequest(file_bytes=self.convert_bytes(file),
                                                                          name=file.split("/")[-1]))

if __name__ == "__main__":
    EtsyActions(api_key="", refresh_token="", shop_id="").post_listing("/Users/amitshachar/Documents/etsy/65/")