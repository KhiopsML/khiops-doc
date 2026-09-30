# Redirecting Khiops Output to Standard Streams

When Khiops runs in batch mode, its command trace, log messages, and progression messages can be written to standard output or standard error instead of separate files. This is useful when Khiops is launched from a script, a container, or another application that collects process output.

The `-e`, `-t`, and `-o` options accept an output path:

- `-e` writes log messages;
- `-t` writes progression messages;
- `-o` writes the commands recorded while the scenario is replayed.

## Unix-like systems

Use `/dev/stdout` to send an output stream to standard output:

```bash
khiops -b -i scenario.prm -e /dev/stdout -t /dev/stdout -o /dev/stdout
```

This command replays `scenario.prm` in batch mode and sends all three output streams to standard output. The output contains entries from the command, log, and progression streams, for example:

```text
Khiops.command	// 2026-07-03 16:56:26
Khiops.command	// khiops
Khiops.command	// -> Khiops
Khiops.command	ClassManagement.OpenFile       // Open...
Khiops.log	Train supervised model for classification of target variable class
Khiops.progression	2026-07-03 16:56:27	progression_start
Khiops.progression	2026-07-03 16:56:27	Completed task	1	Database basic stats	Initialization
Khiops.progression	2026-07-03 16:56:27	progression_stop
```

When the output is redirected to a standard stream, Khiops prefixes each line with the stream that produced it:

- `Khiops.command` identifies the command trace redirected with `-o`;
- `Khiops.log` identifies the log messages redirected with `-e`;
- `Khiops.progression` identifies the progression messages redirected with `-t`.

To send the output to standard error instead, use `/dev/stderr`:

```bash
khiops -b -i scenario.prm -e /dev/stderr -t /dev/stderr -o /dev/stderr
```

Each option can also be directed to a different stream. For example, the following command keeps logs on standard error while leaving the command trace and progression messages on standard output:

```bash
khiops -b -i scenario.prm \
	-e /dev/stderr \
	-t /dev/stdout \
	-o /dev/stdout
```

## Windows

On Windows, use the `CON` device to send the output to the console:

```bat
khiops -b -i scenario.prm -e CON -t CON -o CON
```