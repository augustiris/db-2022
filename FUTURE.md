## Future Plan

> In the future, if we were to add the ability to have popularity tiers to your system, what would need to change? For example, we want more popular books to have earlier due dates (perhaps only checkout for one week). For those books, the late fees would be higher
- What tables need changing and/or adding?
- What API methods would you provide?
- How might existing API methods change?

1. The database could track the amount of times a book has been checked out and how many copies it has. If the ratio of checkouts to book copies reaches a certain threshold the book could be labeled as 'in demand' which could be a boolean column in the books table. The trigger that sets
due dates would have to check to see if 'in demand' is set to true in the books table. In the API another global variable could be made for the increased late fee. In update_fee() the method would check the book's 'in demand' status.

> In the future, if we were to add the ability to have overdue warnings to your system, what would need to change? For example, books that are overdue by more than one week have an automatic notification sent out to the user
- What tables need changing and/or adding?
- What API methods would you provide?
- How might existing API methods change?
- What extra workflow logic would you need?

2. There would need to be a method in the API that is called every day which checks the checked_out table for each item that has a null returned_date to check if 'days_borrowed' exceeds 21 days.