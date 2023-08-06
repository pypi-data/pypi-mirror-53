Feature: `rxdata.field(invokes=[...])` applies pipelines on init and/or attribute set
    `rxdata.field` results will apply pipeline from attribute `invoke`
    Rule: `field(invokes=[...])` pipeline executed upon init and on field `setattr`
      @rxdataobject.invokes.init.defaults
      Scenario Outline: `@rxdata.dataclass` object `invokes` pipelines on default values
      Given sample from `<source>:<dataclass>`
      Then `invokes:init:default` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/invocation.py | unfrozen.plain     |
       | sample/class/invocation.py | unfrozen.inherited |
       | sample/class/invocation.py | unfrozen.composed  |
       | sample/class/invocation.py | frozen.plain       |
       | sample/class/invocation.py | frozen.inherited   |
       | sample/class/invocation.py | frozen.composed    |

      @rxdataobject.invokes.init.defaults
      Scenario Outline: `@rxdata.dataclass` object invokes `rxdata.operators.typeguard` on default values with `data(invokes=rxdata.operators.typeguard(...))`
      Given sample from `<source>:<dataclass>`
      Then `typeguard:init:default` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/invocation.py | unfrozen.plain     |
       | sample/class/invocation.py | unfrozen.inherited |
       | sample/class/invocation.py | unfrozen.composed  |
       | sample/class/invocation.py | frozen.plain       |
       | sample/class/invocation.py | frozen.inherited   |
       | sample/class/invocation.py | frozen.composed    |


      @rxdataobject.invokes.init.kwargs
      Scenario Outline: `@rxdata.dataclass` object `invokes` on init args
      Given sample from `<source>:<dataclass>`
      Then `invokes:init:kwargs` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/invocation.py | unfrozen.plain     |
       | sample/class/invocation.py | unfrozen.inherited |
       | sample/class/invocation.py | unfrozen.composed  |
       | sample/class/invocation.py | frozen.plain       |
       | sample/class/invocation.py | frozen.inherited   |
       | sample/class/invocation.py | frozen.composed    |

      @rxdataobject.invokes.init.kwargs
      Scenario Outline: `@rxdata.dataclass` object invokes `rxdata.operators.typeguard` on init args with `data(invokes=rxdata.operators.typeguard(...))`
      Given sample from `<source>:<dataclass>`
      Then `typeguard:init:kwargs` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/invocation.py | unfrozen.plain     |
       | sample/class/invocation.py | unfrozen.inherited |
       | sample/class/invocation.py | unfrozen.composed  |
       | sample/class/invocation.py | frozen.plain       |
       | sample/class/invocation.py | frozen.inherited   |
       | sample/class/invocation.py | frozen.composed    |


      @rxdataobject.invokes.setattr
      Scenario Outline: `@rxdata.dataclass` object `invokes` pipelines on setattr
      Given sample from `<source>:<dataclass>`
      Then `invokes:setattr` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/invocation.py | unfrozen.plain     |
       | sample/class/invocation.py | unfrozen.inherited |
       | sample/class/invocation.py | unfrozen.composed  |
       | sample/class/invocation.py | frozen.plain       |
       | sample/class/invocation.py | frozen.inherited   |
       | sample/class/invocation.py | frozen.composed    |


      @rxdataobject.invokes.setattr
      Scenario Outline: `@rxdata.dataclass` object invokes `rxdata.operators.typeguard` on setattr with `data(invokes=rxdata.operators.typeguard(...))`
      Given sample from `<source>:<dataclass>`
      Then `typeguard:setattr` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/invocation.py | unfrozen.plain     |
       | sample/class/invocation.py | unfrozen.inherited |
       | sample/class/invocation.py | unfrozen.composed  |
       | sample/class/invocation.py | frozen.plain       |
       | sample/class/invocation.py | frozen.inherited   |
       | sample/class/invocation.py | frozen.composed    |
