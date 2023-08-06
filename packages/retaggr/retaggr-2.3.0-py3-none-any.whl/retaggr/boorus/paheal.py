from retaggr.boorus.base import Booru
from retaggr.errors import NotAvailableSearchException

# External imports
import hashlib
from aiohttp_requests import requests
import xml.etree.ElementTree as ET

class Paheal(Booru):
    """Reverse searches https://rule34.paheal.net for images.

    This booru does require images to be downloaded before searching.
    """
    host = None
    download_required = True

    def __init__(self):
        pass

    async def search_image_source(self, url):
        results = {
            "tags": [],
            "source": None
        }

        m = hashlib.md5()
        r = await requests.get(url)
        async for data in r.content.iter_chunked(8192):
            m.update(data)
        md5_hash = m.hexdigest()
        paheal_request = await requests.get(f"http://rule34.paheal.net/api/danbooru/find_posts?md5={md5_hash}")
        xml_tree = ET.fromstring(await paheal_request.text())

        for post in xml_tree:
            for tag in post.attrib["tags"].split(): 
                results["tags"].append(tag.lower())
            results["source"] = post.attrib["source"]
        return results

    async def search_tag(self, tag):
        """Reverse search the booru for tag data.
        """
        raise NotAvailableSearchException("This engine cannot search tags.")