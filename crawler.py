# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import json
import sys
from io import open

from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings


def usage():
    return """
        python crawler.py posts -u cal_foodie -n 100 -o ./output
        python crawler.py posts_full -u cal_foodie -n 100 -o ./output
        python crawler.py profile -u cal_foodie -o ./output
        python crawler.py profile_script -u cal_foodie -o ./output
        python crawler.py hashtag -t taiwan -o ./output

        The default number for fetching posts via hashtag is 100.
    """


def get_posts_by_user(username, number, detail, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_user_posts(username, number, detail)


def get_profile(username):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_profile(username)


def get_profile_from_script(username):
    ins_cralwer = InsCrawler()
    return ins_cralwer.get_user_profile_from_script_shared_data(username)


def get_posts_by_hashtag(tag, number, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_latest_posts_by_tag(tag, number)


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


def output(data, filepath):
    print("WRITING IN OUTPUT FILE")
    # print(data, filepath)
    out = json.dumps(data, ensure_ascii=False)
    if filepath:
        with open(filepath, "a+", encoding="utf8") as f:
            f.write("\n")
            f.write(out)
    else:
        # print(out)
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Crawler", usage=usage())
    parser.add_argument(
        "mode", help="options: [posts, posts_full, profile, profile_script, hashtag]"
    )
    parser.add_argument("-n", "--number", type=int, help="number of returned posts")
    parser.add_argument("-u", "--username", help="instagram's username")
    parser.add_argument("-t", "--tag", help="instagram's tag name")
    parser.add_argument("-o", "--output", help="output file name(json format)")
    parser.add_argument("--debug", action="store_true")

    prepare_override_settings(parser)

    args = parser.parse_args()

    override_settings(args)

    if args.mode in ["posts", "posts_full"]:
        arg_required("username")
        output(
            get_posts_by_user(
                args.username, args.number, args.mode == "posts_full", args.debug
            ),
            args.output,
        )
    elif args.mode == "profile":
        try:
            with open("pending.json", "r") as f:
                users_list = f.read()

            users_list = json.loads(users_list)
        except:
            print("NOT ABLE TO READ pending.json file")
            exit()

        try:
            with open("visited.json", "r") as f:
                visited = f.read()

            visited = json.loads(visited)
        except:
            print("NOT ABLE TO READ THE visited.json file")
            exit()
        
        visited = set(visited)

        while True:
            # arg_required("username")
            while True:
                if not users_list:
                    print("NO USERS AVAILABLE")
                    exit()
                next_user = users_list[0]
                if next_user not in visited:
                    break
                del users_list[0]
            
            print("CHECKING FOR THE USER ", next_user)
            data = get_profile(next_user)
            output(data, "users.json")
            del users_list[0]
            print("FOUND DATA FOR ", next_user)
            users_list.extend(data.get("followers", []))
            users_list.extend(data.get("following", []))
            users_list = list(set(users_list))
            
            try:
                with open("pending.json", "w") as f:
                    f.write(json.dumps(users_list))
            except:
                print("NOT ABLE TO WRITE THE UPDATED LIST TO pending.json file")

            visited.add(next_user)
            try:
                with open("visited.json", "w") as f:
                    f.write(json.dumps(list(visited)))
            except:
                print("NOT ABLE TO WRITE THE VISITED LIST TO visited.json file")

    elif args.mode == "profile_script":
        arg_required("username")
        output(get_profile_from_script(args.username), args.output)
    elif args.mode == "hashtag":
        arg_required("tag")
        output(
            get_posts_by_hashtag(args.tag, args.number or 100, args.debug), args.output
        )
    else:
        usage()
