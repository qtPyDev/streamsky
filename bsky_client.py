# setup client for streamsky


from streamsky_logger import log
from atproto import Client, models


client = Client()


def authenticate(user):
    profile = None

    try:
        log.info('connecting to bsky...')
        profile = client.login(user.username, user.password)

    except Exception as e:
        log.info(e)
        log.info('failed to connect...')

    return profile


def send_post(text, url):
    embed = models.AppBskyEmbedExternal.Main(
        external=models.AppBskyEmbedExternal.External(
            title='Streamsky Stream Link',
            description='Stream Page',
            uri=url,
        )
    )

    post = client.send_post(
        text = text,
        embed = embed
    )

    post_info = f'submits post at {post.uri}'

    log.info(post_info)
    print(post_info)

    return post
