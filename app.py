from flask import Flask, render_template, request, Response, stream_with_context
import requests
import re
import json

app = Flask(__name__)

def posts_extractor(group_id, cookie_string, user_end_cursor=None):
    cookies = {}
    for cookie in cookie_string.split(";"):
        if "=" in cookie:
            key, value = cookie.strip().split("=", 1)
            cookies[key] = value

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'dpr': '1.25',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-full-version-list': '"Not(A:Brand";v="99.0.0.0", "Google Chrome";v="133.0.6943.127", "Chromium";v="133.0.6943.127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'viewport-width': '744',
    }

    params = {
        'locale': 'ar_AR',
    }

    response = requests.get(f'https://www.facebook.com/groups/{group_id}', params=params, cookies=cookies, headers=headers)
    response_text = response.text
    av = re.search(r"__user=(\d+)", str(response_text)).group(1)
    __hs = re.search(r'"haste_session":"(.*?)",', str(response_text)).group(1)
    __rev = re.search(r'"haste_session":"(.*?)",', str(response_text)).group(1)
    __hsi = re.search(r'"hsi":"(.*?)",', str(response_text)).group(1)
    fb_dtsg = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"', str(response_text)).group(1)
    jazoest = re.search(r'&jazoest=(.*?)",', str(response_text)).group(1)
    lsd = re.search(r'"LSD",\[\],{"token":"(.*?)"', str(response_text)).group(1)
    __spin_r = re.search(r'"__spin_r":(.*?),', str(response_text)).group(1)
    __spin_t = re.search(r'"__spin_t":(.*?),', str(response_text)).group(1)
    # Determine the end_cursor
    if user_end_cursor:
        end_cursor_value = user_end_cursor  # Use the user-provided cursor
        print(f'use the user cursor{end_cursor_value}')
    else:
        end_cursor_value = re.search(r'{"page_info":{"end_cursor":"(.*?)"', response_text)
        end_cursor_value = end_cursor_value.group(1) if end_cursor_value else None  # Handle case where it's not found
    while True:
        headers = {
            'accept': '*/*',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.facebook.com',
            'priority': 'u=1, i',
            'referer': f'https://www.facebook.com/groups/{group_id}?locale=ar_AR',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-full-version-list': '"Not(A:Brand";v="99.0.0.0", "Google Chrome";v="133.0.6943.127", "Chromium";v="133.0.6943.127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-asbd-id': '359341',
            'x-fb-friendly-name': 'GroupsCometFeedRegularStoriesPaginationQuery',
            'x-fb-lsd': lsd,
        }

        data = {
            'av': av,
            '__aaid': '0',
            '__user': av,
            '__a': '1',
            '__req': 'o',
            '__hs': __hs,
            'dpr': '1',
            '__ccg': 'GOOD',
            '__rev': __spin_r,
            '__hsi': __hsi,
            '__comet_req': '15',
            'locale': 'ar_AR',
            'fb_dtsg': fb_dtsg,
            'jazoest': jazoest,
            'lsd': lsd,
            '__spin_r': __spin_r,
            '__spin_b': 'trunk',
            '__spin_t': __spin_t,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'GroupsCometFeedRegularStoriesPaginationQuery',
            'variables': '{"count":3,"cursor":"'+end_cursor_value+'","feedLocation":"GROUP","feedType":"DISCUSSION","feedbackSource":0,"focusCommentID":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"group","scale":1,"sortingSetting":"TOP_POSTS","stream_initial_count":1,"useDefaultActor":false,"id":"'+group_id+'","__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":false,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__CometFeedStoryDynamicResolutionPhotoAttachmentRenderer_experimentWidthrelayprovider":500,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider":false}',
            'server_timestamps': 'true',
            'doc_id': '9215019328566240',
        }

        response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers=headers, data=data)
        feed_data = re.findall(r'"data":\{"node":(.*?)},"extensions":\{', response.text, re.DOTALL)
        for i, post_data in enumerate(feed_data, 1):
            post_dict = {}
            if i in [2, 3]:  
                post_data  = re.sub(r',\s*"cursor":".*?"', '', post_data, flags=re.DOTALL)  # Removes "cursor" keys
                post_data = json.loads(post_data)

                post_dict['actor_name'] = post_data['comet_sections']['content']['story']['actors'][0]['name']
                post_dict['actor_id'] = post_data['comet_sections']['content']['story']['actors'][0]['url']
                post_dict['post_id'] = post_data['comet_sections']['content']['story']['wwwURL']
                try: post_dict['creation_time'] = post_data['comet_sections']['context_layout']['story']['comet_sections']['metadata'][1]['story']['creation_time']
                except: post_dict['creation_time'] = post_data['comet_sections']['context_layout']['story']['comet_sections']['metadata'][0]['story']['creation_time']
                try: post_dict['caption'] = post_data['comet_sections']['content']['story']['comet_sections']['message']['story']['message']['text']
                except: post_dict['caption'] = 'No Caption'
                post_dict['comment_count'] = post_data['comet_sections']['feedback']['story']['story_ufi_container']['story']['feedback_context']['feedback_target_with_context']['comment_rendering_instance']['comments']['total_count']
                post_dict['reaction_count'] = post_data['comet_sections']['feedback']['story']['story_ufi_container']['story']['feedback_context']['feedback_target_with_context']['comet_ufi_summary_and_actions_renderer']['feedback']['reaction_count']['count']
                post_dict['share_count'] = post_data ['comet_sections']['feedback']['story']['story_ufi_container']['story']['feedback_context']['feedback_target_with_context']['comet_ufi_summary_and_actions_renderer']['feedback']['share_count']['count']
                post_dict['profile_pic'] = post_data ['comet_sections']['context_layout']['story']['comet_sections']['actor_photo']['story']['actors'][0]['profile_picture']['uri']
                if 'all_subattachments' in post_data or 'placeholder_image' in str(post_data):
                    post_dict['attachment'] = True
                else:
                    post_dict['attachment'] = False
            else:
                post_data = json.loads(post_data)
                post_dict['actor_name'] = post_data['group_feed']['edges'][0]['node']['comet_sections']['content']['story']['actors'][0]['name']
                post_dict['actor_id'] = post_data['group_feed']['edges'][0]['node']['comet_sections']['content']['story']['actors'][0]['url']
                post_dict['post_id'] = post_data ['group_feed']['edges'][0]['node']['comet_sections']['content']['story']['wwwURL']
                try: post_dict['creation_time'] = post_data['group_feed']['edges'][0]['node']['comet_sections']['context_layout']['story']['comet_sections']['metadata'][1]['story']['creation_time']
                except: post_dict['creation_time'] = post_data['group_feed']['edges'][0]['node']['comet_sections']['context_layout']['story']['comet_sections']['metadata'][0]['story']['creation_time']
                try: post_dict['caption'] = post_data['group_feed']['edges'][0]['node']['comet_sections']['content']['story']['comet_sections']['message']['story']['message']['text']
                except: post_dict['caption'] = 'No Caption'
                post_dict['comment_count'] = post_data['group_feed']['edges'][0]['node']['comet_sections']['feedback']['story']['story_ufi_container']['story']['feedback_context']['feedback_target_with_context']['comment_rendering_instance']['comments']['total_count']
                post_dict['reaction_count'] = post_data['group_feed']['edges'][0]['node']['comet_sections']['feedback']['story']['story_ufi_container']['story']['feedback_context']['feedback_target_with_context']['comet_ufi_summary_and_actions_renderer']['feedback']['reaction_count']['count']
                post_dict['share_count'] = post_data['group_feed']['edges'][0]['node']['comet_sections']['feedback']['story']['story_ufi_container']['story']['feedback_context']['feedback_target_with_context']['comet_ufi_summary_and_actions_renderer']['feedback']['share_count']['count']
                post_dict['profile_pic'] = post_data ['group_feed']['edges'][0]['node']['comet_sections']['context_layout']['story']['comet_sections']['actor_photo']['story']['actors'][0]['profile_picture']['uri']
                if 'all_subattachments' in post_data or 'placeholder_image' in str(post_data):
                    post_dict['attachment'] = True
                else:
                    post_dict['attachment'] = False
            # Yield the post data as it's obtained
            yield f"data: {json.dumps(post_dict)}\n\n"

        new_cursor = re.search(r'"end_cursor":"(.*?)"', response.text)
        end_cursor_value = new_cursor.group(1) if new_cursor else None
        if not end_cursor_value:
            yield f"data: {json.dumps({'last_cursor': last_cursor, 'message': 'No more cursor'})}\n\n"
            break  # Stop fetching if no new cursor
        last_cursor = end_cursor_value  # Update last known cursor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['GET'])
def extract():
    group_id = request.args.get('group_id')
    cookie_string = request.args.get('cookie_string')
    user_end_cursor = request.args.get('end_cursor')  # Optional cursor from user
    
    return Response(
        stream_with_context(posts_extractor(group_id, cookie_string, user_end_cursor)),
        content_type='text/event-stream'
    )


if __name__ == '__main__':
    app.run(debug=True)
