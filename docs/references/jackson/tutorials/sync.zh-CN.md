# 概念组合与同步（Concept composition and sync）

> Source: https://essenceofsoftware.com/tutorials/concept-basics/sync/
> Fetched: 2026-08-28

在另一篇教程中，我给出了 Yellkey——一个流行的 URL 缩短服务——的概念（concept）定义：

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

尽管这个概念相当简单直接，但它有些令人不满意的地方。

概念的判据包括熟悉性和可复用性。这个概念提供的核心功能——缩短 URL——在许多不同的缩短服务中都很常见，有些是独立服务（如 tinyurl.com），有些则内嵌在更大的应用中（如 Google Forms 中的 Google 短链接选项）。但这个概念并不适合那些其他场景，因为它包含了过期功能。

这里的情况是：我们似乎有两个概念，一个关于 URL 缩短，另一个关于过期。我们能把它们解开吗？

# 拆分概念

以下是我们把 Yellkey 概念分解为两个更基本、更可复用的概念的方法。首先，我们定义一个提供简称（shorthand）的概念：

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

这与我们的 Yellkey 概念几乎一样，只是去掉了过期追踪功能。还要注意，我把这个概念做成了多态的：它不再把简称翻译为 URL，而是翻译为某个未指定类型 Target 的对象。这样 Shorthand 概念就能用于更多的上下文；比如你可以为文件系统中的文件路径设置简称，或为用户界面中的命令设置简称。

现在我们把过期追踪功能变成它自己的概念：

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

同样，我把它做成了多态的，这样任何类型的资源都可以被追踪过期。这个概念可以用来实现（相当刻薄的）在已付费时间用完后切断 WiFi 访问的控制。

而且，由于我预期会在更一般的场景中使用这个概念，我加入了两个额外的动作（actions）：让你可以在资源过期前释放它，或者续期以延长其寿命。

# 用同步组合概念

现在我们需要把两个概念组合起来，恢复原始 Yellkey 概念的功能。我们首先用适当的类型实例化这些概念：

```
app YellKey
  include HTTP
  include Shorthand [HTTP.URL] 
  include ExpiringResource [HTTP.URL]
```

我引入了一个未加规格说明的 HTTP 概念，它定义了 URL 类型。在对 Yellkey 更完整的描述中，这个概念还能让我们为查找操作增加重定向功能。

有了这些概念，我们现在通过同步（synchronization/sync）把它们的动作关联起来：

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

同步（sync）约束各概念的执行，使得每当某个特定动作在一个概念中发生时，其他一些动作也在别的概念中发生。所以第一条同步说：当一个简称被注册时（在 Shorthand 概念中），这个简称同时被作为资源分配（在 ExpiringResource 概念中）。第二条说：当一个简称过期时（在 ExpiringResource 中），它被注销（在 Shorthand 中）。第三条同步只包含一个动作；它的作用只是把 lookup 动作（在 Shorthand 中）暴露为应用层的动作。

未在同步中提及的概念动作不会在应用中发生。像 Shorthand.unregister 这样的动作被排除在外，因为 Yellkey 只允许你注册简称，不允许注销。同样，你也不能给简称续期（尽管 ExpiringResource 包含描述该功能的动作）。

# 概念协同

在任何设计中，组合概念都会把各个部分（组成概念）的好处带给整体（整个应用）。而在某些设计中，会发生某种奇妙的事情：整体获得的好处大于各部分好处之和。这就是组合协同（compositional synergy）。

这里就出现了这样一种协同。你可能认为与 ExpiringResource 组合只会从用户视角引入一种限制：原本可以永久使用的资源现在受限了。但在这个案例中，这种限制带来了真实的好处。因为简称的生命周期很短，就可以用小得多的候选简称字典（Shorthand 中集合值的 shorthands 组件）服务同样规模的用户群，这意味着所有简称都可以是常见的单词。

# 另一个例子：用户会话

把 Yellkey 拆分成更基本的概念可能看起来并不令人意外，因为它（至少目前）还不是在别处被广泛使用的设计模式。但有时，即使一个看似已被广泛使用的模式化概念，也能有益地分解为更基本的概念。

管理网站会话的标准功能就是这样一个例子。虽然我们完全可以把它描述为单个概念，但把它当作一个组合来处理，可以暴露出更多结构（以及更多复用机会）。

首先，我们定义最基本形式的用户认证：用户用用户名和密码注册，之后可以通过输入同样的用户名和密码来认证：

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

状态（state）保存已注册用户的集合，以及每个用户对应的用户名和密码。register 动作分配一个用户身份（作为该动作的输出），并把提供的名字和密码与之关联。authenticate 动作对状态没有影响；它的规格只包含一个前置条件：提供的名字和密码与某个已注册用户的相匹配，并返回该用户的身份。

现在我们定义一个单独的概念来表示会话管理：

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

这里的状态保存活跃会话的集合，以及每个会话关联的用户。有一个开始会话的动作，它接收一个用户并返回一个新的会话标识符；一个结束会话的动作；还有一个（会话中执行的）获取关联用户的动作。

现在我们可以通过同步这两个概念，组装出常规的用户会话：

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

该组合的动作是：

- register：用户用用户名和密码注册；这就是 User 概念的 register 动作；
- login：用户用用户名和密码进行认证（在 User 概念中），同时分配一个新会话（在 Session 概念中）；
- authenticate：通过执行 Session 的 getUser 动作，用户在会话中被自动认证；
- logout：用户通过 Session 的 end 动作关闭会话。

# 概念是抽象的

必须理解的是：概念描述的是用户可能观察到的行为模式。它可以在单个计算设备上实现，但这并非必需。状态可以是分布式的，甚至单个组件也可以分散在多个节点上；同样，动作也可以在不同位置执行。

在标准 Web 技术栈中，User 和 Session 的状态都存储在服务器上。为了让客户端能向服务器出示会话标识符，通常还有一块额外的分布式状态，可以这样建模：

```
cookies: Client -> opt Session
```

每个客户端可选地关联一个会话标识符；这一信息通常存储在服务器发送给客户端浏览器的 cookie 中，浏览器保存它，并在向该域名发出的每个请求中把它发回服务器。

动作同样是抽象；单个动作通常对应一个（可能相当繁复的）步骤序列。例如，当用户执行 login 时，通常会发生以下步骤：

- 用户在 Web 表单中输入用户名和密码并点击提交按钮；
- 运行在用户浏览器中的客户端程序携带这些数据向服务器发出 HTTP 请求；
- 服务器中的某个控制器方法执行，并向数据库发出请求，数据库常常运行在另一台机器上；
- 会话标识符以加密形式放在 cookie 中返回给客户端，客户端把 cookie 保存在本地。

# 为什么更基本的概念更好

要理解为什么把这一功能拆分为两个概念是合理的，考虑几个变体设计：

- **生物特征认证。** 假设用户不用用户名和密码登录，而是用某种生物特征。为适应这一点，我们只需把基于密码的认证换成一个生物特征认证概念。Session 概念保持不变。
- **会话中认证。** 一些有会话的应用为了额外的安全性，仍要求在会话进行中做一次显式的用户认证。例如，在银行应用中执行大额金融交易时，即使你已经登录，通常也会被要求再次输入用户名和密码。这用 User 中已有的 authenticate 动作就能轻松满足。如果我们没有把它拆成单独的概念，就得新增一个动作。
- **无会话认证。** 有些场景完全不使用会话，只使用认证。例如，有些应用允许你通过点击一个链接来退订某项服务：链接打开浏览器，但随后要求你输入用户名和密码以执行这一个动作。操作系统也常常要求你为某些动作进行认证：例如 MacOS 在首次打开应用时要求认证，任何需要超级用户权限的动作也要求认证。如果 User 概念尚未定义，这类功能就需要把它创建出来。

# 让会话过期

在一段时间后自动终止会话被视为良好的安全实践。当应用运行在公共机器上时这尤其重要——如果用户忘记退出，下一位用户就能使用他们已有的会话。

我们该怎么实现？你已经猜到了：可以用我们的老朋友 ExpiringResource 概念。我们只需把会话当作资源，在会话开始时分配它们，并在资源过期时结束会话：

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
