# Design Moves for Software

> Source: https://essenceofsoftware.com/posts/design-moves/
> Fetched: 2026-08-28

## The secret of great design

Watch great designers at work, or study their designs, and you may wonder: what's their secret? Are they preternaturally inventive? Do they have better taste and judgment than the rest of us? Perhaps, but I don't believe that this can account for the best designs. Based on my own experience studying design and designers (mostly but not exclusively for software), I'd attribute the success of great designers to two factors.

First, they've done it before. Contrary to the picture of design implicit in the design thinking movement—in which extraordinary ideas emerge out of the blue, and each design problem is considered afresh—most designs are adaptations, extensions and compositions of design ideas that came before. A great designer is able to see the essence of a problem, find analogies to problems previously encountered, and rework old solutions.

Second, they refine their work. Nobody can solve a challenging problem in one step. What distinguishes great designers from mediocre ones isn't that their first attempts are so much better, but that they critique their work ruthlessly, and keep polishing it until no more improvement seems possible. This observation is not unique to design; George Saunders says it's the secret of great writing too (and perhaps it's a general life strategy).

## Implications for software design

Each of these has its implications. The first suggests we might codify a collection of reusable design ideas—both patterns (reusable solutions) and design moves (reusable tactics)—for software. Patterns have been very influential in software engineering (that is, in shaping implementation structures), and concept design is an attempt to find patterns in software design (that is, in shaping behavioral structures). Design moves have been discussed less but are no less important.

The second suggests that we need language, structures and design criteria for expressing and evaluating software designs, and that we need to engage in intensive critique of our designs. User testing is valuable, because you usually learn surprising things from people who approach your designs without your preconceptions. But like any form of testing, it doesn't directly help you make a better product. Think about testing code: it can expose bugs (although rarely the subtle ones), but if you just fix each bug as you find it, you're not going to end up with reliable and robust code. Whereas testing encourages you to focus on local details, and to fix problems with patches that can even reduce clarity and uniformity, critique focuses your attention on the essential and more structural aspects of a design and tends to lead to adjustments that produce better overall alignment and consistency.

Although design thinking has done good things, raising awareness of design and encouraging people in all walks of life to see new opportunities for design, it has also tended—perhaps because of its emphasis on democratization of design—to undermine expertise and the value of critique. Natasha Jen, a Pentagram designer, pokes fun at design thinking for these flaws.

## Concept design moves

Thinking about design moves, I came to realize that many of the case studies that I analyze in EOS involve one or more simple tactics. I've classified them into 3 pairs of design moves, each pair comprising a move and its dual. A design move isn't a panacea; it trades off one quality of the design for another. If applied skillfully though, a single move can transform a design from good to great.

I outline the design moves and give examples of their application in a paper that I'll be presenting in a keynote at the NASA Formal Methods conference in May. (Also see slides on this topic from my recent talk at the Boston ACM/IEEE chapter.) Here, I'll just give a taste of the moves.

Split/merge. Split breaks a concept into multiple smaller concepts; merge forms a composite concept from distinct ones. The tradeoff here is between simplicity and power: with more than one concept, the user has more control but things are also more complicated.

Unify/specialize. Unify takes a collection of concepts that are variants on a theme and unifies them in a single concept specialize breaks a single concept into more specialized variants. The tradeoff here is between generality and problem fit; when you unify, you end up with fewer and more general concepts, but they don't fit the specific applications quite so well.

Tighten/loosen. Tighten increases the synchronization between concepts; loosen weakens it. The tradeoff here is between automation and flexibility. With tight synchronization, the user does less but also has fewer options.

## A language of design: an example

Design moves—and concepts—don't guarantee that your designs will be good. But they give you a language for thinking about design, and a way to turn what might otherwise be an intimidating pile of seemingly arbitrary design options into a structured design space that can be navigated more systematically.

Rather than repeating examples from the paper, I'll illustrate this idea with a design move that has yet to be applied. In EOS, I briefly discussed the problem of raised hands in Zoom. People in a meeting raise their (virtual) hands to request to talk, and when their turn comes, they unmute themselves but often forget to lower their hands again. The host, on later spotting the hand still raised, has to ask: is that from before, or a new request to speak?

When I think about this problem, two design moves come to mind. One is the tighten move: we could synchronize the RaisedHand and Mute concepts so that (for example) when you unmute yourself your hand is automatically lowered. This would allow the two concepts to continue to be used mostly independently, but it would have the annoying consequence of lowering your hand (and losing your place in the queue) if you momentarily (and unintentionally) unmute yourself.

Another option is to apply the merge move to combine the RaisedHand and Mute concepts into a single concept, Moderation say, for moderated discussions. When the host switches to moderation mode, all non-hosts are muted by default and have to raise a hand to speak. The moderator chooses each speaker in turn, and their hand is lowered and they are simultaneously unmuted. This is arguably a simpler solution, but it eliminates the ability to use muting in a more ad hoc way.

This second approach suggests to me that the Mute concept might be serving two distinct purposes: that is, in concept lingo, it's overloaded. One purpose is to let participants in a meeting turn off their microphone for privacy, and the other is to control who is allowed to speak. This suggests applying a split move in which Mute is split into Privacy, a concept that lets users control what other users can see and hear of them, and Permission, which grants users the right to be seen and heard. Our merge move may then be applied to Permission and RaisedHand, leaving Privacy as a distinct concept, which might support some needs more directly. For example, Privacy might provide a toggling action for "going private" when you want to take a brief break.

As always, the challenge will be to balance richness of functionality and automation on the one hand with maintaining simplicity and not overwhelming the user with controls on the other.

## Let's help Zoom!

Here's an experiment in community design. Let's together develop a design to address the Zoom raised-hands problem in the concept forum. I'll post these initial ideas to get the topic going.

From my newsletter: archives and signup here.
