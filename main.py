import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import sys


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
    result = client.execute(query)
    with open('data/contributions.json', 'w') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()
