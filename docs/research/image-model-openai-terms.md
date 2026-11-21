# Research: OpenAI and Higgsfield terms for commercial use of GPT Image 2.5 output

Issue: design-vault #55. Date of research: 2026-09-30.

Question: Can the founder (Luc Moseley) use and publish, for commercial purposes, images that GPT Image 2.5 makes through the Higgsfield API?

## Findings

### F1. OpenAI Services Agreement (API terms) — read in full

Source: https://openai.com/policies/services-agreement/
Fetch: openai.com refused a direct fetch (HTTP 403, Cloudflare). This text comes from the Wayback Machine copy of 2026-09-26 16:10 UTC: http://web.archive.org/web/20260926161009/https://openai.com/policies/services-agreement/
Page dates: "Updated: December 1, 2025". "Effective: January 1, 2026".
Note: The URL https://openai.com/policies/business-terms (Wayback 2026-09-12) gives the same text. The old "Business Terms" now point to this Services Agreement ("View previous business terms").

Scope of the agreement (preamble): "This OpenAI Services Agreement only applies to use of OpenAI's APIs, ChatGPT Enterprise, ChatGPT Business, ChatGPT for Clinicians, and other services for customers who are businesses and developers, and does not apply to OpenAI services used by consumers or individuals unless specified above."

Ownership of output (§4.1): "Customer and Customer's End Users may provide Input and receive Output. As between Customer and OpenAI, to the extent permitted by applicable law, Customer: (a) retains all ownership rights in Input; and (b) owns all Output. OpenAI hereby assigns to Customer all OpenAI's right, title, and interest, if any, in and to Output."

OpenAI use of content (§4.2): "OpenAI will only use Customer Content as necessary to provide Customer with the Services, comply with applicable law, enforce the OpenAI Policies, and prevent abuse. OpenAI will not use Customer Content to develop or improve the Services, unless Customer explicitly agrees to such use."

Reservation (§9.1): "Except as expressly set forth herein, the Agreement does not grant: (a) OpenAI any IP Rights in Customer Content; or (b) Customer any IP Rights in the Services. Customer obtains only a limited right to use the Services, and no ownership rights are transferred to Customer or its End Users under this Agreement."
Limited licence to OpenAI (§9.2): "Customer grants OpenAI only the limited rights that are reasonably necessary for OpenAI to deliver the Services."

Responsibility for output (§4.3): "Customer is solely responsible for all use of the Outputs and for evaluating the accuracy and appropriateness of Output for Customer's use case."
Similarity (§4.4): "Output may not be unique, and other users may receive similar content from OpenAI's services. Responses that are requested by and generated for other users are not considered Customer's Output."

End users (§3.2): "Customer is responsible for all activities that occur under its Account, including the activities of End Users with an End User Account or who access the Services through a Customer Application."
Definition: "End User" means any party: (a) who accesses the Services under Customer's Account; or (b) who uses Customer Applications. End Users may include Customer's and its Affiliate's employees, consultants, customers, agents, representatives, students or any other person authorized by Customer to use the Services through Customer's Account."
Restrictions (§3.3): "Customer will not, and will not permit End Users to: (a) use the Services or Customer Content in a way that violates applicable laws or OpenAI Policies; (b) use the Services or Customer Content in a way that violates third parties' rights; [...] (e) except for a Permitted Exception, use Output to develop artificial intelligence models that compete with OpenAI's products and services; [...] (h) interfere with or disrupt the Services, including circumvent any rate limits or restrictions or bypass any protective measures or safety mitigations for the Services; [...]"
Suspension of end users (§8.1): "If an End User: (a) violates the Agreement; or (b) causes, or will cause, a Security Emergency, then OpenAI may request that Customer suspend or terminate the relevant End User account. If Customer fails to promptly suspend or terminate the End User account, then OpenAI may do so."
No third-party beneficiaries (§16.10): "There are no intended third-party beneficiaries to this Agreement, and it is Customer and OpenAI's specific intent that nothing contained in this Agreement will give rise to any right or cause of action, contractual or otherwise, in or on behalf of any third party."
Policies are part of the agreement (§16.1): "This Agreement hereby incorporates by this reference the OpenAI Policies [...]". "OpenAI Policies" means "the Service-Specific Terms, Sharing and Publication Policy, and Usage Policies."
Order of control (§16.2): "(a) Order Form; (b) Service-Specific Terms; (c) Agreement; and (d) OpenAI Policies."

What this means:
- OpenAI gives ALL its rights in the output to the customer. OpenAI claims no ownership of output. The only licence back to OpenAI is to operate the service (§9.2).
- No clause in the agreement prohibits commercial use of output. The only output-use restriction is (e): do not use output to train competing AI models. That does not apply to website, brand, social or print use.
- The contracting "Customer" is Higgsfield, not the founder. The founder is an "End User" of a "Customer Application" (Higgsfield). Higgsfield is responsible to OpenAI for him (§3.2). The founder has no direct contract with OpenAI and gets no direct rights from this agreement (§16.10).
- Ambiguity A (who owns output that an end user makes): §4.1 assigns output to the "Customer" (Higgsfield), "as between Customer and OpenAI". Reading 1: Higgsfield owns it first and its own terms then pass it to the founder (see Higgsfield findings). Reading 2: §4.1 says "Customer and Customer's End Users may ... receive Output", and "as between Customer and OpenAI" only removes OpenAI's claim; the relation between Higgsfield and the founder is for Higgsfield's terms. Both readings agree on one point: OpenAI claims nothing.
- Duty that reaches the founder: §3.3 says Higgsfield "will not permit End Users to" use the service or output against the law, OpenAI Policies or third-party rights. Thus the Usage Policies reach the founder indirectly, through Higgsfield.

### F2. OpenAI Terms of Use (consumer) — read in full (body; footer navigation skipped)

Source: https://openai.com/policies/terms-of-use/
Fetch: direct fetch refused (HTTP 403). Text from Wayback copy of 2026-09-29 07:03 UTC: http://web.archive.org/web/20260929070333/https://openai.com/policies/terms-of-use/
Page dates: "Published: January 1, 2026". "Effective: January 1, 2026".
Note: https://openai.com/policies/row-terms-of-use/ (Wayback 2026-09-29) gives the same text. The EU/EEA/Swiss/UK version ("these terms" link) was not read.

Scope: "These Terms of Use apply to your use of ChatGPT, DALL·E, and OpenAI's other services for individuals [...]". "Our Business Terms govern use of ChatGPT Enterprise, our APIs, and our other services for businesses and developers."
Thus these terms do NOT govern the founder's Higgsfield API use. They are context only. They apply if he makes images in ChatGPT himself.

Ownership: "As between you and OpenAI, and to the extent permitted by applicable law, you (a) retain your ownership rights in Input and (b) own the Output. We hereby assign to you all our right, title, and interest, if any, in and to Output."
Similarity: "output may not be unique and other users may receive similar output from our Services. Our assignment above does not extend to other users' output or any Third Party Output."
OpenAI use of content: "We may use Content to provide, maintain, develop, and improve our Services, comply with applicable law, enforce our terms and policies, and keep our Services safe." (Opt-out from training is available.)
Relevant "What you cannot do" items: "Use our Services in a way that infringes, misappropriates or violates anyone's rights." / "Represent that Output was human-generated when it was not." / "Use Output to develop models that compete with OpenAI."
Duty to check output: "You must evaluate Output for accuracy and appropriateness for your use case, including using human review as appropriate, before using or sharing Output from the Services."
Policies: "you must comply with all applicable laws as well as our Sharing & Publication Policy, Usage Policies, and any other documentation, guidelines, or policies we make available to you."

What this means:
- The consumer terms also assign output to the user and do not prohibit commercial use.
- IMPORTANT DIFFERENCE: The consumer terms contain "Represent that Output was human-generated when it was not." The API Services Agreement (F1) does NOT contain this item. For API use, a similar rule can come only from the Usage Policies or the Sharing & Publication Policy (see F3 and F4).

### F3. OpenAI Usage Policies — read in full

Source: https://openai.com/policies/usage-policies/
Fetch: direct fetch refused (HTTP 403). Text from Wayback copy of 2026-09-29 06:45 UTC: http://web.archive.org/web/20260929064551/https://openai.com/policies/usage-policies/
Page date: "Effective: October 29, 2025". Changelog top line: "2025-10-29: We've updated our Usage Policies to reflect a universal set of policies across OpenAI products and services." No later change on the page at the capture date.

Who the policy binds: "Your use of OpenAI services must follow these Usage Policies". The policy is one universal set for all OpenAI products (API and consumer). It does not separate the API customer from the end user.

Clauses that can touch image use by a hostel business:
- "Protect people [...] you cannot use our services for: [...] threats, intimidation, harassment, or defamation [...] destruction, compromise, or breach of another's system or property, including malicious or abusive cyber activity or attempts to infringe on intellectual property rights of others [...] circumventing our safeguards"
- "Respect privacy [...] you may never use our services for: [...] use of someone's likeness, including their photorealistic image or voice, without their consent in ways that could confuse authenticity"
- "Empower people [...] we don't allow our services to be used to manipulate or deceive people [...] including any use for: [...] deceit, fraud, scams, spam, or impersonation"
- "Keep minors safe" list (not relevant to hostel brand art, except: do not sexualize or endanger minors in any image).

What the Usage Policies do NOT contain (checked by a full read of the page):
- No rule that requires disclosure that an image is AI-made.
- No rule against a claim that an image is human-made. (That rule is in the consumer Terms of Use only, F2.)
- No rule about C2PA or provenance metadata.
- No rule against commercial use, advertising or marketing. No brand or trademark rule, other than "attempts to infringe on intellectual property rights of others".

Ambiguity B ("circumventing our safeguards"): Reading 1: this means safety filters and refusals inside the service; removing metadata from a finished file is not "circumventing our safeguards". Reading 2: C2PA metadata is a safeguard, so its removal is circumvention. The page does not name C2PA. The favourable reading (Reading 1) is the more natural one: the list item is about use of "our services", and the Services Agreement §3.3(h) gives the same idea as "bypass any protective measures or safety mitigations for the Services" — a rule about the service, not about the output file after delivery. Safe practice: do not remove the metadata on purpose when there is no need.

Practical duties for the founder from this page:
- Do not make a photorealistic image of a real, identifiable person (for example a guest or a staff member) without consent, where the image "could confuse authenticity".
- Do not use images to deceive (for example a fake photograph of a room or a view that misleads a guest about the hostel). This is the "deceit, fraud" item. Stylised brand art and illustrations are not deceit.
- Do not copy other people's intellectual property (for example another company's logo or a copyrighted character).

### F4. OpenAI Service Terms (Service-Specific Terms) — read in full (long paragraphs of sections 3(a), 7, 10 sampled at their first 600 characters; they are about ChatGPT Enterprise, Apps and local software, not images)

Source: https://openai.com/policies/service-terms/
Fetch: direct fetch refused (HTTP 403). Text from Wayback copy of 2026-09-25 06:00 UTC: http://web.archive.org/web/20260925060041/https://openai.com/policies/service-terms/
Page date: "Updated: September 21, 2026".

Rank: "If there is a conflict between the Service Terms and your Agreement, the Service Terms will control."

There is NO section for image generation or for GPT Image models (gpt-image-1, 2, 2.5). Sections are: 1 API; 2 Beta Services; 3 ChatGPT Enterprise, Edu, Healthcare and Business; 4 Codex and Code Generation; 5 GPTs; 6 Image and Video Capabilities; 7 Apps and Actions; 8 Voice Conversations; 9 Medical Use; 10 Licensed Materials; 11 ChatGPT Sites; 12 OpenAI Academy; 13 Financial Plugins and ChatGPT for Financial Services.
The only non-commercial restriction on this page is for voice: "ChatGPT Voice Output is for non-commercial use only [...]".

§6 Image and Video Capabilities (verbatim): "Our models can accept images and videos as part of Inputs to the Services ("Visual Capabilities"). You may not use Visual Capabilities to assist in identifying a person nor to solicit or infer private or sensitive information about a person. You may not use Visual Capabilities to reproduce the likeness of any person without express consent and all necessary rights. By choosing to share an image or video publicly on the Services, such as by sharing it to the Sora feed or uploading it to create a Sora cameo, you represent you have all necessary rights, and you give OpenAI the right to reproduce, distribute, modify, display and perform it for the purpose of operating and promoting the Services. [...]"
Note: "Visual Capabilities" is defined as images and videos given as INPUT. The likeness rule thus applies when the founder uploads a photo of a person as a reference. The licence to OpenAI applies only to images shared "publicly on the Services" (for example the Sora feed). Images made through Higgsfield's API are not shared publicly on OpenAI's Services, so OpenAI gets no display or promotion licence to them.

§1 API — output IP indemnity (verbatim): "OpenAI's indemnification obligations to API customers under the Agreement include any third party claim that Customer's use or distribution of Output infringes a third party's intellectual property right. This indemnity does not apply where: (i) Customer or Customer's End Users knew or should have known the Output was infringing or likely to infringe, (ii) Customer or Customer's End Users disabled, ignored, or did not use any relevant citation, filtering or safety features or restrictions provided by OpenAI, (iii) Output was modified, transformed, or used in combination with products or services not provided by or on behalf of OpenAI, (iv) Customer or its End Users did not have the right to use the Input or fine-tuning files to generate the allegedly infringing Output, (v) the claim alleges violation of trademark or related rights based on Customer's or its End Users' use of Output in trade or commerce, and (vi) the allegedly infringing Output is from content from a Third Party Offering."
What this means: This indemnity protects the API "Customer" (Higgsfield), not the founder. The Services Agreement §16.10 says there are no third-party beneficiaries. The founder must not expect OpenAI to defend him against a copyright claim. The text of the indemnity does not restrict commercial use; it confirms that "use or distribution of Output" is an expected use.

§2 Beta Services: a model offered as "alpha, preview, early access, or beta" is "excluded from any indemnification obligations". Whether GPT Image 2.5 is labelled beta on OpenAI's side was not checked.

### F5. Higgsfield Terms of Use Agreement — sections 1 to 17.1 read in full; sections 17.2 to 19 (withdrawal, arbitration, general provisions) sampled by keyword search only

Source: https://higgsfield.ai/terms-of-use-agreement (linked from the footer of https://higgsfield.ai/)
Fetch: direct fetch succeeded (HTTP 200) on 2026-09-30.
Page dates: "Last updated: July 26, 2026". "Effective: immediately for users who register on or after July 26, 2026; on August 27, 2026 for users who registered before July 26, 2026, or upon earlier acceptance." Thus on 2026-09-30 this version binds the founder, whatever his date of registration.
Scope: the agreement covers the website and "any application programming interfaces ("API") [...]". Thus it covers the founder's API use.

Ownership and commercial use (§4.4 User Inputs and Outputs, verbatim): "Company does not claim ownership of any of your Inputs or Outputs, nor does it restrict your commercial use of Outputs. Your rights in Outputs you have generated and exported survive cancellation of your subscription or deletion or termination of your Account, and you may transfer or sublicense your rights in Outputs to your clients or other third parties."
Second confirmation (§5.1(ii)(e)): "(for clarity, this clause does not limit your commercial use of Outputs as described in Section 4.4)".
Licence to Higgsfield (§4.4): "You acknowledge and agree that Your Content, Inputs, and Outputs may be used by Company to train, develop, enhance, evolve, and improve its (and its affiliates') AI models [...]". "You hereby grant to Company the same rights and license set forth in Section 4.3 with respect to any Inputs and Outputs [...]". §4.3 limits that licence to "the purpose of operating, providing, and maintaining the Service, and as further described in Section 4.4", and it "ends when you delete Your Content or delete your Account" (with exceptions for backups, public content and legal retention).
Marketing use by Higgsfield (§4.4): "Company may use Your Content, Inputs, or Outputs in Company's own marketing or promotional materials, but only (a) where you have made that content publicly available on the Service [...], or (b) with your consent; Company will not use your private content, or private content you create for or on behalf of a client, in its marketing without your consent."
Uniqueness (§4.4): "Other users may receive an Output that is similar or possibly identical to yours. Company does not guarantee the uniqueness, originality, or exclusivity of any Output."

Plan dependence: The current terms contain NO plan condition on commercial use. §4.4 applies to all users; it does not name a free, trial or paid plan. Plans change only usage limits (§1.5 "Usage Limits may vary by subscription tier"), content retention (§3.4) and "Unlimited" fair use (§10.6). (The pricing page is checked in F6.)

Clause that defers to the third-party model provider (§8, second paragraph, verbatim): "Certain features and models available through the Service are provided by third-party model providers. When you use a feature or model powered by a third party, you agree to comply with that provider's applicable acceptable-use or prohibited-use policies (as updated from time to time), in addition to this Agreement; where those policies are more restrictive, the more restrictive terms govern your use of that feature or model."
Flow-down of OpenAI terms: The terms do not name OpenAI (keyword search of the full page). §8 flows down only the provider's "acceptable-use or prohibited-use policies". For OpenAI that is the Usage Policies (F3). It does NOT flow down OpenAI's Services Agreement or its ownership clause. Even if it did, the OpenAI ownership clause (F1 §4.1) is not "more restrictive": it assigns output to the customer.
Ambiguity C: Does §8 bring in the consumer Terms of Use rule "Represent that Output was human-generated when it was not" (F2)? Reading 1 (favourable, and the natural reading): no; §8 names "acceptable-use or prohibited-use policies", and the Terms of Use are a contract, not a use policy. Reading 2: the "What you cannot do" list in the Terms of Use acts as a prohibited-use policy. This ambiguity has no practical effect, because Higgsfield's own terms contain the same rule (below).

Direct duties on the founder in the Higgsfield terms:
- §5.2(xi): not "represent that any Output is human-generated when it is not".
- §11.7 Output Responsibility (applies to API users, §11.1): "You shall not represent to End Users or third parties that Outputs are human-generated. You are responsible for providing any disclosures regarding AI-generated content required by applicable law."
- §5.5 AI Disclosure (verbatim): "Where required by applicable law, you will disclose that Output is artificially generated or manipulated, and you will not remove, alter, or obscure any provenance signals or markings Company applies under Section 6.4."
- §5.1(ii)(b): no Output that "infringes the rights of any person or entity, including their intellectual property or privacy rights, or depicts them without permission or legal justification". §5.1(ii)(a) includes "deceptive, fraudulent".
- §5.2(iv): do not use Outputs to train any AI model (except own Inputs).
- §13.2: "You are solely responsible for conducting any necessary rights clearances before using, distributing, or publishing any Output."
- §6.6: if Higgsfield notifies that an Output violates rights, stop using it, delete it, and do not re-generate it.
- §12: indemnity to Higgsfield for use of Outputs in violation of the agreement or law.

Provenance (§6.4, verbatim): "Company may embed machine-readable watermarks, secure metadata, or content-provenance signals (such as those based on the C2PA / Content Credentials standard) into Outputs so that Outputs can be identified as AI-generated. Company may make such markings imperceptible and enable third parties to detect them. Company does not warrant that any marking will be applied to, or persist in, every Output."
Ambiguity D (scope of "Where required by applicable law" in §5.5): Reading 1 (favourable): the opening words qualify the whole sentence; the founder must disclose AI and keep the markings only where a law requires it. Reading 2 (strict): the opening words qualify only the disclosure clause; the second clause ("you will not remove, alter, or obscure any provenance signals or markings Company applies") is a separate, unconditional promise. Reading 2 is the safer reading. Note also: the no-removal promise covers only markings "Company applies under Section 6.4" — markings that Higgsfield applies. Markings that OpenAI applies inside the model output are not named. A second reading says that markings in the file that Higgsfield delivers are markings Higgsfield "applies". The favourable reading: the promise covers only Higgsfield's own markings.
Related clause (§4.1): "You may not remove, alter, or obscure any copyright, watermark, trademark, service mark or other proprietary notices incorporated in or accompanying the Service." This names the Service, not Outputs. The favourable and more natural reading: it does not apply to marks inside an Output file.
Practical note: normal publishing steps (resize, crop, convert to WebP, re-save for print, upload to social media that removes metadata) can remove C2PA metadata. No clause read here says that such routine processing is a breach.

### F6. Higgsfield: plan dependence of commercial use, and the API catalogue — sampled

Sources and fetch (all direct, HTTP 200, 2026-09-30):
- https://higgsfield.ai/pricing — the plan table is drawn by JavaScript. The server HTML has no plan text; not read.
- The site's English text bundle https://higgsfield.ai/_i18n/en.e35da288da.json (2.2 MB; searched by keyword only). It holds the strings the site shows. The page on which each string shows was NOT verified.
- https://higgsfield.ai/gpt-2 (the GPT Image 2 page) — searched by keyword.
- https://higgsfield.ai/terms-of-use-agreement-23-07-2026 (the previous terms version) — searched by keyword.
- https://open.higgsfield.ai/explore, /pricing and /models/marketing-studio/image/playground (the API site; cloud.higgsfield.ai and higgsfield.ai/api redirect to open.higgsfield.ai) — searched by keyword.

UI strings that make commercial use depend on the plan (verbatim, from the text bundle):
- "Yes. All paid plans include commercial usage rights, so you can use generated content for marketing, advertising, social media, or any other business-related purpose."
- "Yes. All generations made with a paid Higgsfield plan come with a commercial license. Check your plan details for specifics on usage rights."
- "Yes. Generations made through Higgsfield Plugins are covered by the same usage rights as Higgsfield's web platform — including commercial use on paid plans. For full details, see the Higgsfield Terms of Service."
- "Personal use only" and "Watermark is applied for Free Plan" (plan-table strings; context not verified).
- "Team doesn't grant commercial usage rights to your generations." and "Scale doesn't grant commercial usage rights to your generations." (context not verified; "Team" and "Scale" are probably plan names compared with Enterprise).
- Enterprise: "Commercial usage rights, legal indemnification, and no training on your data."
UI strings with no plan condition:
- "Yes. Everything you make on Higgsfield is cleared for commercial use."
- "Yes. You own full commercial rights to all assets generated on the platform, regardless of which model you use. [...]"
- GPT Image 2 page FAQ: "Can I use GPT Image 2 for commercial work? Yes. Accurate logos, readable packaging, brand-consistent colors, and clean typography make it suitable for marketing, advertising, product photography, and editorial content."
The previous terms version (23-07-2026) has the same §4.4 words: "Company does not claim ownership of any of your Inputs or Outputs, nor does it restrict your commercial use of Outputs." No plan condition was found in it.
The API site pricing page and the Marketing Studio Image playground page contain no "commercial", "terms" or "licen" text.

Ambiguity E (plan dependence): Reading 1 (favourable): the binding contract is the Terms of Use (F5). §4.4 says Higgsfield does not "restrict your commercial use of Outputs", with no plan condition, and §19.14 says: "This Agreement constitutes the final, complete, and exclusive agreement between the parties regarding its subject matter and supersedes all prior discussions or agreements." Marketing FAQ text is not part of the agreement. Thus commercial use is allowed on every plan, including a trial. Reading 2: plan descriptions shown at purchase can be "Supplemental Terms" under §1.3 ("described in the applicable supplemental Service or [...] presented to you for your acceptance when you sign up"), and "If these Terms of Use are inconsistent with the Supplemental Terms, then the Supplemental Terms control". Then a plan marked "Personal use only" (probably the free plan), or "Team"/"Scale" if those strings apply to the founder's plan, could limit commercial use.
For the founder: he pays for API use (paid API credits or a paid trial). The UI strings give commercial rights to "all paid plans". Thus under both readings his outputs have commercial rights, UNLESS his plan is one that a plan table marks "Personal use only", "Team" or "Scale". This was not verified, because the plan table needs JavaScript and the founder's plan name is not known here. Action: the founder can look at his plan card on the pricing or billing page once, and keep a screenshot with the date.

Model identity note: On the API catalogue, the endpoints marketing-studio/image/sunburst ("Marketing Studio Image 2.5 Sunburst", released 2026-09-01) and marketing-studio/image/flare ("2.5 Flare") show the company "Higgsfield", not OpenAI. The catalogue data read here does not name OpenAI or GPT Image for these endpoints. The statement that they run GPT Image 2.5 comes from the design-vault context (#34), not from a page read here. This matters a little: Higgsfield §8 applies a provider's use policy "When you use a feature or model powered by a third party". If the endpoint is powered by OpenAI, OpenAI's Usage Policies apply through §8 and through OpenAI's Services Agreement §3.3. The favourable reading and the safe reading give the same practical result, because the OpenAI Usage Policies (F3) add almost nothing beyond Higgsfield's own §5.

### F7. OpenAI provenance (C2PA, SynthID, visible watermark) for GPT Image API output

Sources:
(a) OpenAI Help Center, "Provenance signals (Content Credentials, SynthID) in OpenAI-generated content" — https://help.openai.com/en/articles/8912793-c2pa-in-chatgpt-images — read in full. Direct fetch refused (HTTP 403). Wayback copy of 2026-09-20 14:11 UTC: http://web.archive.org/web/20260920141125/https://help.openai.com/en/articles/8912793-c2pa-in-chatgpt-images . Page date: "Updated: 23 days ago" at capture, thus approximately 2026-08-28.
(b) OpenAI API docs, "Content provenance" — https://developers.openai.com/api/docs/guides/content-provenance.md — read in full. Direct fetch, HTTP 200, 2026-09-30. No date on the page.
(c) OpenAI, "Introducing our latest image generation model in the API" — https://openai.com/index/image-generation-api/ — sampled (Safety paragraph). Wayback copy of 2026-09-16. Page date: April 23, 2025.
(d) OpenAI API docs, image generation guide https://developers.openai.com/api/docs/guides/image-generation.md (sampled by keyword), model pages https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst.md and .../gpt-image-2.5-flare.md (read in full), changelog https://developers.openai.com/api/docs/changelog.md (sampled). Direct fetch, HTTP 200, 2026-09-30.

Which signals GPT Image API output carries — (a), verbatim table row: "Images | C2PA metadata and SynthID watermarks | Supported images generated with ChatGPT, Codex, and the OpenAI API include both signals." Then: "Coverage can vary by product, model, export path, file type, and when the content was created."
(c), for gpt-image-1: "The gpt-image-1 model in the API leverages the same safety guardrails as 4o image generation in ChatGPT, including safeguards that restrict the model from generating harmful images and the inclusion of C2PA metadata in generated images".
(b), example C2PA result: "issuer": "OpenAI OpCo, LLC", "model": "gpt-image".
Visible watermark — (a): "You can request a visible disclosure on images generated with ChatGPT, Codex, and the OpenAI API by prompting the model to include one. [...] Visible watermarks are separate from embedded provenance signals like C2PA metadata and SynthID watermarks." Thus OpenAI adds NO visible watermark by default.

Summary: GPT Image output from the OpenAI API carries (1) C2PA metadata (signed, issuer "OpenAI OpCo, LLC"), and (2) an invisible SynthID watermark inside the pixels. No page read here names gpt-image-2.5 specifically; "Supported images generated with [...] the OpenAI API" is the general statement. Higgsfield's delivered files carry no C2PA metadata (F10).

Rules against removal — what the OpenAI pages say:
- (a) and (b) state as fact that metadata is often lost: (a) "Metadata was stripped during upload, download, editing, conversion, or sharing." (b) "Editing, converting, or sharing a file can remove its metadata." (b) "Compression, cropping, screenshots, metadata removal, and format conversions can erase or weaken a signal." These pages treat such loss as normal. They do not call it a violation.
- (b) has one "Don't" about watermarks, in the section "Use verification results responsibly", which is about the verification API: "Don't use repeated queries to reverse-engineer, remove, or evade a watermark." This is about use of the verification API. It is not a general rule on output files.
- No OpenAI terms or policy page read here (F1 to F4) contains a rule that names C2PA, SynthID, provenance, metadata or watermark removal. The nearest words are "bypass any protective measures or safety mitigations for the Services" (Services Agreement §3.3(h)) and "circumventing our safeguards" (Usage Policies). See Ambiguity B in F3.
- The API image output indemnity (F4, Service Terms §1) is lost where the customer "disabled, ignored, or did not use any relevant [...] safety features". That affects Higgsfield's indemnity, not the founder's right to publish.
Context only: (a) says "Consistent with our commitments under the European Commission's Code of Practice on Transparency of AI-generated content, our goal is to expand provenance signals [...] so customers and developers have clear ways to meet their own transparency obligations". This shows that law (for example the EU AI Act transparency rules) can require AI labels. That is a legal duty, not an OpenAI terms duty, and it was not researched here.

Model facts (d): the changelog entry of Sep 8 (2026) says: "Released GPT Image 2.5 Sunburst and GPT Image 2.5 Flare for image generation and editing through the Image API and the Responses API image generation tool." Model IDs "gpt-image-2.5-sunburst" and "gpt-image-2.5-flare". The model pages give no model-specific terms, and they do not label the models alpha, beta or preview. The image guide says only: "All prompts and generated images are filtered in accordance with our content policy [link: usage-policies]." Thus no GPT Image specific terms page exists among the pages read; GPT Image output is governed by the general terms (F1 to F4).
The names match Higgsfield's endpoints "marketing-studio/image/sunburst" and "/flare" ("2.5 Sunburst", "2.5 Flare"). This supports, but does not prove, that those endpoints call OpenAI's GPT Image 2.5 (see the model identity note in F6).

### F8. OpenAI Sharing & Publication Policy — read in full

Source: https://openai.com/policies/sharing-publication-policy/
Fetch: direct fetch not tried after the other openai.com pages gave HTTP 403. Wayback copy of 2026-09-08 18:25 UTC: https://web.archive.org/web/20260908182503/https://openai.com/policies/sharing-publication-policy/
Page date: "Updated: November 14, 2022".
Status: The Services Agreement (F1) defines "OpenAI Policies" as "the Service-Specific Terms, Sharing and Publication Policy, and Usage Policies", and §16.1 incorporates them. Thus this policy is part of Higgsfield's contract with OpenAI. The consumer Terms of Use (F2) also name it.

Clauses (verbatim):
- Section "Social media, livestreaming, and demonstrations": "Posting your own prompts or completions to social media is generally permissible, as is livestreaming your usage or demonstrating our products to groups of people. Please adhere to the following: Manually review each generation before sharing or while streaming. Attribute the content to your name or your company. Indicate that the content is AI-generated in a way no user could reasonably miss or misunderstand. Do not share content that violates our Content Policy or that may offend others. [...] Recall that you are interacting with the raw model, which means we do not filter out biased or negative responses."
- Section "Content co-authored with the OpenAI API": "Creators who wish to publish their first-party written content (e.g., a book, compendium of short stories) created in part with the OpenAI API are permitted to do so under the following conditions: The published content is attributed to your name or company. The role of AI in formulating the content is clearly disclosed in a way that no reader could possibly miss [...]". "People should not represent API-generated content as being wholly generated by a human or wholly generated by an AI, and it is a human who must take ultimate responsibility for the content being published."

This is the ONLY OpenAI page read that asks for an AI label on published content.

Ambiguity F (does the social-media AI label apply to the founder's brand images?):
- Reading 1 (favourable): The policy is from 2022, before OpenAI sold image models in the API. Its words are text-model words ("prompts or completions", "raw model", "livestreaming your usage", "demonstrating our products"). The social-media section is about showing the tool and its raw results, not about a business that publishes finished brand art. The publication section names only "written content (e.g., a book [...])". Also, Higgsfield's §8 flow-down (F5) brings in only "acceptable-use or prohibited-use policies"; a sharing policy is not clearly one of those. The founder has no direct contract with OpenAI. Under this reading, no OpenAI label duty applies to hostel images on a website, in print, or on social media.
- Reading 2 (strict): Any AI output that is posted to social media is a "completion" that is shared; images are included. The founder, as an End User, reaches this policy through the Services Agreement §3.3(a) duty on Higgsfield ("will not permit End Users to [...] violate [...] OpenAI Policies"). Under this reading, a social-media post of an AI image must show that it is AI-made "in a way no user could reasonably miss". Website and print use are not "social media" and are not "written content", so Reading 2 still does not reach them.
- Favourable reading: Reading 1. Low-cost safe practice under Reading 2: on social media posts that show a GPT Image picture, add a short "AI-generated" note or turn on the platform's own AI label.

### F9. Copyright caveat (context, not a bar) — US Copyright Office

Sources (direct fetch, HTTP 200, 2026-09-30):
- https://www.copyright.gov/ai/ — sampled. It says: "Part 2 was published on January 29, 2025, and addresses the copyrightability of outputs created using generative AI."
- https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf ("Copyright and Artificial Intelligence, Part 2: Copyrightability", January 2025, 52 pages) — sampled: executive summary conclusions, section II analysis of prompts, and section V conclusion.

Verbatim conclusions (executive summary):
- "Copyright does not extend to purely AI-generated material, or material where there is insufficient human control over the expressive elements."
- "Based on the functioning of current generally available technology, prompts do not alone provide sufficient control."
- "Human authors are entitled to copyright in their works of authorship that are perceptible in AI-generated outputs, as well as the creative selection, coordination, or arrangement of material in the outputs, or creative modifications of the outputs."
Analysis: "The Office concludes that, given current generally available technology, prompts alone do not provide sufficient human control to make users of an AI system the authors of the output."

What this means for the founder:
- This is NOT a bar on use or publication.
- It limits what he can STOP OTHERS from doing. A picture made from a prompt alone probably has no US copyright. Then a competitor who copies the picture is probably not infringing a copyright.
- His own human additions can be protected: the logo he draws, text he writes, his edits, and the creative selection and arrangement (for example a poster layout that combines AI art with his own design work).
- Brand protection comes better from trademark law (the hostel name and a logo that is used in trade) than from copyright in AI art. Not researched here.
- Other countries differ. The founder's own jurisdiction was not researched.

### F10. The delivered files: no metadata, no visible mark — all seven read in full

Files: `~/higgsfield-calibration-2026-09-30/r1..r3/v11-gpt-flare.png` and `v12-gpt-sunburst.png` (six files), and `~/higgsfield-palette-52/r1/v1-gpt-sunburst-palette.png`. All are 2688x1520 PNG.

Metadata: each file has only the `IHDR`, `IDAT` and `IEND` chunks. There is no `caBX` (C2PA) chunk, no JUMBF data and no text chunk. Thus Higgsfield delivers the files without OpenAI's C2PA manifest (F7). The founder does not remove it; it is not present when he receives the file.

Visible mark: the full frames and the four 400x220 px corners of each file show no logo, text or badge.

Not done: no SynthID detector was run. The invisible watermark (F7) can still be in the pixels.

## Verdict

Bars commercial use? NO. No OpenAI page read (Services Agreement, Terms of Use, Service Terms, Usage Policies, Sharing & Publication Policy, GPT Image 2.5 model pages) prohibits commercial use of image output. The only non-commercial rule found is for ChatGPT voice output (Service Terms §8), which does not apply to images. Higgsfield §4.4 says it does not "restrict your commercial use of Outputs", and allows transfer and sublicence of Outputs to third parties. Plan caveat: Higgsfield marketing text gives commercial rights to "all paid plans" and shows "Personal use only" on at least one plan (probably free). The founder pays, so he is covered under both readings of Ambiguity E, unless his plan is one that the plan table marks as without commercial rights ("Team", "Scale" — not verified).

Claims output? NO. OpenAI assigns all its rights in Output to the customer and claims none (Services Agreement §4.1; Terms of Use "Ownership of content"). OpenAI keeps only the licence it needs to run the service (§9.2). Higgsfield does not claim ownership (§4.4). BUT Higgsfield takes a licence to use Inputs and Outputs to train its AI models (§4.4), unless an Enterprise Agreement applies; this licence ends when he deletes the content or account (§4.3, with exceptions). Higgsfield may use his Outputs in its marketing only if he makes them public on Higgsfield or consents (§4.4). The founder's ownership chain runs OpenAI -> Higgsfield (the OpenAI "Customer") -> founder (Higgsfield user).

Duties on the founder (all direct from the Higgsfield terms unless marked):
1. Do not say or suggest that an AI image is human-made (Higgsfield §5.2(xi), §11.7). This is a no-false-claim rule, not a duty to label.
2. Disclose AI generation where a law requires it (Higgsfield §5.5, §11.7). Which laws apply to him (for example EU AI Act transparency rules) was not researched.
3. Do not remove Higgsfield's provenance markings on purpose (Higgsfield §5.5, second clause; Ambiguity D: under the favourable reading this also applies only where a law requires it). No OpenAI rule was found that prohibits removal of C2PA or SynthID from a delivered file; OpenAI says ordinary editing and sharing remove metadata. Safe practice: keep the original file; do not strip metadata on purpose.
4. No photorealistic likeness of a real person without consent; no uploads of a person's photo as a reference without consent (OpenAI Usage Policies and Service Terms §6, reaching him through Higgsfield; Higgsfield §4.2(b), §5.1(ii)(b), §5.3).
5. No deceit (for example a fake photo that misleads guests about the hostel), no infringement of other people's IP or trademarks (Usage Policies; Higgsfield §5.1). Rights clearance before publication is his job (Higgsfield §13.2). Neither OpenAI's IP indemnity (it covers Higgsfield, not him, and excludes trademark use in trade) nor Higgsfield protects him against a third-party claim; he indemnifies Higgsfield (§12).
6. Do not use the images to train an AI model (OpenAI §3.3(e); Higgsfield §5.2(iv)).
7. Possible, low-cost: an "AI-generated" note on social media posts of these images (OpenAI Sharing & Publication Policy; Ambiguity F — the favourable reading says it does not apply to him).
8. If Higgsfield notifies that an image violates rights, stop using it and delete it (Higgsfield §6.6).

Net answer for the founder's stated uses (website, brand art, social, print): he may use and publish GPT Image 2.5 output from Higgsfield commercially.

Bound:
- Read in full: OpenAI Services Agreement (Wayback 2026-09-26; same text at business-terms, Wayback 2026-09-12); OpenAI Terms of Use body (Wayback 2026-09-29; row-terms-of-use gives the same text); OpenAI Usage Policies (Wayback 2026-09-29); OpenAI Sharing & Publication Policy (Wayback 2026-09-08); OpenAI Help Center provenance article (Wayback 2026-09-20); OpenAI API content-provenance guide (direct); GPT Image 2.5 Sunburst and Flare model pages (direct); Higgsfield Terms of Use Agreement sections 1 to 17.1 (direct).
- Sampled: OpenAI Service Terms (Wayback 2026-09-25; all section headings and all image, API, beta and voice clauses read; long Enterprise, Apps and Licensed Materials paragraphs read to 600 characters); Higgsfield terms sections 17.2 to 19 (keyword search; §19.14 read); Higgsfield previous terms version 23-07-2026 (keyword search); Higgsfield English UI text bundle (keyword search; page context of each string not verified); Higgsfield /gpt-2 page (keyword search); Higgsfield API site explore, pricing and Marketing Studio Image playground pages (keyword and data search); OpenAI image generation guide and API changelog (keyword search); OpenAI "Introducing our latest image generation model in the API" (Wayback 2026-09-16; Safety paragraph); US Copyright Office AI page and Part 2 report (summary, prompts analysis, conclusion).
- Not read: OpenAI EU/EEA/UK Terms of Use; OpenAI Brand Guidelines; openai.com/verify; Higgsfield pricing plan table (JavaScript page; no text in server HTML); Higgsfield Privacy Policy; any Higgsfield Enterprise Agreement or plan-specific Supplemental Terms; any law on AI labelling (EU AI Act or other) or the founder's local copyright law; a SynthID check of a delivered file. (F10 read the PNG chunks of all seven delivered files.)
