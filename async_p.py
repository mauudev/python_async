# Iterators
# pueden escribirse como clase tabmien mediante herencia
from asyncio import Future
from asyncio import events
import threading
import types
import asyncio
import random
list = [1, 2]
iterator = iter(list)
# print(next(iterator))
# print(iterator.__next__())
# print(next(iterator))

# Generators
# simple generator


def magic_pot(start=1, end=1000):
    limit = 0
    while limit <= 50000:
        limit += 1
        yield f"Number: {random.randint(start, end)} limit: {limit}"


gen = magic_pot()
for a in gen:
    ...
    # print(a)


# Example — generator with send() and yield expression

# def print_me_and_return(value):
#     yield f"Value: {value}", value, type(value)

# def magic_pot(param="initial"):
#     while True:
#         param = (yield print_me_and_return(param))
#         print("param: %s" % param)
#         if param == "stop":
#             yield "magic pot stopped"
#             break


# gen = magic_pot("my value 1")

# print(gen)
# # print(gen.send(None))
# print(next(gen))
# print(gen.send("otro value"))
# print(next(gen))


def magic_pot(start=1, end=1000):
    while True:
        stop = (yield random.randint(start, end))
        print("stop %s" % stop)
        if stop is True:
            yield "magic pot stopped"
            break


gen = magic_pot()

# print(gen)
# print(gen.send(None))  # same as next(gen)
# print("second")
# print(next(gen))
# print(gen.send(True))  # input value for generator

# try:
#     print(next(gen))
# except StopIteration:
#     print('iteration stopped')


# Unix pipelines to read files
def read_file(file_name):
    for row in open(file_name, "r"):
        yield row


def read_csv_row(file_name):
    for row in read_file(file_name):
        yield row.split(',')


def read_csv(file_name):
    for items in read_csv_row(file_name):
        print("Row: " + str(items))


# read_csv('test.csv')


# same but with `yield from`
def read_file(file_name):
    for row in open(file_name, "r"):
        yield row

# Or


def read_file(file_name):
    yield from open(file_name, "r")


# Coroutines
# Asyncio generator coroutines


@asyncio.coroutine
def compute_coroutine(x):
    yield from asyncio.sleep(random.random())  # yield from native coroutine
    print(x * 2)

# asyncio.run(compute_coroutine(2))# Output

# asyncio.run() ->
#  - starts compute_coroutine() coroutine
#  - suspends compute_coroutine() and start asyncio.sleep()
#  - resumes compute_coroutine()
#  - coroutines are suspended/executed with the help of asyncio event loop
# --------------------------------------------------------------------


@asyncio.coroutine
def coroutine_generator(x):
    for i in range(0, x):
        yield i
    print("input=%s" % x)


# asyncio.run(coroutine_generator(2))# Output - yield inside coroutine cannot be used with asyncio
# RuntimeError: Task got bad yield: 0

# Native coroutines

# estos ya estan deprecados desde la 3.8 y pide usar async def

@asyncio.coroutine
def async_gen_data():
    yield 10


@types.coroutine
def types_gen_data():
    yield 10


async def async_native_coroutine():
    print('async_native_coroutine')
    yield 100


async def async_native_coroutine_generator():
    print('async_native_coroutine_generator')
    yield 100


# print(async_gen_data())
# print(types_gen_data())
# print(async_native_coroutine())
# print(async_native_coroutine_generator())


# example1: async native coroutineimport asyncio


async def f1():
    print('before')
    await asyncio.sleep(1)
    print('after 1 sec')

# asyncio.run(f1()) # runs in a event loop and execute# Output

# <coroutine object f1 at 0x101d852c8>
# after 1 sec---------------------------------print(f1())# Output
# RuntimeWarning: coroutine 'f1' was never (coroutine needs to be awaited)---------------------------------
# await f1()      # Output
# SyntaxError: 'await' outside function (should be used inside async function/native coroutine)


# Concurrent Coroutines (async/await, @asyncio.coroutine/yield from):


@asyncio.coroutine
def compute(tid, x, sleep):
    print("%s: input=%s with sleep=%s" % (tid, x, sleep))
    yield from asyncio.sleep(sleep)  # async future
    return x * 2


@asyncio.coroutine
def print_sum(tid, x, sleep):
    result = yield from compute(tid, x, sleep)  # return a value
    print("%s: result=%s" % (tid, result))


async def task(tid, x, sleep):
    return await print_sum(tid, x, sleep)  # await a coroutine


async def main():
    await asyncio.gather(
        task("t1", 2, random.randint(0, 5)),
        print_sum("t2", 3, random.randint(0, 5)),
        task("t3", 4, random.randint(0, 5)),
    )

# asyncio.run(main())# Output - execute 3 tasks concurrently

# t1: input=2 with sleep=0.7909687238238471
# t2: input=3 with sleep=0.25100171976591423
# t3: input=4 with sleep=0.4164068460815761
# t2: result=6
# t3: result=8
# t1: result=4
# await asyncio.gather() - Run alls coroutines concurrently inside the event loop and gathers all the results to be returned by main()


# Event loop
# event loop with multiple coroutines calls


async def f1():
    print('tid:%s - before' % threading.get_ident())
    await asyncio.sleep(1)
    print('tid:%s - after 1 sec' % threading.get_ident())


def run(fn):
    loop = events.new_event_loop()
    loop.run_until_complete(fn)
    loop.close()


# print('tid:%s - start' % threading.get_ident())
# # creates 2 new event loop for each run()
# run(f1())
# run(f1())# Output

# tid:4638019008 - start
# tid:4638019008 - before
# tid:4638019008 - after 1 sec
# tid:4638019008 - before
# tid:4638019008 - after 1 sec
# Event loop uses only unix thread(tid is the same in all outputs) to schedule tasks for each run()
# which created new_event_loop() every-time.


# Futures
# A Future is a special low-level awaitable object that represents an eventual result of an asynchronous operation.
# Future object is awaited it means that the coroutine will wait until the Future is resolved in some other place


async def num_calc(name, number):
    f = 1
    for i in range(2, number + 1):
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: multiplier({number}) = {f}")
    return f


async def main():
    # schedule calls concurrently & gathers all async future results
    results = await asyncio.gather(num_calc("A", 2), num_calc("B", 3), num_calc("C", 4))
    print(results)

# asyncio.run(main())# Output
# Task A: multiplier(2) = 2
# Task B: multiplier(3) = 6
# Task C: multiplier(4) = 24
# [2, 6, 24]# Results [2, 6, 24] are printed based on await on the futures

# Coordination between Futures


async def child_future(future):
    print("child sleep")
    await asyncio.sleep(1)
    print("child woke")
    future.done()
    future.set_result("future is resolved")
    return "child complete"


async def parent(future):
    print("parent wait for child")
    print(await future)
    return "parent complete"


async def main():
    future = Future()
    print(await asyncio.gather(parent(future), child_future(future)))


# asyncio.run(main())  # Output : parent waits for child to complete the task
# parent wait for child
# child sleep
# child woke
# future is resolved
# ['parent complete', 'child complete']


# Tasks

# Tasks is a subclass of Future. 
# Tasks are used to schedule coroutines concurrently in event loop. Coroutine is wrapped into a Task with functions like asyncio.create_task() 
# the coroutine is automatically scheduled to run soon. Task has add_done_callback() to handle further code cleanup/done logic.
import asyncio


async def nested():
    return 42


def result_callback(future):
    print("Callback: %s" % future.result())


async def main():
    # Schedule nested() to run soon concurrently with "main()".
    task = asyncio.create_task(nested())
    task.add_done_callback(result_callback)

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task


# asyncio.run(main())# Output
# Callback: 42
# Prints callback result after the task is complete.


# Asynchronous Generators:
# ‘yield’ inside a native coroutine returns a asynchronous generator

# Rationale: (from PEP 255)Regular generators enabled an elegant way of writing complex data producers and have them behave like an iterator. 
# However, currently there is no equivalent concept for the asynchronous iteration protocol (async for). 
# This makes writing asynchronous data producers unnecessarily complex, 
# as one must define a class that implements __aiter__ and __anext__ to be able to use it in an async for statement.
async def smth():
    ...

def func():            # a function
    return

def genfunc():         # a generator function
    yield

async def coro():      # a coroutine function
    await smth()

async def read(db):    # a coroutine function without await
    pass

async def asyncgen():  # an async generator coroutine function
    await smth()
    yield 42
    
# The result of calling an asynchronous generator function is an asynchronous generator object, 
# which implements the asynchronous iteration protocol defined in PEP 492.


# Asynchronous Iteration Protocol
# An __aiter__ method returning an asynchronous iterator.
# An __anext__ method returning an awaitable object, which uses StopIteration exception to “yield” values, and StopAsyncIteration exception to signal 
# the end of the iteration.
# esto es util para sacar data en chunks
async def async_generator():
    for i in range(2):
        await asyncio.sleep(1)
        yield i * i


async def main():
    gen = async_generator()
    print(gen)
    print(await gen.__anext__()) # await for the 'yield'
    print(await gen.__anext__())
    await gen.aclose()           # close the generator for clean-up

# asyncio.run(main())

# Output
# 0
# 1
# 'yield' has to be awaited until exhausted to close the async generator in a clean way. Otherwise, it can cause task 'shutdown' exceptions.


# Async for
# Simplifies the iteration of asynchronous generator (yield).

# combination of using async generator and coroutine

async def main():
    async for i in async_generator():
        print(i)

loop = asyncio.get_event_loop()
asyncio.ensure_future(main())
asyncio.ensure_future(main())
# loop.run_forever()

# Output
# 0
# 0
# 1
# 1


# Simple HTTP API Crawler Example
# Simple example to crawl http urls in parallel
import aiohttp
import asyncio
import time


async def get_req(page_no):
    print("called at time1: " + str(time.time()))
    async with aiohttp.ClientSession() as session:
        async with session.get("http://reqres.in/api/users?page=" + str(page_no), headers={}) as resp:
            print("called at time2: " + str(time.time()))
            return await resp.json()


async def fetch_all_urls():
    results = await asyncio.gather(*[get_req(page_no) for page_no in range(1, 5)], return_exceptions=True)
    # results = [await get_req(page_no) for page_no in range(1, 5)]
    for result in results:
        print('page: %s, size: %s' % (result['page'], len(result['data'])))
    return results


def get_htmls():
    loop = asyncio.get_event_loop()
    htmls = loop.run_until_complete(fetch_all_urls())
    return htmls


start = time.time()
print("start time: " + str(start))
get_htmls()
print("time taken: " + str(time.time() - start))

# Uncomment the bold line (replace "await asyncio.gather" line with the next commented line and check the results). 
# Request are completed done sequentially and takes 2 seconds to complete. 
# In this case, await iterated sequentially can lose all concurrency and thats how started this journey of understanding the asyncio.


# Summary
# - ‘yield’ keyword create regular generators. ‘yield from’ is a shortcut to iterate and exhaust the generator
# - generator.send() helps to send values to a coroutine. ‘(yield)’ is bi-directional for iteration between coroutines.
# - Event loops use cooperative scheduling. Concurrent tasks are scheduled in an Event Loop managed by a Thread.
# - @asyncio.coroutine creates asyncio generator coroutine objects and uses ‘yield from’ to work on native/generator coroutines. 
# - yield from statement gives up control back to the event loop to let other coroutine execute.
# - @types.coroutine is similar to @asyncio.coroutine which helps to convert regular generators to coroutine objects and interoperable between native coroutines.
# - asyncio is a library to write concurrent code using the async/await syntax.
# - coroutines declared with async/await syntax is the preferred way of writing asyncio applications.
# - async/await is latest equivalent of @asyncio.coroutine/‘yield from’
# - native/generator coroutine, future, tasks are awaitable’s
# - Future is a special low-level awaitable object that represents an eventual result of an asynchronous operation.
# - Tasks is a subclass of Future. Tasks are used to schedule coroutines concurrently in event loop for execution.
# - ‘async for’ is used to iterate over asynchronous generator
# - ‘async with’ is used to do async operations with cleanup(garbage collected)
