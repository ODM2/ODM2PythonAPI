Contribute to Documentation
============================

This guide is a reference on how to contribute to ODM2 Documentation effort
for the many `ODM2 Software Ecosystem <https://github.com/ODM2/odm2-software-ecosystem>`__.

Conventions
-----------

There are a few conventions that should be followed
when writing docstrings within the code:

- Docstrings should follow `Google Style Documentation
<http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`__.
- Do not say "**defaults to ____**" for any arguments,
unless the argument needs further explanation.
The default value is already available in the method/function definition.
- If function needs to be instantiated, explicitly show in example. See
`here <https://stackoverflow.com/questions/17134653/difference-between-class-and-instance-methods>`__
for discussion of class vs instance methods.
- Provide link to `Controlled Vocabulary <http://vocabulary.odm2.org/>`__
if an argument needs a CV as value.

Please add any additional conventions that you think should be in place
within `the github issue #106 <https://github.com/ODM2/ODM2PythonAPI/issues/106>`__.

Pull requests
-------------

Once changes has been in place within your forked copy of the repository
you are working on, please create a pull request to add your contribution
to the **master** branch of the repository.
