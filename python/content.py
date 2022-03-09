from accounts import InstagramAccount

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
        return self.url


    def create(post_json):
        typename = post_json['node']['__typename']
        if typename == "GraphImage":
            return InstagramPhotoContent(post_json)
        elif typename == "GraphVideo":
            return InstagramVideoContent(post_json)
        else:
            raise Exception("Unknown content type: " + typename)



class InstagramVideoContent(InstagramContent):
    def __init__(self, post_json):
        super().__init__(post_json)


    def _parse(self):
        super()._parse()
        self.video_url = self.node['video_url']
        self.views = self.node['video_view_count']



class InstagramPhotoContent(InstagramContent):
    def __init__(self, post_json):
        super().__init__(post_json)


    def _parse(self):
        super()._parse()
        self.photo_url = self.node['thumbnail_src']



if __name__ == "__main__":
    a = InstagramAccount("koberdoodle")

    print(a.profile.toString())

    print(a.get_most_commented_post().toString())

    post = a.get_most_liked_post()

    content = InstagramContent.create(post.post_json)

    print(type(content))