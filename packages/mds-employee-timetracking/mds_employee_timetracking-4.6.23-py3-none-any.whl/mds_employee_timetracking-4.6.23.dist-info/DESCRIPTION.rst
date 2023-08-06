mds-employee-timetracking
=========================
Working time recording for employees, with multiple time accounts, 
time account rules, automatic pause control and report.

Install
=======

pip install mds-employee-timetracking

Requires
========
- Tryton 4.6

HowTo
=====

For more information, read the files in the doc folder.

ToDo
====
- extend manual
- support for NFC door device

Changes
=======

*4.6.23 - 07.10.2019*

- fix: generate a valid calendar name in the Employees Wizard

*4.6.22 - 12.09.2019*

- upd: optimized selection of open presence-time by wizard
- upd: presence-times - workflow now allows: examine->editable
- fix: open presence-times appear in correct month
- fix: permissions for role working-time-admin

*4.6.21 - 06.09.2019*

- fix: permissions for employee to edit its sick days

*4.6.20 - 05.09.2019*

- add: employee can enter its sick days

*4.6.19 - 03.09.2019*

- add: new role 'Employee edit its start balance'

*4.6.18 - 02.09.2019*

- add: account rule extended - 
   applies on public holidays / not on public holidays / not set

*4.6.17 - 30.08.2019*

- fix: exception when deleting the start position of a period with 
   the existing end position

*4.6.16 - 14.08.2019*

- add: initial balance of a time account can be set manually

*4.6.15 - 19.07.2019*

- updt: field placement in employee wizard optimized
- fix: exception when accessing overlap calculation

*4.6.14 - 25.04.2019*

- new: config wizard

*4.6.13 - 18.04.2019*

- fix: calculation of remainig vacation days

*4.6.12 - 15.04.2019*

- new: holiday planning (new depency to mds-pim-calendar)

*4.6.11 - 14.02.2019*

- new: calendar view in evaluation + presence period + break time
- new: colors of background/text in calendar view selectable 
   for employee + type of presence, time account...
- info: GooCalendar on client side is neccasary

*4.6.10 - 11.02.2019*

- new: Attendance wizard extended, employee can enter his break times
- fix: report causes exception

*4.6.9 - 30.01.2019*

- fix: edit employee also corrects the associated company on the cronjob
- updt: optimized tests
- new: Time Entry Wizard accepts any number of Presence Types

*4.6.8 - 07.09.2018*

- fix: closing the work time did not always find the right period
- fix: overlap check improved

*4.6.7 - 29.08.2018*

- fix: entering the end of work by wizard sometimes did not work

*4.6.6 - 04.07.2018*

- fix: exception in overlapcheck of period item
- fix: bug in workflow transition from 'locked' to 'edit' at period item 

*4.6.5 - 18.06.2018*

- add: info about permisions in readme
- fix: optimize contraints for table *breaktime*

*4.6.4 - 15.06.2018*

- first public version
- added working time model, break time rules, report, how to

*4.6.3 - 22.05.2018*

- report: added list of additions

*4.6.2 - 20.05.2018*

- added evaluation-report

*4.6.0 - 22.02.2018*

- init


