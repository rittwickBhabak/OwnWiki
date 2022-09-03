Introduction
^^^^^^^^^^^^^

Wikipedia is one of the most visited websites on the internet. All of us have used it, some of us have even edited it. Wikipedia is an example of a wiki, a collection of easy-to-edit pages which have links to each other. In this assignment, you are required to create a similar application which allows creating, updating, removing and viewing operations for articles.

This is an application, in python language, which maintains a wiki as a repository of articles in Markdown format. It provides a rendered view of the articles, and permit creation of new articles and editing and removal of existing articles.

Links in the Mardown files are interpreted as links to other pages in the wiki. The user gets redirected to the relevant page upon clicking on the link. If the page does not exist, the user is given the choice to create it.

For example, suppose a page named markdown has the following contents:

\# Markdown

\*\*Markdown\*\* is a simple way to write \*formatted text\*.

Markdown
^^^^^^^^

**Markdown** is a simple way to write *formatted text*.

There is a way to see the list of all articles in the wiki, and selecting an article from the list opens it.
The editor mode have live preview of the Markdown text. That is, during editing, the GUI has 2 panes, one for writing the Markdown source code and one to view the formatted result in real time.

REFERENCES:
===========
* HyperlinkManager module is taken from this link: https://stackoverflow.com/questions/50327234/adding-link-to-text-in-text-widget-in-tkinter
* Python Tkinter library is used to build the GUI
* GitHub is used for version control

Authors:
=======
Rittwick Bhabak (2022MCS2054)

Sagar Agrawal (2022MCS2065)

Manik Jain (2022MCS2832)