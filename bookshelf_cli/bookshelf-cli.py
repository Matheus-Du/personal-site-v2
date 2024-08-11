import requests
import sys
from dotenv import load_dotenv
import os, os.path
from pymongo import MongoClient, timeout as pymongo_timeout
from pymongo.errors import PyMongoError


def connect():
    try:
        conn = MongoClient(f"mongodb://{os.getenv('MONGOUN')}:{os.getenv('MONGOPW')}@localhost:27117/?timeoutMS=10000")
        return conn.personal_site
    except Exception as exc:
        return exc


def parseReview(file):
    with open(file, 'r') as data:
        return data.read()


def getArgVals(args):
    data = {
        'title': None,
        'isbn': None,
        'author': None,
        'date_read': None,
        'cover_image': None,
        'review': None,
        'tags': []
    }

    for i in range(len(args)):
        if args[i] == '-t': data['title'] = args[i+1]
        elif args[i] == '-i': data['isbn'] = args[i+1]
        elif args[i] == '-a': data['author'] = args[i+1]
        elif args[i] == '-d': data['date_read'] = args[i+1]
        elif args[i] == '-c': data['cover_image'] = args[i+1]
        elif args[i] == '-r': data['review'] = parseReview(args[i+1])
    for key in data.keys():
        if data[key] == None:
            data[key] = input(f"Enter value for {key}: ")
    
    return data


def getTags(tags):
    return [tag['name'] for tag in tags.find()]


def addTags(tags, existingTags):
    tag = input(f"Current Tags:{tags}\nEnter a tag value (1 to view existing tags, 0 to exit): ")
    if tag == '1':
        print(existingTags)
        return addTags(tags, existingTags)
    elif tag == '0': return tags
    return addTags(tags + [tag], existingTags)


def main():
    db = connect()
    if type(db) == Exception:
        print(f"Error connecting to MongoDB\n{db}")
        return

    args = sys.argv[1:]
    if len(args) == 0 or '-h' in args:
        print("Usage: python bookshelf.cli -t <book title> -a <author> -i <isbn> -r <path/to/review.txt> -d <date read (YYYYMM)> -c <cover image link>")
        return
    data = getArgVals(args)
    existingTags = getTags(db.book_tags)
    data['tags'] = addTags([], existingTags)
    for tag in data['tags']:
        if tag not in existingTags:
            db.book_tags.insert_one({
                'name': tag,
                'colour': '#' + input(f"New tag {tag} detected. Input a hex colour for the tag: #"),
                'books': []
                })
        db.book_tags.update_one({'name': tag}, {'$push': {'books': data['isbn']}})
    print(data)
    db.books.insert_one(data)
    

if __name__ == '__main__':
    load_dotenv()
    main()