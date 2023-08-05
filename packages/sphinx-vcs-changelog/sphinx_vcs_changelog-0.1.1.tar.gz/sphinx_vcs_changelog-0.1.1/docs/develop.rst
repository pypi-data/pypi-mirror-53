Developing
===============================================================================

As we developing changelog parser for git we follow some rules
for commit messages:

- Each commit SHOULD prefixed with commit functional group identification
- Functional groups are:
   - fun: Functions or new possibilities
   - ref: Refactoring, i.e.  code changes brings nothing into function,
     like formatting or adding docstrings
   - fix: Fixing changes fixing error cases or possible errors
   - doc: Documentation only
   - Merge: git default merge requests
