import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import sys


def get_contributions(client, user):
    query = gql('''
        query {
          user(login: "%s"){
            contributionsCollection {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    contributionCount
                    date
                    color
                  }
                }
              }
            }
          }
        }
        ''' % user)
    return client.execute(query)


def get_languages(client, user):
    query = gql('''
        query {
          user(login: "%s"){
            repositories(first: 30, orderBy: {field: CREATED_AT, direction: DESC}) {
              # totalCount
              nodes {
                languages(first: 5, orderBy: {field: SIZE, direction: DESC}) {
                  edges {
                    node {
                      id
                      name
                      color
                    }
                  }
                }
              }
            }
          }
        }
        ''' % user)
    return client.execute(query)


def main():
    args = sys.argv

    if len(args) != 3:
        raise Exception('引数の数が違います')

    user = args[1]
    token = args[2]
    headers = {
        'Authorization': f'Bearer {token}'
    }
    transport = AIOHTTPTransport(url='https://api.github.com/graphql', headers=headers)
    client = Client(transport=transport)

    result = get_contributions(client, user)
    with open('data/contributions.json', 'w') as f:
        json.dump(result, f, indent=2)

    result = get_languages(client, user)
    with open('data/languages.json', 'w') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()
