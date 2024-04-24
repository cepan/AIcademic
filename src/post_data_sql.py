from piazza_api import Piazza
import pandas as pd
import time
from sqlalchemy import create_engine
import re

# Initialize Piazza API with your email and password
p = Piazza()
p.user_login(email='youremail', password='your password')


course_ids = ['lr557t7zde528n', 'lll4pykal4l3k3']
filter_words = ['Released', 'released', 'office hour', 'grade', 'grading', 'grades', 'Camera Setup', 'Regrades', 'regrade']

def remove_tags(content):
    clean_content = re.sub(r'<[^>]*>', '', content)
    return clean_content

def extract_content():
    question_posts = []
    answer_posts = []
    for course_id in course_ids:
        course = p.network(course_id)
        posts = course.iter_all_posts()

        for iter, post in enumerate(posts):
            if iter % 30 == 0 and iter != 0:
                print("The code is sleeping...")
                time.sleep(120)
            content = post['history'][0]['subject'] + post['history'][0]['content']
            if any(keyword in content for keyword in filter_words):
                continue
            else:
                content = remove_tags(content)
                question_posts.append(content)
                if 'children' in post:
                    answers = ''
                    for followup in post['children']:
                        if 'subject' in followup:
                            followup_content = followup['subject']
                            followup_content = remove_tags(followup_content)
                            answers += followup_content
                    answer_posts.append(answers)
                else:
                    answer_posts.append(None)
            print(iter)
    return question_posts, answer_posts

posts_content, answer_posts = extract_content()
answer_posts = [posts if posts else None for posts in answer_posts]

DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/dsci553'
engine = create_engine(DATABASE_URI)
df = pd.DataFrame({'Question': posts_content, 'Follow_Up': answer_posts})
df.to_sql("posts", con=engine, if_exists='replace', index=False)
print("Successfully stored piazza posts data to mysql")