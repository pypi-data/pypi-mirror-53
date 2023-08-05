# BUSY

Task and plan management tool, for use from the terminal prompt on Linux and MacOS systems.

## Installation

Requires Python 3.6.5 or later.

```
pip3 install busy
```

## Getting started

Add some tasks to your queue.

```
busy add "Take a shower"
busy add "Do the laundry"
busy add "Phone mom"
busy add "Donate to the Busy project"
```

Find out what to do next:

```
busy get
```

Returns:

```
Take a shower
```

When you're done, mark it off to find the next task.

```
busy finish; busy get
```

Returns:

```
Do the laundry
```

See the whole queue, with sequence numbers.

```
busy list
```

Returns:

```
1  Do the laundry
2  Phone mom
3  Donate to the Busy project
```

Decide to do the top task later.

```
busy drop; busy list
```

Returns:

```
1  Phone mom
2  Donate to the Busy project
3  Do the laundry
```

Decide to do a specific task now.

```
busy pop 2; busy get
```

Returns:

```
Donate to the Busy project
```

Push that task to tomorrow.

```
busy defer --to tomorrow
```

Add all the tasks scheduled for today to the list.

```
busy activate --today
```

### Core Commands

- `add` adds a new item to the bottom of the queue. The item description may be included after the command or written to stdin (i.e. typed on the next line).
- `get` gets the top item in the queue, referred to as the "current" item. There are no options.
- `list` lists the items in the queue in order with their sequence numbers.
- `pop` moves a task or set of items to the top of a queue.
- `drop` moves a task or set of items to the bottom of a queue.
- `delete` permanently removes a task or set of items from a queue. Deletion requires confirmation via input or the `--yes` option.
- `manage` opens a text editor to edit items.

The `list`, `pop`, `drop`, `delete` and `manage` commands allow the designation of specific items.

Item designation can be performed using sequence numbers or tags.

### Sequence Numbers

Sequence numbers appear in the output from the `list` command. Note that the numbering starts with 1, and is not an ID -- the number of a item will change when the queue is modified. So always reference the most recent output from the `list` command.

When used to designate items, a range of sequence numbers is separated by a hyphen, with no whitespace, and is inclusive. For example, `4-6` designates items 4, 5, and 6. A hyphen without a number after it includes all the items from that item to the end of the queue. A hyphen on its own indicates the last item in the queue.

Below are some examples of task designations by sequence number.

`busy pop 5` pops item number 5

`busy drop 3-7` drops items 3 through 7 (4 items)

`busy list 3-` lists all the items from number 3 through the end of the list

`busy delete 3 5 7 9` deletes only the items designated

`busy defer -` defers the last task

`busy manage -4` is an error! Use `busy manage 1-4` instead.

Items will always be handled in the order they appear in the queue, regardless of the order the criteria are provided. So for example, if a `pop` command designates some items, they will be moved to the top of the queue in the order, relative to each other, they currently appear in the queue.

The sequence numbers in the `list` command output are from the queue itself. So the `list` command does not modify the sequence numbers, even when item designation is applied.


### Tags

Items can have tags, which are space-separated hashtags in the item description. An item can have no tags, one tag, or more than one tag. For example the following item description has the tag "errands":

```
go to the supermarket #errands
```

Hash tags may be used for item designation, in which case the hash itself ("#") is omitted from the command line. For example, the following command will move all the items with the `#errands` hash to the top of the queue.

```
busy pop errands
```

Whitespace-separated item designation criteria are additive -- that is, a logical OR. For example, the following command will delete all the admin tasks, sales tasks, and tasks 3 and 4.

```
busy delete admin sales 3 4
```

Commands that accept item designations support logical defaults, which are:

| **Command** | **Default item(s)** |
| ---         | ---              |
| `list`      | All items        |
| `pop`       | Last item        |
| `drop`      | First item       |
| `delete`    | First item       |
| `manage`    | All items        |

### Alternate Queues

Busy will manage any number of queues, which are entirely separate ordered sets of items. For example, you might have a `shopping` queue for items to buy at the store, and a `movies` queue for films you'd like to watch. The default queue is called `tasks` and has special properties related to planning.

To designate an alternate queue, use the `--queue` option on the command.

```
busy add "Skimmed Milk" --queue shopping
busy get --queue movies
```

### Managing Plans with the `defer` and `activate` commands

The default `tasks` queue supports several specific commands related to planning -- that is, scheduling tasks for the future. Planned tasks are kept in another special queue called `plans`.

There are two commands related to plan management.

- `defer` removes a task or set of tasks from the `tasks` queue and schedules it or them to reappear at a future date in the `plans` queue.
- `activate`removes a task or set of tasks from the `plans` queue and replaces it or them into the `tasks` queue.

The `defer` and `activate` commands accept item designations. The `defer` command deals with the `tasks` queue; its default is the top item in the `tasks` queue. The `activate` command deals with the `plans` queue; its default is all the items scheduled for the current date or earlier.

Planning is by date, not time, and is relative to the current date according to the system clock.

In the `defer` command, the date can be specified using the `--to` or `--for` option (they are interchangable). If the options are omitted, then the date can be provided as input.

The date may take any of the following forms:

- A specific date in `YYYY-MM-DD` format, such as `2018-10-28`. Slashes are also acceptable, but the order is always year, then month, then day
- A specific date without the year in `MM-DD` format, such as `7-4`, which will defer the item to that date in the future (even if it's in the next year)
- A specific day of the month as a simple integer, such as `12`, which will defer the item to that day of the month, in either the current month or the next month
- An integer, a space, and the word `day` or `days`, such as `4 days`, which will defer the item to that number of days from today
- An integer without a space and the letter `d`, such as `4d`, which is a short form of `4 days`
- The word `tomorrow`, which is also the default if no date is provided
- The word `today`, which is a little odd but obvious

As an example, the following command will defer tasks 4, 5, and 6 from the `tasks` queue to the date 4 days from today, keeping them in the `plans` queue until that date.

```
busy defer 4-6 --for 4 days
```

Note that the `plans` queue is keeping the task information (verbatim from the `tasks` queue) along with the date information (as an absolute date).

To pull tasks off the `plans` queue and put them back on the `tasks` queue, use the `activate` command. There are two ways to use the `activate` command:

- With the `--today` option, which is the normal way, and activates all the tasks scheduled for today or earlier, bringing the `tasks` list up to date
- With designated items from the `plans` queue; note that the `activate` command accepts item designation from the `plans` queue itself

If no items are designated, and there is no `--today` option, no tasks will be activated.


## Followons and the `finish` command

Like `defer`, the `finish` command only works on the `tasks` queue. It removes the designated Task (or the top task if none is designated) from the queue and adds it to the `done` queue, with today's date to indicate when it was completed.

Optionally, a Task can have a Followon, which is another task to be added to the queue after the first task is finished. Followons are describe in a Task using an arrow notation. In the following example, the Task "eat" has a followon task "drink".

```
eat --> drink
```

Note that the hyphens and whitespace are optional; really the marker that matters for delimiting a followon is the right angle bracket (">"). Also note that right angle bracket is not a valid character in a task description.

When the `finish` command is executed on the task above, the "eat" task will be recorded as "done" and the "drink" task will be added to the bottom of the `tasks` queue.

Note that followons can be chained. For example, when the `finish` command is run on the task illustrated below, a new task "drink > be merry" will be added to the queue. Only when that Task is finished will the "be merry" task itself appear on the queue.

```
eat > drink > be merry
```

### Repeating tasks

A special type of Followon is the Repeat. In this case, instead of adding the next task to the bottom of the queue, the entire current task -- including the Followon itself -- is entered into the `plans` queue at some point in the future. Repeats allow for easy management of repeating tasks. Some examples follow.

`check email --> repeat in 1 day`

`phone mom --> repeat on sunday`

`balance the checkbook --> repeat on 6`

The exact syntax for a Repeat is the word "repeat" followed by either "on" or "in" and a relative date phrase -- the same phrases that work with the `defer` command.

Note that the repetition itself only happens on the `finish` command. The completed task (i.e. "check email") is entered in the `done` queue and then the entire task (with the Repeat) is scheduled in the `plans` queue for the appropriate time in the future.

### Projects and the `start` command

Another special feature of the `tasks` and `plans` queues is the `start` command, which deals with projects.

If a task has tags, the first tag is considered to be its "project" for the purposes of the `start` command.

The `start` command is used to start work on a project. If an argument is passed to the command, that's the chosen project. Otherwise the chosen project is the project of the current task (the top item in the `tasks` queue). The command basically combines steps:

- Calls `activate --today` so the active task list is up-to-date
- Calls `manage` on the project, to edit the list of tasks for the project
- Calls `pop` on the project, so its tasks are at the top of the list

### Details of the `manage` command

The `manage` command launches the user's default text editor to directly edit a queue or part of a queue.

The definition of the "default text editor" depends on the OS and configuration but here's the logic:

1. Try the EDITOR environment variable
1. If that doesn't exist, try the `sensible-editor` command (Ubuntu)
1. If that doesn't exist, try the `open -W` command (OSX)

The default use of `manage` will edit the entire queue.

```
busy manage --queue movies
```

But it's also possible to designate tasks to be managed. The `manage` command does its best to replace the edited items in place in the list order. So if you `manage` the current project (in which all the tasks are at the top), then the edited tasks will still appear at the top. Even if you add tasks, they will be inserted after the last task in the managed set, not at the end of the list. But all the tasks brought up in the editor will be managed. So if you remove a task in the editor, it will be deleted and the others will be moved up to take its place.

### Data storage

Busy keeps the queues in plain text files, so if the tool doesn't do something you want, you may edit the files. The files are in a directory together, referred to as the "root". Each file is the name of the queue with a `.txt` extension. If a required file is missing, it will be created automatically. So typically, the root includes `tasks.txt`, `plans.txt`, and any number of custom queue files.

Technically, they are pipe-delimited data files, though `tasks.txt` only has one field (description); `plans.txt` has only two fields (date and description), and there is no support for managing separate fields in the Busy tool itself.

The root is designated in one of the following ways, which are tried in order.

- The `--root` option on the command
- The `BUSY_ROOT` environment variable, if no `--root` option is provided
- A directory at `~/.busy`, which will be generated as needed if no `--root` option or `BUSY_ROOT` environment variable are provided,

Note that the `--root` option must come after `busy` but command-specific options (`--yes`, `--to`, `--for`, `--queue`, and `--today`) must come after commands.

The following example shows the `--root` option with command-specific options on the same command line.

```
busy --root ~/.config/busy activate --today
```

Note that Busy does not support concurrency in any form. If two commands are executing at the same time, they may overwrite each other. Overwriting is especially risky with the `manage` command, which keeps the user's editor open until they close it.

The format is designed to be simple (i.e. non-default queues are really just lists of items) but not idiot-proof. Experimentation might result in unintended consequences.

## Usage with Slack and Dropbox

We are developing a Slack slash command to access Busy which requires Dropbox integration. This is a work in progress. At the moment, you have to configure the slash command yourself, and it only works when your root is in Dropbox. Also the only command that's working at this moment is the `get` command to get the current task.

### Using Busy in Slack

Once it's all configured right, it's easy to use! Just type:

```
/busy
```

... and Busy will tell you what to work on.

### Configuring Busy for use in Slack

The steps below assume you're already using Busy locally

1. Install Dropbox (if you don't already have it), and move your Busy root to ~/Dropbox/Apps/Busy
1. Create an AWS account (if you don't already have it) and sign into the AWS console
1. Install the AWS CLI (if you don't already have it)
1. Create an AWS profile called `lambda-deploy` with the ability to deploy to Lambda
1. Create a Lambda function called `busy`
1. Add an environment variable to the Lambda function called `DROPBOX_TOKEN` with your Dropbox token (comes from the Dropbox web UI)
1. Create a Slack workspace (if you don't already have one) and create a Slack app called `busy` with a slash command
1. Add an environment variable to the Lambda called `SLACK_TOKEN` and enter the token from your slash command
1. Set the Lambda function to run `lambda.lambda_handler`
1. Create an API Gateway trigger for the Lambda function with "Open" access, and copy the full URL into the Slack slash command
1. Clone the project from GitLab (if you haven't already) and run `make publish-lambda` from the root of the project

## Development

Although it requires Python 3.6.5 or higher, Busy is designed to function with the Python standard library without any additional pip modules.

However, we use Pip packages in the devops pipeline, so:

```
sudo pip3 install coverage pycodestyle twine
```

Then to run the test suite:

```
make test
```

Or to run test coverage:

```
make cover
```

And to check style:

```
make style
```
