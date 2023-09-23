import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import sys


def main():
    args = sys.argv

    if len(args) != 2:
        return

    token = args[1]
    headers = {
        'Authorization': f'Bearer {token}'
    }
    transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=headers)
    client = Client(transport=transport)
    query = gql("""
    query {
      user(login: "enkatsu"){
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """)
    result = client.execute(query)
    with open('data/contributions.json', 'w') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()
