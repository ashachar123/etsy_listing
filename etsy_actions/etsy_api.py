import time
import requests
import etsyv3
from etsyv3.enums import WhenMade, WhoMade, ListingType
from etsyv3.models.listing_request import CreateDraftListingRequest
import os
from etsyv3.models.file_request import UploadListingFileRequest, UploadListingImageRequest
from datetime import datetime, timedelta
from concept_generator import GptActions


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
        print("uploading Listing to etsy...")
        subject, tags = GptActions().create_subject(
            f"{[file for file in os.listdir(project_path + '/Stock') if file[0] != '_'][0]}")
        token, refresh_token, expiry = self.refresh_etsy_token()
        api = etsyv3.EtsyAPI(keystring=self.api_key,
                             token=token,
                             refresh_token=refresh_token,
                             expiry=expiry
                             )
        title = f"{subject.get('subject')} SVG PNG Collection  {subject.get('theme1')} Hand Drawn Clipart {subject.get('theme2')} Themed Vector Illustration SVG Files for Printing and Crafts".replace(".jpg", "")
        if len(title) >= 139:
            title = f"{subject.get('subject')} SVG PNG Collection {subject.get('theme1')} Hand Drawn Clipart Vector Illustration SVG Files for Printing and Crafts".replace(".jpg", "")
        listing = CreateDraftListingRequest(
            quantity=999,
            title=title,
            description=f"""Features {subject.get("subject")} svg clipart graphics perfect for a variety of uses such as home decor, birthday parties, invitations, crafting, scrapbooking, product design, T-shirts, mugs, clothing, books, stationery, software, games, textiles, packaging, personalized gifts, and more. You are encouraged to creatively combine these graphics with your own text and other images or graphics to create unique designs for your projects.

✨ File Details:

Includes 4 SVG and 4 PNG files
PNG format at 4000 x 4000 pixels, 300 dpi, transparent background

INSTANT DOWNLOAD - This is a digital product, no physical items will be sent - PRINTABLE ART

Suitable for both Personal and Commercial Use. Digital resale in original form is not permitted.

TERMS OF USE

FOR PERSONAL & COMMERCIAL USE
These images are available for both personal and commercial use.
Redistribution of the clipart in its original form is not allowed. You may use these images in digital designs, provided you incorporate them into your design by adding text or other elements. Digital resale as is is prohibited.

REFUND POLICY
Due to the digital nature of this product, we do not offer returns or refunds; please ensure you are certain of your purchase by thoroughly reviewing the item description.

Thank you for choosing my graphics! I hope my clipart helps you create wonderful projects.
Feel free to reach out with any questions.""",
            price=22,
            who_made=WhoMade.I_DID,
            when_made=WhenMade.TWENTY_TWENTIES,
            taxonomy_id=2078,
            tags=tags,
            is_taxable=True,
            listing_type=ListingType.DOWNLOAD,
            should_auto_renew=True,

        )
        # /Users/amitshachar/Documents/etsy/31/Product
        pngs = [f"{project_path}/Mockup/{file}" for file in
                os.listdir(f"{project_path}/Mockup") if file.endswith('.jpg')]
        files = [f"{project_path}/Product/{file}" for file in
                 os.listdir(f"{project_path}/Product") if file.endswith('.zip')]
        if len(files) < 4:
            for i in range(0, 10):
                print("fuck me there arent 4 zip files at all")
                time.sleep(1)
                files = [f"{project_path}/Product/{file}" for file in
                         os.listdir(f"{project_path}/Product") if file.endswith('.zip')]
                if len(files) == 4:
                    break
        new_listing = api.create_draft_listing(shop_id=self.shop_id, listing=listing)
        for index, image in enumerate(pngs):
            if ".mp4" not in image:
                rank = int(image.split("/")[-1].split(".")[0]) + 2 if int(image.split("/")[-1].split(".")[0]) != 0 else 1
            else:
                rank = 4
            api.upload_listing_image(shop_id=self.shop_id, listing_id=new_listing.get("listing_id"),
                                     listing_image=UploadListingImageRequest(image_bytes=open(image, 'rb'), rank=rank))
        for file in files:
            api.upload_listing_file(shop_id=self.shop_id, listing_id=new_listing.get("listing_id"),
                                    listing_file=UploadListingFileRequest(file_bytes=self.convert_bytes(file),
                                                                          name=file.split("/")[-1]))

        print("Listing Uploaded")


if __name__ == "__main__":
    init = EtsyActions(api_key="xuaafzb74heexv0ige5doz1r",
                       refresh_token="882842516.kSA-FdLo8B_n8pNMipgGuBPsI1L2GjYw3wKm4x6NgKh9wa2GmCDeszDVHvl-h_3jDVIy3NhbD6UCmW9nTs3i5KTSkn",
                       shop_id="49127261").post_listing(f"/Users/amitshachar/PycharmProjects/file_orginizer/etsy/4")
    # for num initn range(61, 65):
    #     threading.Thread(target=init.post_listing, args=(f"/Users/amitshachar/Documents/etsy/{num}/", )).start()
    # post_listingt_listing("/Users/amitshachar/Documents/etsy/78/")
