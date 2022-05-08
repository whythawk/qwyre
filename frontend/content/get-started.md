---
title: Guide to publishing a standards-compliant ebook
description: Guide to preparing your creative work, and converting a well-formatted Microsoft Word .docx file into a standards-compliant EPUB3 ebook.
---

> **Your creative work and rights:** Your work is not uploaded to the **Qwyre** server until you authorise it, and nothing will be saved on our servers unless you expressly decide to monetize your work via the app. You maintain complete control of the build process. You are not giving up any of your rights over your work, and **Qwyre** is not acting as an agent, publisher, or distributor on your behalf. This is a free service for writers, and respects your property.

Everyone's creative process is different, but there is no doubt that getting to this point - where you are ready to release your work for others to read - has cost you, whether that be forgone income, or quality time with those dearest to you.

For most, the next step is self-publishing and the fraught process of ensuring your text is converted into a standards-compliant ebook. While accessible, the [EPUB3.1 standard](http://idpf.org/epub/30/) can be daunting.

**Qwyre** will guide you through a four-step process to convert your [Microsoft Word](https://www.microsoft.com/en-us/microsoft-365/word) `.docx` file into a standards-compliant `.epub` which you can then further edit, or release.

1. **Describe** your work to prepare the data and terms that allow readers to find your book,
2. **Upload** your cover and text for conversion,
3. **Dedicate** your work to someone or something dear to you (obviously, optional).
4. **Build** your work.

If you prefer to build your ebook programmatically, or maintain complete control of the process, then have a look at [Chapisha](https://github.com/whythawk/chapisha). **Qwyre** is a web app wrapper around **Chapisha**. Everything you can do here, you can do with it too, only on your own computer.

## Describe your work

### Keywords and terms

The terms you use to describe your work are called _metadata_. **Qwyre** will automatically provide an `identifier` and default `language`, but only you can know your `title` and name, as `creator`.

![Describe your work so we know what it is](/content/conversion-describe.jpg)

The more information you can include the better since these data are stored in your _epub_ and used by the distribution platforms you are likely to release your work on to help readers search for something to read.

These are the list of terms available to you:

- _Title_: Name given to the creative work.
- _Description_: A short, single-sentence summary of the creative work.
- _Long description_: The pitch, or jacket-cover, description of the creative work.
- _Creator_: Name of a person, organisation, etc. responsible for the creation of the work. May be more than one.
- _Subject_: The subject, or tag, of the creative work. May be more than one.
- _Rights_: A short, single-sentence statement of copyright and publication terms for the creative work, e.g. 'All rights reserved.' or 'Attribution-NonCommercial-ShareAlike 4.0 International.' If none added, 'All rights reserved.' will be assumed.
- _Identifier_: [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier), [DOI](https://www.doi.org/) or [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) of the creative work. A UUID will be generated if not included.
- _Work website_: The website address for your creative work.
- _Date_: The publication date of the creative work. Provide in ISO format, YYYY-MM-DD.
- _Language_: Specify the language of the creative work.

### Word `.docx` requirements

**Qwyre** will generate your epub, including the cover and table of contents, from the files you upload.

This app currently only supports uploading of `.docx` files. Underneath, we use Pandoc, a ubiquitous open-source file-conversion system, and - while it supports a variety of text formats to epub conversion - only `.docx` files seem to maintain the format from the source file. If this changes (or we find a work-around) we'll upgrade the app.

Your `.docx` file must contain **only** the creative content you wish included in the table of contents. Your document must also be correctly marked up to ensure proper chapter creation. If, after you build your _epub_, you see anything weird in structure or in the table of contents, come back here and review the requirements.

> **Be mindful of this caveat:** EPUB documents will be read on multiple and diverse electronic devices. Don't have any expectations for page number-dependant formatting, preserving your favourite font, line-endings, spacing, or structure. Most ereaders let the user decide exactly how they want their books to be presented. **Qwyre** ensures that this reader sovereignty is supported.

- Each chapter must have a title, formatted as `Heading 1`, with lower-level headings formatted for each heading type.
- There must be no title page, contents, or anything else. Chapter 1 starts at the top of the first line of the document.
- Page numbers and other page-specific information will be lost.
- Fonts or typographic formats and alignment will be lost, although `bold` and `italics` will be maintained.
- Images will be maintained.

Once the work is built you can enhance its styling. However, there are still limits in the EPUB3 standard in comparison to a printed work.

## Attribute artist & contributors

### Give credit to your contributors

Acknowledge the cover artist as a contributor. Other contributors can include editors and translators.

![Provide attribution to those who collaborated or contributed to your work.](/content/conversion-attribute.jpg)

Additional metadata you can add are:

- _Contributor_: Name of a person, organisation, etc. that played a secondary role - such as an artist, editor, or translator - in the creation of the work. May be more than one. This is also where you would list the creator of your cover image, as well as the rights under which these contributions are released.
- _Publisher_: Name of a person, organisation, etc. responsible for making the creative work available.
- _Publisher website_: The URI for the publisher of your creative work.

Please also ensure you have the appropriate rights to use the image on your cover. There are more than sufficient services providing openly-licenced, or even public domain, work for you to use. You wouldn't want anyone to use your work without respecting your rights; have the same respect for visual creators.

### Cover image requirements

<div class="flex"><p>There is, unfortunately, no standardisation on the image size, dimensions or resolution required for an EPUB. However, a recommendation is an image (`.jpeg`, `.jpg` or `.png`) of 1,600 by 2,400 pixels, and less than 5Mb in size. You will need to create your image (or have someone create it for you) exactly as you wish it to appear on the cover. Nothing will be added, removed, or changed.</p><svg xmlns="http://www.w3.org/2000/svg" class="inline-flex font-thin text-xs" width="150" height="240" viewBox="0 0 27.517 43.392"><path fill="#e6e6e6" d="M.529.529h26.458v42.333H.529z" /><path d="M24.62 41.01c0-7.408.183-29.633.183-37.041h-.184-.184c0 7.408.184 29.633.184 37.041zM2.117 3.004c4.233 0 16.933.177 21.166.177v-.177-.178c-4.233 0-16.933.178-21.166.178z"/><text textLength="23" x="1" y="35%">1:1.6</text></svg></div>

## Build your work

The description and content you set are presented in the way you're probably familiar with from various publication sites. Review your text and, when you're satisfied, build your work.

You also have the opportunity to offer a dedication. One is not required, but is appreciated ;p

![Build your work.](/content/conversion-build.jpg)

Depending on how big the files you uploaded are, this may take a little time. Once complete, you can download your work.

> [**Your creative work and rights:**](/privacy-rights) Your work is not uploaded to the **Qwyre** server until you authorise it, and nothing will be saved on our servers unless you expressly decide to monetize your work via the app. You maintain complete control of the build process. You are not giving up any of your rights over your work, and **Qwyre** is not acting as an agent, publisher, or distributor on your behalf. This is a free service for writers, and respects your property.
