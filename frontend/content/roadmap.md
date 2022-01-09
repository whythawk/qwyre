---
title: Qwyre software and development roadmap
description: Qwyre will be a progressive web app (PWA) with offline support for the reader's library of ebooks. Books can be bought as epubs, or streamed via web monetisation.
---
## Open source and open roadmap

Qwyre is a progressive web app (PWA) with offline support for a reader's library of ebooks. Books can be bought as epubs, or streamed via web monetisation. What a reader buys via web monetisation, they own. Once they have streamed an entire book, they will be able to download an epub version of the work.

We follow an `open roadmap` as our approach for ethics and technical development:

> _Umumtu ngumuntu ngabangtu_ - "I am because we are." There is no line between creator and consumer just as there is no line between genres, stories and influences.

You can read our monthly development updates at [Web Monetization's community forum](https://community.webmonetization.org/qwyre).

Our approach to software development is `encapsulation`. Solid, discrete and modular components that play well together, and stand alone. The components we have already developed and released as part of our roadmap are:

- [Nuxt.js for FastAPI](https://github.com/whythawk/nuxt-for-fastapi)
- [FastAPI, PostgreSQL and Neo4j base project generator](https://github.com/whythawk/full-stack-fastapi-postgresql)
- [Chapisha epub generator](https://github.com/whythawk/chapisha)

More will be added as our roadmap develops.

## Development roadmap

These are the components we aim to deliver to support a Qwyre workflow:

- EPUB generator: convert a `.docx` file to a standards-compliant `.epub` [complete],
- Editor recruitment: manage the recruitment and contractual agreement between a writer and editor [complete],
- eReader: an online standards-compliant EPUB reader [complete],
- Web monetisation: books can be read by streaming and, once paid for via monetisation, can be downloaded as an epub [complete],
- Editor's forum: a formal review process to permit dispute resolution between writers and their editors,
- Curation: create lists of works which can be shared and promoted,
- Search and discovery: a neutral, automated method to categorise and assess creative works to support reader discovery [mostly complete].
- Multilanguage support: all content and text on the app to be translated into multiple languages [partial].

At this time, given the diverse needs of writers and their preferred ways of working, Qwyre will not offer any online editing or writing support. These are to take place offsite.

Where possible, components will be released as free-standing apps as they are developed.
