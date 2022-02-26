from accounts import InstagramAccount

# Represents video/photo content metadata
class InstagramContent:
    def __init__(self, post_json):
        node = post_json['node']
        self.display_url = node['display_url']
        self.type = node['__typename']


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



class InstagramPhotoContent(InstagramContent):
    def __init__(self, post_json):
        super().__init__(post_json)



if __name__ == "__main__":
    account = InstagramAccount("koberdoodle")

    print(account.profile.toString())

    print(account.get_most_commented_post().toString())

    post = account.get_most_liked_post()

    content = InstagramContent.create(post.post_json)

    print(type(content))