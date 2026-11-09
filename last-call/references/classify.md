# Classifying a thread

Inputs: sender address and display name, subject, snippet, Gmail `labelIds` (especially `CATEGORY_*`), message count, and the Rules database. Output: `Junk` or `Keep`, plus a reason of a few words for the Ledger (e.g. `promotions tab, "30% off" subject`).

Work through these in order. The first that applies decides.

## 1. Rules for this sender

Match the sender address first, then the domain (a `brand.com` rule also covers `mail.brand.com`).

- `Keep` → **Keep**.
- `Junk all` → **Junk**, unless it's a protected category (step 2) that the rule's Note doesn't explicitly cover.
- `Junk promos` → **Junk** if it's promotional (step 4) and not protected, even with only one weak signal.

## 2. Protected categories → Keep

Keep anything that looks like one of these, even from a sender with a junk rule, unless the user explicitly named that category for that sender:

- Receipts, invoices, orders, order confirmations, shipping and delivery updates, returns, refunds
- Bookings, reservations, tickets, boarding passes, itineraries, check-in
- Security codes, OTPs, verification links, password resets, login and new-device alerts
- Banking, payments, payouts, statements, tax, insurance, pensions
- Account and legal notices: terms or privacy changes, subscription renewals, billing problems, account closure, data breach notices
- Government, healthcare, school, utilities
- Calendar invites and anything about a scheduled meeting or appointment
- Job applications, interviews and recruiter messages written to the user
- Mail written by a person to the user (personal or work), including cold outreach that names them specifically
- Anything in Gmail's `CATEGORY_PURCHASES` or `CATEGORY_RESERVATIONS`

A promotional subject combined with a transactional one ("Your order has shipped + 20% off your next order") is protected.

## 3. Preferences in the user's words

Apply lines from "Your preferences" on the Notion page. For example, "clear social notifications" makes `CATEGORY_SOCIAL` notification mail **Junk**. If nothing applies, continue.

## 4. Is it promotional?

Strong signals:

- `CATEGORY_PROMOTIONS` in `labelIds`
- Sale language in the subject or snippet: % off, sale, deal, discount, coupon, promo code, free shipping, limited time, last chance, ends tonight, flash sale, new arrivals, new collection, Black Friday, Cyber Monday, gift guide
- Re-engagement: "we miss you", "come back", "still interested?", "complete your profile", "you left something in your cart"
- Content recommendations: "recommended for you", "pins/videos/posts you may like", "trending this week"
- Bulk marketing sender: `marketing@`, `promo@`, `offers@`, `deals@`, `news@`, `newsletter@`, `recommendations@`, or a marketing subdomain like `email.brand.com` or `explore.brand.com`

These signals apply in any language. Judge the meaning of the subject and snippet, not the English keywords.

Weak signals:

- Product announcements, feature tips, webinar or event invitations, surveys, "your weekly digest" from a company
- `noreply@` style sender combined with brand-voice subject lines

Decision:

- `CATEGORY_PROMOTIONS` plus at least one other strong signal → **Junk**
- `CATEGORY_PROMOTIONS` plus only weak signals → **Junk** only if the sender has a `Junk promos` rule, otherwise **Keep**
- Not in Promotions (Primary, Updates, Social, Forums) → **Junk** only with two or more strong signals from a bulk marketing sender; otherwise **Keep** and count it as a close call if it looked promotional
- Anything else → **Keep**

## Not promotional by default

These stay unless the user says otherwise:

- Editorial newsletters the user likely subscribed to on purpose (Substack, writers, publications), as opposed to brand marketing
- Social and community notifications (LinkedIn, X, GitHub, Discord, forums)
- Service updates and usage summaries ("your monthly activity", "your storage is almost full")

## Confidence check

Before returning **Junk**, ask: would a careful assistant bet the user won't miss this email? If not sure, return **Keep**.
