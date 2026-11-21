# Survey: how design-inspiration libraries let a person browse

Ticket: lucmoseley/design-vault#22 (map #17). Access date for all facts: 2026-09-30, unless a line gives a different date.

Method: I read the public pages of each site with a fetch tool (the fetch tool converts the page to text). I did not use an account. A fact marked **[secondary]** comes from a source that is not the site itself. A fact marked **[not seen]** means that the fetched page did not show it; it does not mean that the site does not have it.

## Findings per library

### Godly (now Recent)

- Status: `https://godly.website` gives a 301 redirect to `https://recent.design/?ref=godly` (curl, 2026-09-30). The Recent Info page says: "Recent also takes the place of Godly, the popular website inspiration gallery, with a broader feed that goes beyond sites alone." Source: https://recent.design/info (2026-09-30).
- The facts about Godly below come from Wayback Machine copies of godly.website. Sources: https://web.archive.org/web/20251129032828/https://godly.website/directory and https://web.archive.org/web/20251214005244/https://godly.website/website/framer-906 (both read 2026-09-30).
- Top-level ways in (Godly, Nov 2025): the first screen is a feed of site videos with only "Index", "Info", "Subscribe". The "Directory" page has 7 axes: **Types** (industry and kind of site: Design, Agency, Portfolio, Personal, E-commerce, Startup, SaaS, Mobile App, Web App, Motion ...), **Styles** (Light, Large Type, Minimal, Colourful, Animation, Illustrative, Interactive, Scrolling Animation, Dark, Grid, Single Page, Clean, Pastel, Big Background Image, Transitions, Black & White, Fun, Gradient, Unusual Layout, Long Scrolling, 3D, Typographic), **Fonts**, **Platforms** (WordPress, Webflow, Shopify, Framer ...), **Frameworks** (GSAP, React, Next.js ...), **Hosting**, **CMS**. Each axis shows about 20 values and a "View all" link, with a count per value. The Directory page sub-title is "Navigate websites by type, style, platform or a variety of different technologies."
- Each site page shows the tags in labelled groups: "Type", "Style", "Font", "Platform", "Hosting". One tag = one URL (for example `/websites/animation`, "290 animation websites").
- Page-part names: none. Godly tags a whole site, not a section of a page.
- Colour: no separate colour axis. Colour words are Style tags (Light, Dark, Colourful, Pastel, Black & White, Gradient).
- Motion: motion is **tags inside Style** (Animation 290, Interactive 278, Scrolling Animation 225, Transitions 139, Long Scrolling 97, 3D 94). Also "Motion" is a Type (sites of motion studios). The feed shows each site as a video, so the preview itself shows motion (**[secondary]**: HN launch thread https://news.ycombinator.com/item?id=37226805, search result only, 2026-09-30).
- Search or browse: browse. I found no search box on the archived pages.
- Recent (the replacement, live 2026-09-30): top menu "Design", "Websites", "OG Images", "App Screenshots", "App Icons", then "Tools", "Skills", "Jobs". The Websites page has **one** axis: 22 industry chips (All, AI, Agency, Portfolio, SaaS, Ecommerce, Startup, Product, Technology, Finance, Food & Drink, Music, Art, Photography, Architecture, Health, Education, Entertainment, Web3, Crypto, Editorial, Personal). The style axes of Godly are gone. Source: https://recent.design/websites (2026-09-30). Item titles in the Recent feed name motion in words ("prism triangle motion study", "invite code microinteraction", "macOS search to Siri transition"), but I saw no motion filter. Source: https://recent.design (2026-09-30).

### Mobbin

- Scope: product UI (iOS, Android, web apps) and, since a later date, marketing websites ("Sites"). Home page: "Featuring over 1,000 iOS & Web apps, and 200 sites". Source: https://mobbin.com (2026-09-30).
- Top-level ways in: first a **platform** switch with 3 tabs: "Mobile", "Web", "Sites". Then "Browse by category" with 3 or 4 axes per platform:
  - Mobile and Web apps: "Categories" (app industry), "Screens" (screen type: Home, Login, Checkout, Settings ...), "UI Elements" (Tab Bar, Bottom Sheet, Toast, Dialog, Carousel ...), "Flows" (Onboarding, Logging In, Subscribing & Upgrading, Filtering & Sorting ...), plus "Popular Collections". Source: https://mobbin.com/explore/mobile (2026-09-30).
  - Sites: "Categories" (industry), "Sections" (page part), "Styles" (look). Source: https://mobbin.com/explore/sites (2026-09-30).
  - Each card in the feed shows its tags from all axes at once (for example "Hero Section | Finance | Black & White | Illustration | Minimal").
- Page-part names (Sites > Sections, values with a count): 404, About, Blog, CTA Section, Comparison, Contact, Downloads, FAQ, Features (3,586, the largest), Footer Section, How It Works, Newsletter, Pricing, Showcase Section, Social Proof (2,281), Stats Section, Store. "Hero Section" is the most frequent tag on cards in the feed but it does not show in the list page text that I fetched. The list page also mixes in many names without a count ("Nav Bar", "Testimonial Examples", "Why Choose Us", "Pricing Table" ...). These look like search-landing pages, not true sections. Source: https://mobbin.com/explore/sites/sections and https://mobbin.com/explore/sites (2026-09-30).
- Page-part names for app screens (UI Elements, sample): Tab Bar, Top Navigation Bar, Bottom Sheet, Floating Action Button, Segmented Control, Banner, Card, Empty State, Search Bar, Toast, Dialog, Carousel, Sidebar, Progress Indicator, Button. Source: https://mobbin.com/explore/mobile and https://mobbin.com (2026-09-30).
- Style names (Sites > Styles, values with a count): 3D, Black & White, Bold, Colorful, Dark, Editorial, Fun, Glass, Grid, Motion (113), Photography, Scroll Effects (123), Typography. Feed cards also show Light, Minimal, Illustration. Source: https://mobbin.com/explore/sites/styles (2026-09-30).
- Colour: not an axis on Sites; colour words are Styles (Dark, Colorful, Black & White). The footer links a separate "Colors" page (https://mobbin.com/colors). I did not read it.
- Motion: two ways. (1) For Sites, motion is a **Style tag**: "Motion" and "Scroll Effects". (2) For apps, a Flow can play as a "Video": "Experience flows in their natural form complete with micro-interactions, animations and more." Source: https://mobbin.com (2026-09-30). The product overview says: "A free account provides limited access. Paid plans unlock the full library, search, flows, animations, and additional features." Source: https://mobbin.com/index.md (2026-09-30).
- Search or browse: the site presents **search first**. The home page headline block is "Find design patterns in seconds." with tabs "Screens | UI Elements | Flows | Text in Screenshots". The product overview calls Mobbin "a searchable library" and says paid plans unlock "search". The agent tools are three searches only: `search_screens`, `search_flows`, `search_sections`. Browsing by axis is public without an account. Sources: https://mobbin.com, https://mobbin.com/index.md, https://mobbin.com/llms.txt (2026-09-30).

### Awwwards

- Scope: an award site for whole websites, plus a separate "Elements" library of page parts and interactions. Sources: https://www.awwwards.com/websites/ and https://www.awwwards.com/elements/ (2026-09-30).
- Top-level ways in (Websites page): the "Explore" menu has 4 groups: "Awards", "Trending", "By Category", "By Technology", then "Collections". The filter bar on the Websites grid has **7 filters**: "Awards", "Category", "Tag", "Technology", "Country", "Font", "Color". The Category, Tag, Technology, Country and Font filters each have their own search field inside the filter. Colour is a row of swatches with no text labels. Source: https://www.awwwards.com/websites/ (2026-09-30).
  - Category (27, industry): Architecture, Art & Illustration, Business & Corporate, Culture & Education, Design Agencies, E-Commerce, Events, Experimental, Fashion, Film & TV, Food & Drink, Games & Entertainment, Hotel / Restaurant, Institutions, Luxury, Magazine / Newspaper / Blog, Mobile & Apps, Music & Sound, Other, Photography, Promotional, Real Estate, Social responsibility, Sports, Startups, Technology, Web & Interactive.
  - Tag (about 55, a mix of style, page part and motion): for example 3D, Animation, Clean, Colorful, Flat Design, Minimal, Retro, Typography (style); 404 pages, About Page, Contact Page, Footer Design, Header Design, Navigation Menu, Menu - Horizontal, Menu - Vertical, Forms and Input, Gallery, Project Page (page part); Microinteractions, Parallax, Scrolling, Transitions, Infinite Scroll, Gestures / Interaction, Storytelling, Video (motion).
- Page-part names ("Elements" library, Category filter, 46 values): 404 pages, About Us, Animation, Blog, Branding (Logo, Design Systems), CTA, Contact, Content, Cookie, Desktop thumbnail, FAQ, Footer, Forms, Gallery, Header, Hero Image, Icons, Illustration, Interaction, Layout, Loading, Login/Sign up, Maps, Menu, Microcopy and UX writing, Mobile thumbnail, Modal/ Popup, Mouse Interaction, Navigation, Newsletter, Notification (alerts, toast/flash messages), Other Element, Pagination, Photo, Pricing page, Products, Scroll, Search, Shopping cart, Sidebar, Social Share, Stats, Team, Transition, UI Components, Video. The Elements page has only 2 filters: "Category" and "Color". Its sub-title: "Find inspiration for your projects, featuring 100s of examples of forms, great UX/UI, footers, transitions and much more." Source: https://www.awwwards.com/elements/ (2026-09-30).
- Motion: motion is in **three places**. (1) Tags on Websites: Animation, Scrolling, Transitions, Parallax, Microinteractions, Infinite Scroll. (2) Technology filter: GSAP, Lottie, Anime.js, Locomotive Scroll, BARBA.js, Motion, Three.js, WebGL. (3) In Elements, motion values sit **in the same list as page parts**: Animation, Interaction, Mouse Interaction, Scroll, Transition, Loading. Most Element cards are a short **video** ("Page scrolls", "Home to project detail", "Intro loader"). The "Trending" menu also lists "Animated websites" and "Scrolling". Sources: https://www.awwwards.com/websites/ and https://www.awwwards.com/elements/ (2026-09-30).
- Search or browse: **browse and filter** does most of the work. There is a site search in the header, but the Websites and Elements pages lead with the filter bar and the grid. Element detail views are marked "PRO" (paid). Source: same pages (2026-09-30).

### Land-book

- Access: the live site gives HTTP 403 to the fetch tool and to curl (2026-09-30). The facts below come from Wayback Machine copies of the site itself: https://web.archive.org/web/20260928193229/https://land-book.com/ (home, 28 Sep 2026) and https://web.archive.org/web/20260519091202/https://land-book.com/sections (sections, 19 May 2026). Read 2026-09-30.
- Top-level ways in: a tab row with **"Websites", "Sections", "Mobile", "Motion" (marked "New"), "OG Images", "Headlines"**. Under "Websites" there is a row of **page-type** chips: Landing, Portfolio, Blog, Ecommerce, Other, About Us, Career, Sign Up, Pricing, Case Study, Blog Post, Product listing, Product page. Then one "Filters" panel with **6 filters**: "Industry", "Style", "Type", "Typography", "Color", "Platform". Sort: Most Recent, Recommended, Most liked, Most viewed.
  - Industry (37): Advertising, AI, Animals, Architecture, Art, Automotive, Beauty, Charity, Design, Ecommerce, Education, Event, Fashion, Finance, Food & Drinks, Furniture & Interiors, Gaming, Health & Fitness, HR, Kids, Local Business, Magazine, Marketing, Medical, Movie, Music, Nature, News, NFT / Crypto / Web3, Photography, PR, Productivity, Real Estate, Sport, Tech, Travel, Writing.
  - Style (25): 3D, Animation, Apple Style, Background Image, Background Video, Big Footer, Big Type, Big Type in Footer, Black & White, Bottom Navigation, Bright Colors, Brutalism, Cards, Dark Colors, Flat Design, Fun, Gradient, Illustration, Light Colors, Parallax, Pastel Colors, Pattern, People, Stripe Style, Visible Borders. (Style mixes look, colour, layout and motion.)
  - Type (14): Agency, Beta, Community, eBook, Infographic, Mobile App, OS App, Personal, Physical Product, Resource, Saas, Service, Single Page, Software.
  - Typography (3): Display, Sans Serif, Serif.
  - Color (7 named): Red, Yellow, Green, Azure, Blue, Black, White.
  - Platform (5): Figma, Framer, Shopify, Webflow, WordPress.
- Page-part names ("Sections" tab, 14 values, page title "The best section design examples"): **Hero, Value proposition, Features, How it works, Testimonial, Brands, Stats, Pricing, Resources, FAQ, Call to action, Footer, About us, Case study.** The same 6 filters apply to sections. Source: the May 2026 sections copy above.
- Motion: three ways. (1) A **separate top-level tab "Motion"**, marked "New" in Sep 2026. The live page title is "Motion Gallery - Landbook" (**[secondary]**: web search result title, https://land-book.com/motion, 2026-09-30). I could not read the page itself (403 live, no archive copy), so its internal filters are **[not seen]**. (2) Style tags: Animation, Parallax, Background Video, 3D. (3) A search result snippet says free accounts get limited access to motion (**[secondary]**, search result for https://land-book.com/pro, 2026-09-30).
- Search or browse: **browse and filter**. The home page shows the tabs, chips and filters; I saw no search field in the page text. Home sub-title: "We're a curated website design gallery for Creatives, updated daily."

### Savee

- Scope: a general visual-reference board tool (images and videos of any kind), not a website-only gallery. "Members save images and videos from anywhere on the web into boards, discover work through color search, tags, and visual similarity". Source: https://savee.com/llms.txt (2026-09-30). `savee.it` redirects to `savee.com` (curl, 2026-09-30).
- Top-level ways in: the public home page shows **no category axis**. Search needs a login: `https://savee.com/search/` redirects to `/login/?next=%2Fsearch%2F` (curl, 2026-09-30). The Features page names three ways to find things: "Search by Image & Color" ("Upload an image or filter by color to discover visually similar content"), "Related content" ("When you save something you love, Savee shows you visually related inspiration"), and user "boards". Source: https://savee.com/features/ (2026-09-30). The FAQ says related content uses "Tags, context, and visual cues". Source: https://savee.com/faq/ (2026-09-30).
- Page-part names: none.
- Motion: saves can be **videos** ("Saves are the images and videos you collect on Savee"). I saw no motion filter. Source: https://savee.com/faq/ (2026-09-30).
- Search or browse: **search and similarity** do most of the work, as the site presents it ("Powerful discovery ... advanced filters, AI-powered recommendations, and search by image" on https://savee.com, 2026-09-30). The llms.txt names "Search by exact color, tag, or visual similarity" as a key feature.

### Cosmos

- Scope: a general visual-reference tool (images and videos, any subject). Source: https://www.cosmos.so (2026-09-30).
- Top-level ways in: menu "Explore", "Sequence", "Shop", then a **search field** ("Try 'vitsoe shelving'"). The Explore page shows "Selected by Cosmos" collections and one row of **18 subject categories**: Featured, Fashion, Interiors, Graphic Design, Art, Branding, Typography, Architecture, Weddings, Interfaces, Nature, Cinema, Motion, Technology, Portraiture, Quotes, Emotion, Symbol & Myth. Source: https://www.cosmos.so/explore (2026-09-30).
- The home page shows the search modes: "Search the way you think.", then a colour hex ("#bc361b") "By color", "by visual similarity", and an "AI content" filter ("Content detected as likely generated by AI | Show | Blur | Hide"). It also says Cosmos "researches images—surfacing the artist, source, and story." Source: https://www.cosmos.so (2026-09-30).
- Page-part names: none. "Interfaces" is one subject among 18.
- Motion: **one subject category**, "Motion", in the same row as the other subjects. Source: https://www.cosmos.so/explore (2026-09-30).
- Search or browse: **search first**. Home page headline: "Every search opens a new world." and "Your collections, your references, your taste. Connected, searchable, yours." Source: https://www.cosmos.so (2026-09-30).

### One Page Love

- Scope: one-page websites, templates, and a **page-section** library. Source: https://onepagelove.com (2026-09-30).
- Top-level ways in: the "Websites" menu shows **5 axes**, each with a count per value: "Category" (industry and kind: Portfolio, Landing Page, Digital Product, Launching Soon, App, Service, Personal, Event, SaaS, E-commerce ...), "Style" (Illustrative, Scroll Effects, Minimal, Flat Design, Typographic, Fun, Horizontal Layout, Retro & Vintage, 3D, Gradients, Brutalism, Narrow Layout, Grunge, Modular Layout, Glassmorphism, Futuristic, Pixel Art, Editorial, Glitch, Luxury, Bold, Skeuomorphism, Grid Layout, Corporate), "Platform" (WordPress, Webflow, Framer ...), "Tech" (Tailwind CSS, GSAP, Next.js, Lottie, Three.js ...), and "Sections". The footer "Browse" row is: Websites, Sections, Templates, Typefaces, Articles, Resources. Source: https://onepagelove.com (2026-09-30).
- Page-part names ("Sections", page title "Page Section Examples", about 70 values with counts). The largest: Social Proof (740), Lead Capture (524), Testimonials (499), FAQ (361), Pricing (349), Pricing Table (331), Team (320), Client Logos (315), Testimonials Grid (314), Screenshots (311), Contact Form (306), FAQ Accordion (293), Device Mockup (287), Newsletter (282), Header Navigation (259), Infographics (258), Navigation (258), Call-To-Action (249), Footer (238), Waitlist or Beta Sign Up (233), How It Works (192), Client Logo Row (174), Call-To-Action Hero (167), Testimonial Slider (164), Scroll Hint (153), Metrics (149), Client Logo Grid (142), Call-To-Action Footer (137), About (118), Timeline (104), Bento Grid (88). Smaller: Biography, Eyebrow Text, FAQ Grid, Bento Grid - Features, Highlights Row, Feature Carousel, Marquee, Speaker List, Food & Drinks Menu, Manifesto, Looping Product Demo, Client Name List, Z-Pattern Layout, Services List, Hero (22), Lead Capture Hero, Comparison Table, Before After, Product Mockup, Road Map, Avatar Stack, Explainer Video, Recent Blogs, Pricing Slider, Hero Banner, Features (5), Showreel. Note: the sections are **nested** (a parent like "Testimonials" and children like "Testimonials Grid", "Testimonial Slider", "Testimonial Tweets", "Testimonial Videos"). Source: https://onepagelove.com/sections (2026-09-30).
- Colour: no colour axis seen.
- Motion: **Style tag** "Scroll Effects" (1,331, the second-largest style), plus Tech values GSAP, Lottie, Three.js, plus motion-shaped **section** names: Marquee, Scroll Hint, Looping Product Demo, Explainer Video, Showreel, Feature Carousel, Testimonial Slider. Source: https://onepagelove.com and https://onepagelove.com/sections (2026-09-30).
- Search or browse: **browse** leads (the axes fill the menu). A search field ("Search") is in the header. Source: https://onepagelove.com (2026-09-30).

### SaaS Landing Page

- Scope: marketing pages of SaaS companies ("Discover the best 840 landing page examples created by top-class SaaS companies and startups"). Source: https://saaslandingpage.com (2026-09-30).
- Top-level ways in: the first screen shows **one axis, page type**, as 8 tabs: Landing page, Pricing, About Us, Features, Blog, Testimonials, FAQ, Contact Us. The footer adds three more axes: "Popular stacks" (React, Next.js, Tailwind CSS, Webflow, GSAP, Framer, WordPress), "Popular tags" (Productivity, Dark, AI, Code Tool, Finance, Design Tool, B2B) and "Popular fonts" (Inter, Graphik, Geist Sans, Suisse Int'l, Roobert, Geist Mono, Tiempos Headline). Source: https://saaslandingpage.com (2026-09-30).
- Page-part names: the 8 tabs above are **whole pages** ("Pricing pages", "Testimonials pages", "FAQ pages" in the footer), not sections of one page.
- Motion: no motion axis seen; "GSAP" is a stack value.
- Search or browse: **browse**. I found no search field in the page HTML.

### Httpster

- Scope: whole websites, "Hand-picked website design inspiration with typographic, minimal, brutalist vibes." 3,116 sites. Source: https://httpster.net (2026-09-30).
- Top-level ways in: **2 axes** in the menu, each value with a count: "Styles" (19: Colourful, Brutalist, Dark, Fullscreen, Grid, Illustrative, Interactive, Light, Low carbon, Minimal, Monotone, Unusual Layout, Unusual Navigation, Photographic, Print, Responsive, Retro, Scrolling Behaviour, Typographic) and "Types" (31, industry and kind: Advertising, Application / Software, Architecture & Industrial Design, Art & Photography, ... Motion, Music, Ecommerce, Product, Showcase ...). Source: https://httpster.net (2026-09-30).
- Page-part names: none.
- Colour: only as styles (Colourful, Dark, Light, Monotone).
- Motion: **Style tags** "Interactive" (263) and "Scrolling Behaviour" (611); "Motion" is a **Type** (143, sites of motion studios and work). Source: https://httpster.net (2026-09-30).
- Search or browse: **browse** only. No search field in the HTML.

### Page Flows

- Scope: product UI flows and screens from apps, plus emails. Source: https://pageflows.com (2026-09-30).
- Top-level ways in: a **platform** switch "iOS | Android | Web | Email", a **search box** ("Search iOS Products, Screens, UI Elements, Flows"), then **4 axes**: "Products" (named apps), "Screens" (Sign Up, Login, Checkout, Upgrade, Filter, Product details, Search, Dashboard, Plans & pricing, Forgot password ...), "UI Elements" (Text Field, Buttons, Cards, Bottom sheet, Tabs ...), "Flows" (Onboarding, Booking, Buying, Adding, Chat; and grouped lists such as "Account Management": Upgrading Account, Logging In, Resetting Password ...; "Content": Creating & Adding, Searching & Finding, Filtering & Sorting ...), plus "Emails". Source: https://pageflows.com (2026-09-30).
- Page-part names: app-screen names, not marketing-site sections.
- Motion: a flow is a **screen recording** (video). The home page says: "Watch detailed screen recordings with step-by-step annotations highlighting key UI/UX design elements & interac[tions]" and sells "Unlimited access to all user flow recordings". There is no motion filter; the recording is the unit. Source: https://pageflows.com (2026-09-30).
- Search or browse: **both**; the search box sits above the axes on the first screen.

### Refero

- Access: the web pages render only with JavaScript; the fetch tool and curl got an empty shell (2026-09-30). The facts below come from Refero's own machine-readable pages: https://refero.design/llms.txt (last updated 2026-09-05) and https://doc.refero.design/mcp/data-model.md, both read 2026-09-30.
- Scope: web product and marketing screens, iOS app screens, user flows, and "styles". Source: https://refero.design/llms.txt (2026-09-30).
- Top-level ways in: a **platform** split (web, iOS), then **search** of "screens" and "flows", plus browse pages for its **vocabulary**: "Web page types" (`/pagetypes`), with "related vocabulary pages" `/patterns` and `/elements`. The llms.txt says: "Use browse pages to learn Refero's vocabulary: page types, UX patterns, and UI elements." Source: https://refero.design/llms.txt (2026-09-30).
- Each screen carries **three tag lists**: `page_types` ("such as `Dashboard`, `Settings`, or `Paywall & Subscription`"), `ux_patterns` ("such as `Billing & Plans`, `Empty State`, or `Dark Mode`") and `ui_elements` ("such as `Button`, `Table`, `Modal`, or `Switch & Toggle`"), plus `fonts`, `hex_colors` and `colors`, and a prose `content.description` and `content.layout`. Source: https://doc.refero.design/mcp/data-model.md (2026-09-30).
- A "style" is "a semantic design reference extracted from a real web marketing or product page", with fields `northStar` ("short visual thesis"), `theme` ("light, dark, or mixed"), `colors`, `typography`, `spacing`, `layout` ("composition and section rhythm"), `imagery`, `dos` and `donts`. Source: same page. This is the closest match I found to this vault's `image_recipe` / `vocabulary` fields.
- Page-part names: I could not read the full `/pagetypes` list (JavaScript only). **[not seen]**.
- Colour: `hex_colors` per screen, so colour can be searched. The web UI colour filter is **[not seen]**.
- Motion: no motion axis in the data model. "Motion — timing, easing, micro-interactions, reduced motion" is a craft rule in the Refero Skill, not a browse axis. Source: https://doc.refero.design/skill/overview.md (2026-09-30).
- Search or browse: **search first**. Every "Search and browse" link in llms.txt is a search URL except the vocabulary pages; the MCP tool `query` takes "screen type, UI element, pattern, state, company, or on-screen text". Sources: https://refero.design/llms.txt and https://doc.refero.design/mcp/tools.md (2026-09-30).

### Dribbble

- Access: the live site answers the fetch tool and curl with HTTP 202 and a "verify that you're not a robot" page (2026-09-30). The facts below come from Wayback Machine copies of the site itself: https://web.archive.org/web/20250602112050/https://dribbble.com/shots/popular/ and https://web.archive.org/web/20250602045401/https://dribbble.com/ (June 2025), read 2026-09-30.
- Scope: single images and short videos ("shots") by designers, of any design medium, not only websites.
- Top-level ways in: a sort ("Popular", "New & Noteworthy"), then **one row of 9 medium categories**: Discover, Animation, Branding, Illustration, Mobile, Print, Product Design, Typography, Web Design. A "Filters" panel has **3 filters**: "Tags" (free-text), "Color" (a swatch grid of about 90 colours, or "Enter hex or select"), "Timeframe" (Now, This Past Week, This Past Month, This Past Year, All Time). The home page also shows a search area with "Trending searches": landing page, e-commerce, mobile app, logo design, dashboard, icons.
- Page-part names: none. Page parts appear only as free tags or shot titles (for example "Finance website Design", "Tech Consulting Landing Page").
- Motion: **a top-level category**, "Animation", in the same row as the other media. A shot can be a video. No motion sub-types.
- Colour: a real **colour filter** by hex, with a swatch grid.
- Search or browse: **both**. The home page pairs a search field and "Trending searches" with the category row; the categories are a medium axis only.

### Lapa Ninja

- Access: the live site gives HTTP 403 to the fetch tool and to curl (2026-09-30). The facts below come from Wayback Machine copies of the site itself: https://web.archive.org/web/20260723232129/https://www.lapa.ninja/ (home, 23 Jul 2026) and https://web.archive.org/web/20260607082914/https://www.lapa.ninja/elements/ (7 Jun 2026), read 2026-09-30.
- Scope: landing pages ("over 7,300 landing page designs since 2015, along with 15,000+ full-page website screenshots ... complete with full website screenshots and video recordings").
- Top-level ways in: a **search field** at the top ("Search websites and design resources"), then a "Websites" menu with **4 axes**: "Categories" (about 95 values, with a count each; a mix of industry and look: SaaS, Business, Minimal, Agency, Portfolio, 3D Websites, AI, Finance, Illustration, Typography, Gradient, Pattern, Bento Grid, Isometric, Retro Style ...), "Colors" (18: blue, black, white, Multiple Colors, gray, green, red, orange, purple, yellow, navy, teal, pink, brown, aqua, maroon, Ultra Violet, olive), "Platform" (Webflow, Framer, Wordpress, Shopify, Astro ...), "Year" (2015 to 2026). Then top links: "Motion", "OG Images", "Fonts", "Sections", "Templates".
- Page-part names: the "Sections" link goes to `/elements/`, titled "Design Elements Library": "Find inspiration for your projects, featuring the best examples of galleries, menus, footers, transitions, and much more." The values (with item counts): **Loading (14), Mouse Interaction (12), Menu (12), Hover (10), Gallery (9), Footer (4), Text Effect (1)**. This is small and mostly motion; it has no hero, pricing or testimonials.
- Motion: three ways. (1) A **separate top-level "Motion"** link (`/motion/`); I could not read that page (no archive copy, live 403). **[not seen]**. (2) The "Sections" (Elements) list is mostly **interaction types**: Loading, Mouse Interaction, Hover, Text Effect. (3) Sites come with "video recordings".
- Colour: a real **colour axis**, 18 named colours.
- Search or browse: **both**; the search field is the first control, and the home page sells "unlimited access to website categories, past versions, filtering, and search results" as a paid feature.

### Siteinspire

- Access: the live site is behind a Vercel bot check (HTTP 429 to curl; the fetch tool got the page once, then 429). The facts below come from the fetch tool's one read of https://www.siteinspire.com (2026-09-30) and from a Wayback copy: https://web.archive.org/web/20250413040202/https://www.siteinspire.com/websites (13 Apr 2025), read 2026-09-30.
- Top-level ways in: menu "Websites", "Profiles", "About", "Subscribe", "Search". The Websites page shows **tabs for 4 axes plus a shortcut tab**: "Popular Categories", "Styles", "Types", "Subjects", "Platforms". The "Popular Categories" tab (the only one in the static HTML) lists 12 values with counts: Typographic (2,564), Agencies & Consultancies (2,479), Design & Art Direction (2,121), Portfolio (1,491), Web & Interactive Design (1,045), E-Commerce (926), Fashion (908), Grid Layout (805), Minimal (779), Unusual Layout (774), **Use of Animation (578)**, Product Catalogues & Collections (95). Time views: Today's Best, Most Popular this Week, This Month's Best, This Year's Best.
- The values under "Styles", "Types", "Subjects" and "Platforms" are rendered by JavaScript; I did not see the full lists. **[not seen]**. From the popular list, Styles likely holds Typographic, Minimal, Grid Layout, Unusual Layout, Use of Animation; Types holds Agencies & Consultancies, Portfolio, E-Commerce; Subjects holds Fashion, Art, Photography (the fetch tool grouped them so, 2026-09-30).
- Page-part names: none. Siteinspire tags whole sites.
- Motion: **one style tag**, "Use of Animation".
- Search or browse: **browse**. A "Search" link is in the menu, but the page leads with the category tabs.

## Summary: one row per library

"Axes on first screen" counts the browse axes that a visitor sees before a click, not the values inside them.

| Library | Unit of content | Top-level ways in | Axes on first screen | Page-part axis | Motion | Colour | Search or browse | Read from |
|---|---|---|---|---|---|---|---|---|
| Godly (closed; now Recent) | whole site, as a video | Types, Styles, Fonts, Platforms, Frameworks, Hosting, CMS (on the Directory page) | 0 on the home feed; 7 on Directory | no | tags inside Style (Animation, Scrolling Animation, Transitions, Interactive); video previews | colour words inside Style | browse | archive, Nov-Dec 2025 |
| Recent (Godly's successor) | any design item | medium tabs (Design, Websites, OG Images, App Screenshots, App Icons); industry chips on Websites | 1 or 2 | no | words in item titles only | no | browse | live |
| Mobbin | app screen, flow, site section | platform switch (Mobile, Web, Sites), then Categories + Sections + Styles (Sites) or Categories + Screens + UI Elements + Flows (apps) | 1 switch + 3 or 4 | yes: "Sections" (17 counted values) | Style tags "Motion", "Scroll Effects"; app flows play as video | colour words inside Styles | search first (paid); browse is free | live |
| Awwwards | whole site; "Element" (page part or interaction) | Awards, Category, Tag, Technology, Country, Font, Color | 7 | yes: separate "Elements" library (46 values) | tags (Animation, Scrolling, Transitions, Parallax, Microinteractions), tech (GSAP, Lottie), and Element categories (Animation, Interaction, Mouse Interaction, Scroll, Transition, Loading), mostly video | swatch filter | browse and filter | live |
| Land-book | whole site; section | tabs Websites, Sections, Mobile, Motion, OG Images, Headlines; 13 page-type chips; filters Industry, Style, Type, Typography, Color, Platform | 6 tabs + 6 filters | yes: "Sections" (14 values) | separate "Motion" tab (new, 2026) + Style tags (Animation, Parallax, Background Video) | 7 named colours | browse | archive, May and Sep 2026 |
| Lapa Ninja | landing page, with video | search; Categories, Colors, Platform, Year; links Motion, Sections, Fonts | 1 search + 4 | small: "Sections" = 7 elements, mostly interactions | separate "Motion" link; elements Loading, Hover, Mouse Interaction, Text Effect | 18 named colours | both | archive, Jun-Jul 2026 |
| Siteinspire | whole site | Styles, Types, Subjects, Platforms (+ Popular Categories) | 4 | no | one style tag, "Use of Animation" | not seen | browse | live (partial) + archive, Apr 2025 |
| One Page Love | one-page site; section | Category, Style, Platform, Tech, Sections | 5 | yes: "Sections" (about 70, nested) | Style "Scroll Effects"; section names Marquee, Scroll Hint, Looping Product Demo, Showreel | no | browse (search field present) | live |
| SaaS Landing Page | whole page of a SaaS site | page type (8 tabs); footer: stacks, tags, fonts | 1 | page types only (Pricing, Features, Testimonials, FAQ ... as whole pages) | none | "Dark" tag only | browse | live |
| Httpster | whole site | Styles (19), Types (31) | 2 | no | Style tags Interactive, Scrolling Behaviour; Type "Motion" | colour words inside Styles | browse | live |
| Page Flows | app screen, flow, email | platform (iOS, Android, Web, Email); search; Products, Screens, UI Elements, Flows, Emails | 1 switch + search + 4 or 5 | app screen types | a flow is a screen recording | no | both | live |
| Refero | screen, flow, "style" | platform (web, iOS); search; vocabulary pages page types, UX patterns, UI elements | search + 3 vocabularies | page types (list not seen) | none | hex colours per screen | search first | own llms.txt and docs |
| Savee | image or video (any subject) | colour, search by image, tags, boards, feed | 0 public axes | no | videos allowed; no filter | exact colour search | search and similarity | live |
| Cosmos | image or video (any subject) | search; 18 subject chips (one is "Motion") | search + 1 | no | one subject, "Motion" | colour search | search first | live |
| Dribbble | "shot" (image or short video) | 9 medium categories (Animation, Branding, Illustration, Mobile, Print, Product Design, Typography, Web Design, Discover); Tags, Color, Timeframe | 1 row + 3 filters | no | one medium category, "Animation" | hex swatch filter | both | archive, Jun 2025 |

### What the table shows

1. **Style + industry is the base pair for website galleries.** 7 of the 15 (Godly, Mobbin Sites, Awwwards, Land-book, Siteinspire, One Page Love, Httpster) have both a look axis (Style, Styles, or Awwwards "Tag") and an industry axis (Category, Industry, Type, Types, Subjects). Lapa Ninja mixes both in one "Categories" list. The product-UI and general-image libraries do not have this pair. The look axis always mixes look, colour, layout and motion words in one list (for example Land-book Style has "Dark Colors", "Big Footer", "Parallax" side by side).
2. **Page part is a separate axis where a site has one.** Mobbin, Land-book, One Page Love and Awwwards put page parts in their own tab or library ("Sections" or "Elements"), not inside Style. The website-only galleries with no page-part axis (Godly, Siteinspire, Httpster) tag whole sites.
3. **Motion has three patterns.** (a) A tag inside Style: Godly, Mobbin Sites, Httpster, One Page Love, Siteinspire, Land-book. (b) A separate top-level tab or library: Land-book "Motion" (new in 2026), Lapa Ninja "Motion", Awwwards "Elements" (mostly video). (c) One medium or subject among others: Dribbble "Animation", Cosmos "Motion", Httpster Type "Motion". Two sites put motion kinds **in the same list as page parts**: Awwwards Elements (Loading, Scroll, Transition, Mouse Interaction next to Footer, Header) and Lapa Ninja Sections (Loading, Hover, Mouse Interaction next to Footer, Menu). The newest change is toward a separate motion area (Land-book tab marked "New").
4. **Colour is a real filter on about half.** Named colour chips: Land-book (7), Lapa Ninja (18). Swatch or hex: Awwwards, Dribbble, Savee, Cosmos, Refero. The rest put colour words inside Style.
5. **First-screen load is 1 to 7 axes.** The median is about 4. Sites with more axes show them behind one "Filters" button (Land-book, Awwwards) or on a separate "Directory" page (Godly), not all at once.
6. **Search leads where the library is large and paid.** Mobbin, Refero, Savee and Cosmos present search first; Mobbin and Refero put search behind a paid plan. The curated galleries (Godly, Httpster, Siteinspire, One Page Love, Land-book, SaaS Landing Page) lead with browse. Page Flows, Lapa Ninja and Dribbble show both on the first screen.
7. **A platform or medium switch comes first when the library holds more than one kind of thing.** Mobbin (Mobile, Web, Sites), Page Flows (iOS, Android, Web, Email), Refero (web, iOS), Recent (Design, Websites, OG Images, App Screenshots, App Icons), Dribbble (9 media). The switch changes which axes show below it (Mobbin: Sites has Sections and Styles; apps have Screens, UI Elements and Flows).

## Draft common page-part list

Method: I put each marketing-page part name from the five libraries that have a page-part list (Mobbin Sites "Sections", Land-book "Sections", One Page Love "Sections", Awwwards "Elements", Lapa Ninja "Sections"/Elements) and the page-type tabs of SaaS Landing Page into one table. "Shared by" counts the libraries that use the name or a clear variant. I did not count Mobbin names that have no item count (they look like search-landing pages).

| Draft name | Shared by | Names used by each library |
|---|---|---|
| Header / navigation | 3 | Awwwards "Header", "Menu", "Navigation"; One Page Love "Header Navigation", "Navigation"; Lapa "Menu"; Awwwards tag "Header Design" |
| Hero | 4 | Mobbin "Hero Section"; Land-book "Hero"; One Page Love "Hero", "Call-To-Action Hero", "Lead Capture Hero", "Hero Banner"; Awwwards "Hero Image" |
| Value proposition | 1 | Land-book "Value proposition" (keep: it names the block under the hero) |
| Features | 4 | Mobbin "Features"; Land-book "Features"; One Page Love "Features", "Bento Grid - Features", "Feature Carousel"; SaaS Landing Page "Features" (page) |
| How it works | 3 | Mobbin "How It Works"; Land-book "How it works"; One Page Love "How It Works" |
| Social proof: logos | 3 | Mobbin "Social Proof"; Land-book "Brands"; One Page Love "Social Proof", "Client Logos", "Client Logo Row" |
| Testimonials | 3 | Land-book "Testimonial"; One Page Love "Testimonials", "Testimonials Grid", "Testimonial Slider"; SaaS Landing Page "Testimonials" (page) |
| Stats | 4 | Mobbin "Stats Section"; Land-book "Stats"; One Page Love "Metrics"; Awwwards "Stats" |
| Pricing | 5 | Mobbin "Pricing"; Land-book "Pricing"; One Page Love "Pricing", "Pricing Table"; Awwwards "Pricing page"; SaaS Landing Page "Pricing" (page) |
| Comparison | 2 | Mobbin "Comparison"; One Page Love "Comparison Table" |
| FAQ | 5 | Mobbin "FAQ"; Land-book "FAQ"; One Page Love "FAQ", "FAQ Accordion"; Awwwards "FAQ"; SaaS Landing Page "FAQ" (page) |
| Call to action | 4 | Mobbin "CTA Section"; Land-book "Call to action"; One Page Love "Call-To-Action", "Call-To-Action Footer"; Awwwards "CTA" |
| Newsletter / sign-up | 3 | Mobbin "Newsletter"; One Page Love "Newsletter", "Lead Capture", "Waitlist or Beta Sign Up"; Awwwards "Newsletter" |
| Gallery / showcase | 4 | Mobbin "Showcase Section"; Awwwards "Gallery"; Lapa "Gallery"; One Page Love "Screenshots", "Device Mockup" |
| Resources / blog | 5 | Land-book "Resources"; Mobbin "Blog"; Awwwards "Blog"; SaaS Landing Page "Blog" (page); One Page Love "Recent Blogs" |
| About / team | 5 | Mobbin "About"; Land-book "About us"; One Page Love "About", "Team"; Awwwards "About Us", "Team"; SaaS Landing Page "About Us" (page) |
| Case study | 1 | Land-book "Case study" (also a Land-book page type) |
| Contact | 4 | Mobbin "Contact"; One Page Love "Contact Form"; Awwwards "Contact"; SaaS Landing Page "Contact Us" (page) |
| Footer | 5 | Mobbin "Footer Section"; Land-book "Footer"; One Page Love "Footer"; Awwwards "Footer"; Lapa "Footer" |
| 404 / error | 2 | Mobbin "404"; Awwwards "404 pages" |

Names that some libraries file next to page parts but that describe **motion or interaction**, not a part: Loading / intro loader (Awwwards, Lapa), Hover (Lapa), Mouse Interaction (Awwwards, Lapa), Scroll (Awwwards; also "Scroll Effects" in Mobbin and One Page Love styles; "Scrolling Animation" in Godly; "Scrolling Behaviour" in Httpster), Transition (Awwwards; "Transitions" in Godly), Text Effect (Lapa), Microinteractions and Parallax (Awwwards tags; Land-book style "Parallax"), Marquee and Scroll Hint (One Page Love sections). A draft motion list from these: **scroll, hover / cursor, transition (page or state), loading / intro, text effect, ambient loop (marquee, looping demo, background video)**.

Two conventions to note:
- **Suffixes differ, the roots agree.** "Hero" / "Hero Section" / "Hero Image"; "CTA" / "Call to action" / "CTA Section". A short root word works for all of them.
- **Parent and child names.** One Page Love nests (Testimonials > Testimonials Grid, Testimonial Slider, Testimonial Tweets, Testimonial Videos; FAQ > FAQ Accordion, FAQ Grid). For a small library, the parent name alone is enough; a child name can be a free tag.

## Patterns that would suit a small private library (a few hundred references, several projects)

These are my inferences from the survey, not facts from a source.

1. **One kind switch first, when the library holds different kinds of thing.** A vault that holds web pages, brand art and motion can do the same: the switch picks the kind, and only the axes that make sense for that kind appear.
2. **Three axes below the switch, not seven.** Look (style), page part, and motion cover what the large sites spread over 5 to 7 filters. Industry, font, platform and technology matter less for a private library whose "industry" is the founder's own projects; a **project** chip can take the place of industry.
3. **Page part as its own axis, with about 15 to 20 root names.** Use the draft list above. Land-book's 14 names plus Header, Contact, Gallery and 404 cover the five libraries' shared names.
4. **Motion as its own axis with a few kinds.** Most sites file motion as one tag inside Style, which loses the kind of motion. A reference with no motion simply has no motion value.
5. **Colour as a few named chips, not a hex picker.** With a few hundred items, a hex picker returns almost nothing. Land-book's 7 named colours and Lapa Ninja's 18 show the scale; about 8 to 12 names would fit.
6. **A count next to every value, and hide values with a count of 0.** In a small library counts tell the founder where the library is thin.
7. **Every tag on a card is a link.** Mobbin feed cards show the tags from each axis ("Hero Section | Finance | Black & White | Minimal"); Godly detail pages group them under "Type", "Style", "Font".
8. **One stable URL per value.** Godly (`/websites/animation`) and One Page Love (`/section/footer`) give each value its own address, so a brief can link straight to "all hero references".
9. **Browse first, with a plain text filter.** The curated galleries of this size lead with browse; search-first sites are the large paid ones (Mobbin, Refero, Savee, Cosmos). A text box over title, note and tags is enough at a few hundred items.
10. **Motion references as video or a looping preview.** Godly, Awwwards Elements, Page Flows and Lapa Ninja show motion as video. A still of a motion reference hides the reason it was saved.

Bound: I read these pages in full (as fetched text or HTML): Mobbin home, /explore/mobile, /explore/sites, /explore/sites/sections, /explore/sites/styles, /explore/sites/categories (first part), /mcp, /llms.txt, /index.md; Awwwards /websites/ and /elements/ (filter lists in full, grid sampled); One Page Love home and /sections; SaaS Landing Page home; Httpster home; Page Flows home; Savee home, /features/, /faq/, /mcp/, /llms.txt; Cosmos home and /explore; Recent home, /websites, /info; Refero llms.txt and doc.refero.design data-model, tools, examples and skill overview. I read these from Wayback Machine copies of the site's own pages, not the live site: Godly (Directory, one site page, the animation tag page, home; Nov-Dec 2025), Land-book (home Sep 2026, Sections May 2026), Lapa Ninja (home Jul 2026, Elements Jun 2026), Siteinspire (/websites Apr 2025), Dribbble (home and popular, Jun 2025). I only sampled, or did not see: Siteinspire's full Styles, Types, Subjects and Platforms lists (JavaScript-rendered); Land-book /motion and Lapa Ninja /motion (403 live, no archive copy); Refero's /pagetypes, /patterns and /elements lists (JavaScript-rendered); Mobbin /colors and the app-side Screens and UI Elements full lists; any page behind a login. Taken from secondary sources: Godly video previews (a Hacker News search result title) and the Land-book Motion page title and its free-plan limit (web search result text); both are marked [secondary] above. I did not survey Savee's or Cosmos's search results, which need an account.
