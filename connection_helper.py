import requests
from collections import OrderedDict

def remote_login(host, username, password):
    r = requests.post(host, verify=False, json={"email": username, "password": password})
    if r.status_code == 200:
        return r.json()['key']
    else:
        return False

def get_remote_users():
    pass

def get_remote_posts(host):
    r = requests.get(host + "/author/posts", verify=False)
    if r.status_code == 200:
        content = r.json()
        num_posts = content["count"]
        posts = content["posts"]
        returned_posts = []
        for post in posts:
        #     # parse the content of post
        #     if post["contentType"] == "text/plain":
        #         post["text_type"] = 1
        #     elif post["contentType"] == "text/markdown":
        #         post["text_type"] = 2

        #     if "origin" in post:
        #         post["origin_post"] = post["origin"]
        #     else:
        #         post["origin_post"] = ""
            returned_posts.append(OrderedDict(post))
        return returned_posts
    else:
        return False

def get_remote_friends(host):
    r = requests.get(host, verify=False)

def check_friendship(host, userid_local, userid_remote):
    r = requests.get(host + "/author/" + userid_local + "/friends/" + userid_remote, verify=False)
    return r.json()["friends"]

def check_FOAF():
    pass

# def main():
#     # print(remote_login("http://127.0.0.1:8000/login/", "test1@gmail.com", "passqwer"))

#     #  post
#     # r = get_remote_posts("https://spongebook-develop.herokuapp.com")
#     # print(r["posts"])

#     # friend2friend
#     r = check_friendship("https://spongebook-develop.herokuapp.com", "13930e65-ca56-4743-ab8f-2dd6b45e2cb1", "49784bac-7e1d-43f4-a77d-761141c81f66")
#     print(r)
# main()