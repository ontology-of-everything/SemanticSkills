# 概念规格说明的结构(Structure of a concept specification)

> Source: https://github.com/61040-fa25/concept_backend/blob/main/design/background/concept-specifications.md
> Fetched: 2026-08-28

说明:术语首次出现时保留英文原词——concept(概念)、purpose(目的)、principle / operational principle(操作原理)、state(状态)、actions(动作)、queries(查询)、system action(系统动作)。文中的规格片段与代码示例按原文原样保留,不作翻译。

一个 concept(概念)按以下结构进行规格说明:

- **concept**:一个描述性的名称,在使用上的通用性与恰当的具体性之间取得平衡
- **purpose**:该概念存在的理由,以及它所赋能的事情
- **principle**:一个动机场景,确立该概念在典型情况下如何达成其 purpose
- **state**:对概念所存储状态的描述,即执行中的概念对已发生动作所记住的内容
- **actions**:一组以传统前置/后置条件(pre/post)风格规定的动作,对应概念执行过程中所采取的各个步骤。

## 概念名称与类型参数(Concept name and type parameters)

concept 部分给出概念的*名称*,以及一个*类型参数*列表。这些类型参数用于在概念外部创建的对象的类型,概念必须以完全多态的方式对待它们(也就是说,概念不能假定它们具有任何属性,只能对其进行比较,以判断该类型的两个实例是否为同一个标识符/引用、从而代表同一个对象)。

例如,下面这个 concept 部分

**concept** Comment \[User, Target\]

把概念命名为 *Comment*,并声明它的 state 与 actions 将引用两个外部定义的泛型类型的值:*User*(后面会用来引用评论的作者)与 *Target*(后面会用来引用每条评论的目标)。取决于概念被使用的上下文,*User* 类型的值很可能是由某个用户认证或用户资料概念生成的注册用户的身份标识;*Target* 类型的值可能是帖子或评论的身份标识,或任何被评论的对象。

## 概念的 purpose(Concept purpose)

*purpose* 用一个简短的短语或句子定义该概念存在的动机,以及它所服务的需求。purpose 常常是显而易见的,比如 *Comment* 概念的 purpose:

**purpose** associate some text with another artifact (usually itself textual) that remarks on, augments or explains it
(译:把一段文本与另一个制品(通常本身也是文本)相关联,以对其进行评述、补充或解释)

有时 purpose 看似显而易见,实际上却比许多用户最初以为的更微妙。例如,*Trash*(回收站)概念的 purpose 是:

**purpose** support deletion of items with possibility of restoring
(译:支持删除条目,并保留恢复的可能性)

回收站由 Apple 在 1980 年代为 Lisa 引入,如今在众多应用中广泛使用。它的 purpose 并不是支持删除条目,而是支持*反删除*(undeletion),因为回收站的全部意义就在于被删除的条目可以被恢复。

有时 purpose 是微妙的。例如,*ParagraphStyle*(段落样式)概念(见于许多文档处理工具,如 Microsoft Word)的 purpose 是:

**purpose** make consistent changes to formatting of a document easy
(译:让对文档格式进行一致的修改变得容易)

这一 purpose 是通过在 state 中维护段落与其样式之间的关联来达成的:修改某个段落样式会导致所有关联段落的格式随之更新。你也许以为其 purpose 是允许把预定义格式应用到段落上——这一目的确实也被满足了,但它不是定义性的 purpose,因为那个更简单的目的可以由一个更基础的概念来实现:该概念只保存一组样式及其格式,而不维护段落与样式之间的任何关联。

一个好的 purpose 应满足以下标准:
- **聚焦需求(Need-focused)**。purpose 应以用户的需求来陈述。例如,_Upvote_(点赞/顶)概念的 purpose 不应是"表达你对某条目的认可",因为那没有实际收益;更好的 purpose 可以是"利用众包的认可对条目进行排序"。
- **具体(Specific)**。purpose 应针对当前概念的设计。例如,尽管 Gmail 中的 _Autocomplete_(自动补全)概念可能让应用对消费者更有吸引力,但说它的 purpose 是"扩大 Gmail 用户群"并无用处,因为想必所有概念都有这个目标;更好的 purpose 可以是"节省用户的输入操作"。
- **可评估(Evaluable)**。purpose 应能作为衡量概念设计的标尺。例如,*Trash* 概念的一个好 purpose 是"允许反删除";看似相近的 purpose"防止误删"则不好,因为要按这个目标评估概念设计,需要对用户行为做出各种假设。

## 概念的 principle(Concept principle)

*operational principle*(操作原理,或简称 *principle*)是一个典型场景,解释概念如何达成其 purpose。

解释某个事物如何运作,一种有说服力的方式是讲一个故事。不是随便什么故事,而是一种具有定义性的故事:通过一个典型场景,展示这个事物为何有用、如何达成其 purpose。

- 例如,Minuteman 图书馆网络提供了一项很棒的服务:如果我请求借阅一本书,那么当这本书在我本地的图书馆可借时,我会收到一封电子邮件,通知我可以去取书了。

注意这个场景的形式:_如果_你执行某些动作,_那么_会出现某个满足有用目的的结果。许多机制都可以用这种方式描述:

- 如果你在工作期间每月缴纳社保,那么退休后你将从政府获得一份基本收入。
- 如果你把一片面包放进烤面包机并按下手柄,那么几分钟后手柄会弹起,你的面包就烤好了。
- 如果你成为某人的朋友,而后对方发布了一个条目,你就能看到它。

以下是一些 principle 的例子:

- **Password(密码)**。如果你用某个用户名和密码注册,之后又用同一个用户名和密码登录,你就会被认证为当初注册的那个用户。
- **Personal access token(个人访问令牌)**。如果你为某个资源创建一个访问令牌并交给另一个用户,那么该用户输入令牌字符串即可获得访问权;但如果你吊销(revoke)该令牌,此后对方将无法再获得访问权。

注意,principle 并不总是最简单的场景。以 *PersonalAccessToken* 为例,把令牌被吊销后会发生什么包含进来非常重要,因为"能够吊销令牌"是这个概念的本质所在,也是它与 *Password* 概念的区别。比如,如果你用普通密码把自己账户的访问权交给另一个用户,那么一旦共享出去,阻止对方继续访问的唯一办法就是改密码,而这会给你自己(以及所有其他共享了该密码的人)带来不便。

再举一个例子,*ParagraphStyle* 概念的 principle:

**principle** after a style is defined and applied to multiple paragraphs, updating the style will cause the format of all those paragraphs to be updated in concert
(译:定义一个样式并将其应用到多个段落之后,更新该样式会使所有这些段落的格式协同更新)

一个好的 principle 应满足以下标准:
- **聚焦目标(Goal focused)**。principle 应展示 purpose 是如何被达成的。例如,既然 *Trash* 概念的 purpose 是允许恢复已删除的条目,那么其 principle 就不能只包含删除而没有随后的恢复。
- **有区分度(Differentiating)**。principle 应能把该概念的功能与其他概念(尤其是更简单的概念)区分开。例如,*PersonalAccessToken* 的 principle 必须包含令牌的吊销,因为那是这一设计的动机所在,也是它区别于更简单的 *Password* 概念之处;*ParagraphStyle* 概念的 principle 必须包含不止一个段落被同一样式修饰,否则就无法展示"一次更新多个段落格式"的能力。
- **典型(Archetypal)**。principle 不应包含那些对展示概念如何达成 purpose 并非必需的边角情形。例如,*RestaurantReservation*(餐厅预订)概念的 principle 应包含预订餐桌并最终入座,但不需要包含预订被取消的可能性,尽管概念中会包含支持取消的动作。之所以不需要这些情形,是因为 state 与 actions 部分已完整定义了概念的行为,从而隐式定义了所有可能的场景;principle 的职责是指出那个驱动设计、并展示 purpose 如何达成的本质场景。

## 概念的 state(Concept state)

概念的 state 是一个数据模型,表示执行中的概念的所有可能状态的集合。例如,一个用于认证用户的概念,其 state 可以这样声明:

	a set of Users with
		a username String
		a password String

这表示 state 包含一个用户集合,并为每个用户关联一个 username 和一个 password,二者都是字符串。用数学语言来说,这表示存在一个用户集合和两个关系——一个叫 username,一个叫 password——它们都是从用户到字符串的关系。state 中的每个值要么是原始值(如数字、布尔值或字符串),要么是实体值(如某个用户)。实体值应被视为身份标识或引用。

### 关注点分离与不同视图(Separation of concerns and different views)

虽然可以把上面这样的声明理解为定义了一组复合对象(带有 username 和 password 字段的用户),但这种理解并不完全可靠,因为它无法解释概念的 state 可以表示同一对象的不同侧面这一事实。例如,一个独立的 *UserProfile* 概念的 state 可以包含这样的声明

	a set of Users with
		a bio String
		a thumbnail Image

为每个用户关联一段简介(bio)和一张头像缩略图(thumbnail)。这两处声明描述的是用户的不同属性,最好把它们理解为用户的不同视图,或数据模型的一种划分。这种关注点分离是概念设计的核心特征,用传统面向对象的观念很难解释,因为后者要求一个对象只有一个全局定义。

## 概念的 actions(Concept actions)

概念执行时,其可观察行为由交错出现的事件与查询序列构成。事件是 *actions*(动作)的实例,通常是 state 的修改者。概念规格说明总是包含其动作的定义。相比之下,queries(查询)通常由 state 隐式定义,不需要显式规定,见下文相关小节。

一些动作的例子:
- *UserAuthentication* 概念:register、login、logout
- *RestaurantReservation* 概念:reserve、cancel、seat、noShow
- *Trash* 概念:delete、restore、empty
- *Labeling* 概念:addLabel、removeLabel
- *Folder* 概念:createFolder、delete、rename、move

如果 state 需要以领域特定的方式初始化,就需要相应的动作。例如,如果 *RestaurantReservation* 概念只使用固定时间段(比如允许在任何一天的 18 点到 22 点之间预订),那么这一假设可以硬编码到概念行为中;但如果 *RestaurantReservation* 概念只允许在餐厅老板预设的时间内预订,就必须包含用于设置可预订时段的动作。

### 动作的参数与结果(Action arguments and results)

动作可以有输入参数和结果。例如,*UserAuthentication* 概念的 *register* 动作可以写成

	register (username: String, password: String): (user: User)

它表示 register 动作的每次发生都以一个用户名字符串和一个密码字符串作为输入,并以(某个)用户(的标识符)作为输出返回。

在概念规格说明中,所有参数和结果都是具名的,并且允许多个结果。错误与异常被当作普通结果来对待。因此,为了表示 register 动作可能失败,我们可以声明该动作的一个重载版本,返回一个错误字符串:

	register (username: String, password: String): (error: String)

与 ML 这类函数式语言的模式匹配语法类似,概念规格说明可以为同一个动作名声明多种形式,只要它们的参数/结果名互不相同。做设计时通常不规定错误情形;为实现编写概念规格时则要包含它们。

用 TypeScript 代码实现动作时,每个动作表示为一个方法,它以一个字典对象作为输入,并返回一个字典对象作为输出。字典对象的字段即输入参数名和结果名。

### 空结果(Empty results)

注意,在实现中,成功的执行*必须*返回一个字典(但可以是空字典)。空字典可以用来表示成功完成;但如果该动作同时存在一个返回错误的重载版本,则成功情形必须返回非空字典。因此下面是合法的

	register (username: String, password: String): (user: User)
	register (username: String, password: String): (error: String)

而下面是不合法的

	register (username: String, password: String)
	register (username: String, password: String): (error: String)

因为非错误情形(隐式地)返回空字典。由于 sync(同步)支持不指定参数名的部分匹配,一个未指定结果名的部分模式会同时匹配这两种情形,从而无法区分成功的非错误情形。

### 前置条件与后置条件(Pre and post conditions)

每个动作的详细行为以经典的前置/后置(pre/post)形式规定。前置条件以关键字 *requires* 标注,规定允许执行的条件,是对 state 和输入参数的约束;后置条件以关键字 *effects* 标注,规定执行结果(返回值与新 state),是对输入、执行前 state、执行后 state 及输出的约束。

例如,下面是 *Counter*(计数器)概念的规格说明:

**concept** Counter

**purpose** count the number of occurrences of something

**principle** after a series of increments, the counter reflects the number of increments that occurred

**state**
  count: Number = 0

**actions**
  increment ()
    **requires** true
    **effects** count := count + 1

  decrement ()
    **requires** count > 0
    **effects** count := count - 1

  reset ()
    **requires** true
    **effects** count := 0

注:
- 大多数前置条件是 true:这意味着动作随时可以发生。
- 后置条件写成了赋值形式,但也可以用非形式化的方式书写。例如,increment 的后置条件可以写成"把计数加一";也可以采用更声明式的风格,写成"执行后的计数比执行前多一"。
- 一般而言,动作规格以非形式化方式书写,并默认框架条件(frame conditions,即未提及的任何 state 组件都不被更新)。

### 用户动作与系统动作(User and system actions)

动作可以由用户执行(或作为经由 synchronization(同步)转发的用户请求的结果),也可以由系统自主执行。前文提到的所有动作都是用户动作,这也是默认情形。要把某个动作标记为 system action(系统动作),用 *system* 关键字标注,如下:

**system** notifyExpiry ()
**requires** the current time is after *expiryTime* and *notified* is false
**effects** set *notified* to true

注意,该前置条件允许动作在计时器到期后的任何时刻发生,但在实践中,实现应让这类动作尽早发生。

### 前置条件即触发条件(Preconditions are firing conditions)

前置/后置的规格写法是约定俗成的,与许多规格语言使用的是同一套。但要注意,在其中大多数语言里,前置条件是对调用方的一种*义务*(obligation):也就是说,前置条件为假时动作仍*可以*执行,只是结果不确定。

与之相反,在概念规格中,*前置条件是触发条件*(firing conditions)。这意味着当前置条件为假时,动作绝不可能发生。对于系统动作,前置条件指明了它们应当在何时发生。

## 概念的 queries(Concept queries)

queries(查询)是对概念 state 的读取。在设计层面通常不使用显式的查询规格,但在面向代码的概念规格中,所有可能用到的查询都应当被规定出来。
例如,对于具有如下 state 的 *UserProfile* 概念

	a set of Users with
		a username String
		a password String

可以定义查询来提取某个用户的用户名和密码:

**queries**
	\_getUsername (user: User) : (username: String)
		**requires** user exists
		**effects** returns username of user

	\_getPassword (user: User) : (password: String)
		**requires** user exists
		**effects** returns password of user

有些查询会返回多个对象。例如,群组包含用户集合

	a set of Groups with
		a users set of User

那么可以定义一个查询,接收一个群组并返回其中的用户集合:

**queries**
	\_getUsers (group: Group) : (user: User)
		**requires** group exists
		**effects** returns set of all users in the group

注意,与动作不同,查询可以返回结构化对象。例如,基于上面用户与群组的定义,我们可以定义查询

	\_getUsersWithUsernamesAndPasswords (group: Group) : (user: {username: String, password: String})
		**requires** group exists
		**effects** returns set of all users in the group each with its username and password

它返回一个用户集合,其中每个用户都带有 username 和 password 属性。

## 概念不是对象(Concepts are not objects)

一个常见误解是把概念等同于面向对象编程中的对象。关键区别如下:
- 概念在其 state 中保存的是与它所体现的行为关注点相关的*所有*对象的集合,而不是单个对象的属性。
- 因此,概念的规格说明没有构造函数;对象改由动作来分配。
- 概念必须体现与某一行为关注点相关的全部功能;而对象常常依赖其他对象才能运转。
- 概念分离关注点;而面向对象编程中的对象倾向于把与某类对象相关的所有属性和方法聚合在一起。

为了说明这些区别,考虑这样一个功能:把标签(label)关联到条目(item)上,然后检索匹配某个标签的条目。例如 Gmail 用这一功能来组织邮件。在面向对象设计中,可能会有一个 *EmailMessage* 类,其实例变量保存一个标签数组;一个 *Label* 类,其实例变量保存标签的字符串名称;以及一个 *Mailbox* 类,其实例变量保存一个 *EmailMessage* 对象数组。

与之相对,在概念设计中,我们会只用一个概念,例如叫 *Labeling*,其 state 是从泛型条目到标签集合的映射:

**concept** Labeling \[Item\]
**state**
  a set of Items with
    a labels set of Label
  a set of Labels with
    a name String
**actions**
  createLabel (name: String)
  addLabel (item: Item, label: Label)
  deleteLabel (item: Item, label: Label)

注:
- *Labeling* 概念在其 state 中包含被打标签的全部条目集合(该 state 组件实际上就是一个从条目到标签的关系)
- *Item* 类型是泛型的,运行时可以用任意类型实例化(比如邮件)
- 与面向对象的情形不同,这里没有关注点的混杂。这个概念只处理打标签这一件事;而在 OO 的情形中,*EmailMessage* 类持有标签实例变量,从而把打标签与邮件的其他功能混在了一起。
- 这个概念在行为上是完整的;而 OO 情形中的 *Label* 类单独并不可用。特别地,这个概念支持标签的添加、删除和查询;在 OO 设计中,添加和删除属于 *EmailMessage* 类,按标签查询则要同时涉及 *Mailbox* 与 *EmailMessage* 两个类。

尽管有上述种种差异,概念通常仍以面向对象的类来实现。运行时通常只有一个概念实例,负责处理所有相关对象。这个实例通过调用实现该概念的类的构造函数来创建。
