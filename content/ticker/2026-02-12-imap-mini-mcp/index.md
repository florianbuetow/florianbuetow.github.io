---
title: "IMAP Mini MCP"
date: 2026-02-12
draft: false
description: "A lightweight MCP server that connects to any IMAP provider and gives AI agents read access to your inbox - but no sending."
author: "Florian Buetow"
readTime: "2 min read"
categories: ["AI Engineering", "Tools", "Ticker News"]
tags: ["MCP", "Email", "Open Source"]
---

My favorite workflow upgrade this week. I finally had enough of manually sifting through 100+ emails a day and creating custom rules in my email client.

I tried several email MCP servers - they were either too complex for what I needed or the AI did things I absolutely didn't want. Like replying to emails without asking, or marking important emails as read.

So I built my own: IMAP Mini MCP - a lightweight MCP server that connects to any IMAP provider and gives AI agents read access to your inbox plus the ability to draft replies and move emails between folders.

---

## The key design decision: no sending

Agents can read, search, organize, and compose drafts - but they cannot send anything. I don't trust AI to send emails on my behalf (yet).

- List and search emails by time range, sender, or domain
- Fetch full email content and attachments
- Create and update draft replies with proper threading
- Organize with folder management and email moves

With this and speech-to-text, I now ask Claude each morning to fetch the last 24 hours of email and generate a complete overview of what's new and what matters. I can then instruct the AI verbally on what replies to write, links to open, and emails to archive.

[Comment on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7427765798993309696/)

## References

- [imap-mini-mcp on GitHub](https://github.com/florianbuetow/imap-mini-mcp)
