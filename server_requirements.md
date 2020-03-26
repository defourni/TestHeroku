# Requirements

** User Stories

- [x] As an author I want to make posts.
- [x] As an author I want to edit posts.
- [x] As an author, posts I create can link to images.
- [ ] As a server admin, images can be hosted on my server.
- [x] As an author, posts I create be private to me
- [x] As an author, posts I create be private to another author
- [x] As an author, posts I create be private to my friends
- [x] As an author, posts I create be private to friends of friends
- [ ] As an author, posts I create be private to only friends on my host
- [x] As an author, posts I create can be public
- [x] As an author, posts I make can be in simple plain text
- [x] As an author, posts I make can be in markdown (commonMark is good)
- [ ] As an author, I want a consistent identity per server
- [x] As a server admin, I want to host multiple authors on my server
- [ ] As a server admin, I want to share or not share posts with users
         on other servers.
- [ ] As a server admin, I want to share or not share images with users
         on other servers.
- [ ] As an author, I want to pull in my github activity to my "stream"
- [ ] As an author, I want to post posts to my "stream"
- [ ] As an author, I want to delete my own posts.
- [ ] As an author, I want to befriend local authors
- [ ] As an author, I want to befriend remote authors
- [ ] As an author, I want to feel safe about sharing images and
         posts with my friends -- images should not publicly accessible
         without authentication.
- [ ] As an author, I want un-befriend local and remote authors
- [ ] As an author, I want to be able to use my web-browser to manage
         my profile
- [ ] As an author, I want to be able to use my web-browser to manage/author
         my posts
- [x] As a server admin, I want to be able add, modify, and remove
         authors.
- [ ] As a server admin, I want to be able allow users to sign up but
          require my OK to finally be on my server
- [ ] As a server admin, I don't want to do heavy setup to get the
         posts of my author's friends.
- [ ] As a server admin, I want a restful interface for most operations
- [ ] As an author, other authors cannot modify my data
- [ ] As an author, I want to comment on posts that I can access
- [ ] As an author, my server will know about my friends
- [ ] As an author, When I befriend someone it follows them, only when
         the other authors befriends me do I count as a real friend.
- [ ] As an author, I want to know if I have friend requests.
- [ ] As an author I should be able to browse the public posts of everyone
- [ ] As an author I should be able to browse the posts of others depending on my status
- [ ] As a server admin, I want to be able to add nodes to share with
- [ ] As a server admin, I want to be able to remove nodes and stop
         sharing with them.
- [ ] As a server admin, I can limit nodes connecting to me via
         authentication.
- [ ] As a server admin, node to node connections can be authenticated
         with HTTP Basic Auth
- [ ] As a server admin, I can disable the node to node interfaces for
         connections that are not authenticated!
- [ ] As an author, I want to be able to make posts that are unlisted,
         that are publicly shareable by URI alone (or for embedding images)
** Main Concepts
- Author
  - makes posts
  - makes friends
  - befriends other authors
- Server Admin
  - manages a node
  - allows people to sign up
  - responsible for private data :(
- Follow
  - Friend another author without an accepted friend request
- Friend
  - Friend another author and they accept the friend request
- Server
  - a host that hosts authors and vouches for them
- Restful service
  - The model of the service and its API
- UI
  - The HTML/CSS/JS coated version user interface
- FOAF
  - Friend of a friend

** Requirements

- [ ] Implement the webservice as described in the user stories
- [ ] Provide a webservice interface that is restful
- [ ] Provide a web UI interface that is usable
- [ ] Prove your project by connecting with at least 2 other
     groups.
- [ ] Make a video demo of your blog (desktop-recorder is ok)
- [ ] Make a presentation about your blog
- [ ] Follow the guidelines in the example-article.json for the
     URLs and services
- [x] friend querying via POSTs to <http://service/friends/userid>
- [ ] friend2friend querying via GETs to <http://service/author/><userid>/friends/<userid>
- [ ] implement author profiles via <http://service/author/userid>
- [x] Enforce some authentication
  - Consider HTTP Basic Auth
- [x] implement a restful API for <http://service/posts/postid>
  - a PUT should insert/update a post
  - a POST should insert the post
  - a GET with a postfixed "postid" should return the post
  - a GET without a postfixed "postid" should return a list of all "PUBLIC" visibility posts on your node
- [ ] FOAF verification involves the 3 hosts of the 3 friends
     A->B->C assuming A B C reside on different hosts.
- [ ] Allow users to accept or reject friend requests
- [x] friend requests can be made by POSTing a friend request to
     <http://service/friendrequest>
- [x] <http://service/author/posts> (posts that are visible to the currently authenticated user)
- [x] <http://service/author/{AUTHOR_ID}/posts> (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
- [ ] Images get the same protection that posts get as they are POSTS
- [ ] example-article.json is adhered to.
** Take-aways
- [ ] 1 Working Website
- [ ] 1 Github git repo
- [ ] 1 Presentation
- [ ] 1 Video

** Restrictions

- [ ] Use Python 3.6 (otherwise get approval)
- [ ] Use Django or Flask (otherwise get approval)
- [ ] Must run on one of the following:
  - [ ] provided VMs
  - [ ] Heroku
- [ ] License your code properly (use an OSI approved license)
  - Put your name on it!

** API Guidelines

   When building your API, try to adhere to these rules for easy compatibility with other groups:

- REST API calls may be prefixed. ie. <http://service_address/api/author/{AUTHOR_ID}/posts/>
- Document your service address, port, hostname, prefix(if used), and the username/password for HTTP
    Basic Auth(if used) in your README so that HTTP clients can connect to your API.
