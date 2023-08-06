======================
sphinxcontrib-editable
======================

In-line editable documentation

Overview
--------

I read a `discussion
<https://groups.google.com/d/msg/ledger-cli/u648SA1o-Ek/j8cSvPNkCwAJ>`__ by a
library maintainer who uses Google Docs instead of Sphinx for his project
documentation because it lets users provide corrections and feedback inline. He
explains:

    it's a dynamic and collaborative experience. It's a living process. **It
    makes it trivially easy for anyone, with or without an account, with or
    without programming skills, to update the content and collaborate with me
    on it, in-context.** To pop in a correction for a wrong number (so many
    corrections so far!). To reword a phrase poorly constructed (thank you
    readers!). The experience is substantially distinct and better than a wiki
    as well, especially if you have non-technical readers. Comments and
    suggestions are treated differently than content, and integrated with a
    notification system via email. There's no awkward syntax to learn. Even
    technical users have a difficult time keeping wikis up-to-date! I'm
    witnessing it daily, both in the OSS world and in the commercial sphere.
    Maintaining up-to-date docs is REALLY difficult for engineers. Here ...
    well you just make the edit right there in front of your eyes as you notice
    something that needs a change and an email is automatically sent to the
    author.


These sound like important benefits of using Google Docs. But I want to write
my docs in a markup language because it's much more powerful. So my ideal
documentation system would have several features:

* Maintainers can write docs in a powerful markup language.
* Users can edit the docs in-line as they're reading, without needing to log in
  or know reStructuredText.
* Users can comment on the docs with points of clarification.
  (`sphinxcontrib-disqus <https://robpol86.github.io/sphinxcontrib-disqus/>`__
  provides a comments section at the bottom of the page, but no in-line
  comments. This is still a missing piece.)

This library demos no-login editing capability for Sphinx docs.


Live demo
----------

Try out a `live demo here <https://editable-docs-demo.readthedocs.io/en/latest/usage.html>`__.



Contribute
-----------

I need help, especially making the Javascript work better. Come to the issue tracker `on GitHub <https://github.com/metatooling/sphinxcontrib-editable>`__.
