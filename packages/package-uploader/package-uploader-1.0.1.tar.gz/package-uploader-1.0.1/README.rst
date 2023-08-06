#########################
 Python Package Uploader
#########################

.. warning::
  **This is NOT a replacement for Twine!**
  This package is not created to compete with twine and it is not suitable for uploading to pypi.org or repositories
  with compatible upload API.

This package is created to create similar (or better) experience when uploading your project to any repository, website,
artifact storage or any other place where you want to keep your built packages. It does **NOT** currently support PyPI
upload API, so if your repository supports it, use twine instead.

Supported uploaders
===================

Currently only SSH/SFTP uploader is supported that will upload your packages in directory structure compatible with
Python Package Index simple layout. This means that you can just point your HTTP server to main directory of your
package repository and it will work just fine.
