# sphinx-aimms-theme

This Sphinx theme was designed to provide a great reader experience for documentation users on both desktop and mobile devices for AIMMS projects.

**This theme also includes:** 
- an **AIMMS [pygment lexer](http://pygments.org/)** to highlight your AIMMS [code blocks in sphinx](http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block) 
- an **AIMMS [Domain](http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html)** to document your own AIMMS code.

Please find the documentation of those 2 elements in the Wiki.

This theme is inherited from the great [Read the Docs](https://github.com/readthedocs/sphinx_rtd_theme) but can work with any Sphinx project. 

You can find a working demo of the theme on AIMMS documentation websites:
- [How-to](https://how-to.aimms.com)
- [Documentation](https://documentation.aimms.com)

Installation
===============

This theme is distributed on PyPI and can be installed with pip:

`pip install sphinx-aimms-theme`

To use the theme in your Sphinx project, you will need to add the following to your conf.py file:

``` python
extensions = [
    ...
    "sphinx_aimms_theme",
]

html_theme = "sphinx_aimms_theme"
```

Configuration
================

Theme options
----------------

The following options can be defined in your project’s conf.py file, using the html_theme_options configuration option.

For example:

``` python
html_theme_options = {
    'doc_title': 'Title of my docs',
    'home_page_description': 'my meta description',
}
```

*(if not specified, the option is a string)*

* **doc_title** 

    Title you will see on the top left corner of your docs

* **home_page_title** 

    HTML Title that will appear in the html meta title of your home page 

* **home_page_description** 

    Description that will appear in the html meta description of your home page
    
* **display_community_help_link** 

    Boolean - Displays a link at the bottom of every article redirecting to the [AIMMS community](https://community.aimms.com/) search page filled with the title of the current page.
    
* **display_community_embeddable** 

    Boolean - Displays an embbedable from the AIMMS Community, showing topics filtered with the title of the current page

    
    

Note
---------

**All readthedocs options are available as well !**

https://sphinx-rtd-theme.readthedocs.io/en/latest/configuring.html

This theme is highly customizable on both the page level and on a global level. See https://sphinx-rtd-theme.readthedocs.io/en/latest/configuring.html 


