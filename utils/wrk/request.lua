wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body = [[
{
  "query": "query DiscussionComments(\n  $canonical: String!\n  $offset: Int!\n) {\n  discussion(canonical: $canonical) {\n    id\n    canonical\n    comments(offset: $offset) {\n      ...Comment\n      replies {\n        ...Comment\n      }\n    }\n  }\n}\n\nfragment Comment on Comment {\n  id\n  content\n  user {\n    id\n    nick\n  \tname\n  }\n}\n",
  "variables": {
    "canonical": "www.novinky.cz/clanek/45435",
    "offset": 0
  },
  "operationName": "DiscussionComments"
}
]]
