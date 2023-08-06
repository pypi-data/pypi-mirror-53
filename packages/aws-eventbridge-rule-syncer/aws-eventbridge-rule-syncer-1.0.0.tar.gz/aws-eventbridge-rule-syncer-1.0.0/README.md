# AWS Event Bridge Rules helper
This module provides rules syncer and local rules evaluator for AWS Event 
Bridge.

## Rules Syncer
Rules syncer syncs rules from a local file to Remote AWS Event Bridge. The 
rules can be configured in a file like this:
```
[
  {
    "pattern": {
      "detail": "something"
    },
    "target": "target",
    "name": "rule",
    "description": "test rule",
    "state": "ENABLED"
  }
]
```

* Pattern: This is the pattern against which the incoming events will be 
matched against.
* Target: Name of the SQS Queue. This will be the target.
* name: Name of the rule.
* Description: Rule description.
* state: State of the rule. It can either be ENABLED or DISABLED.

All the rules and targets names are prepended with a prefix.

Before syncing the rules, the existing rules are backed up to a file.

## Local rules evaluator
Local rules evaluator evaluates an incoming event against a set of rules. 
Pattern matching uses the same pattern matching concepts as used in a remote 
AWS Event Bridge.

For more information, check this https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html