# Function questions: what to ask the client, and when to ask rather than infer (#130)

Ticket: lucmoseley/design-vault#130 (map #96). Status: complete (13 Oct 2026). Language: ASD-STE100 Simplified Technical English.

Source-strength labels used in this file:
- **Primary**: the owner of the method writes it (for example, the GOV.UK Service Manual about GOV.UK practice, Gerry McGovern about top tasks).
- **Expert**: a recognised research or practice body writes about practice (for example, Nielsen Norman Group).
- **Practitioner**: a studio or a single practitioner writes about their own practice.
- **House**: this repo or a sibling repo, read here.

Era labels (#96 Notes): **timeless** (it holds for all design of a service to people), or **era-bound** with a date.

## Findings

### F0. What the house asks today (House)

- `plugin/skills/design-project/SKILL.md` §1 asks the founder one time, at set-up, for "the one thing a visitor should do". It asks also for audience, seniority, register, colours, fonts, voice and standing rules. It asks no question about pages, about the order of importance of visitor tasks, or about the evidence behind the answer.
- `plugin/skills/design-round/SKILL.md` §1 (the brief), field **Intent**: "the surface, the job it does ... Where the founder has not settled the job, `impeccable shape` interviews him for it." Thus one ask route exists already, but it has no trigger rule. Nothing says when the job is "not settled".
- impeccable 4.5.0 `reference/shape.md` Phase 1 is a discovery interview. Its rules: "Ask two or three related questions per round, then wait. One round is the default"; "Do not dump a questionnaire ... Assert the likely reading and invite correction." Its Round 1 questions: what the surface is for; who reaches it, in what situation and state of mind; the primary thing they must understand or do, and what success looks like; what is uniquely true here.
- impeccable 4.5.0 `reference/init.md` Step 3 asks for the product record (`PRODUCT.md`): "Who is the primary user, in what situation, and what job are they doing?"; "What does the product make possible ...?"; "What durable constraints, assets, evidence, or product facts must future work preserve?". It says: "Before asking, scan enough to avoid making the user repeat known facts" and "Ask only about material gaps the repository and original request do not answer with strong evidence ... Confirm inferences." It says also: "Record undecided facts instead of inventing them."
- `references/fit-gate.md` (set-up) gives the critic three checks: audience register, the client's colours and marks, standing rules. It has no check about function or task priority.
- Consequence: the house has two interview sources (design-project §1 and impeccable `init`/`shape`). Both ask about the surface as one unit. Neither asks which visitor tasks come first, which page serves each task, or what each element on a page is for. Neither names a signal that makes Claude ask.

### F1. What experts ask to learn function and priority

Each entry gives: the source and its strength, the questions or fields, what a client who is not a designer can answer well, the conditions, and the era.

**F1.1 GOV.UK Service Manual and design principles: user needs, and evidence before opinion.**
- Source: GOV.UK Service Manual, "Start by learning user needs" (read 13 Oct 2026); "How the discovery phase works" (last updated 21 Jun 2021); Government Design Principles (first published 3 Apr 2012, updated 2 Apr 2025); GOV.UK publishing guidance "Identify user needs". **Primary.**
- Form of a need: "As a… [which type of user has this need?]" / "I need/want/expect to… [what does the user want to do?]" / "So that… [why does the user want to do this?]".
- Evidence first: "analytics, search logs, call centre data, previous research reports"; then "interviewing and observing actual or likely users"; then "talking to people inside and outside your organisation who work with actual or likely users".
- The rule on opinion: "Treat any opinions or suggestions that do not come from users as assumptions that have to be proven by doing research." Principle 1: "what they ask for isn't always what they need." Publishing guidance: "Every piece of published content should meet a valid user need."
- Discovery: learn "what the user's trying to achieve and how they go about doing it"; find the hard and soft constraints; "prioritise your risky assumptions".
- What a non-designer client answers well here: who the users are, what the organisation wants to change (GOV.UK "policy intent"), the constraints, and where evidence lives. What he answers badly: the user need itself, which GOV.UK files as an assumption until research shows it.
- Conditions: GOV.UK has user researchers, analytics and call-centre data at scale. A solo professional has none of these at scale. The rule "an opinion is an assumption" still holds; the means to test it are smaller (F2.2).
- Era: **timeless** (the principle). The format "As a / I need / So that" is era-bound (agile practice, about 2001 onward) and is a format only.

**F1.2 Top tasks (Gerry McGovern): a ranked list of visitor tasks, set by a visitor vote.**
- Source: Gerry McGovern, "What Really Matters: Focusing on Top Tasks", A List Apart, 21 Apr 2015. **Primary** (the method's author). NN/g (Evan Sunwall, "A Lesson on Top Tasks from Hurricane Beryl", 19 Jul 2024) as **Expert** confirmation.
- Definition: "the small set of tasks (usually less than 10, often less than five) that matter most to your customers."
- Method: gather 300 to 500 candidate tasks from customer feedback, stakeholder interviews, rival sites, social media, site behaviour and search data; cut to a shortlist of "no more than 100"; each customer ranks five tasks (5 to the most important); the result is a league table. In the Cisco case "three tasks got as much of the vote as the bottom 44."
- On the client's guess: tiny tasks are "full of organizational ego". In a reader comment (19 May 2015) McGovern says the team also votes on "What do you think your customers want most?", and "Those 'pet ideas' usually get dismal scores from customers!" Page visits "reflect what you have, not necessarily what customers want."
- NN/g: top tasks are "activities that users must be able to do with a product"; stakeholder interviews and user surveys are "good techniques for determining this top-task list"; priority changes with context ("when the crisis hits, that top task surges to number one").
- What a non-designer client answers well here: the candidate task list (what people ask him, what they come for). What he answers badly: the rank, which needs visitors.
- Conditions: the vote needs hundreds of visitors. A solo professional site has too few visitors to vote. So for a small client the method gives the **question shape** (a short ranked list of visitor tasks, in the visitor's words) and not the **method** (a vote). The rank then comes from the client's best evidence (enquiries he received, F2.2), and it stays labelled as his estimate.
- Era: **timeless** for the principle (few tasks carry most of the value). The vote is a method with a date (McGovern, about 2000s onward).

**F1.3 Jobs to be done: the progress a person tries to make in a situation.**
- Source: Bob Moesta and Chris Spiek, jobstobedone.org/learn (read 13 Oct 2026), **Primary** (method authors). Christensen, Hall, Dillon and Duncan, "Know Your Customers' 'Jobs to Be Done'", HBR Sep 2016, **Primary**; only the summary was readable here, so the definition below is from the Moesta page, not from HBR.
- Definition: "a way of understanding why customers really buy", focused on "the progress a person wants to make in a specific situation". Four forces: "the push of the current situation, the pull of the new solution, the anxiety of the unknown, and the habit of the present."
- Method: do not look for jobs "in surveys or focus groups"; interview "people who recently switched", and rebuild the decision in "forensic detail" from the first thought.
- What a non-designer client answers well here: the story of real recent clients. For example: "Think of the last client who hired you. What was going on for them? How did they find you? What did they need to be sure of before they wrote to you?" A client can tell a true story about a past event. He cannot reliably predict the reasons of a typical visitor (F1.5).
- Conditions: JTBD is built for products with many buyers. For a solo professional the "switch" is one hiring decision. The **anxiety** force maps to the site's trust job: what a visitor must be sure of before contact (credentials, past clients, independence). This is a design input: it decides what proof sits next to the contact action.
- Era: **timeless** (the principle that people hire a thing for progress in a situation); the method is about 1990s onward.

**F1.4 Content priority guide and page table: the job and priority of each page and each part.**
- Content priority guide: Emily Gray, Sparkbox, "Content Priority Guide", 11 Nov 2013. **Practitioner** (it is the origin of the method). It lists "all the content on each unique page", breaks it into items, and "puts them all in their priority order using only text". It records which items repeat across pages and which are optional. Sparkbox "invited our clients to review and edit them" in a shared document. The ticket names Ahava Leibtag; no content priority guide or page table by her was found (search ran; see Bound).
- Page table: University of Wisconsin-Madison IT, "Page tables" (updated 18 May 2026), **Practitioner**. Fields: "Page Goal/Objective: What this page is meant to achieve"; "Target Audience"; "Key Messages: The main points or information the page must communicate"; "Call to Action (CTA): What the user should do next"; "Role/Purpose: How the page supports the overall user journey or site structure"; and content, SEO and governance fields. Secondary sources (Kapost, Chapter Three) tie the page table to Halvorson and Rach, *Content Strategy for the Web* (2nd ed. 2012, Brain Traffic). I did not read the book, so this tie is **unverified**.
- What a non-designer client answers well here: the key message of a page in his own words, and whether a page or item must stay or can go (he knows his business). What he answers less well: the order of the parts on a page, which is a design decision that the visitor's task decides.
- Conditions: a content priority guide is a design artefact that the **designer** drafts and the client **edits**. It is not a questionnaire. This matches the founder's constraint (F2.4): Claude drafts the priority list as its best guess, and the client corrects it.
- Era: **era-bound**, responsive-design practice from about 2012-2013; still current practice in content design (2026).

**F1.5 NN/g: stakeholder interviews, and why self-report about behaviour misleads.**
- Source: Sarah Gibbons, "Stakeholder Interviews 101", NN/g, 23 Oct 2022, **Expert**. Jakob Nielsen, "First Rule of Usability? Don't Listen to Users", NN/g, 4 Aug 2001, **Expert**. Jakob's Law, NN/g video, 18 Aug 2017, **Expert**.
- Stakeholder questions (subset that bears on function): "What are you aiming to achieve with that work? Why is that important to the organization?"; "What does success look like for you and your team?"; "Can you tell me about any constraints related to the work I'm doing that you think would be important for me to know about?"; "Can you tell me about any solutions to this problem or similar projects you've tried before?" Stakeholders "focus on the business and its needs"; they may share what they "know or hear from users or customers".
- Nielsen 2001: "Watch what people actually do." Self-report of past behaviour is "typically 3 steps removed from the truth"; answers about future behaviour are guesses about what sounds appealing. Self-report stays good for motivation ("Why are you visiting our site today?") and for preference after real use.
- Jakob's Law: "Users spend most of their time on other sites", so they "prefer your site to work the same way as all the other sites they already know." This is the basis for inference from category conventions (F2.2).
- What the client answers well here: goals, success, constraints, history, and what people tell him. What he answers badly: what visitors do on the site, and what visitors will do.
- Era: **timeless**.

**F1.6 Agency and studio intake questionnaires.**
- Sources: Ybug, "Website design questionnaire: 32 questions" (Jun 2026); Typeform website questionnaire templates; HTML Burger; Bonsai. **Weak** (vendors that sell form tools; not studios with a published method). A questionnaire from a named reputable studio was searched for and not found in a readable form (see Bound).
- Common questions: the primary goal of the site (leads, sales, awareness, portfolio); "the one action" visitors should take; the audience; rivals; brand assets; functions needed.
- Assessment: these lists ask the client the questions that F1.1, F1.2 and F1.5 say he answers badly ("who is your audience", "what do visitors want") as if they were facts. They give no evidence step and no default. They also mix function with taste ("what sites do you like"). **Do not adopt**.
- Era: era-bound (current templates, 2020s).

**F1.7 impeccable `init` and `shape` (House-adopted craft spine, #119).**
- See F0. impeccable asks the same core questions as F1.1-F1.3 (who, in what situation, what job, what success is) and has the two rules that fit the founder's constraint: scan the repository first and "Confirm inferences"; "Assert the likely reading and invite correction"; one round of two or three questions by default.
- Era: era-bound (impeccable 4.5.0, Oct 2026).

**F1.8 Summary: which questions a non-designer client answers well, and which mislead.**

| Kind of question | Example | Client answers well? | Why (source) |
|---|---|---|---|
| Fact about his business | "What services do you sell? Which do you want more of?" | Yes | He owns the fact (NN/g stakeholder interviews). |
| Goal and success | "What would make the site worth it to you in a year?" | Yes | Stakeholder goal (NN/g; GOV.UK "policy intent"). |
| A real past event | "How did your last three clients find you, and what did they ask first?" | Yes, mostly | A true story of a past event (JTBD). Memory of detail is weak (Nielsen 2001), so ask for recent cases. |
| What people tell him | "What do people ask you before they hire you?" | Yes | Second-hand evidence of the need (GOV.UK "people ... who work with ... users"). |
| Constraint | "What will you give: photos, words, time?" | Yes | Hard or soft constraint (GOV.UK discovery). |
| Keep or cut a page or item | "Keep the blog? The gallery?" | Yes, if a default and a reason come with it | He knows what he uses; Sparkbox client edit. |
| The rank of visitor tasks | "What do most visitors care about?" | **No, it misleads** without evidence | Opinion is an assumption (GOV.UK); "pet ideas" score low (McGovern); about two in three ideas do not improve the metric they target (Kohavi, Microsoft ExP slides, **Expert**). |
| What visitors will do | "Would visitors use a contact form?" | **No** | Prediction of behaviour (Nielsen 2001). |
| Design order on a page | "Which section should come first?" | **No**; it is a design decision | It follows the task rank (#127 B3) and conventions (Jakob's Law). |
| Taste in the abstract | "Modern or classic?" | Partly | Word-pair scales help (mmm-infra#10 opener); taste is best judged on real drafts (#102). Not a function question. |

The founder's own example questions sit in two rows. "What is the most important page you want a visitor to visit" is a **goal** question (the client's wish) and he answers it well, but it must not be read as the visitor's top task. "Why do you think most people care about having easy obvious access to" is a **rank-of-visitor-tasks** question: it asks the client to guess for visitors. Reword it as an evidence question: "What do people most often ask you or look for before they contact you?"

### F2. When to ask rather than infer

**F2.1 The decision rule in the sources: ask only when the doubt is real and a wrong guess costs more than the question.**
- Horvitz, "Principles of Mixed-Initiative User Interfaces", CHI 1999, pp. 159-166. The paper PDF is a scan that I could not read; its principles are taken from Alan Blackwell's Cambridge lecture slides (MPhil ACS R230, 30 Jan 2021), so the strength is **Expert, secondary**. The principles: "Consider uncertainty about user's goals"; "Infer ideal action in light of costs, benefits, and uncertainties"; "Employ dialog to resolve key uncertainties", "consider costs of bothering user needlessly"; "Minimise cost of poor guesses about action and timing"; "Autonomous actions should be taken only when an agent believes that they will have greater expected value than inaction for the user." The framework has two probability thresholds on whether the user has the goal: one between inaction and dialog, one between dialog and action; between them, ask. This comes from Horvitz's patent texts that reuse the framework (US 6,505,167 and 6,553,358, via a search result), **Expert, secondary**; the CHI paper's own text was not read. The same texts say that a cheaper wrong action lowers the probability needed before the agent acts.
- Zhang and Choi, "Clarify When Necessary: Resolving Ambiguity Through Interaction with LMs", Findings of NAACL 2025. **Expert, abstract only** (ACL Anthology listing via search): whether to ask depends on the user's tolerance for interruption and whether one reading of the request clearly dominates.
- impeccable `init` (House spine): "Ask only about material gaps the repository and original request do not answer with strong evidence"; "Confirm inferences"; "Record undecided facts instead of inventing them." impeccable `shape`: "Do not ... repeat settled facts, or turn obvious facts into menus. Assert the likely reading and invite correction."
- GOV.UK discovery: list the assumptions, then "prioritise your risky assumptions". A risky assumption is one where a wrong answer changes what you build.
- Synthesis (mine, from the four): ask about a function only when all three hold. (1) **Doubt**: Claude has two or more readings and the evidence does not make one dominant. (2) **Consequence**: the readings lead to different designs that a later round cannot cheaply fix (a different page order, a different primary action, a page added or cut, a different asset brief). (3) **Owner**: the client or the founder owns the answer, and Claude cannot find it in the files, the current site or the category. When (1) holds and (2) does not, Claude infers, writes the inference as an assumption in the brief, and lets the founder's look at the round correct it. Confidence 0.75: the rule follows from the sources; no source tests it on a design round.

**F2.2 What Claude can infer itself, before any question.**

| Source of evidence | What it tells about function | Strength for a solo professional (mmm-infra) | Strength for a product (Manta) |
|---|---|---|---|
| The client's current site: its pages, menu, buttons, what sits first | What the client chose to put first; which pages exist | High as a record of his choices; low as a record of visitor need ("page visits reflect what you have", McGovern). mmm-infra: one long page plus a blog, a `mailto:` "Get in Touch", no form, broken `/forum` and `/members` (mmm-infra `docs/research/site-audit.md` §1-§4) | Medium: Manta is new; its own routes are the record |
| Site statistics and search terms | Which pages and posts visitors open; what they search | Low to medium. mmm-infra has only Wix built-in statistics in a dashboard nobody has read, and public view counters on the 12 blog posts (site-audit §2.6, §5). Reading the dashboard needs the client or a login | High once live: analytics, search logs (GOV.UK; McGovern) |
| What people ask the client (enquiry emails, first calls) | The candidate top tasks, in the visitor's words | High, but only the client has it, so it is a question (F2.4), not an inference | Medium: support mail, reviews |
| Category conventions and rival sites | What visitors expect to find and where (Jakob's Law) | High for structure (an advisor's site has a profile, expertise, publications, contact). mmm-infra already has precedent research (`docs/research/site-look-precedent.md`) | High: Baymard for accommodation search (#119) |
| The client's own writing | What he wants to be known for; his key message | High for mmm-infra (12 posts, 24 papers and talks; voice guide #21) | Medium |
| The project's rules file and earlier rulings | Audience, register, the one action, standing rules | High where written, but a line marked "assumed" is an inference, not an answer (mmm-infra brand sheet §1: "The one action: get in touch with Mark. This is assumed, not yet confirmed by Mark") | High (Manta `PRODUCT.md`, brand sheet) |
| Earlier round records on sibling tickets | The founder's verdicts about the same client | High (site-look S9 says no step reads them) | High |

- Consequence: for a solo professional, most function facts about **structure** can be inferred (category conventions, current site, his writing). The two facts that only the client holds are the **evidence of visitor need** (what people ask him) and **his own goal** (which work he wants more of). For a product with traffic, the evidence of visitor need comes from data, and the question to the client narrows to goals and constraints.

**F2.3 Signals that function is unknown (each one a trigger to check F2.1).**
1. A page in the plan that the brief does not name, or a page in the current site with no stated job (mmm-infra: `/forum`, `/members`, Gallery, "Docs"). Infer first from F2.2: a broken or empty page with no traffic is cut without a question (the site audit already says "Do not keep"). A page with content he made (Gallery, the publications list) is a keep-or-cut question with a default.
2. Two plausible priorities for one page, where the order changes the layout. Example: on mmm-infra's home page, "get in touch" against "read his publications" against "check his record (CV)". The brief must rank them. If the client's goal and the evidence do not settle the rank, it is a question.
3. A client idea with no stated scope: an idea for one part that could be read as an idea for the whole (site-look S9: Mark's four animation backgrounds became whole-site looks). Ask "for which part?" or infer the narrow scope and say so.
4. An element in a draft with no job that Claude can name (#127 Part D Q1: "A part with no clear function and no D code is noise"). This is not a question to the client. The critic or the builder cuts it or names its job (example: the hairline frame in #102 B9, "a strange box for no reason").
5. An asset judged with no stated use (photos-to-reply S1 and S7: a photo judged for a new-site slot when the question was about its current use). Restate the use first. The founder's own rule: "he didn't specify for what purpose, so we should judge relative to the way he is currently using them". That is an **infer** rule: the current use is the default.
6. A critic that cannot answer a function question from the brief: #127 Part D Q6 needs "task priority for this page"; Q9 needs whether the moment is high-stakes. Where the brief has no rank, the critic reports "function unknown" as a FIT RISK (the fit-gate word) and does not guess.
7. A rules-file line marked "assumed" or "open" that a round now depends on.

**F2.4 The cost of asking, and the trade-offs of the founder's constraint.**
- Cost to the founder: he relays every client question and "will not babysit" a tool. So the questions go out in **one batch** per stage, each plain, each with a default.
- Cost to the client: for mmm-infra, "He doesn't want to do any effort here" (site-look S10, quoted in `docs/research/mmm-infra-site-look-round.md`, which cites session 631cff6d L7785). The client's question budget is small. A questionnaire to Mark already exists as the batch vehicle (mmm-infra#10, ruled on #1 as "One send"), and it already holds the animation block, the voice points and the logo-file ask.
- Fatigue: answers to later questions get shorter and less varied (Galesic and Bosnjak 2009; Krosnick 1991 satisficing, both via mmm-infra `docs/research/option-load.md` §3.3, **Strong secondary** there). So function questions go **early** in the batch and stay few. My limit, from impeccable's "two or three ... per round" and the satisficing evidence: **at most five function questions** to a client per batch. Confidence 0.6; no source tests the number for this use.
- The trade-off of a default answer. A default makes a question fast to answer and lets the client say "yes". But "agreement" is a named form of satisficing (Krosnick, via option-load §3.3): a tired or busy client accepts a default that he would not have chosen. A default therefore **leads** the client.
  - Resolution: given a default that rests on evidence (his own site, his writing, the category), offer it, state its basis in one clause, and name the main other reading, so a "yes" is a choice between two things. Given a default that rests only on Claude's guess about visitors, do not offer it as the client's answer: ask the evidence question ("what do people ask you first?") and keep the guess for the brief, labelled as an assumption.
  - Given a question where a wrong answer costs only one round (a section order inside an agreed page), do not ask; infer, and let the founder's review correct it (#102: the founder corrects drafts quickly, and taste is best judged on real drafts).
- A benefit of asking: participation in the input stage raises the client's identification with the result (Franke, Schreier and Kaiser 2010, via mmm-infra `docs/research/client-feedback-format.md` §1.3). So a few good function questions also help the client accept the site. This does not justify many questions; the effect is from input, not from volume.
- A risk of asking: false certainty. A client's answer about visitors ("most people want my CV") becomes a rule in the rules file and then binds the critic, although it is a guess (GOV.UK: "assumptions that have to be proven"). Resolution: record each answer with its kind: **fact** (his business), **goal** (his wish), **evidence** (what people asked him, with how many cases), or **estimate** (his guess about visitors). The brief's Client values hold evidence and estimate answers as defaults that a round can test, not as gates. The fit gate takes only facts and goals.

### F3. Adopt before build (#119 test)

- No outside source has a question set for this case: an AI that asks a client through a founder who relays, with a small question budget. GOV.UK, top tasks and JTBD assume a team that does its own research with users.
- **Adopt impeccable `shape` Round 1 and `init` Step 3 as the question set.** Reasons: (1) it is already the house's pinned craft spine (#119), and design-round §1 **Intent** already names `impeccable shape` as the interview; (2) it is written for an agent; (3) its core questions (what the surface is for, who reaches it and in what state, the primary thing they must do, what success is, what is uniquely true) match GOV.UK's user need and JTBD's job; (4) it has the two rules the founder's constraint needs: "Assert the likely reading and invite correction" and "Ask only about material gaps ... Confirm inferences".
- **Adopt GOV.UK's evidence rule** as the standard for the answers: "Treat any opinions or suggestions that do not come from users as assumptions that have to be proven". GOV.UK pages carry the Open Government Licence v3.0 (footer of each page; not re-checked here). This rule gives the four answer kinds in F2.4 (fact, goal, evidence, estimate).
- **Cite McGovern's top tasks** for the **shape** of the priority answer: a short ranked list (at most five) of visitor tasks in the visitor's words. Do not adopt the vote for a small client (F1.2 conditions).
- **Cite Sparkbox's content priority guide** for the **artefact** of a page's function: Claude drafts, per page, the parts in priority order as text, and the founder (or client) edits it. This is the "best guess as default" in a form that a non-designer can correct.
- **The house writes only** what no source covers: the triggers (F2.3), the ask-or-infer rule (F2.1), the answer kinds (F2.4), the relay batch (one per stage, at most five client questions), and where each question sits (F4). This follows #119's level 5: "WRITE only where no outside source exists".
- What `shape` lacks, and the house must add: it asks the session's user (the founder), not the end client; it asks for one primary action, not a ranked task list; it has no question about evidence (what people ask the client); and it works per surface, with no site-level set at set-up.
- Era: impeccable is **era-bound** (4.5.0, Oct 2026; it changes weekly, #119 F1). Pin its version in the brief as #119 says. GOV.UK's evidence rule is **timeless**.

### F4. Where each question belongs

| Stage | What is asked | Who answers | Trigger |
|---|---|---|---|
| Set-up (`design-project` §1) | Site-level function: the client's goal; evidence of visitor need (what people ask him); the one action (confirm a default); what a visitor must be sure of; keep or cut each current page (with defaults); what the client will give | Client questions go to the founder as one batch to relay; he may answer any himself | Always, one time, before step 2 writes the rules file. Skip each item that the files or the current site answer (impeccable `init` "scan first") |
| Round brief (`design-round` §1 Intent) | Surface-level function: this page's ranked parts (a content priority list Claude drafts); the scope of a client idea; the use of a supplied asset | The founder, in the session | Only when F2.1's three conditions hold. Otherwise Claude writes the inference in the brief as an **Assumptions** line, and the round goes ahead |
| Critic (`design-critique`, #127 Part D) | No question to anyone. A part whose function the brief does not give is reported as **FIT RISK: function unknown**, with the readings and what each changes. A part with no job at all is a finding (cut it or name its job) | The founder reads it at the reveal (#95: he judges before he reads the critic) | When #127's Q1 or Q6 cannot be answered from the brief |
| Next round's brief | The open FIT RISK from the critic becomes one brief-delta question, with a default | The founder | Once per open FIT RISK |

- Why not ask during a round: the founder judges candidates blind before the critic's verdicts (#95), and he "will not babysit". A mid-round question stops the round. A FIT RISK in the record waits for his normal review.
- Why the set-up batch asks facts and goals but not page-part order: before a layout exists, a client cannot picture page parts (Nielsen 2001: preference is reliable after use, not before). Page-part order is asked at the round, as an edit of Claude's draft list.
- Conflict with impeccable `init`/`shape` cadence ("two or three questions per round"): the set-up batch to a client can be up to five function questions plus the existing set-up items. Resolution: impeccable's cadence is for a live user in a session; the client is reached once, by relay, so one larger batch costs less than several small ones. Keep impeccable's cadence for questions to the founder in a session.

### F5. Test against mmm-infra's history

Units are those of #102 (`docs/research/past-design-rejections.md`) Parts A, B and the mmm-infra part of D (D1-D14): 37 founder rejections or corrections. I add two site-look findings that #102 does not count as units: S9 (inside B8) and S10. "Question" means a function question to the client or the founder, asked up front. "Internal" means a step where Claude states the function of an element or asset itself before it builds or judges, with no question.

| Unit | Founder's words (short) | Would a function step have prevented it? | Which |
|---|---|---|---|
| A5 | "takes far too long, given the purpose of the site" | **Yes**, likely | Question: "What is the opening animation for, and how often does one visitor see it?" The audience was known, so an internal step might also have caught it; it is counted once, as a question. design-round §6's motion brief now asks it. |
| B7 | "a personal expert advisor", never "the firm is the brand" | **Partly** | The fact was already in the brand sheet §5. A page-table "key message" line in the brief would have made it the job each tile answers. The cause was the missing fit gate (#113), not a missing question. |
| B8 (with site-look S9) | the tiles "turned every dial up"; fix "how busy or quiet the background feels" | **Partly** | Scope question (signal 3): "Mark's four background ideas: for the opening animation, or for the whole site?" |
| D14 | "portraits ... must all be held to a very high standard" | **Partly** | Question to the founder: "How many photos does each use need, and how strict is each use?" The standard per use is also taste structure (photo-review P11). |
| B9 | "The line around the edge just reads as a strange box for no reason" | **Yes**, internal | The critic's function walk (#127 Q1): a part with no job is cut. No question needed. |
| D1 | "he didn't specify for what purpose, so we should judge relative to the way he is currently using them" | **Yes**, internal | Restate the asset's use before judging; default to its current use (the founder's own rule). |
| D8 | "What was the point of wiping the name card. How does that improve the image?" | **Yes**, internal | Name the job of each edit before making it (design-critique §3 already says this). |
| D3 | "we need to know why blur is bad, especially as it seems to have been an intentional choice" | **Partly**, internal | Ask what the blur does in that photo's use before calling it a fault. |
| D7 | "This is really weirdly written" (cold-email rules on a reply to Mark) | **Partly**, internal | State what the message is for and to whom, then pick its rules. Correspondence, not design. |
| D10 | "Does it truly have enough pixels when cropped tight enough on Mark's face to work as a portrait?" | **Partly**, internal | Judge in the slot of its use (photo-review P2). |
| Site-look S10 (not a #102 unit) | "Mark will not be doing a photo shoot ... He doesn't want to do any effort here." | **Yes** | A constraint question at set-up: "What will the client give: photos, words, time?" Not a function question; it is in the set because it gates every asset brief. |
| The other 27 units | A1-A4, A6-A12, B1-B6, B10-B11, D2, D4-D6, D9, D11-D13 | **No** | Build errors (curves, gaps, cut-outs, duplicates, ranks), craft (flow), register and taste (childish, techy, boring), process (look before motion), and wrong agent rules. B1 and B2's facts were already written; the gap there was the fit gate (#113). |

Result: of 37 units, a function question asked up front would likely have prevented **1** (A5) and partly prevented **3** (B7, B8, D14). An internal function step, with no question, would likely have prevented **3** (B9, D1, D8) and partly **3** (D3, D7, D10). **27** have no function cause. One more correction (S10) is prevented by a constraint question.

What the test shows:
1. In mmm-infra's history, the costly function faults were inside Claude: it did not state what an element, an asset or a client idea was **for** before it built or judged. The cheapest fix is the internal step (state the function, infer from the evidence, write it as an assumption), not a question.
2. **No rejection traces to a wrong page priority or a wrong primary action.** But mmm-infra has not yet run a layout round: the round-one record moved "Mark is not yet seen or heard" to "the layout round and ... Mark's questionnaire (#10)" (#102 B7), and the brand sheet's one action is still "assumed, not yet confirmed by Mark". So the page-level questions (S1-S5 and R1 in the Answer) are supported by the sources but are **untested** by this history. The layout round and Mark's questionnaire (mmm-infra#10, the natural batch for S1-S6) are their first test.
3. The founder's own rule (D1) is an **infer** rule: when a client does not give the purpose, judge by the current use. This agrees with F2.1: infer when one reading dominates.
4. Sample caveat: 37 units, one client, about one week, all from one founder (#102's caveat applies). Manta has run no round (#102 Part C).

### F6. Clashes between practices, and the resolutions

1. **The client's goal against the visitor's task.** The founder's example "what is the most important page you want a visitor to visit" asks the client's wish. Top tasks and GOV.UK put the visitor's need first. Given a solo professional, the two usually agree on the action (contact) and differ on the route (the client wants contact; the visitor first wants to check the record). Resolution: the visitor's top task sets the **order** of the first view (the proof that this is the right advisor), and the client's goal sets the **primary action** inside it (#127 B3.1: one prominent action per view). Given a product (Manta), the business goal (a booking) and the visitor task (find a bed) are the same path; the conflict is rare, and data settles it. My synthesis; confidence 0.65.
2. **Ask early against ask when the doubt is real.** GOV.UK asks in discovery, before build; impeccable asks only for material gaps. Resolution: at set-up ask only the site-level facts and goals that every later round needs (they are risky assumptions in GOV.UK's sense); ask surface-level questions only on a trigger (F2.3).
3. **The client's word against evidence.** A client's estimate about visitors and a later data point disagree. Resolution: data wins for the rank of tasks (McGovern, GOV.UK); the client's word wins for his goals and his constraints.

### F7. Unconditioned advice met in this research

- Agency questionnaires (F1.6): "Ask the client to name one primary action" and "who is your audience" with no evidence step and no condition. **Unconditioned.**
- impeccable `shape`: "Ask two or three related questions per round" states no condition for a client reached through a relay. **Unconditioned** for this case.
- impeccable `init`: "Do not ask for an aesthetic direction ... during init" is conditioned (it says why: new-work owns visual direction) and agrees with this note: function questions and taste questions are separate.
- GOV.UK "Every piece of published content should meet a valid user need" states its condition (government publishing) but not what to do on a one-person site with no data. It holds here only with F2.2's smaller evidence sources.

## Answer

### The proposed question set

Each question is plain, with Claude's default where the default rests on evidence. "Kind" is the answer kind from F2.4. "To" says who answers: **client** (the founder relays it, or answers himself if he knows), or **founder**.

**At set-up (`design-project` §1), one batch, before the rules file is written. Ask only the items the files and the current site do not answer.**

| # | Question (plain) | What it decides in the design | Kind | To | Default offered |
|---|---|---|---|---|---|
| S1 | "What work do you want more of from the site? Name one or two kinds of client or project." | Which services lead; the words of the primary action | Goal | Client | The service list on the current site |
| S2 | "Think of your last three or four clients. How did each first hear of you, and what did they want to check or ask before they got in touch?" | The visitor's top tasks and their rank; the route to the action | Evidence | Client | None: an evidence question. "Skip" is allowed; then the category's conventions stand as the assumption |
| S3 | "When someone visits the site, what should they do before they leave? Our guess: write to you. Is that right, or is it something else, for example download your CV?" | The one primary action | Goal | Client | From the current site's main button |
| S4 | "What must a visitor be sure of before they write to you? Our guess: that you have done this kind of work for organisations like theirs." | The proof that sits next to the action (record, publications, named clients) | Evidence or estimate | Client | From his own writing and the category |
| S5 | "Here are the pages on your current site and what we plan for each (keep, merge or drop). Change any?" | The site map | Fact | Client or founder | From the site audit |
| S6 | "What will you give for the new site: photos, text, time to review? Our guess: no new photos, two short reviews." | Every asset brief (it would have prevented site-look S10, F5) | Constraint (fact) | Client or founder | From what he has already said |

For a product such as Manta, where the founder is the client and data exists: S2 and S4 come from data first (search logs, reviews, support mail; Baymard for the category), and the questions go to the founder in the session, not by relay.

**In a round's brief (`design-round` §1 Intent), only when F2.1's three conditions hold.**

| # | Question (plain) | What it decides | To | Default |
|---|---|---|---|---|
| R1 | "For [page], this is what we think it must do, in order: 1 …, 2 …, 3 …. Is the order right?" (a content priority list) | The order and weight of the page's parts (#127 B3, Part D Q6) | Founder | Claude's draft list |
| R2 | "[Client]'s idea [X]: is it for [the part we think], or for the whole site?" | The scope of a client idea | Founder | The narrowest part the idea names |
| R3 | "We will judge [asset] for [use]. Is that the use?" | The test an asset is judged by | Founder | Its current use (the founder's D1 rule) |

**From a critic:** no question. A part whose function the brief does not give is reported as **FIT RISK: function unknown**, with the readings and what each changes. The next brief delta turns each open FIT RISK into one R-question with a default.

### The ask-or-infer rule

1. **State before you build or judge.** For each page, each element and each supplied asset in the work, write its function in one line. Take it from the rules file, the current site, the client's writing, the category's conventions and earlier rulings (F2.2).
2. **Infer** when one reading clearly dominates, or when a wrong guess costs one round at most. Write the inference in the brief as an **Assumptions** line. The founder's review of the round corrects it.
3. **Ask** only when all three hold: two or more readings with no dominant one; the readings lead to different designs that a later round cannot cheaply fix; and the answer belongs to the client or the founder and is in no file.
4. **Batch.** Client questions go out one time per stage, at most five function questions, early in the batch, each with a default where a default rests on evidence. Founder questions go in the session, two or three at a time.
5. **Record the kind** of each answer (fact, goal, evidence, estimate). Only facts and goals become gate lines.
6. **Never guess in a critic.** A critic reports "function unknown" as a FIT RISK and does not score that part's function.

Conditions: the rule is for a client who answers through a relay with a small budget (mmm-infra). For a product where the founder is the client (Manta), step 4's limit relaxes, and data replaces the evidence questions. Confidence in the whole six-step rule: 0.7 (the ask condition of step 3 alone: 0.75, F2.1). It rests on the sources in F1-F2 and on one client's history; no source tests it on a design round.

## Bound

- **Read in full:** the issue bodies of design-vault #130 and #96; `plugin/skills/design-project/SKILL.md`; `docs/research/mmm-infra-site-look-round.md`; [mmm-infra-setup-library.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/mmm-infra-setup-library.md); `docs/research/past-design-rejections.md` (lines 15-162, which is all of the findings, counts, answer and bound); impeccable 4.5.0 `reference/shape.md`, `reference/mode-persuade.md`, `reference/routing.md`; `plugin/skills/design-project/references/fit-gate.md` (its three sections).
- **Read in part:** `plugin/skills/design-round/SKILL.md` (§1 the brief, lines 31-42, and a grep of the whole file for brief, function, purpose and question); impeccable `reference/init.md` (Steps 1-3 and the lines that grep found for question, ask, interview, infer); [mmm-infra-photo-review.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/mmm-infra-photo-review.md) (header, every finding's founder's words and root cause, the rubric table, Went well, Lessons); [mmm-infra-photos-to-reply.md](https://github.com/lucmoseley/design-vault/blob/b4a0b43d5/docs/research/mmm-infra-photos-to-reply.md) (grep for purpose, function and use; S1 and S7 bodies); `docs/research/adopt-or-build.md` (outline and Answer); `.claude/tmp/research-function-fit.md` (#127, running in parallel: B3, B7, Part D); mmm-infra `docs/brand/brand-sheet.md` §1-§5, `docs/research/site-audit.md` §1-§2.6 and §4, `docs/research/option-load.md` §3.3-§3.4, and greps of `client-feedback-format.md`; mmm-infra#10 body and comments.
- **Web pages read through the fetch tool:** GOV.UK Service Manual "Start by learning user needs" and "How the discovery phase works"; GOV.UK Government Design Principles; GOV.UK publishing guidance "Identify user needs"; McGovern, A List Apart 2015; NN/g "Stakeholder Interviews 101" (2022), "First Rule of Usability? Don't Listen to Users" (2001), "A Lesson on Top Tasks from Hurricane Beryl" (2024), Jakob's Law video page (2017); jobstobedone.org/learn; Sparkbox "Content Priority Guide" (2013); UW-Madison "Page tables" (2026); Cambridge IWML lecture 2 slides (Horvitz summary, text extracted locally with pypdf).
- **Not readable:** HBR 2016 JTBD article (paywall; summary only); Horvitz CHI 1999 PDF (scanned images); erichorvitz.com (connection refused).
- **Searches run:** McGovern top tasks method; NN/g top tasks (nngroup.com only); content priority guide with Ahava Leibtag (no Leibtag source found); page table with Brain Traffic and Meghan Casey (no Brain Traffic template found); page table with Halvorson's *Content Strategy for the Web* (not confirmed); JTBD switch interview (Moesta); Erika Hall stakeholder questions (no question list found); website design client questionnaire (vendor templates only); Kohavi one-third of ideas; Hinge Research Institute professional-services buyers (no website finding found); Horvitz mixed-initiative principles and thresholds; clarifying questions in language models. No search came back empty, so none was re-run.
- **Not opened:** any session transcript; mmm-infra `docs/research/design-process-order.md` and `site-look-precedent.md`; `docs/research/mmm-infra-logo-motion.md` beyond a grep (its units are in #102 Part A); Manta files (Manta has run no round, #102 Part C); the full texts of Kohavi's slides, Zhang and Choi 2025, and Krosnick 1991 (taken through search results and mmm-infra's option-load note).
- **Not verified:** that page tables come from Halvorson and Rach (2012); the HBR definition of a job; the Open Government Licence on the pages read (assumed from GOV.UK's standard footer); that five is the right limit for client questions (my inference).
