.. _rebot:

Post-processing outputs
=======================

`XML output files`_ that are generated during the test execution can be
post-processed afterwards by the ``rebot`` tool, which is an integral
part of Robot Framework. It is used automatically when test
reports and logs are generated during the test execution, and using it
separately allows creating custom reports and logs as well as combining
and merging results.

.. contents::
   :depth: 2
   :local:

Using ``rebot`` tool
--------------------

Synopsis
~~~~~~~~

::

    rebot|jyrebot|ipyrebot [options] robot_outputs
    python|jython|ipy -m robot.rebot [options] robot_outputs
    python|jython|ipy path/to/robot/rebot.py [options] robot_outputs
    java -jar robotframework.jar rebot [options] robot_outputs

``rebot`` `runner script`_ runs on Python_ but there are also ``jyrebot``
and ``ipyrebot`` `runner scripts`_ that run on Jython_ and IronPython_, respectively.
Using ``rebot`` is recommended when it is available because it is considerable
faster than the alternatives. In addition to using these scripts, it is possible to use
``robot.rebot`` `entry point`_ either as a module or a script using
any interpreter, or use the `standalone JAR distribution`_.

Specifying options and arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The basic syntax for using ``rebot`` is exactly the same as when
`starting test execution`_ and also most of the command line options are
identical. The main difference is that arguments to ``rebot`` are
`XML output files`_ instead of test data files or directories.

Return codes with ``rebot``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Return codes from ``rebot`` are exactly same as when `running tests`__.

__ `Return codes`_

Creating different reports and logs
-----------------------------------

You can use ``rebot`` for creating the same reports and logs that
are created automatically during the test execution. Of course, it is
not sensible to create the exactly same files, but, for example,
having one report with all test cases and another with only some
subset of tests can be useful::

   rebot output.xml
   rebot path/to/output_file.xml
   rebot --include smoke --name Smoke_Tests c:\results\output.xml

Another common usage is creating only the output file when running tests
(log and report generation can be disabled with  `--log NONE
--report NONE`) and generating logs and reports later. Tests can,
for example, be executed on different environments, output files collected
to a central place, and reports and logs created there. This approach can
also work very well if generating reports and logs takes a lot of time when
running tests on Jython. Disabling log and report generation and generating
them later with ``rebot`` can save a lot of time and use less memory.

Combining outputs
-----------------

An important feature in ``rebot`` is its ability to combine
outputs from different test execution rounds. This capability allows,
for example, running the same test cases on different environments and
generating an overall report from all outputs. Combining outputs is
extremely easy, all that needs to be done is giving several output
files as arguments::

   rebot output1.xml output2.xml
   rebot outputs/*.xml

When outputs are combined, a new top-level test suite is created so
that test suites in the given output files are its child suites. This
works the same way when `multiple test data files or directories are
executed`__, and also in this case the name of the top-level test
suite is created by joining child suite names with an ampersand (&)
and spaces. These automatically generated names are not that good, and
it is often a good idea to use :option:`--name` to give a more
meaningful name::

   rebot --name Browser_Compatibility firefox.xml opera.xml safari.xml ie.xml
   rebot --include smoke --name Smoke_Tests c:\results\*.xml

__ `Specifying test data to be executed`_

Merging outputs
---------------

If same tests are re-executed or a single test suite executed in pieces,
combining results like discussed above creates an unnecessary top-level
test suite. In these cases it is typically better to merge results instead.
Merging is done by using :option:`--merge` option which changes the way how
``rebot`` combines two or more output files. This option itself takes no
arguments and all other command line options can be used with it normally::

   rebot --merge --name Example --critical regression original.xml merged.xml

How merging works in practice is explained in the following sections discussing
its two main use cases.

Merging re-executed tests
~~~~~~~~~~~~~~~~~~~~~~~~~

There is often a need to re-execute a subset of tests, for example, after
fixing a bug in the system under test or in the tests themselves. This can be
accomplished by `selecting test cases`_ by names (:option:`--test` and
:option:`--suite` options), tags (:option:`--include` and :option:`--exclude`),
or by previous status (:option:`--rerunfailed`).

Combining re-execution results with the original results using the default
`combining outputs`_ approach does not work too well. The main problem is
that you get separate test suites and possibly already fixed failures are
also shown. In this situation it is better to use :option:`--merge (-R)`
option to tell ``rebot`` to merge the results instead. In practice this
means that tests from the latter test runs replace tests in the original.
The usage is best illustrated by a practical example using
:option:`--rerunfailed` and :option:`--merge` together::

  robot --output original.xml tests                          # first execute all tests
  robot --rerunfailed original.xml --output rerun.xml tests  # then re-execute failing
  rebot --merge original.xml rerun.xml                       # finally merge results

The message of the merged tests contains a note that results have been
replaced. The message also shows the old status and message of the test.

Merged results must always have same top-level test suite. Tests and suites
in merged outputs that are not found from the original output are added into
the resulting output. How this works in practice is discussed in the next
section.

.. note:: Merging re-executed results is a new feature in Robot Framework 2.8.4.
          Prior to Robot Framework 2.8.6 new tests or suites in merged outputs
          were skipped and merging was done using nowadays deprecated
          :option:`--rerunmerge` option.

Merging suites executed in pieces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another important use case for the :option:`--merge` option is merging results
got when running a test suite in pieces using, for example, :option:`--include`
and :option:`--exclude` options::

    robot --include smoke --output smoke.xml tests   # first run some tests
    robot --exclude smoke --output others.xml tests  # then run others
    rebot --merge smoke.xml others.xml               # finally merge results

When merging outputs like this, the resulting output contains all tests and
suites found from all given output files. If some test is found from multiple
outputs, latest results replace the earlier ones like explained in the previous
section. Also this merging strategy requires the top-level test suites to
be same in all outputs.
