# Concept criteria: what's a concept?

> Source: https://essenceofsoftware.com/tutorials/concept-basics/criteria/
> Fetched: 2026-08-28

## Two sides of a coin

The key to concept design is, perhaps not surprisingly, the idea of concepts. A concept is two things at once. On the one hand, a "concept" means what you'd expect it to mean: a mental construct that you need to understand to be able to use an app effectively. So you might say that to use Photoshop you need to understand the "concept of a layer"; to use Facebook you need to understand the "concept of friending"; and so on. But if concepts were just vague mental constructs, there wouldn't be much you could do with them.

On the other hand, a concept is a coherent unit of functionality. In this sense, concepts belong to the long line of modularity mechanisms in software that include procedures, classes, abstract data types, processes, and so on.

The novelty of concepts comes in part from the way in which these two views are aligned. The concept as a mental construct is the same concept as the functional unit. The alignment of these two makes concepts a little unusual when viewed through these two perspectives.

## A new kind of mental construct

Because the concept as a mental construct corresponds to a unit of function, it is inherently dynamic. Many people think of concepts as static, often as a form of classification in which a concept ("pond", say) is defined as a set of objects (bodies of water, say) that have certain properties (small, still, land-based, etc). In concept design, however, concepts are defined by their dynamic behavior. A restaurant reservation isn't a category of things in the world that you'd identify by classifying all possible things (dogs, car dealerships, headaches, etc) and then rejecting the ones that don't match. Imagine a Martian appearing on Earth and asking you to explain what a restaurant reservation is. You wouldn't explain how to distinguish one from other things (a social security number, a tax return). You'd explain it by saying what it's for (to help diners so they can be confident a table will be available, and to help restaurant owners fill their tables) and how to use it (call the restaurant, pick an available time, and then turn up at that time).

## Three parts

This explanation has demonstrated three essential parts of a concept: the name ("restaurant reservation"), the purpose (ensuring a table will be available) and the operational principle (picking a time in advance and turning up at that time).

## A new kind of functional unit

Just as the requirement to correspond to functionality makes a concept an unusual kind of mental construct, so the requirement to be a mental construct makes a concept an unusual kind of functional unit. Most importantly, a mental construct has to be understandable without reference to other mental constructs. This property of independence is what makes mental constructs understandable.

For example, the concept of a "comment" in a social media app is easy to understand because you don't need to know anything else. The purpose is for people to share their reactions to particular artifacts, and the operational principle is simply that you pick your artifact, write your thoughts, and they then appear associated with the artifact.

In practice of course that artifact that the comment is about will be a social media post, or perhaps a reply, or maybe even another comment. But you don't need to know that to understand what the concept of a "comment" means; the concept is independent of whatever it's attached to. In computer science lingo, the concept is "polymorphic."

Why go to the trouble? The reason for defining concepts this way isn't just to align the mental model and functional units views. It's that the properties concepts end up having make them a particularly effective way to modularize function. In particular, the independence of concepts makes them more likely to be reusable in different contexts, not only at the design level but at the implementation level too.

# Concept Criteria

## Uses of criteria

A more comprehensive list of criteria can be given for distinguishing concepts from other things. These criteria are useful for a variety of purposes:

- When learning concept design, they help you understand the difference between concepts and other kinds of software notions (such as entities, classes, features, microservices, etc).
- When analyzing an application, they help you identify coherent units of functionality that shape the app and characterize it.
- When designing an app, they help you recognize the larger units of functionality whose design can be pursued independently.

## The criteria

Here is a list of criteria that every concept must satisfy:

- **User facing.** Concepts are always experienced by the user of an application. So the structures that are only internal to an application and are hidden from the user are not concepts. Of course an implementation structure may support a user-facing concept. And programmers themselves should be viewed as users when considering the design of an API.
- **Semantic.** Concepts are made of static and dynamic structures that are abstract and semantic in nature. A user interface widget is not a concept, nor is a color scheme or a UI skin.
- **Independent.** A concept can be understood by itself without reference to other concepts. In contrast to classes in OOP, there are no "dependencies" that link one concept to another and prevent the former from being used without the latter.
- **Behavioral.** Every concept has a behavior associated with it. Usually the behavior is quite simple. For example, in the upvoting concept, when people upvote items, the items with the most upvotes rise to the top of the ranking. Applications can have much more complex behaviors, of course, but these are often due to the interactions of many small concepts.
- **Purposive.** A concept serves a particular purpose that is intelligible to its users and that brings real value by itself. Something pretending to be a purpose may just be a role played in a larger context. For example, the concept of a social security number has the purpose of allowing the government to associate pensions with individuals. The action of obtaining a social security number may seem at first to have a purpose ("getting a social security number"?) but on reflection you'll realize that's just a role it plays in the larger concept, and by itself it delivers no real value.
- **End-to-end.** A criterion related to being purposive and independent is that a concept's functionality must be end-to-end. A user authentication concept, for example, couldn't include actions for registering an account but not also include the authentication action itself. (To check that a concept is end-to-end, try writing an operational principle, and if it takes the form "when this action happens, the state is updated in this way" you'll know something is missing.)
- **Familiar.** Most concepts are familiar to users. This is what makes it possible for users to start using a new app without reading a manual. Of course an app can have new concepts, but novelty can come even more from a new combination of old concepts, or subtle adjustments to them. The key concepts used in social media (post, friend/follow, upvote, reply, comment, hashtag, etc) appear in almost an identical form in every app (Facebook, Twitter/X, Instagram), albeit with some small variations that may have significant impacts on usage (such as Instagram's better support for images, or Twitter/X's restricted post length).
- **Reusable.** As a consequence of many of these criteria (being purposive, embodying end-to-end functionality, independence, etc), concepts are often reusable in different contexts. For example, Zoom introduced the concept of a meeting identifier (whose purpose was to allow parties to join a meeting without requiring each participant to be called), but it was eventually copied by Google Meet and Microsoft Teams.

## Distinctions

We can apply these criteria to distinguish concepts from some other software constructs:

- **Classes.** Classes in OOP (and similarly abstract data types) are not generally user-facing, and are rarely independent.
- **Features.** Application features are indeed user facing, but they are usually not independent. Typically a feature is defined in terms of some base functionality; without that, the feature may be hard to understand. For example, one feature of Instagram is that "accounts can be made private"; from a concept design point of view, this is an augmentation of the follower concept with an approval mechanism that some users can elect to use.
- **User stories.** In agile development, user stories are a popular way to organize requirements. A single user story, however, may not be end-to-end (or purposive). For example, the story "As a teacher, I would like to record which students in my class are present today" does not, by itself, bring any value. From a concept design point of view, the concept might be attendance, and it would cover not only daily entry of attendance data but also end-of-term summaries, and perhaps also repeated absence warnings, etc. Because user stories are not end-to-end, I am concerned that they cannot be properly evaluated and so are not appropriate increments of functionality for implementation.
- **Microservices.** Microservices are a popular way to structure large applications. But because they aggregate many distinct pieces of functionality with distinct purposes, and because they are not generally independent of one another, they are not usually reusable either.
