import obspython as obs
import bsky_client
import streamsky_config as config
from streamsky_logger import log

from collections import namedtuple



User = namedtuple('User', 'username, password')


def script_description():
    desc = [
        f'{config.APP_DESCRIPTION}\n',
        f'Author: {config.APP_AUTHOR}',
        f'Version: {config.APP_VERSION}'
    ]
    return '\n'.join(desc)


def script_defaults(settings):
    log.info(f'starting [{config.APP_NAME}]...')
    print(f'starting [{config.APP_NAME}]...')

    obs.timer_add(check_if_streaming, 10000)

def script_update(settings):
    global blueskyUsername
    global blueskyPassword
    global blueskyProfile
    global streampathURL
    global isStreaming

    blueskyUsername = obs.obs_data_get_string(settings, 'blueskyUsername')
    blueskyPassword = obs.obs_data_get_string(settings, 'blueskyPassword')
    streampathURL = obs.obs_data_get_string(settings, 'streampathURL')
    blueskyProfile = None
    isStreaming = False


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(
        props, 'blueskyUsername', 'Username', obs.OBS_TEXT_DEFAULT
    )
    obs.obs_properties_add_text(
        props, 'blueskyPassword', 'Password', obs.OBS_TEXT_PASSWORD
    )
    obs.obs_properties_add_text(
        props, 'streampathURL', 'Stream URL', obs.OBS_TEXT_DEFAULT
    )
    obs.obs_properties_add_button(
        props, 'blueskyLogin', 'Login', login
    )

    return props


def login(*args):
    global blueskyProfile

    user = User(blueskyUsername, blueskyPassword)

    blueskyProfile = bsky_client.authenticate(user)
    print(blueskyProfile)


def check_if_streaming(*args):
    if obs.obs_frontend_streaming_active() is True:
        print('stream started')
        log.info('stream started')
        push_stream_to_bluesky()
        obs.remove_current_callback()
        obs.timer_add(check_if_not_streaming, 10000)


def check_if_not_streaming(*args):
    if obs.obs_frontend_streaming_active() is False:
        print('stream stopped')
        log.info('stream stopped')
        obs.remove_current_callback()
        obs.timer_add(check_if_streaming, 10000)


def push_stream_to_bluesky():
    global streampathURL
    global blueskyProfile

    stream_info = [
        # 'TEST_MODE\n',
        'I have started streaming on Twitch !\n',
        f'Find my stream at:'
    ]
    post_text = '\n'.join(stream_info)

    print(post_text)

    login()
    bsky_client.send_post(post_text, streampathURL)
