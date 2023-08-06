# refit

A prototype for a simpler and faster alternative to ansible.

## Parallelism

The requirements are as follows:

### Provisioning multiple machines

If you have two application servers, they can be provisioned at the same time.

This is the main win with async.

### Simultaneous tasks

For a single machine, there are tasks which have no dependencies on each other, so can be run concurrently.

I don't know how easy it is to do this effectively.

Would you need multiple ssh connections?

Or have a Python agent on the server, which does the async?

Even then async for those kinds of tasks ... tricky.

I think the agent runs asyncio, but you just run the tasks as subprocesses.

https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.asyncio.subprocess.Process

You can await it like any coroutine.

OK ... so I'll keep to a single worker on the master. And a single agent on the server, using subprocesses.

Now I need a way to tell the agent what to do. Can serialise it, or generate Python code. Just generate the Python code.

With templates ... always kick these coroutines off at the start ... since
uploading seems to be the biggest bottleneck.

I need a good way of expressing async behaviour ... both inside a machine, and across machines. For example ... can be provisioning a database server and an application server. There's only a single sync point - when the app starts, the database has to be ready.

## Issues with ansible

I think one other issue with Ansible is the lack of a GUI ...

Makes it seriously hard to know what's going on. If there was a better visualisation, with icons and stuff (for example, an icon for a template). Maybe with a simple GUI built in.
