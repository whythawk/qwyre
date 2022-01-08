import base64
from typing import List, Dict
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import bleach
import dateutil.parser
from lxml import etree

from chapisha.helpers.updatezipfile import UpdateZipFile

from app.schemas import WorkStreamCreate
from app.schema_types import ContributorRoleType

###################################################################################
# HTML PARSER
###################################################################################

# https://stackoverflow.com/questions/699468/remove-html-tags-not-on-an-allowed-list-from-a-python-string
# https://stackoverflow.com/questions/8499633/how-to-display-base64-images-in-html
# https://stackoverflow.com/questions/57922988/splitting-a-string-that-includes-html-tags-into-its-building-blocks-in-python


class ChapterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bits = []

    def handle_starttag(self, tag, attrs):
        if tag != "img" and tag != "a":
            self.bits.append(f"<{tag}>")
        if tag == "a":
            for key, value in attrs:
                if key == "href":
                    self.bits.append(f"<{tag} href='{value}'>")
                    break

    def handle_endtag(self, tag):
        if tag != "img":
            self.bits.append(f"</{tag}>")

    def handle_data(self, data):
        if data not in ["\n", "\t", "\r"] and data.strip():
            self.bits.extend([d.strip() for d in data.strip().split(" ") if d.strip()])


###################################################################################
# METADATA PARSER
###################################################################################


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.terms = {}
        self.tag = None

    def handle_starttag(self, tag, attrs):
        self.tag = None
        if tag.startswith("dc"):
            self.tag = tag.split(":")[1]
            if self.tag not in self.terms:
                self.terms[self.tag] = []
        elif tag == "meta":
            for key, value in attrs:
                if key == "property" and len(value.split(":")) > 1:
                    self.tag = value.split(":")[1]
                    break
        if self.tag and self.tag not in self.terms:
            self.terms[self.tag] = []

    def handle_data(self, data):
        if self.tag:
            self.terms[self.tag].append(data.strip())


###################################################################################
# PROCESS EPUB
###################################################################################


class StreamFromWork:
    def __init__(self):
        self.keys = [
            "identifier",
            "title",
            "language",
            "rights",
            "description",
            "creator",
            "date",
            "subject",
            "publisher",
            "long-description",
            "work-uri",
            "word-count",
        ]
        self.list_keys = ["creator", "subject"]
        self.ns = {
            "n": "urn:oasis:names:tc:opendocument:xmlns:container",
            "opf": "http://www.idpf.org/2007/opf",
            "dc": "http://purl.org/dc/elements/1.1/",
        }

    def _get_content_opf(self, path_list: List[str]) -> str:
        return list(filter(lambda x: "content.opf" in x, path_list))[0]

    def _get_page_path(self, source: str, path_list: List[str]) -> str:
        return list(filter(lambda x: source in x, path_list))[0]

    def _get_spine_pages(self, spine: BeautifulSoup, path_list: List[str]) -> List[str]:
        idrefs = [e["idref"] for e in spine.find_all("itemref")]
        return [self._get_page_path(ref, path_list) for ref in idrefs]

    def _get_start_page(self, contents: BeautifulSoup) -> str:
        pages = [e.get("href") for e in contents.guide.find_all("reference") if e.get("type") == "bodymatter"]
        if pages:
            return pages[0]
        pages = [
            e.get("href")
            for e in contents.manifest.find_all("item")
            if "1." in e.get("href") and e.get("media-type") == "application/xhtml+xml"
        ]
        if pages:
            return pages[0]
        return None

    def _get_publisher_uri(self, contents: BeautifulSoup) -> str:
        tag_id = f"#{contents.find('dc:publisher').get('id')}"
        publisher_uri = [c for c in contents.find_all("meta", property="se:url.homepage") if c.get("refines") == tag_id]
        if publisher_uri:
            return publisher_uri[0].next_sibling.strip()
        return ""

    def _get_contributors(self, contents: BeautifulSoup) -> List[Dict]:
        contributor_in = []
        for contributor in contents.find_all("dc:contributor"):
            try:
                role = ContributorRoleType(contributor.get("id").split("-")[0])
            except ValueError:
                continue
            contributor_in.append({"role": role, "name": contributor.string})
        return contributor_in

    def _get_long_description(self, contents: BeautifulSoup) -> str:
        long_description = contents.find("meta", property="se:long-description")
        if long_description:
            return long_description.next_sibling.strip()
        return ""

    def _get_fulltitle(self, contents: BeautifulSoup) -> str:
        if contents.find("dc:title", id="fulltitle"):
            return contents.find("dc:title", id="fulltitle").string
        if contents.find("dc:title", id="title"):
            return contents.find("dc:title", id="title").string
        return ""

    def _get_cover_source(self, contents: BeautifulSoup, source_list: List[str]) -> str:
        cover_source = contents.find("item", {"properties": "cover-image"}).get("href")
        cover_source = list(filter(lambda x: cover_source in x, source_list))
        if cover_source:
            return cover_source[0]
        return None

    def _clean_metadata(self, metadata: dict) -> Dict:
        allowed_tags = bleach.sanitizer.ALLOWED_TAGS + ["p"]
        for key in metadata.keys():
            if isinstance(metadata[key], str):
                metadata[key] = bleach.clean(metadata[key], tags=allowed_tags)
            if isinstance(metadata[key], list):
                if isinstance(metadata[key][0], dict):
                    replacement = []
                    for item in metadata[key]:
                        for k in item.keys():
                            if isinstance(item[k], str):
                                item[k] = bleach.clean(item[k], tags=allowed_tags)
                        replacement.append(item)
                    metadata[key] = replacement
                else:
                    metadata[key] = [
                        bleach.clean(v, tags=allowed_tags) for v in metadata[key] if bleach.clean(v, tags=allowed_tags)
                    ]
        return metadata

    def _get_work_stream(self, page: BeautifulSoup) -> List[str]:
        try:
            while page.section.svg:
                # Remove SVG image elements which cause chaos.
                page.section.svg.decompose()
        except AttributeError:
            pass
        try:
            page_xml = "".join([str(e) for e in page.section.contents if e not in ["\n", "\t", "\r"]])
        except AttributeError:
            return []
        parser = ChapterParser()
        parser.feed(page_xml)
        if len(parser.bits) >= 3:
            # i.e. there's an enclosing tag and data
            return parser.bits
        return []

    def _get_work_metadata(self, contents: BeautifulSoup) -> Dict:
        parser = MetadataParser()
        for term in [str(e) for e in contents.contents if e not in ["\n", "\t", "\r"]]:
            parser.feed(term)
        metadata = {
            key: (value[0] if key not in self.list_keys else value)
            for key, value in parser.terms.items()
            if key in self.keys
        }
        metadata["date"] = dateutil.parser.isoparse(metadata["date"]).date()
        metadata["publisher-uri"] = self._get_publisher_uri(contents)
        metadata["long-description"] = self._get_long_description(contents)
        metadata["title"] = self._get_fulltitle(contents)
        metadata["contributor"] = self._get_contributors(contents)
        return self._clean_metadata(metadata)

    def _get_first_500(self, stream: List[List[str]], start_page: int) -> str:
        if not stream:
            return ""
        first500 = " ".join(stream[start_page][:500]) + " ..."
        # Fix the borken html
        soup = BeautifulSoup(first500, "lxml")
        return "".join([str(t) for t in soup.body.findChildren(recursive=False)])

    def get_work_stream(self, source: str) -> WorkStreamCreate:
        work_stream = {
            "cover": "",
            "stream": [],
            "spine": [],
            "first500": "",
            "start_page": 0,
        }
        with UpdateZipFile(source, "a") as w:
            # Ensure have a valid content.opf file in the work
            container_file = list(filter(lambda x: "container.xml" in x, w.namelist()))
            if not container_file:
                raise ValueError("Invalid EPUB: missing 'container.xml'")
            container = w.read(container_file[0])
            tree = etree.fromstring(container)
            opf_file = tree.xpath("n:rootfiles/n:rootfile/@full-path", namespaces=self.ns)
            if not opf_file:
                raise ValueError("Invalid EPUB: missing 'content.opf'")
            contents = w.read(opf_file[0])
            contents = BeautifulSoup(contents.decode("utf-8"), "lxml")
            # Process cover
            cover_source = self._get_cover_source(contents=contents, source_list=w.namelist())
            if cover_source:
                work_stream["cover"] = base64.b64encode(w.read(cover_source))
            # Process metadata
            metadata = self._get_work_metadata(contents)
            if metadata:
                work_stream["metadata"] = metadata
            # Process stream
            start_page = self._get_start_page(contents)
            stream_page = 0
            for page in self._get_spine_pages(contents.spine, w.namelist()):
                page_xml = w.read(page)
                source = BeautifulSoup(page_xml.decode("utf-8"), "lxml")
                stream = self._get_work_stream(source)
                if stream:
                    if start_page and start_page in page:
                        work_stream["start_page"] = stream_page
                    stream_page += 1
                    work_stream["spine"].append(source.title.string)
                    work_stream["stream"].append(stream)
            work_stream["first500"] = self._get_first_500(
                stream=work_stream["stream"], start_page=work_stream["start_page"]
            )
        return WorkStreamCreate(**work_stream)
