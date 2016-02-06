# repodoctor
Check your repository health

This project started out as a little hack during the Mozilla Science Lab WOW 2016.
Use this webapp to scan your repository and find out how contributor friendly it is.


###List of checks
- Existence of README.md
- Existence of LICENSE
- Existence of CONTRIBUTING.md
- Existence of .travis.yml
- Existence of .gitignore
- Existence of test cases
- Code of Conduct
- Length of README.md
- Travis CI build status
- GitHub milestones

The application works with the repository url. The Python scripts runs above
checks to rate your project on the basis of collaborative friendliness of the
project. We also have an API which we plan to use for creating GitHub badges
with Shields.

Please see CONTRIBUTING.md if you are interested in getting involved.
