# Concept composition and sync

> Source: https://essenceofsoftware.com/tutorials/concept-basics/sync/
> Fetched: 2026-08-28

In another tutorial, I showed a concept definition for Yellkey, a popular URL shortening service:

```
concept Yellkey
purpose shorten URLs to common words
principle
  if you register a URL u for t seconds
  and obtaining a shortening s, looking up s
  will yield u until the shortening expires
  t seconds from now
state
  used: set String
  shortFor: used -> one URL
  expiry: used -> one Date    
  const shorthands: set String
actions
  // register URL u for t seconds
  // resulting in shortening s
  register (u: URL, t: int, out s: String)
    s in shorthands - used
    s.shortFor := u
    s.expiry := // t secs after now
    used += s

  // lookup shortening s and get u back
  lookup (s: String, out u: URL)
    s in used
    u := s.shortFor

  // shorthand s expires
  system expire (out s: String)
    s.expiry is before now
    used -= s
    s.shortFor := none
    s.expiry := none
```

Although it's fairly simple and straightforward, there's something unsatisfying about this concept.

The criteria for concepts include being familiar and reusable. The essential functionality that this concept offers—shortening URLs—is common to many different shortening services, some freestanding (such as tinyurl.com) and others embedded in larger applications (eg, Google short URL option in Google Forms). But this concept would not be a good match for those other settings because it includes the expiration functionality.

What's going on here is that we seem to have two concepts: one about URL shortening and the other about expiry. Can we disentangle these?

# Factoring concepts

Here's how we might factor the Yellkey concept into two more basic and reusable concepts. First, we define a concept that provides shorthands:

```
concept Shorthand [Target]
purpose provide access via shorthand strings
principle
  after registering a target t and obtaining
  a shorthand s, looking up s will yield t:
  register (t, s); lookup (s, t') {t' = t}
state
  used: set String
  shortFor: String -> opt Target
  const shorthands: set String
actions
  register (t: Target, out s: String)
    s in shorthands - used
    s.shortFor := t
    used += s
  unregister (s: String)
    s in used
    used -= s
    s.shortFor := none
  lookup (s: String, out t: Target)
    s in used
    t := s.shortFor
```

This is just like our Yellkey concept, but the expiry-tracking functionality has been removed. Note also that I've made the concept polymorphic: it no longer translates shorthands into URLs, but into objects of some unspecified type Target. This would allow the Shorthand concept to be used in many more contexts; you could have shorthands for file paths in a file system, for example, or for commands in a user interface.

Now we turn the expiry-tracking functionality into its own concept:

```
concept ExpiringResource [Resource]
purpose handle expiration of short-lived resources
principle
  after allocating a resource r for t seconds,
  after t seconds the resource expires:
  allocate (r, t); expire (r)
state
  active: set Resource
  expiry: Resource -> one Date    
actions
  allocate (r: Resource, t: int)
    r not in active
    active += r
    r.expiry := // t secs after now
  deallocate (r: Resource)
    r in active
    active -= r
    r.expiry := none
  renew (r: Resource, t: int)
    r in active
    r.expiry := // t secs after now
  system expire (out r: Resource)
    r in active
    r.expiry is before now
    active -= r
    r.expiry := none
```

Again, I've made this polymorphic, so that any kind of resource can have its expiry tracked. This concept could be used to implement (the rather mean) control that turns off wifi access after the time paid for has passed.

And because I'm anticipating using this concept in a more general setting, I've included two additional actions that let you deallocate a resource before it expires, or renew it so that its life is extended.

# Composing concepts with syncs

Now we need to put our two concepts together to recover the functionality of our original Yellkey concept. We do this by first instantiating the concepts with the appropriate types:

```
app YellKey
  include HTTP
  include Shorthand [HTTP.URL] 
  include ExpiringResource [HTTP.URL]
```

I've included a concept called HTTP that I haven't specified that defines the URL type. In a fuller description of Yellkey, this concept would allow us to augment the lookup with a redirect.

With the concepts in hand, we now associate their actions through synchronizations:

```
  sync register (url: URL, short: String, life: int)
    when Shorthand.register (url, short)
    ExpiringResource.allocate (short, life)

  sync expire (out short: String)
    when ExpiringResource.expire (short)
    Shorthand.unregister (short)
    
  sync lookup (short: String, url: URL)
    Shorthand.lookup (short, url)
```

A synchronization (or "sync") constrains the executions of the concepts so that whenever one particular action occurs in one concept, some other actions occur in other concepts. So the first one says that when a shorthand is registered (in the Shorthand concept) that same shorthand is allocated as a resource (in the ExpiringResource concept). The second one says that when a shorthand expires (in ExpiringResource) it is unregistered (in Shorthand). The third sync includes only one action; its effect is just to make the lookup action (in Shorthand) available as an application action.

Concept actions that aren't mentioned in syncs don't occur in the application. Actions like Shorthand.unregister are excluded because Yellkey only lets you register shorthands and doesn't let you unregister them. Similarly, you can't renew a shorthand (even though the ExpiringResource includes an action to describe that functionality).

# Concept synergy

In any design, composing concepts brings to the whole (the overall app) the benefits of each of the parts (the constituent concepts). In some designs, something magical happens, and the benefit to the whole is more than the sum of the benefits of the parts. This is compositional synergy.

Such a synergy occurs here. You might think that composing with ExpiringResource would add only a limitation from the user's perspective: that a resource that would otherwise be free is now limited. But in this case, there is a real benefit that comes with this limitation. Because the shorthands have brief lifetimes, it's possible to serve the same size user base with a much smaller dictionary of possible shorthands (the set-valued shorthands component in Shorthand), and that means that the shorthands can all be familiar words.

# Another example: user sessions

Factoring Yellkey into more basic concepts may not seem very surprising since it's not (yet at least) a design pattern that is used elsewhere. But sometimes even a concept that seems to be a widely used pattern can profitably be broken down into more elemental concepts.

The standard functionality that governs website sessions is such a case. Although we could easily describe it as a single concept, we can expose more structure (along with more opportunities for reuse) by treating it as a composition.

First, let's define the most basic form of user authentication in which a user registers with a username and password and can later authenticate by entering the same username and password:

```
concept User
purpose authenticate users
principle
  after a user registers with a username and password,
  they can authenticate as that user by providing a matching
  username and password:
  register (n, p, u); authenticate (n, p, u') {u' = u}
state
  registered: set User
  username, password: registered -> one String
actions
  register (n, p: String, out u: User)
    u not in registered
    registered += u
    u.username := n
    u.password := p
  authenticate (n, p: String, out u: User)
    u in registered
    u.username = n and u.password = p
```

The state holds the set of registered users, and for each of them, a username and password. The register action allocates a user identity (which is an output of the action) and associates the provided name and password with it. The authenticate action has no effect on the state; its specification consists only of a precondition that the provided name and password match those of some registered user, whose identity is returned.

Now we define a separate concept to represent session management:

```
concept Session [User]
purpose authenticate user for extended period
principle
  after a session starts (and before it ends), 
  the getUser action returns the user identified at the start:
  start (u, s); getUser (s, u') {u' = u}
state
  active: set Session
  user: active -> one User
actions
  start (u: User, out s: Session)
    s not in active
    active += s
    s.user := u
  getUser (s: Session, out u: User)
    s in active
    u := s.user
  end (s: Session)
    active -= s
```

The state here holds the set of active sessions, and for each one, the user associated with it. There's an action to start a session, which takes a user and returns a fresh session identifier; an action to end a session; and an action (performed mid-session) that obtains the associated user.

Now we can assemble the conventional user session by synchronizing these two concepts:

```
concept UserSession
  include User
  include Session [User.User]
  
  sync register (username, password: String, out user: User)
    User.register (username, password, user)

  sync login (username, password: String, out user: User, out s: Session)
    when User.authenticate (username, password, user)
    Session.start (user, session)

  sync authenticate (s: Session, u: User)
    Session.getUser (s, u)

  sync logout (s: Session)
    Session.end (session)
```

The actions of the composition are:

- register: the user registers with a username and password; this is just the register action of the User concept;
- login: the user authenticates with a username and password (in the User concept) and a fresh session is allocated (in the Session concept);
- authenticate: the user is spontaneously authenticated mid-session by the execution of the getUser action of Session;
- logout: the user closes the session with the end action of Session.

# Concepts are abstract

It's important to understand that a concept describes a pattern of behaviors that users may observe. It may be implemented in a single computing device, but that is not necessary. The state may be distributed, with even a single component spread across nodes, and the actions likewise can be performed at different locations.

In a standard web stack, the User and Session states are both stored on the server. To enable the client to present a session identifier to the server, there is usually an additional piece of distributed state, which could be modeled like this:

```
cookies: Client -> opt Session
```

Each client is optionally associated with a session identifier; this information is typically stored in a cookie that the server sends to the client browser that is then set aside and sent back to the server with every request to its domain.

Actions likewise are abstractions, and a single action typically corresponds to a (potentially elaborate) sequence of steps. For example, when the user executes login, the following steps typically occur:

- The user enters a username and a password in a web form and clicks the submit button;
- The client program running in the user's browser makes an HTTP request to the server with this data;
- A controller method executes in the server, and requests are made to a database, often running on another machine;
- The session identifier is returned, encrypted, in a cookie to the client, which saves the cookie locally.

# Why more basic concepts are better

To see why factoring this functionality into two concepts makes sense, consider some variant designs:

- **Biometric authentication.** Suppose the user logs in not with a username and password, but rather using some biometric property. To accommodate this, we can just swap out the password based authentication for a biometric authentication concept. The Session concept remains unchanged.
- **Mid-session authentication.** Some apps that have sessions still require an explicit user authentication in the middle of a session for extra security. For example, if you try to execute a large financial transaction on a banking app, you will typically be required to enter your username and password again even if you're already logged in. This is easily accommodated with the existing authenticate action in User. If we hadn't had a separate concept, we would have needed to add a new action.
- **Non-session authentication.** Some situations use authentication without sessions at all. For example, some apps let you unsubscribe from a service by clicking on a link that opens a browser but then requires you to enter your username and password to perform that one action. And operating systems often require you to authenticate for certain actions: MacOS requires authentication for opening apps for the first time, for example, and for any action that requires superuser status. This functionality would require the creation of the User concept if it hadn't already been defined.

# Making sessions expire

It's regarded as good security practice to terminate sessions automatically after some time has passed. This is especially important when the app is running on a public machine, and if a user forgot to check out, the next user would be able to use their existing session.

How can we achieve this? You saw this coming: we can use our friend the ExpiringResource concept. All we need to do is treat sessions as resources, allocating them when sessions start, and ending sessions when the resources expire:

```
concept ExpiringUserSession
  include User
  include Session [User.User]
  include ExpiringResource [Session.Session]
  
  sync register (username, password: String, out user: User)
    User.register (username, password, user)

  sync login (username, password: String, out user: User, out s: Session)
    when User.authenticate (username, password, user)
    Session.start (user, session)
    ExpiringResource.allocate (session, 300) // set expiration to 5 mins

  sync logout (s: Session)
    when Session.end (session)
    ExpiringResource.deallocate (session)
    
  sync authenticate (s: Session, u: User)
    Session.getUser (s, u)

  sync terminate (s: Session)
    when ExpiringResource.expire (s)
    Session.end (s)
```
