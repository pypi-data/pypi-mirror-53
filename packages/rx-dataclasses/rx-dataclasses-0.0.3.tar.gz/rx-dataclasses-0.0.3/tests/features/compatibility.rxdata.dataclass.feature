Feature: `rxdata.dataclass` decorator implements conventional dataclass
    `@dataclasses.dataclass` can be safely replaced by `@rxdata.dataclass`

    Rule: `@rxdata.dataclass` accepts type annotations and `dataclasses.field` in class declarations
        @class.transparency
        Scenario Outline: `@rxdata.dataclass` can create class from `@dataclasses.dataclass` declaration
            Given sample from `<source>:<dataclass>`
            Given cls created by calling imported `dataclasses:dataclass` on sample
            Given sample from `<source>:<dataclass>`
            Given cls created by calling imported `rxdata:dataclass` on sample
            Then `(instances:equal:except_magic) or (instances:equal:annotations)` is satisfied with cls

        Examples: dataclass compatible declarations
           | source                       | dataclass           |
           | sample/class/transparency.py | Dataclass.Fielded   |
           | sample/class/transparency.py | Dataclass.Annotated |
           | sample/class/transparency.py | Dataclass.Mixed     |

        @class.transparency
        Scenario Outline: : `@rxdata.dataclass` can mix type annotations, `dataclasses.field` and `rxdata.field` in class declarations
            Given sample from `<source>:<rxdataclass>`
            Given cls created by calling imported `rxdata:dataclass` on sample
            Given sample from `<source>:<equivalent>`
            Given cls created by calling imported `dataclasses:dataclass` on sample
            Then `(instances:equal:except_magic) or (instances:equal:annotations)` is satisfied with cls

        Examples: mixed field types for rxdata and their equivalent from dataclasses
           | source                       | rxdataclass                 | equivalent                          |
           | sample/class/transparency.py | MixedFieldTypes.RXDataclass | MixedFieldTypes.DataclassEquivalent |


        @decorator.transparency
        Scenario: `@dataclasses.dataclass` calling arguments is subset of `@rxdata.dataclass`
            Given imported function `rxdata:dataclass`
            Given imported function `dataclasses:dataclass`
            Then `functions:conformant` is satisfied with function

        @object.transparency
        Scenario Outline: `rxdata` objects that created from `dataclasses` declarations are exact same
            Given sample from `<source>:<dataclass>`
            Given cls created by calling imported `dataclasses:dataclass` on sample
            Given sample from `<source>:<keywords>`
            Given object created by calling cls on keywords sample

            Given sample from `<source>:<dataclass>`
            Given cls created by calling imported `rxdata:dataclass` on sample
            Given sample from `<source>:<keywords>`
            Given object created by calling cls on keywords sample

            Then `instances:equal:exact` is satisfied with object

        Examples: dataclass compatible declarations results in exact same attributes upon replace `@dataclasses.dataclass` with `@rxdata.dataclass`
           | source                       | dataclass         | keywords                   |
           | sample/class/transparency.py | Dataclass.Mixed   | Dataclass.Mixed.keywords   |
           | sample/class/transparency.py | Dataclass.Fielded | Dataclass.Fielded.keywords |
