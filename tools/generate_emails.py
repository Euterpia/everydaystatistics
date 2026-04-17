#!/usr/bin/env python3
"""
Generate 44 HTML email bodies for the Everyday Statistics MailerLite automation.
Pure Python — no external dependencies required.
"""

import os
import re

# ── Sequence definition ──────────────────────────────────────────────────────

SEQUENCE = [
    # (file_stem, day, subject, opener)
    ("0-1",  1,
     "Day 1 of 44 — Why 'a billion pounds' means almost nothing",
     "Welcome. Over the next 44 days you'll read one short unit from Everyday Statistics — a free curriculum designed to make you harder to manipulate with numbers. Today's unit is where everyone starts: the gap between a million and a billion, and why that gap is where most large-number manipulation lives."),

    ("0-2",  2,
     "Day 2 of 44 — The percentage trick politicians use daily",
     "Yesterday we established number scale. Today we move to the vocabulary of proportion — percentages, fractions, and ratios — and specifically the distinction between a percentage point change and a percentage change, which is one of the most reliably exploited gaps in public numeracy."),

    ("0-3",  3,
     "Day 3 of 44 — The word 'average' is probably lying to you",
     "The word 'average' does a lot of work in public discourse, and it is doing it on behalf of whoever chose which kind of average to report. Today you meet all three — mean, median, mode — and learn which one gets suppressed when the truth is inconvenient."),

    ("0-4",  4,
     "Day 4 of 44 — How to spot a doctored graph in three seconds",
     "A graph communicates through visual impression before you've processed a single number. That impression can be engineered. Today's unit catalogues the five tricks — truncated axes, area distortion, dual axes, and others — that account for the vast majority of misleading data visualisation you'll encounter."),

    ("0-5",  5,
     "Day 5 of 44 — Why your gut feeling about risk is wrong by design",
     "Before we reach formal probability, you need an intuitive vocabulary for risk — and you need to understand why your intuitive risk assessment is systematically biased in predictable directions that are routinely exploited. Today's unit is the foundation for everything in Areas 3 and 4."),

    ("1-1",  6,
     "Day 6 of 44 — Two definitions of probability, both in use, rarely distinguished",
     "Most people think probability is a single, agreed concept. It isn't. There are two legitimate interpretations — frequentist and Bayesian — and they give different answers to many real questions. Today you meet both, and learn why the distinction matters every time you read a poll, a forecast, or a risk figure."),

    ("1-2",  7,
     "Day 7 of 44 — Why your brain sees patterns that aren't there",
     "Random sequences look far more 'clumpy' than people expect. Understanding this protects you from one of the most seductive errors in statistics: seeing a pattern in noise and inventing a cause for it. Today's unit is short, and it will change how you read sports commentary forever."),

    ("1-3",  8,
     "Day 8 of 44 — The four rules that govern every probability claim",
     "Today we make probability formal — but just formal enough. Four rules: addition for exclusive events, addition for non-exclusive events, multiplication for independent events, and the complementary rule. These are the tools behind every probability claim you'll ever encounter, and behind some of the most effective ways those claims mislead."),

    ("1-4",  9,
     "Day 9 of 44 — The error that has sent innocent people to prison",
     "The probability of A given B is not the same as the probability of B given A. This seems obvious when stated plainly. It is not obvious in the wild, and confusing the two — the prosecutor's fallacy — has contributed to multiple wrongful convictions. Today you get the tool that sits at the heart of Bayes' theorem."),

    ("1-5", 10,
     "Day 10 of 44 — The number behind every lottery ticket, bet, and policy",
     "Expected value is what probability theory predicts will happen on average, over many trials. The people selling you lottery tickets and insurance policies know it precisely and are counting on you not to. Today you learn to calculate it, and to know when it applies and when it doesn't."),

    ("1-6", 11,
     "Day 11 of 44 — Two identical averages, completely different realities",
     "Two datasets can have identical means and be entirely different in character. Variance and standard deviation measure how far outcomes scatter around the centre — and in finance, medicine, and policy, ignoring spread is how people get catastrophically misled. Today's unit sets up the risk communication work in Area 3."),

    ("1-7", 12,
     "Day 12 of 44 — Why a 99% accurate test is probably wrong",
     "This is the unit at the centre of the curriculum. A positive test result for a rare disease is probably a false positive, even when the test is 99% accurate. The reason is prior probability — and once you understand it, you will read medical screening news, drug trial results, and security threat assessments in a fundamentally different way."),

    ("2-1", 13,
     "Day 13 of 44 — Beyond mean and median: the full descriptive toolkit",
     "Mean and median were the start. Today we complete the picture: variance, standard deviation, percentiles, quartiles, the five-number summary, box plots, weighted averages. These are the tools that let you see what a dataset actually looks like — and notice when someone has shown you only a flattering slice of it."),

    ("2-2", 14,
     "Day 14 of 44 — The bell curve that contributed to the 2008 financial crisis",
     "The normal distribution appears everywhere in nature and in textbooks. That ubiquity led financial modellers to apply it to asset returns, where it doesn't hold — with consequences that are now part of economic history. Today you understand the 68-95-99.7 rule, z-scores, and the normality assumption: what it is, when it's valid, and when it's a very expensive mistake."),

    ("2-3", 15,
     "Day 15 of 44 — What happens when the real world isn't bell-shaped",
     "Real data is rarely normal. Skew, fat tails, bimodal distributions, log-normal distributions, and power laws each produce systematic errors when you treat them as if they were bell curves. Today's unit shows what those errors look like and why they cost money, elections, and lives."),

    ("2-4", 16,
     "Day 16 of 44 — How a survey of two million people got it catastrophically wrong",
     "In 1936, the Literary Digest polled ten million Americans to predict the presidential election — and got it spectacularly wrong, while a smaller sample of 50,000 got it right. Today's unit uses this disaster to explain population vs sample, random sampling, convenience sampling, and self-selection bias."),

    ("2-5", 17,
     "Day 17 of 44 — Why a thousand people can speak for sixty million",
     "A randomly chosen thousand can accurately represent sixty million. A million carefully selected people might tell you almost nothing. Today we look at why size alone is not the point — how the sample was gathered is what determines whether the number means anything."),

    ("2-6", 18,
     "Day 18 of 44 — Almost everyone misreads uncertainty bands — including scientists",
     "Confidence intervals appear everywhere in reported research, and almost everyone who reads them misreads them — including many of the scientists who publish them. Today you get the correct interpretation, and learn why the misreading is not a minor technicality but the difference between knowing something is uncertain and believing it isn't."),

    ("2-7", 19,
     "Day 19 of 44 — The most abused number in science",
     "The p-value is the most cited and most misunderstood number in public science. Almost everyone who uses it is using it wrong — including many scientists who publish with it. Today you learn what it actually means, why the 0.05 threshold is completely arbitrary, and why a result can be both statistically significant and completely worthless."),

    ("2-8", 20,
     "Day 20 of 44 — Two ways a statistical test can fail — and who gets to choose",
     "Every statistical test can fail in exactly two ways: it can find an effect that isn't there, or miss an effect that is. Which failure you find more tolerable is not a technical question — it is a values question, and the answer determines how the system treats you. Today you meet Type I and Type II errors in their natural habitat."),

    ("2-9", 21,
     "Day 21 of 44 — The trick that inflates false discoveries without anyone technically cheating",
     "Today we assemble the full null-hypothesis significance testing procedure: confidence intervals, p-values, error types, one-tailed versus two-tailed tests, and multiple comparisons. The multiple comparisons problem alone accounts for a significant fraction of the replication crisis — and it requires no fraud to operate."),

    ("2-10", 22,
     "Day 22 of 44 — Two frameworks that answer completely different questions",
     "Null-hypothesis testing tells you how surprising your data would be if nothing were going on. Bayesian inference tells you how probable your hypothesis is, given what you now know. These are not the same thing — and the difference matters every time a drug is approved, a trial proceeds to verdict, or a screening programme is designed."),

    ("2-11", 23,
     "Day 23 of 44 — Half of published psychology research doesn't replicate",
     "In 2015, the Open Science Collaboration attempted to replicate 100 published psychology studies. Fewer than 40% produced the same results. This is not a scandal unique to psychology — it is a structural feature of how incentives, publishing norms, and statistical thresholds interact. Today you understand why it happens and how to read primary research with appropriate scepticism."),

    ("3-1", 24,
     "Day 24 of 44 — The trick behind every pharmaceutical advertisement ever written",
     "This is the unit the whole curriculum has been building towards. Lipitor's trial found a 36% reduction in heart attack risk. What the headline didn't say: the absolute risk fell from 3% to 1.9% — a difference of 1.1 percentage points. You need to treat 91 people for three years for one person to benefit. Today you learn to demand both numbers, always."),

    ("3-2", 25,
     "Day 25 of 44 — How to choose the data that proves anything",
     "Cherry-picking doesn't require lying. You can get almost any result you want by choosing which time period to examine, which subgroup to report on, and which of the existing studies to cite. Today's unit makes the mechanics of this visible — so you can spot the invisible denominator every time."),

    ("3-3", 26,
     "Day 26 of 44 — The comprehensive guide to the doctored graph",
     "We started with graph reading in Unit 0.4. Today we go deep: every major technique for visual manipulation, with real examples from politics, media, and corporate communications. By the end, you'll be reading graphs the way a forensic accountant reads balance sheets."),

    ("3-4", 27,
     "Day 27 of 44 — We only see the planes that came back",
     "During World War II, Abraham Wald was asked to recommend where to reinforce returning bombers based on where they had been hit. His insight — that the returning planes were the survivors — saved lives. The same blind spot distorts investment returns, entrepreneurship mythology, and medical evidence wherever failures disappear from the data before you see it."),

    ("3-5", 28,
     "Day 28 of 44 — Why punishment appears to work and praise appears not to",
     "Extreme measurements are followed by less extreme ones — not because anything changed, but because that is how randomness works. This is regression to the mean, and misattributing it to an intervention is one of the most common errors in medicine, management, and sport. It is also why feedback and coaching are systematically undervalued."),

    ("3-6", 29,
     "Day 29 of 44 — Who isn't in this study, and why that matters",
     "The quality of any research finding depends not just on how the sample was selected, but on who was systematically excluded — and why. Today's unit covers the unrepresentative sample: healthy worker effects, WEIRD research populations, funding-driven participant selection, and the gap between trial populations and the people you actually want to treat."),

    ("3-7", 30,
     "Day 30 of 44 — The error in every second headline",
     "'Eating chocolate linked to lower heart disease risk.' 'Countries with more TVs have better health outcomes.' Correlation is not causation — you've heard this. Today you get the full picture: what confounding variables are, what reverse causation looks like, and the specific causal inference tools that let researchers move beyond correlation to something more defensible."),

    ("3-8", 31,
     "Day 31 of 44 — When group statistics don't apply to individuals",
     "The ecological fallacy is the mistake of drawing conclusions about individuals from data measured at the group level. It sounds obvious. It is not obvious in practice, and it has generated some deeply misleading — and occasionally damaging — public health conclusions. Today you learn to spot the unit of analysis before you read any result."),

    ("3-9", 32,
     "Day 32 of 44 — The statistical error at the heart of wrongful convictions",
     "P(A|B) ≠ P(B|A). We covered this in Unit 1.4. Today we see it in its most consequential form: the prosecutor's fallacy, where the probability of the evidence given innocence is presented as if it were the probability of innocence given the evidence. This error has contributed to criminal convictions in multiple jurisdictions."),

    ("3-10", 33,
     "Day 33 of 44 — How to manufacture 'statistically significant' results without lying",
     "Statistical significance can be produced without fraud, simply by making enough analysis choices until the right number appears. Run the analysis twenty different ways, report the one that hits p < 0.05, and you have published a false positive without technically cheating. Today you learn to recognise p-hacking in published research — and in your own intuitions."),

    ("3-11", 34,
     "Day 34 of 44 — The studies that vanish before you see them",
     "For every published study reporting a drug's effectiveness, there may be several unpublished studies reporting that it doesn't work. This is the file drawer problem: negative results don't get published, so the evidence base you're reading is a systematically biased subset of all the evidence that was gathered. Today you see how large that gap can be — and what is being done about it."),

    ("3-12", 35,
     "Day 35 of 44 — The complete toolkit for reading any risk claim",
     "We've covered relative risk, absolute risk, NNT, confidence intervals, p-values, and the full range of biases. Today's unit assembles them into a working framework: a practical checklist for reading any risk claim, from a drug trial to a news headline to a government policy announcement. This is Area 3's closing summary."),

    ("4-1", 36,
     "Day 36 of 44 — Why terrorism feels more dangerous than diabetes",
     "We are now in Area 4: the cognitive errors that make us vulnerable even after we've learned the statistics. The availability heuristic is the tendency to judge probability by how easily an example comes to mind — which means dramatic, recent, or vivid events feel far more probable than they are. Today you see how it's exploited."),

    ("4-2", 37,
     "Day 37 of 44 — The error that makes rare events feel common",
     "Base rate neglect is the failure to weight prior probability correctly when evaluating new information. It is the cognitive version of what Bayes' theorem corrects for mathematically. Today you see the specific ways it manifests — in medical decision-making, criminal justice, and everyday risk assessment — and what 'correcting' for it actually involves."),

    ("4-3", 38,
     "Day 38 of 44 — When adding detail makes something feel more probable",
     "Linda is 31 years old, single, outspoken, and concerned with social justice. Is it more likely that Linda is a bank teller, or that she is a bank teller who is active in the feminist movement? Most people choose the second option. That is logically impossible. Today's unit is about the conjunction fallacy — and what it reveals about how narrative hijacks probability."),

    ("4-4", 39,
     "Day 39 of 44 — Why 'due a win' is always wrong",
     "A coin has come up heads five times in a row. The next flip 'must' be tails. This is the gambler's fallacy, and it is deeply intuitive and completely incorrect. Independent events have no memory. Today you learn the cognitive mechanism, the correct understanding of randomness, and the precise conditions under which the fallacy does and does not apply."),

    ("4-5", 40,
     "Day 40 of 44 — The hot hand — and why it's more complicated than you think",
     "The hot hand — the belief that a player on a scoring run is more likely to score again — was declared a fallacy in 1985. In 2015, a reanalysis showed the original study had a statistical flaw, and the hot hand may be partially real. Today's unit is about both the substantive question and what the controversy reveals about how statistical claims get made and overturned."),

    ("4-6", 41,
     "Day 41 of 44 — The irrelevant number that changes every number that follows",
     "Anchoring is the tendency to rely on the first number you encounter when making an estimate — even when that number is clearly arbitrary. Judges give longer sentences after rolling a high number on a die. Shoppers spend more when prices are anchored high. Today you learn the mechanism and, more practically, what to do about it."),

    ("4-7", 42,
     "Day 42 of 44 — Why experts are confidently wrong — and how to calibrate yourself",
     "Overconfidence is pervasive, consistent across domains, and worse in experts than in novices on questions outside their direct expertise. Calibration — having your stated confidence match your actual accuracy — is trainable. Today you see what good calibration looks like, why it matters, and the specific techniques that improve it."),

    ("4-8", 43,
     "Day 43 of 44 — The heuristic that makes stereotypes feel like statistics",
     "The representativeness heuristic is the tendency to judge probability by how much something resembles a typical case — rather than by base rate frequency. It is how stereotypes override data, how profiling feels rational even when it isn't, and how Linda became a feminist bank teller. Today's unit brings together base rate neglect and the conjunction fallacy under one explanatory roof."),

    ("4-9", 44,
     "Day 44 of 44 — The calibrated mind: everything assembled",
     "This is the final unit. Bayes' theorem is the mathematical synthesis of everything in this curriculum: prior knowledge, new evidence, posterior belief, and the discipline of holding uncertainty accurately. Today we return to where we began in Unit 1.7 — but now with the full context of 43 units behind it. Thank you for being here for all 44 days."),
]


# ── Markdown-to-HTML converter (pure Python) ─────────────────────────────────

def md_to_html(text):
    """Convert a subset of Markdown to HTML. Handles the constructs used in these units."""

    # Strip HTML comments (visualisation placeholders, etc.)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    lines = text.split('\n')
    html_parts = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Horizontal rule
        if re.match(r'^-{3,}\s*$', line):
            html_parts.append('<hr>')
            i += 1
            continue

        # ATX headings
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            content = inline_md(m.group(2))
            html_parts.append(f'<h{level}>{content}</h{level}>')
            i += 1
            continue

        # Unordered list — collect contiguous list items
        if re.match(r'^[-*+]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^[-*+]\s+', lines[i]):
                items.append(f'<li>{inline_md(lines[i][2:].strip())}</li>')
                i += 1
            html_parts.append('<ul>\n' + '\n'.join(items) + '\n</ul>')
            continue

        # Ordered list — collect contiguous list items
        if re.match(r'^\d+\.\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                content = re.sub(r'^\d+\.\s+', '', lines[i])
                items.append(f'<li>{inline_md(content.strip())}</li>')
                i += 1
            html_parts.append('<ol>\n' + '\n'.join(items) + '\n</ol>')
            continue

        # Blank line — paragraph break
        if line.strip() == '':
            i += 1
            continue

        # Paragraph — collect lines until blank or block element
        para_lines = []
        while i < len(lines):
            l = lines[i]
            if (l.strip() == '' or
                re.match(r'^#{1,6}\s', l) or
                re.match(r'^-{3,}\s*$', l) or
                re.match(r'^[-*+]\s+', l) or
                re.match(r'^\d+\.\s+', l)):
                break
            para_lines.append(l.strip())
            i += 1
        if para_lines:
            html_parts.append(f'<p>{inline_md(" ".join(para_lines))}</p>')

    return '\n'.join(html_parts)


def inline_md(text):
    """Convert inline markdown: bold, italic, code, links."""
    # Bold (must come before italic)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text


# ── YAML frontmatter parser ───────────────────────────────────────────────────

def strip_frontmatter(text):
    """Remove YAML frontmatter and return (frontmatter_dict_raw, body)."""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end]
    body = text[end + 4:].lstrip('\n')
    # Minimal key: value parse (single-line values only, enough for our needs)
    fm = {}
    for line in fm_text.split('\n'):
        m = re.match(r'^(\w+):\s*"?([^"]*)"?$', line.strip())
        if m:
            fm[m.group(1)] = m.group(2)
    return fm, body


# ── Email HTML template ───────────────────────────────────────────────────────

EMAIL_CSS = """
body {
    margin: 0; padding: 0;
    background-color: #f5f5f5;
    font-family: Georgia, 'Times New Roman', serif;
}
.wrapper {
    max-width: 640px;
    margin: 0 auto;
    background-color: #ffffff;
}
.header {
    background-color: #1a1a2e;
    padding: 28px 40px;
}
.header a {
    color: #ffffff;
    text-decoration: none;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.progress-bar {
    background-color: #2a2a4a;
    padding: 10px 40px;
}
.progress-bar p {
    margin: 0;
    color: #9999cc;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 12px;
    letter-spacing: 0.5px;
}
.progress-track {
    background-color: #3a3a5a;
    border-radius: 3px;
    height: 4px;
    margin-top: 8px;
}
.progress-fill {
    background-color: #6699ff;
    border-radius: 3px;
    height: 4px;
}
.opener {
    padding: 32px 40px 0;
    border-bottom: 1px solid #eeeeee;
    padding-bottom: 28px;
}
.opener p {
    margin: 0;
    color: #555566;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.7;
}
.content {
    padding: 32px 40px;
    color: #222233;
    font-size: 16px;
    line-height: 1.8;
}
.content h2 {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 36px 0 14px;
    padding-top: 20px;
    border-top: 1px solid #eeeeee;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
}
.content h2:first-child {
    margin-top: 0;
    border-top: none;
    padding-top: 0;
}
.content h3 {
    font-size: 17px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 28px 0 10px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
}
.content p {
    margin: 0 0 18px;
}
.content ul, .content ol {
    margin: 0 0 18px;
    padding-left: 24px;
}
.content li {
    margin-bottom: 8px;
}
.content strong {
    color: #1a1a2e;
}
.content em {
    font-style: italic;
}
.content hr {
    border: none;
    border-top: 1px solid #eeeeee;
    margin: 32px 0;
}
.content code {
    background: #f0f0f8;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 14px;
    font-family: 'Courier New', monospace;
}
.content a {
    color: #3355bb;
    text-decoration: underline;
}
.footer {
    background-color: #f8f8fc;
    border-top: 1px solid #e0e0ee;
    padding: 28px 40px;
}
.footer p {
    margin: 0 0 10px;
    color: #888899;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 13px;
    line-height: 1.6;
}
.footer p:last-child {
    margin-bottom: 0;
}
.footer a {
    color: #3355bb;
    text-decoration: underline;
}
.web-link {
    background-color: #f0f4ff;
    border: 1px solid #ccd4ff;
    border-radius: 6px;
    padding: 16px 20px;
    margin: 0 40px 28px;
}
.web-link p {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 13px;
    color: #445588;
}
.web-link a {
    color: #3355bb;
    font-weight: 600;
}
"""


def build_email_html(day, total, title, unit_id, opener, body_html, web_url):
    pct = round(day / total * 100)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Everyday Statistics Day {day}</title>
<style>
{EMAIL_CSS}
</style>
</head>
<body>
<div class="wrapper">

  <div class="header">
    <a href="https://everydaystatistics.com">Everyday Statistics</a>
  </div>

  <div class="progress-bar">
    <p>Day {day} of {total} &nbsp;·&nbsp; Unit {unit_id} &nbsp;·&nbsp; {pct}% complete</p>
    <div class="progress-track">
      <div class="progress-fill" style="width:{pct}%;"></div>
    </div>
  </div>

  <div class="opener">
    <p>{opener}</p>
  </div>

  <div class="content">
{body_html}
  </div>

  <div class="web-link">
    <p>Read this unit on the web: <a href="{web_url}">{web_url}</a></p>
  </div>

  <div class="footer">
    <p>You're receiving this because you signed up for the Everyday Statistics 44-day course at <a href="https://everydaystatistics.com">everydaystatistics.com</a>.</p>
    <p>The full curriculum is free to read any time at <a href="https://everydaystatistics.com/reference">everydaystatistics.com/reference</a>.</p>
    <p><a href="{{{{unsubscribe}}}}">Unsubscribe</a> &nbsp;·&nbsp; Everyday Statistics, c/o Euterpia Ltd, Scotland, UK</p>
  </div>

</div>
</body>
</html>"""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    units_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'content', 'units')
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'email-drafts')
    os.makedirs(output_dir, exist_ok=True)

    for (file_stem, day, subject, opener) in SEQUENCE:
        unit_file = os.path.join(units_dir, f'{file_stem}.md')
        if not os.path.exists(unit_file):
            print(f'WARNING: {unit_file} not found, skipping.')
            continue

        with open(unit_file, 'r', encoding='utf-8') as f:
            raw = f.read()

        fm, body = strip_frontmatter(raw)
        title = fm.get('title', file_stem)
        unit_id = fm.get('unitId', file_stem.replace('-', '.'))

        body_html = md_to_html(body)

        # Slug for the web URL — same as the file stem with dot notation slug
        slug = file_stem  # e.g. "3-1"
        web_url = f'https://everydaystatistics.com/unit/{slug}'

        html = build_email_html(
            day=day,
            total=44,
            title=title,
            unit_id=unit_id,
            opener=opener,
            body_html=body_html,
            web_url=web_url,
        )

        out_file = os.path.join(output_dir, f'day-{day:02d}-{file_stem}.html')
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f'Day {day:02d} — {title} → {os.path.basename(out_file)}')

    # Also write a subject-lines manifest for easy MailerLite entry
    manifest_file = os.path.join(output_dir, '_subject-lines.txt')
    with open(manifest_file, 'w', encoding='utf-8') as f:
        f.write('Everyday Statistics — Email Subject Lines\n')
        f.write('=' * 60 + '\n\n')
        for (file_stem, day, subject, opener) in SEQUENCE:
            f.write(f'Day {day:02d}: {subject}\n')

    print(f'\nDone. {len(SEQUENCE)} email files written to: {output_dir}')
    print(f'Subject lines manifest: {manifest_file}')


if __name__ == '__main__':
    main()
