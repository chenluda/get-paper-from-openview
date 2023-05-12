'''
Description: 从 openreview 获取被接收的顶会论文保存至数据库
Version: 1.0
Author: Glenn
Email: chenluda01@outlook.com
Date: 2023-05-04 13:45:40
FilePath: main.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''
import openreview
import mysql.connector
import time

def get_papers_from_openreview(conference_id):
    """
    从 openreview 获取被接收的顶会论文
    """
    def get_accepted_forum_ids(blind_notes):
        """
        从提交的论文中获取被接收的论文
        """
        forum_ids = set()
        for note in blind_notes:
            for reply in note.details["directReplies"]:
                if reply["invitation"].endswith("Decision") and 'Accept' in reply["content"]['decision']:
                    forum_ids.add(reply['forum'])
        return forum_ids

    def format_note(note, conference_name):
        """
        获取需要存储的论文信息
        """
        authors_string = ','.join(note.content['authors'])
        tags_string = ','.join(note.content['keywords'])
        localTime = time.localtime(note.pdate/1000)
        strTime = time.strftime('%Y-%m-%d', localTime)
        return {
            'title': note.content['title'],
            'url': 'https://openreview.net/forum?id=' + note.forum,
            'pub_date': strTime,
            'summary': note.content['abstract'],
            'authors': authors_string,
            'tags': tags_string,
            'read_num': 0,
            'conference': conference_name,
            'venue': note.content['venue']
        }

    # 获取该会议的所有提交论文
    submissions = client.get_all_notes(
        invitation=conference_id + '/Conference/-/Blind_Submission', details='directReplies')
    # 从提交的论文中获取被接收论文的 id
    accepted_forum_ids = get_accepted_forum_ids(submissions)
    # 通过 id 获取需要存储的论文信息
    notes_list = [format_note(note, conference_name) for note in submissions if note.forum in accepted_forum_ids]

    return notes_list


def insert_papers_to_db(papers):
    """
    将获取的论文信息保存至数据库
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='your-host-address',
            user='your-username',
            password='your-password',
            database='your-database'
        )

        cursor = connection.cursor()
        for paper in papers:
            query = '''
                INSERT INTO card_data (title, abstracts, tags, authors, date, url, read_num, conference, venue)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (
                paper['title'],
                paper['summary'],
                paper['tags'],
                paper['authors'],
                paper['pub_date'],
                paper['url'],
                paper['read_num'],
                paper['conference'],
                paper['venue']
            ))
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to insert paper: {error}")
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == '__main__':
    client = openreview.Client(baseurl='https://api.openreview.net')

    # 会议名称，建议先在官网上查看下收录会议该年的论文是否已经放出
    conference_name = 'ICLR'
    # 会议年份
    conference_year = '2023'
    
    # conference_name = 'NeurIPS'
    # conference_year = '2022'

    paper_list = get_papers_from_openreview(
        conference_name + '.cc/' + conference_year)
    pass
    
    if paper_list:
        insert_papers_to_db(paper_list)
    else:
        print("No papers found to insert into the database.")
