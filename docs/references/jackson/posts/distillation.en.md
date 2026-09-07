# The Essence of the Essence

> Source: https://essenceofsoftware.com/posts/distillation/
> Fetched: 2026-08-28

This article summarizes the key ideas in the book The Essence of Software. It is not intended to be understandable by itself. It gives almost no examples, makes claims without justifying them, and cites almost no related work. And it's not nearly so much fun to read as the book :-). But, hey, at least it's short(ish)!

If you haven't read the book, I recommend that you don't start with this, but watch my ACM talk instead. But perhaps you don't really want to read the book, and just want to be able to hold your own at a cocktail party showing off your sophistication in software design. In that case, this may be for you.

If you've read the book, this summary should be a useful reminder of the key ideas, to help you solidify them in your mind and relate them to other approaches. In this sense, it augments the shorter list of provocative questions in Chapter 12 of the book.

A final warning before you jump in: this summary assumes a fairly extensive background in software design and development. The book itself is aimed at a broader audience, introduces the ideas more gently by way of example, and relegates the harder technical stuff to end notes.

## Defining Software Design

In most fields, "design" means shaping an artifact to meet the needs of users, thus sitting at the boundary between humans and machines. Despite Kapor's notable manifesto in 1990, and the book edited by Winograd that followed in 1996, little attention has been paid to software design.

Enormous effort, in contrast, has been devoted to software engineering (whose interest instead is software's internal structure and means of construction). This disparity of attention has resulted in great advances in programming, represented by a major body of knowledge and well-known design principles.

The field of human-computer interaction has likewise produced an impressive body of knowledge about user interfaces and how they shape the way we understand and use software. But for software design, where the focus is on the fundamental abstractions that underlie both the interface and the implementation, our knowledge is much more limited, and we have had to be content with being guided instead by vaguer notions, and (albeit sensible) appeals to simplicity and clarity.

## The Book's Aims and Approach

The aims of the book are to highlight a central aspect of software design; to lay out a way to structure and express software designs from this perspective; to provide some heuristics and principles for design; and, more generally, to inspire a renewed focus on software design as a discipline.

The book is driven by examples drawn from over 100 apps. By focusing on widely used software produced by the best companies, it seeks to show that serious problems are rife, and challenge even the most talented developers, and that the book's ideas and techniques apply to real software.

The book presents a design approach comprising simple textual and diagrammatic notations, a collection of readily applicable heuristics, and some deeper principles. In order to explain the approach in more detail, and to show how it differs from many prior approaches, a collection of end notes is included covering topics from design thinking to formal methods.

## The Problem

Software is harder to use than it needs to be. We spend an increasing portion of our lives engaged with software apps and systems, so improving the design of software impacts the quality of our lives and our ease of working effectively together.

As software becomes an ever more critical part of our civic infrastructure, we rely on apps and systems to behave predictably and reliably. A high proportion of failures are due to user errors, for which poor design is usually to blame. And even when a failure is attributed to a bug in the code, it is likely that the bug is due to lack of clarity in design (rather than a simple failure to meet a specification).

Lack of clarity in software design also makes software harder to build, and leads to degradation over time as accretions to a codebase compromise its modularity yet further.

## Levels of Design

Software design activities and criteria can be assigned to three levels: physical, which concerns the choice of colors, type, layout, etc, and is influenced by particular human anatomical and cognitive capabilities; linguistic, which concerns the use of icons and labels, terminology, etc, and is dependent on shared cultural and linguistic assumptions; and conceptual, which concerns the underlying semantics of the application, including the actions that can be performed and the effects they have, and the structure and interpretation of the state as viewed by the user.

The conceptual level is the most fundamental; different physical and linguistic designs for an app might be equally effective, but even small changes to the conceptual design are usually very disruptive to users. Users' problems with apps arise more often from incorrect conceptual understandings than from an inability to interpret the physical and linguistic signals of the user interface.

This is due in part to the great advances that have been made in the last decades at the physical and linguistic levels. Many books and online collections of heuristics teach user interface design very effectively, and given also that many client-side frameworks now provide professionally designed widgets, there is little excuse nowadays for a design that fails at these levels.

## Prior Work on Conceptual Design

The importance of the conceptual level has been recognized for more than half a century. From early on, researchers noted the importance of a user's "mental model", and the need for the design to construct such a model explicitly, so that the user's model and the system model coincide. Fred Brooks coined the term "conceptual integrity" and argued that the conceptual aspects of software design represented the essence of the field, as opposed to the accidental aspects, to which he relegated the concerns of "representation." The fields of conceptual modeling, domain modeling and formal methods all emphasized the centrality of an abstract model of state (and, in the case of formal methods, also behavior) in the design of software.

And yet none of these fields expressly addressed the problem of designing the conceptual structure of software in order to meet the needs of the user and to align the user's understanding. Formal methods focused primarily on the problem of correctness, and ensuring conformance of the implementation to the model. Conceptual modeling and domain modeling focused primarily on the representation of knowledge about the context of operation of a system, rather than on the structures that the designer invented.

Most curiously missing was a well defined notion of "concept." Even in the field of conceptual modeling, there is no shared understanding of what a concept might be, or even well-known candidate definitions. An entire conceptual model seems to be too large to count as a single concept, and its constituent entities (or classes or objects) are too small, especially since an informal understanding of a concept tends to involve relationships amongst multiple elements.

## A New Definition of Concept

A concept is a reusable unit of user-facing functionality that serves a well-defined and intelligible purpose. Each concept maintains its own state, and interacts with the user (and with other concepts) through atomic actions. Some actions are performed by users; others are output actions that occur spontaneously under the control of the concept.

A concept typically involves objects of several different kinds, holding relationships between them in its state. For example, the Upvote concept, whose purpose is to rank items by popularity, maintains a relationship between the items and the users who have approved or disapproved of them. The state of a concept must be sufficiently rich to support the concept's behavior; if Upvote lacked information about users, for example, it would not be able to prevent double voting. But the concept state should be no richer than it need be: Upvote would not include anything about a user beyond the user's identity, since the user's name (for example) plays no role in the concept's behavior.

## Concept Reuse and Familiarity

Most concepts are reusable across applications; thus the same Upvote concept appears for upvoting comments in the New York Times and for upvoting answers on Stack Overflow. A concept can also be instantiated multiple times within the same application.

This archetypal nature of concepts is essential. From the user's perspective, it gives the familiarity that makes concepts easy to understand: a user encountering the same context in a new setting brings their understanding of that concept from their experience in previous settings.

From a designer's perspective, it allows concepts to be repositories of design knowledge and experience. When a developer implements Upvote, even if they can't reuse the code of a prior implementation, they can rely on all the discoveries and refinements previously made. Many of these are apparent in the behavior of the concept itself, but others are associated with the implementation, or are subtle enough to need explicit description. The community of designers could develop "concept catalogs" that capture all this knowledge, along with relationships between concepts (for example, that Upvote often relies on the Session concept for identifying users, which itself is associated with the User concept for authenticating users).

## Concept Independence

Perhaps the most significant distinguishing feature of concepts, in comparison to other modularity schemes, is their mutual independence. Each concept is defined without reference to any other concepts, and can be understood in isolation.

Early work on mental models established the principle that, in a robust model, the different elements must be independently understandable. The same holds in software: the reason a user can make sense of a new social media app, for example, is that each of the concepts (Post, Comment, Upvote, Friend, etc) are not only familiar but also separable, so that understanding one doesn't require understanding another.

Concept independence lets design scale, because individual concepts can be worked on by different designers or design teams, and brought together later. Reuse requires independence too, because coupling between concepts would prevent a concept from being adopted without also including the concepts it depends on.

Polymorphism is key to independence: the designer of a concept should strive to make the concept as free as possible of any assumptions about the content and interpretation of objects passed as action arguments. Even if a Comment concept is used within an app only for comments on posts, it should be described as applying comments to arbitrary targets, defined only by their identity.

Pushing polymorphism as far as possible is a useful strategy: for getting to the essence of a concept; for finding other opportunities to use a concept within the same app (and in other apps); for discovering that what appears to be an app-specific concept is actually a general and familiar one; and, when it's not possible, for identifying concept subtleties or design flaws.

Concepts can be implemented independently also; in the Deja Vu platform, Santiago Perez De Rosso showed how apps could be constructed by glueing together reusable, full-stack concepts drawn from a library.

## A Structure for Describing Concepts

To work with concepts, we need a simple structure for describing them. A concept is defined by its behavior, which comprises its state space and a set of actions. These can be defined using standard methods and notations.

For defining the state space, a data model is given that consists of a collection of components, each of which is a scalar/option, set or relation (of any arity). This model can be recorded with textual declarations or as an extended entity-relationship diagram. The details of the data model are not fundamental to concepts, and different models could be used. What is important is that the state of a concept is (by default) visible to users, so states should make sense to users (and at the very least should be defined explicitly in the spirit of "model-based specification" rather than implicitly by algebraic axioms).

Actions can be initiated by the user or by the system, and a single action can have both inputs and outputs. A single action can abstract what would be an entire use case in object-oriented modeling approaches, allowing a much terser form of description. An action can also abstract away (that is, not represent in detail) the creation of complex inputs; for example, an action input may be a rich-text object that in the implementation would be produced by an extended interaction with a rich-text editor.

Actions read and write states. An action may have a precondition that makes it applicable only in certain states; when the precondition does not hold, the action is blocked and may not occur. Actions can be non-deterministic, resulting in more than one possible outcome for a given pre-state/input combination. But any non-determinism must be exposed in output arguments, so that the state of a concept is always a function of the trace of actions that have occurred so far. For example, an airline reservation concept could have an assignSeat action that picks an arbitrary seat and assigns it to the customer, but the seat must be represented as an output of the action (in addition to appearing in the post-state of the relation that maps customers to seats).

From a data modeling perspective, there is no global data model. Instead, there is a collection of local data models, one for each concept. Each concept's data model is just rich enough to support its actions. (In teaching data modeling, I have found that this makes it much easier for programmers to scope their models. In traditional modeling, it's all too easy to get carried away with building a data model based on ontological observations that are not actually relevant to the design of the system.)

If the state and action definitions are written in a formal notation such as Alloy, the concept behavior can be analyzed automatically, with generation of sample executions, comparison of action versions, and checking properties. The modularity that concepts provide amplify the effectiveness of automated analysis. Such analysis is always inherently intractable (the number of executions to check rising super-exponentially with the number of objects in the state), so researchers have always looked for ways to decompose a system into smaller parts. Concepts provide such a decomposition, aligned naturally with the functionality boundaries of the system.

The definition of a concept augments this basic behavioral description with two more novel parts explained in more detail below: the purpose and the operational principle.

## Concept Purposes

The idea that an artifact should have a purpose distinct from its specification is hardly novel, and many researchers have recognized the importance of purposes, and the impossibility of expressing them fully and precisely (most notably Christopher Alexander in Notes on the Synthesis of Form).

What is novel in concept design is the idea that it is not sufficient for the system or app as a whole to have a purpose (or a collection of purposes). Each concept in its design should have its own purpose. A concept's purpose defines, in a general setting, the reason for its invention and what benefits it offers; in the setting of a particular app, it defines the motivation and justification for including the concept.

Purposes also clarify subtle distinctions between related concepts. In social media, for example, there are several concepts that may sit behind a "thumbs up" widget: Upvote, whose purpose is to rank items by popularity so that users (purportedly) see the most valuable content first; Reaction, whose purpose is to convey an emotional reaction to the author of an item; Recommendation, whose purpose is to learn a user's preferences so that subsequent items can be recommended more reliably; and Profile, whose purpose is to track the user's interests in order to target advertising.

Because purposes sit at the boundary of the human/computer interface, they cannot be judged formally (the way correctness can, eg). Nevertheless, the book provides criteria for determining whether a purpose is compelling, and when two distinct purposes may be masquerading as one.

## The Operational Principle

A concept definition also includes its operational principle (OP), an archetypal scenario that shows how the concept fulfills its purpose.

Superficially, the OP is like a use case, but it plays a very different role. Use cases are a specification notation, and a full spec typically requires many use cases. Use cases are often expressed at a low level too, in terms of the micro-interactions of the user interface (clicking buttons etc). Since a concept's actions fully define its behavior, nothing more is needed to predict how the concept will behave.

Instead, the OP captures the dynamic essence of the concept, telling the most basic story about how the concept works. Sometimes the OP is so simple it barely even needs stating: when you add a comment to a post, your comment will subsequently appear along with the post (the OP of the Comment concept). But often the OP is more interesting. It may require two distinct scenarios: when you delete a item, you can restore it from the trash; once you empty the trash, though, it's gone forever and its space is reclaimed (Trash). It may need to be quite elaborate in order to demonstrate the purpose and distinguish the concept from similar but less powerful concepts: if you assign a style to two items, and then you update the style, both items will be updated in concert (Style). And it may involve multiple users: after users have upvoted items, the items will be ranked by the number of times they were upvoted (Upvote).

The OP may also be aspirational, applying only in ideal circumstances (even if they are typical). It is not true that if you reserve a restaurant table, and then turn up, a table will necessarily be available (since guests at your table may have stayed longer than expected); nor that a successful authentication associated with a user account must have been performed by the same user that registered the account (since someone may have stolen your password). Like many aspects of concepts, the OP may appear to be obvious until you consider things more deeply.

The OP often provides the clearest way to explain a concept. To use the PORT elevator system, a rider selects their destination floor on the device in the lobby, which responds with the identifier of the lift car to be taken; the rider enters that car and is taken to their floor. This is complicated enough—and different enough from standard elevators—for the maker (Schindler) to advertise that it's "as easy as 1-2-3" (namely involves an OP with multiple steps).

Paradoxically a full behavioral description is often less helpful, since (a) it fails to distinguish the essential aspects of the concept design (how style updates effect items) from more arbitrary design decisions (what happens when a style is deleted); and (b) it conveys the motivation for the behavior. For Michael Polanyi, from whose work the idea of the OP is taken, this latter consideration is the key to understanding the difference between design/engineering on the one hand and science on the other (put bluntly, why physics cannot explain how a clock works).

## Concept Synchronization

Within an app, concepts can operate largely without interaction: commenting on posts, for example, may be orthogonal to upvoting them. But often concepts need to be coupled together to achieve the app's goals. For example, it may be problematic for users to edit posts after they have been upvoted (since the upvotes responded to content that may have changed). To mitigate this the upvote action of the Upvote concept could be synchronized with the edit action of the Post concept, to prevent edits after a post has been upvoted or to remove upvotes when a post is edited.

For some concepts, synchronization is part of their intended usage. An access control concept is intended to suppress some actions in another concept when the user lacks the right permissions; a subscription concept is intended to react to certain actions by generating subsequent notification actions. In these cases, the concept typically offers 'placeholder' actions that are synchronized with the real actions in other concepts: an access control concept may have an access action, for example, which is then pinned to the action to be controlled in another concept.

Synchronizations are defined reactively: when an action occurs in one concept, some actions should occur in other concepts. Arguments can be passed between actions, so that synchronization includes data flow. Each synchronization is atomic and happens in its entirety or not at all, so if one of the reactive actions is blocked by its concept, the initial action cannot occur either.

This model of communication and interaction is inspired by Hoare's CSP, and can be formalized in its terms. A crucial property of the model is that the behavior of each individual concept is preserved. Synchronization can prevent a concept from executing an action, and it can limit the arguments presented to an action, but it can never cause an action to occur (or an output to be produced) that would not be possible for the concept in isolation. As will be explained below, composing concepts maintains their integrity.

The synchronization mechanism is also essential for maintaining concept independence and avoiding the need for one concept to 'call' another. At the code level, composition requires mediators to implement the synchronization; these mediators make reference to the concepts, but the concepts themselves remain free of mutual references.

## Synchronization and Automation

Synchronization of concepts is often a form of automation, in which the user is saved the trouble of executing a concept action because it follows execution of an action in another concept automatically. Omission of a desirable automation can be attributed to under-synchronization of an app's concepts: in Zoom, for example, the raised hand concept might be synchronized with the audio muting concept so that participants' hands are automatically lowered after they have their turn.

Automation preempts the user's manual control and thus, if not configurable, can be problematic. Such automation can be attributed to over-synchronization of an app's concepts: in some calendar apps, deleting in the event concept leads undesirably to declining in the invitation concept.

## Synchronization and Decomposition

What an app presents as a single concept may be better understood as a synchronization of multiple component concepts. A hint that such a decomposition is warranted is often found in the presented concept having multiple, conflicting purposes.

Facebook, for example, appears to offer a 'like' concept, but on closer examination, this concept is a synchronization of several of the concepts described above: Upvote, Recommendation, Reaction and Profile. This synchronization is responsible for some confusions and critical commentary about Facebook's design (notably, that an 'angry' reaction produces a positive upvote—by some accounts counted for more than a simple 'like'). With this decomposition in mind, different design options are easy to see: having separate buttons for "I'm angry" and "I want to see more of this kind of post", for example.

## Concept Synergy

In most compositions, concepts bring additive value. But in some designs, concepts can take advantage of each other so that one concept achieves its own functionality in part by relying on another concept. This is synergy in the setting of concept design, where the value of putting two concepts together is more than the sum of their individual values.

An example is Apple's synergistic composition of the Folder and Trash concepts. By making the trash a folder, the design allows the action of moving items between folders to be used to restore items from the trash. Achieving this synergy is non-trivial, and the book explains its subtle evolution over time.

Attempted synergies can backfire. A version of Outlook placed system logs (reporting for example on connection failures between client and server) in mail folders as if they were messages, but this led to numerous problems (for example that reports of connection failure could not be delivered to clients if… connections failed).

## Concept Dependence Diagrams

As explained above, concepts are inherently uncoupled and free standing, so they can be understood, designed, evaluated and reused independently. Bringing concepts together in an app does not couple them either, since the synchronization mechanism ensures that each concept will conform to its own behavioral expectations even if its actions are tied to the actions of other concepts. Furthermore, implementation need not introduce any dependencies between concepts.

There is a kind of dependence between concepts, however, that is useful to analyze, and that arises in the context of usage in a particular app or system. A concept C1 is said to depend on a concept C2 in an app A when the inclusion of C1 only makes sense if C2 is also present. Note that "makes sense" doesn't mean that C1 would somehow break if C2 were missing, so there is no traditional software-engineering dependence here. Rather, the dependence reflects an understanding of the role of C1 in A. In a social media app with a Comment concept and a Post concept, for example, Comment might depend on Post because it was included to allow users to comment on posts, and if there are no posts, there's not much point in having comments.

As with conventional dependencies, the concept dependence relation can be depicted as a dependence graph or diagram. Dependences have several uses. They determine which orders of explanation of an app's concepts will be intelligible; you'd explain posts before comments on posts, for example, They define, implicitly, an entire application family (as the set of subgraphs in which some subset of the concepts appears and a concept never appears without those it depends on). The dependence diagram can thus be used to make scoping decisions about which concepts to include or exclude. Dependencies also suggest a development order: it's better to build Post before Comment, so that comments have targets to be tested on.

## Concept Mapping

In an implementation of a concept design, the concepts must be mapped to the user interface, connecting the conceptual level of design to the physical and linguistic levels. Actions might be executed by gestures or button presses, for example, and the states of the concepts will be displayed in various views.

The standard techniques and heuristics of user interface design apply directly to concept mapping. The lens of concept design helps focus this work.

Some concepts present tricky mapping challenges, and good mappings can be part of the design knowledge associated with a concept. For the filtering view in the Label concept, in which a collection of items is filtered by a selected label, for example, it might seem desirable to maintain an invariant that the items displayed are exactly those carrying the label, but this turns out not to be a good idea.

In Gmail, the Label concept is used to classify messages, but the user interface shows messages in the context of conversations and associates labels with conversations instead. This mapping design is troubled, and leads to a variety of odd behaviors.

## Testing and Prototyping Are Not Enough

A concept design is ultimately evaluated in the context of use, and misfits (in which a design fails to fulfill its intended purpose) are never fully predictable, because they depend on properties of the human environment which may not even be knowable until the design is deployed.

User testing offers some limited value, especially for evaluating concept mappings, and for catching egregious flaws, but (unlike real deployment) will rarely encounter the corner cases that are most troublesome in a design. Prototyping is a valuable strategy for exploring candidate designs early on, and indeed many of the practices of design thinking can be fruitfully combined with concept design, and are made more useful by the separation of concerns that concepts offer.

But generate-and-test is not a viable method for finding a good design in a large design space, let alone a great design. To do that requires an expert designer who can apply prior knowledge of likely problems and known solutions, often acquired in very different settings. Concepts provide a framework for recording and retrieving such knowledge.

A note for computer scientists: the known problems of standard concepts are sometimes grounded in technology (eg, the difficulty of achieving consistent views of data in a distributed system) but are more often a result of human behavior (eg, that ticket sales invite scalpers who then drive up prices).

## The Need for Concept Design Principles

Over the last few decades, a rich body of UX design principles has been developed. These include prescriptive adaptations of psychological ideas, such as the Gestalt principles of grouping, which can be used to guide layout design, and James Gibson's notion of affordance, made applicable in user interfaces by Don Norman's principle that affordances should be explicitly "signified". Norman's book The Design of Everyday Things introduced several additional principles, such as the idea of "mapping" (a different usage from concept mapping) in which a user interface mirrors the structure of the domain being controlled. Other pioneers produced explicit collections of principles: Ben Shneiderman's golden rules, Jakob Nielsen's heuristics, and Bruce Tognazzini's principles of interaction design.

Especially in the hands of experts, these principles make it possible to design a user interface that is likely to be highly usable, with a low probability of serious usability flaws. Indeed, there is no excuse nowadays for poor user interface design, and user testing is much less important for routine design work (although it's still valuable of course, especially for very novel or critical designs).

Almost all of these principles, however, are focused on the physical and linguistic levels of design. New principles are needed at the conceptual level. The book presents three such principles and explains them in detail with many examples from contemporary apps.

## Concept Design Principles

Familiarity. When possible, a familiar concept should be preferred to a new, unfamiliar one. With familiar concepts, users can rely on their prior experience, and don't need to learn a concept afresh. And designers can take advantage of the body of knowledge associated with a known concept, reducing the risk of a design with unexpected misfits. The familiarity principle can be seen as an application of a meta principle of consistency: when a purpose arises in an app that has arisen before, the same solution should be used.

Specificity. If you draw up a list of the purposes purportedly served by an app, the purposes and the concepts that aim to fulfill them should be in one-to-one correspondence. This implies first that every purpose should have at least one concept that fulfills it, and that every concept has some purpose that motivates it. So much is obvious, although there are examples in real apps (which the book explains) of unhelpful concepts that serve no user purpose, and purposes that are essential to an app that are fulfilled by no concept.

The more subtle implications are: no redundancy, namely that each purpose should be fulfilled by at most one concept, and no overloading, namely that each concept should serve at most one purpose. Redundancy is clearly undesirable because it involves a waste of resources (in the designer's work and in the user's understanding). Overloading is a more subtle notion: that a concept that tries to serve multiple purposes is pulled in different directions, and cannot serve any one purpose effectively. This idea is related to the independence axiom in Nam Suh's theory of mechanical design, and to the common observation in programming that each segment of code should have a single goal.

The book gives many examples of concepts doomed by overloading, classifying them into different causes for the overloading:

1. false convergence, when a concept is designed for two different functions that were assumed (wrongly) to be aspects of the same purpose;
2. denied purpose, when a purpose was ignored by the designer, despite the desires of users;
3. emergent purposes, in which new purposes arise for old concepts, often invented by the users themselves; and
4. piggybacking, when an existing concept is adapted or extended to accommodate a new purpose.

Integrity. This principle says that when concepts are put together into an app, the each concept should continue to behave according to its (app-independent) concept definition. If concepts are composed by synchronization, integrity will be preserved by design. But if composition is more ad hoc, or if concepts are adjusted to suit the larger context of the app, there is a risk of violation. Google Drive, for example, offers a sync concept (not to be confused with concept sync!) in which local files on disk are kept in sync with files in the cloud. But in an egregious violation of integrity of this concept, only conventional files are properly synced, and files associated with Google Apps (such as Google Docs) are treated specially, and are represented on the local disk not by their contents but by a URL. A lack of awareness of this limitation has been catastrophic for some users.

## Comparisons to Other Approaches

Concept design builds on more than 50 years of advances in a variety of fields, and contributes some new ideas. First, some work that sounds similar but is not really relevant:

Concept maps are diagrammatic representations of collections of facts, with each edge representing a proposition that applies a predicate (the label of the edge) to two atoms (the nodes it connects). Concept maps are an application of knowledge graphs; they were proposed as an educational tool. They are "conceptual" in the sense that predicate logic lets you formalize all kinds of relationships, at any level of abstraction; and since the predicates don't need to be designated (using Michael Jackson's term), they can express ideas that would be hard to nail down precisely. The very flexibility of concept maps seems to limit their leverage in software design.

Concept lattices are representations of partial orders between classifications, where the order is set inclusion. Classification is a useful activity but is limited in the context of software design because it doesn't address relationships, and is usually static, so does not address behavior.

At the other end of the spectrum, the most closely related work is:

Conceptual modeling. The field of conceptual modeling is broad and has many motivations, but part of it is concerned with explicit representations of the structures that underlie both applications and the mental models of users. The emphasis of the field has tended in the direction of ontologies (eg, for reasoning and knowledge representation), or in the direction of domain modeling (eg, for understanding the environment in which a software system operates), and in these respects conceptual structures are usually discovered rather than invented. In contrast, concept design focuses more on concepts as socio-technical inventions that serve a purpose. Most conceptual models are essentially abstract data models (in the spirit of entity-relationship diagrams), although there is work on dynamic models too (although these are hard to distinguish from standard kinds of dynamic models such as Statecharts). What concept design seeks to provide, which seems to be missing from conceptual modeling, is the notion of a identifiable concepts. Without this, there can be no modularity in conceptual models, and it is not possible to talk about concepts as separable contributions, to identify common concepts between models, or to reuse concepts. The terminology of conceptual modeling sometimes seems to imply that the entities of a data model are concepts, but these are not good concepts, since concepts typically involve relationships between objects. Some approaches seek to identify concepts with objects or classes, but this has an implementation flavor to it, since there is rarely a natural way to assign relationships and behavior to a single object or class.

Objects and classes. In the early days of object-oriented programming and development, the idea that objects naturally mirrored or modeled the real world was seen as a major benefit. Over time, the idea became less plausible, first because object-oriented programming took on more arcane forms moving further away from domain structures (under the influence of the Gang of Four patterns and other advanced programming techniques), and second because the inherent implementation bias in object-oriented design became clearer. The key problem is that, in the real world, the properties and behavior of objects involve relationships between them, and can rarely be satisfactorily assigned to individual objects. In practice, this is usually addressed by defining objects that hold relationships between other objects, but such a style is not really object-oriented. Worse, objects cannot generally be defined independently of one another (and in fact, as explained in the book, tend to produce code dependences that violate Parnas's principles).

Domain-driven design. DDD is a very popular and successful approach to software development, created by Eric Evans. It can be viewed as a modern incarnation of the idea of building a software system on an explicit model of its problem domain, which goes back to Simula and JSD. A key innovation of DDD is the idea of "bounded context": that each system or app has its own domain model, which serves its own functionality, reflects the world view of its development team, and may differ from (and even be inconsistent with) the domain models of other systems that operate in the same (larger) domain. Concept design proposes a more fine-grained structure, focusing on modularity within an app, each concept in a sense having its own bounded context (defined by its state/data model). In addition to the domain modeling aspect, DDD embodies an extensive collection of patterns and practices for building more flexible software. One pattern in particular suggests you "look for the underlying conceptual contours", and it seems likely that concept design should thus be a good match for DDD. Finally, one key difference: a domain-driven design typically starts by constructing a model of the specific domain in a bottom-up fashion; one popular approach called "event storming" starts by classifying key events in the domain (just as JSD did). Concept design instead starts with recognizing standard concepts that can be assembled for the app at hand, and thus places more emphasis on reuse of domain models. This difference should not be fundamental however, and it seems likely that the two approaches could be used profitably together.

Feature-oriented development. Features are increments of functionality; a feature model comprises a set of features and constraints on which subsets of features can be combined together, implicitly defining a product family. Feature-based frameworks (such as Don Batory's AHEAD tool suite) automate the configuring of features and merging of code fragments. In contrast to concepts, features are more flexible, and can not only model arbitrary increments of functionality but can also address aspects of a system that are not user-facing; a caching feature, for example, might improve performance without producing any observable change in behavior. The price paid is that features, unlike concepts, are not generally independent of one another, and cannot be easily reused across applications.

Cross-object modularity mechanisms. A variety of mechanisms have been developed to accommodate functionality that cross-cuts the traditional object boundaries in OO programming. These include aspect-oriented programming, subject-oriented programming and role-based programming. The latter two are similar to concepts in factoring out behaviors that serve distinct purposes, separating them from the existence of particular objects. Unlike concepts, however, these notions are not generally independent of one another, and (like features) are intended to be implemented in the context of a particular system and not transportable between systems.

Feature interaction. In the context of telephony, "features" have a different connotation, and are (like concepts) user facing and typically intended to be independent of one another. The "feature interaction" problem arises when a system includes features that prescribe conflicting behaviors. In concept design terms, feature interaction is a violation of integrity, and would be resolved by not allowing conflicting features to be active at the same time. This is one approach taken in telephony, but more flexible approaches are taken too (for example, giving priority to one feature over another). This flexibility might be achieved with concepts by designing concepts with non-determinism that can be resolved in composition.

Microservices. Most backend applications are nowadays structured as a collection of "microservices", each providing an API and its own internal logic and storage. A concept can be viewed, at least from a functionality perspective, as a "nanoservice"—like a microservice but with a much more limited scope (with a single focused purpose rather than a collection of purposes around some area of functionality such as billing or advertising). Microservices are not generally independent of one another, and because they aggregate app-specific collections of functions, are not reusable across apps.

## Strategies

Each chapter of the book includes an outline at the end of some practical strategies, and a final chapter presents a set of questions for each kind of person (program manager, consultant, UX designer, etc) who might use concept design. Here are some highlights of ways to use concept design in your work:

- Design concepts for a new app, or for new functionality in an existing app, using the concept design structure, formulating purposes and operational principles to bring design focus.
- Avoid reinventing the wheel when designing an app, by always looking for ways in which existing, familiar concepts might suffice (and by spotting concepts that are small variations away from familiar concepts).
- Inventory the concepts in your app (or app family) to get a bird's eye view of its functionality. Construct a dependence diagram to show what subsets are possible. Do this as a retrospective review of an existing app, in designing a new app, or in planning extensions or digital transformations.
- Identify concepts that are the most valuable (eg, product differentiators), the most troublesome (in terms of user confusion/complaints, development costs, etc), the least valuable (which might be dropped or replaced by more powerful concepts), etc.
- Genericize one or more concepts by reformulating its purpose independently of the type of objects it works on, and consider how making it more polymorphic might allow it to be simplified and applied in more contexts within your app (and across your app family or suite).
- Decompose concepts that serve multiple purposes into single-purpose concepts that are synchronized together.
- Find familiar concepts lurking behind the concepts of your app, and adjust your concepts or decompose them to expose familiar concepts that will make the app more intelligible to users.
- Look for synchronization opportunities that would increase the degree of automation in your app; conversely look for ways in which synchronization is excessive and eliminates manual controls that users would welcome.
- Identify redundant concepts that could be removed by being replaced by existing concepts (which may need some enrichment).
- Identify overloaded concepts that are complex or brittle, and split them into separate concepts. When users have trouble understanding your app, first consider overloading as a possible cause.
- Examine the data model or schema of your app and consider how you might decompose it into the local data models of individual concepts.
- Create help and training materials that are concept-driven so they can be grasped more easily by users: follow the dependence diagram for ordering; use consistent names for a concept throughout; note when a familiar concept is being used; present concepts with purposes and operational principles first (before the details of all their actions).

## Fun things

The end notes include mini-essays on some serious topics, including:

- Empiricism and its pitfalls
- Design thinking and "content-free" process
- Verification and its pernicious consequences
- Christopher Alexander, patterns and misfits
- Inevitability as a design criterion
- Mental models and gulfs of evaluation and execution
- Normal and radical design
- The pitfalls of object-oriented programming

and also include some lighter topics such as:

- My favorite pasta sauce recipe
- How to prevent ice dams and water leaks in your house
- An Easter egg in Don Norman's book
- Why pixels and inches in CSS don't mean what you think

## Comments & reactions?

Join the discussion at forum.essenceofsoftware.com!
