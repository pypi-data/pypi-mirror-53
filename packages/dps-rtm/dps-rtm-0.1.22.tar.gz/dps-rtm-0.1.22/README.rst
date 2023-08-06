=========================================
Requirements Trace Matrix (RTM) Validator
=========================================

Validate a Function & Design Requirements document.

Free software: MIT license


J&J Quick Start
---------------
1. **Install Python**
    a. Navigate to J&J App Store. You may need to use Internet Explorer. Users have had difficulty with Chrome.
    #. Search ``Python``. You should see something similar to ``Python 3.6``. Add it to cart and install.
    #. No restart is required.
#. **Run Command Prompt with Elevated Privileges**
    a. Do not call IRIS.
    #. Hit the ``Windows Key`` and type ``cmd`` to search for the Windows command prompt
    #. Right-click ``cmd`` and select ``open file location``. This opens File Explorer.
    #. Right-click on the ``cmd`` icon and select ``Run with elevated privileges``.
#. **Install** ``dps-rtm``
    a. In Command Prompt, type ``pip install dps-rtm``
    #. If this throws an error, try instead: ``python -m pip install dps-rtm``. Hint: the up-arrow accesses previous commands to reduce the amount of typing you need to do.
    #. Note: You might see a note about ``pip`` being out of date. This is ok, but feel free to update it as suggested.
#. **Run** ``rtm``
    a. In Command Prompt, type ``rtm``

Validation Rules
-----------------
General Notes
'''''''''''''
- The FDR sheet must have the title 'Procedure Based Requirements'
- If multiples headers share the same name, only the first will be used.
- All columns get checked for 1) Exist and 2) Correct left-to-right order.

ID
''
- **UNIQUE**: Each ID must be unique
- **ALPHABETICAL SORT**: The entire column must be in alphabetical order.
- **PROCEDURE STEP FORMAT**: Procedure Step IDs must be formatted `PXYZ` e.g. `P010`
- **START WITH ROOT ID**: All other IDs must start with the ID of its root Procedure Step. Example: if a Procedure Step has an ID of "P010", then the following VOC USER NEED could have an ID of "P010-0010".

Cascade Block
'''''''''''''
The Cascade Block is a group of columns: Procedure Step, Need, Design Input, Solution Level 1, ..., Solution Level n.

- **NOT EMPTY**: Error if Cascade Block row is entirely empty.
- **SINGLE ENTRY**: Warning if more than one cell in Cascade Block row has an entry. Only the first is considered.
- **USE ALL COLUMNS**: Warning if any Cascade Block columns are completely blank.
- **ORPHAN WORK ITEMS**: Each work item must trace back to a procedure step.
- **SOLUTION LEVEL TERMINAL**: Each requirements trace terminates at the Solution Level.
- **F ENTRY**: Terminal work items are marked with 'F' in the Cascade Block.
- **X ENTRY**: All other work items are marked with 'X'.


Cascade Level
'''''''''''''
- **NOT EMPTY**
- **VALID INPUT**: Procedure Step, VOC User Need, Business Need, Risk Need, Design Input, or Solution Level
- **CASCADE BLOCK MATCH**: matches selection in Cascade Block

Requirement Statement
'''''''''''''''''''''
RTM Validator recognizes text string as tags if they meet these criteria:

- Text string starts with `#` (pound sign)
- Text string begins on a new line.

Some tags (e.g. #ParentOf, #ChildOf) take modifiers. RTM Validator recognizes text strings as modifiers if they meet these criteria:

- Text string is separated from tag by white space (one or more spaces).
- Occurs on same line as tag
- modifiers cannot contain white space.

Examples:

- `#ParentOf P010-020` - tag: `ParentOf`; modifier: `P010-020`.
- `#ChildOf P 020-054` - tag: `ChildOf`; modifier: `P`. Note that the `020-054` is ignored.
- `#ParentOf` - tag: `ParentOf`; modifier: (None).

Available Base Tags:

- ParentOf
- ChildOf
- Function
- MatingParts
- MechProperties
- UserInterface

Checks

- **NOT EMPTY**
- **MISSING TAGS**: Use each base tag at least once in the document
- **CUSTOM TAG**: Custom tags are allowed, but produce a warning.
- **PARENT/CHILD MODIFIERS** ParentOf and ChildOf modifiers must match a value in the ID column.
- **MUTUAL PARENT/CHILD**: Each ChildOf work item must point to a work item that is itself a ParentOf the first work item.

Requirement Rationale
'''''''''''''''''''''
- **NOT EMPTY**

VorV Strategy
'''''''''''''
- **NOT EMPTY**
- **BUSINESS NEED N/A**: Business Need work items are marked with 'N/A'.

VorV Results
''''''''''''
- **NOT EMPTY**
- **BUSINESS NEED N/A**: Business Need work items are marked with 'N/A'.

Devices
'''''''
- **NOT EMPTY**

DO Features
'''''''''''
- **NOT EMPTY**
- **CTQ FORMAT**: if contains features that are CTQs, CTQ ID should be formatted as "(CTQ##)"
- **MISSING CTQ**: if CTQ Y/N yes, check for CTQ IDs in DO Features column

CTQ Y/N
'''''''
- **NOT EMPTY**
- **VALID INPUT**: "yes", "no", "N/A", or " - " (only procedure step can have " - ")
- **CTQ -> YES**: If DO Feature has a ctq, then this cell needs a yes

Potential Future Features
-------------------------
- Report on Windchill documents (WC#s, where used)

Developer Notes
---------------
How It Works
''''''''''''''
The Requirements Trace Matrix (RTM) documents the requirements cascade for an New Product Development (NPD) project.
Broad core requirements flow into multiple subrequirements, which themselves spawn yet more subrequirements, and so on.
Each (sub)requirement can have multiple parents, though most have only one.
Each of these (sub)requirements is called a **work item**.

Expressed in terms of `Graph Theory <https://en.wikipedia.org/wiki/Graph_theory>`_,
the RTM is a collection of one or more directed, acyclic graphs.
Each graph node is represented as a single row in the RTM Excel worksheet.
Each node has multiple fields, represented by worksheet columns.
The graph edges are represented by the worksheet's Cascade Block. To find a node's primary parent,
find the last '**X**' in the previous column of the Cascade Block.
All other parents are called out with tags in the **Requirements Statement** field.

The RTM Validator works by first reading all rows of each field into an object.
Then each work item (node) is read into its own object.
Finally, validation functions are called, field by field.
The output (pass/warning/fail) is displayed on the console.


Release History
---------------

v 0.1.1
''''''''''
* Initial PyPI upload

v 0.1.2
''''''''''
* added README

v 0.1.3|4|5
''''''''''''
* implement tkinter

v 0.1.6
''''''''''
* implement click cli

...

v 0.1.16
''''''''''''
* add Cascade Block validation

v 0.1.17
''''''''''''
* add Cascade Level & Requirement Statement validation

v 0.1.22
''''''''''''
* add excel markup