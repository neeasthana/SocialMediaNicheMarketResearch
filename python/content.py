from accounts import *

# Represents video/photo content metadata
class InstagramContent:
    def __init__(self, post_json):
        self.post_json = post_json
        self.node = post_json['node']
        self._parse()


    def _parse(self):
        self.display_url = self.node['display_url']
        self.type = self.node['__typename']


    def content_url(self):
        return self.display_url


    def create(post_json):
        typename = post_json['node']['__typename']
        if typename == "GraphImage":
            return InstagramPhotoContent(post_json)
        elif typename == "GraphVideo":
            return InstagramVideoContent(post_json)
        elif typename == "GraphSidecar":
            return InstagramSidecarContent(post_json)
        else:
            raise Exception("Unknown content type: " + typename)



class InstagramVideoContent(InstagramContent):
    def __init__(self, post_json):
        super().__init__(post_json)


    def _parse(self):
        super()._parse()
        self.video_url = self.node['video_url']
        self.views = self.node['video_view_count']


    def content_url(self):
        return self.video_url



class InstagramPhotoContent(InstagramContent):
    def __init__(self, post_json):
        super().__init__(post_json)


    def _parse(self):
        super()._parse()
        self.photo_url = self.node['display_url']


    def content_url(self):
        return self.photo_url


# Sidecars are posts with multiple pieces of content (multiple photos and videos)
class InstagramSidecarContent(InstagramContent):
    def __init__(self, post_json):
        super().__init__(post_json)
        self.content_list = []

    def _parse(self):
        super()._parse()
        pieces_of_content = self.node["edge_sidecar_to_children"]["edges"]
        self.content_list = [InstagramContent.create(content) for content in pieces_of_content]


    def content_urls(self):
        return [content.display_url() for content in pieces_of_content]




if __name__ == "__main__":
    a = InstagramAccount("mindmatterswithdiv")

    print(a.profile.toString())

    print(a.get_most_commented_post().toString())

    post = a.get_most_liked_post()

    content = InstagramContent.create(post.post_json)

    print(type(content))